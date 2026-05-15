from pathlib import Path

output = Path('docs/PROJECT_DOCUMENTATION.pdf')

lines = [
    'Portfolio Project Documentation',
    '',
    '1. Project Overview',
    'Django portfolio platform with web pages, authentication, REST API, PostgreSQL, Docker, and Nginx.',
    '',
    '2. Modules',
    '- accounts_app: auth, dashboard, profile',
    '- projects_app: project CRUD, slug logic',
    '- contact_app: contact form/messages/email',
    '- api_app: DRF endpoints + token auth',
    '- portfolio_site: settings and root routing',
    '',
    '3. UML (Textual)',
    'User 1---1 Profile',
    'Project: title, slug, tech_stack, featured, ordering',
    'ContactMessage: name, email, subject, message, read_flag',
    '',
    '4. High-Level Diagram',
    'Client -> Nginx -> Django Apps -> PostgreSQL',
    '                    -> Email Backend',
    '',
    '5. Low-Level Flow',
    'Client -> URL Router -> View/APIView -> Serializer/Form -> Model/ORM -> DB -> Response',
    '',
    '6. API Surface',
    '/api/projects/, /api/projects/{slug}/, /api/projects/featured/',
    '/api/contact/, /api/profile/, /api/auth/login/, /api/auth/logout/, /api/auth/profile/',
    '',
    '7. Security',
    'Session + Token authentication, admin-only write endpoints, CSRF middleware, configurable CORS.',
]

# very small PDF writer using built-in Helvetica
content = ['BT', '/F1 11 Tf', '50 790 Td']
leading = 15
for i, line in enumerate(lines):
    safe = line.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
    if i == 0:
        content.append('/F1 16 Tf')
        content.append(f'({safe}) Tj')
        content.append('/F1 11 Tf')
    else:
        content.append(f'0 -{leading} Td')
        content.append(f'({safe}) Tj')
content.append('ET')
stream = '\n'.join(content).encode('latin-1', errors='replace')

objects = []

def add_obj(data: bytes):
    objects.append(data)

add_obj(b'<< /Type /Catalog /Pages 2 0 R >>')
add_obj(b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>')
add_obj(b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>')
add_obj(b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>')
add_obj(f'<< /Length {len(stream)} >>\nstream\n'.encode() + stream + b'\nendstream')

pdf = bytearray(b'%PDF-1.4\n')
offsets = [0]
for idx, obj in enumerate(objects, start=1):
    offsets.append(len(pdf))
    pdf.extend(f'{idx} 0 obj\n'.encode())
    pdf.extend(obj)
    pdf.extend(b'\nendobj\n')

xref_pos = len(pdf)
pdf.extend(f'xref\n0 {len(objects)+1}\n'.encode())
pdf.extend(b'0000000000 65535 f \n')
for off in offsets[1:]:
    pdf.extend(f'{off:010d} 00000 n \n'.encode())
pdf.extend(f'trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n'.encode())

output.write_bytes(pdf)
print(f'Wrote {output}')
