"""
Comprehensive test suite for the Portfolio Site Django application.
Tests cover models, views, API endpoints, forms, and authentication.
"""
import pytest
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from projects_app.models import Project
from contact_app.models import ContactMessage
from accounts_app.models import Profile


# ─── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture
def client():
    return Client()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def regular_user(db):
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='TestPass123!',
        first_name='Test',
        last_name='User'
    )
    return user


@pytest.fixture
def admin_user(db):
    user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='AdminPass123!',
    )
    return user


@pytest.fixture
def sample_project(db):
    return Project.objects.create(
        title='Test Django Project',
        description='A test portfolio project built with Django and PostgreSQL for testing purposes.',
        short_description='A test project description',
        tech_stack='Python, Django, PostgreSQL, Docker',
        github_link='https://github.com/test/project',
        live_demo_link='https://demo.example.com',
        is_featured=True,
    )


@pytest.fixture
def sample_contact(db):
    return ContactMessage.objects.create(
        name='John Doe',
        email='john@example.com',
        subject='Test Subject',
        message='This is a test message with enough characters to pass validation.',
    )


# ─── Model Tests ─────────────────────────────────────────────────────────────

class ProjectModelTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title='My Portfolio Project',
            description='A detailed description of this amazing portfolio project.',
            tech_stack='Python, Django, React, PostgreSQL',
            github_link='https://github.com/test/repo',
        )

    def test_project_creation(self):
        self.assertEqual(self.project.title, 'My Portfolio Project')
        self.assertIsNotNone(self.project.slug)

    def test_slug_auto_generation(self):
        self.assertEqual(self.project.slug, 'my-portfolio-project')

    def test_slug_uniqueness(self):
        project2 = Project.objects.create(
            title='My Portfolio Project',
            description='Another project with same title.',
            tech_stack='Python',
        )
        self.assertNotEqual(self.project.slug, project2.slug)
        self.assertIn('my-portfolio-project', project2.slug)

    def test_get_tech_list(self):
        tech_list = self.project.get_tech_list()
        self.assertIsInstance(tech_list, list)
        self.assertIn('Python', tech_list)
        self.assertIn('Django', tech_list)

    def test_get_absolute_url(self):
        url = self.project.get_absolute_url()
        self.assertIn(self.project.slug, url)

    def test_str_representation(self):
        self.assertEqual(str(self.project), 'My Portfolio Project')


class ContactMessageModelTest(TestCase):
    def test_contact_message_creation(self):
        msg = ContactMessage.objects.create(
            name='Jane Doe',
            email='jane@example.com',
            message='Test message content here.',
        )
        self.assertEqual(msg.name, 'Jane Doe')
        self.assertFalse(msg.is_read)
        self.assertIsNotNone(msg.created_at)

    def test_str_representation(self):
        msg = ContactMessage.objects.create(
            name='Test User',
            email='test@example.com',
            message='Test message.',
        )
        self.assertIn('Test User', str(msg))


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='profileuser', password='pass')

    def test_profile_auto_created(self):
        # Profile should be auto-created via signal
        self.assertTrue(Profile.objects.filter(user=self.user).exists())

    def test_get_skills_list(self):
        profile = self.user.profile
        profile.skills = 'Python, Django, Docker, PostgreSQL'
        profile.save()
        skills = profile.get_skills_list()
        self.assertIsInstance(skills, list)
        self.assertIn('Python', skills)
        self.assertEqual(len(skills), 4)


# ─── View Tests ──────────────────────────────────────────────────────────────

class PublicViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_about_view(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_projects_list_view(self):
        response = self.client.get(reverse('projects_list'))
        self.assertEqual(response.status_code, 200)

    def test_contact_view_get(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)

    def test_project_detail_view(self):
        project = Project.objects.create(
            title='Test Project Detail',
            description='Full description of this test project for detail view testing.',
            tech_stack='Python, Django',
        )
        response = self.client.get(reverse('project_detail', kwargs={'slug': project.slug}))
        self.assertEqual(response.status_code, 200)

    def test_project_detail_404(self):
        response = self.client.get(reverse('project_detail', kwargs={'slug': 'non-existent-slug'}))
        self.assertEqual(response.status_code, 404)


class AuthViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='authtest',
            password='SecurePass123!',
            email='auth@test.com'
        )

    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        response = self.client.post(reverse('login'), {
            'username': 'authtest',
            'password': 'SecurePass123!'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_failure(self):
        response = self.client.post(reverse('login'), {
            'username': 'authtest',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)

    def test_signup_view_get(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_signup_success(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@test.com',
            'password1': 'SecureTestPass123!',
            'password2': 'SecureTestPass123!',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_dashboard_accessible_when_logged_in(self):
        self.client.login(username='authtest', password='SecurePass123!')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)


class ProjectCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            username='admin', password='AdminPass123!', email='admin@test.com'
        )
        self.regular = User.objects.create_user(
            username='regular', password='RegPass123!', email='reg@test.com'
        )

    def test_project_create_requires_staff(self):
        self.client.login(username='regular', password='RegPass123!')
        response = self.client.get(reverse('project_create'))
        # Should redirect non-staff users
        self.assertNotEqual(response.status_code, 200)

    def test_project_create_admin(self):
        self.client.login(username='admin', password='AdminPass123!')
        response = self.client.post(reverse('project_create'), {
            'title': 'New Test Project',
            'description': 'A comprehensive description of this new test project.',
            'tech_stack': 'Python, Django, PostgreSQL',
            'github_link': 'https://github.com/test/new',
            'live_demo_link': '',
            'short_description': 'Short desc',
            'order': 0,
        }, follow=True)
        self.assertTrue(Project.objects.filter(title='New Test Project').exists())

    def test_project_delete_admin(self):
        project = Project.objects.create(
            title='Delete Me',
            description='This project will be deleted in the test.',
            tech_stack='Python',
        )
        self.client.login(username='admin', password='AdminPass123!')
        response = self.client.post(
            reverse('project_delete', kwargs={'slug': project.slug}),
            follow=True
        )
        self.assertFalse(Project.objects.filter(title='Delete Me').exists())


# ─── API Tests ───────────────────────────────────────────────────────────────

class APITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            username='apiadmin', password='ApiAdminPass123!', email='api@test.com'
        )
        self.token, _ = Token.objects.get_or_create(user=self.admin)
        self.project = Project.objects.create(
            title='API Test Project',
            description='A project used for API testing in the test suite.',
            tech_stack='Python, Django, REST API',
        )

    def test_get_projects_list(self):
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, 200)

    def test_get_project_by_slug(self):
        response = self.client.get(f'/api/projects/{self.project.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'API Test Project')

    def test_create_project_requires_auth(self):
        response = self.client.post('/api/projects/', {
            'title': 'Unauthorized',
            'description': 'This should fail',
            'tech_stack': 'None',
        })
        self.assertEqual(response.status_code, 401)

    def test_create_project_with_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post('/api/projects/', {
            'title': 'Authorized Project',
            'description': 'This is a valid project description for the API test.',
            'tech_stack': 'Python, Django',
        })
        self.assertEqual(response.status_code, 201)

    def test_contact_api_post(self):
        response = self.client.post('/api/contact/', {
            'name': 'Test User',
            'email': 'testapi@example.com',
            'message': 'This is a valid test contact message with enough content.',
        })
        self.assertEqual(response.status_code, 201)

    def test_api_login(self):
        response = self.client.post('/api/auth/login/', {
            'username': 'apiadmin',
            'password': 'ApiAdminPass123!'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)

    def test_api_login_invalid(self):
        response = self.client.post('/api/auth/login/', {
            'username': 'apiadmin',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 401)

    def test_api_serializer_validation(self):
        """Test that serializer rejects invalid data"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post('/api/projects/', {
            'title': 'A',  # Too short
            'description': 'Short',  # Too short
            'tech_stack': '',
        })
        self.assertEqual(response.status_code, 400)


# ─── Contact Form Tests ───────────────────────────────────────────────────────

class ContactFormTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_contact_form_valid_submission(self):
        response = self.client.post(reverse('contact'), {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Hello',
            'message': 'This is a valid test message with enough content.',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ContactMessage.objects.filter(name='John Doe').exists())

    def test_contact_form_invalid_email(self):
        response = self.client.post(reverse('contact'), {
            'name': 'Test',
            'email': 'not-an-email',
            'message': 'Test message content here.',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(ContactMessage.objects.filter(name='Test').exists())
