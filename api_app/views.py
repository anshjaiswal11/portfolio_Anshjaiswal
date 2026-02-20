from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from projects_app.models import Project
from contact_app.models import ContactMessage
from accounts_app.models import Profile
from .serializers import ProjectSerializer, ContactMessageSerializer, ProfileSerializer


class ProjectListCreateAPIView(generics.ListCreateAPIView):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save()


class ProjectDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'slug'

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]


class FeaturedProjectsAPIView(generics.ListAPIView):
    queryset = Project.objects.filter(is_featured=True).order_by('order')
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]


class ContactMessageCreateAPIView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        contact_msg = serializer.save()

        # 1. Notify admin
        try:
            send_mail(
                subject=f'[Portfolio Contact] {contact_msg.subject or "New Message"} from {contact_msg.name}',
                message=(
                    f'You received a new contact message.\n\n'
                    f'Name: {contact_msg.name}\n'
                    f'Email: {contact_msg.email}\n'
                    f'Subject: {contact_msg.subject or "N/A"}\n\n'
                    f'Message:\n{contact_msg.message}'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            # Log the error but don't break the request
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f'Failed to send admin notification email: {e}')

        # 2. Send confirmation email to the sender
        try:
            send_mail(
                subject='Thanks for reaching out!',
                message=(
                    f'Hi {contact_msg.name},\n\n'
                    f'Thank you for your message! I have received it and will get back to you as soon as possible.\n\n'
                    f'Here is a copy of what you sent:\n'
                    f'---\n'
                    f'Subject: {contact_msg.subject or "N/A"}\n'
                    f'{contact_msg.message}\n'
                    f'---\n\n'
                    f'Best regards,\n'
                    f'Rahul'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[contact_msg.email],
                fail_silently=False,
            )
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f'Failed to send confirmation email to {contact_msg.email}: {e}')


class ProfileAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return Profile.objects.filter(user__is_superuser=True).first()


@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff,
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_logout(request):
    request.user.auth_token.delete()
    return Response({'message': 'Logged out successfully'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_profile(request):
    try:
        profile = request.user.profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    except Profile.DoesNotExist:
        return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
