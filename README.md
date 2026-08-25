# 📚 Digital Library

### A modern, full-stack Digital Library Management System built with Django

<p align="center">
  <strong>Discover. Explore. Authenticate. Read.</strong>
</p>

<p align="center">
  A production-minded Django application focused on digital library management, secure authentication, intelligent book metadata retrieval, category-based discovery, and role-based administration.
</p>

<p align="center">
  <a href="https://github.com/Hasnain-118/Django">Repository</a>
  ·
  <a href="https://github.com/Hasnain-118/Django/issues">Issues</a>
  ·
  <a href="https://github.com/Hasnain-118/Django/network">Contribute</a>
</p>

---

## ✨ Overview

**Digital Library** is a Django-powered web application designed to provide a clean and intuitive platform for discovering, browsing, and managing digital books.

The project goes beyond a basic CRUD implementation by combining:

* 🔐 Full user authentication
* 🔑 Email-based password recovery
* 🔵 Google OAuth authentication
* 📚 Automated book metadata retrieval
* 🏷️ Dynamic category-based discovery
* 🛡️ Role-based administrative controls
* 🔔 In-app user notifications
* 📱 Responsive web interface
* 🧩 Modular Django architecture
* ⚙️ Environment-aware configuration

The application is being developed as a complete web-development project with a strong emphasis on **real application functionality, maintainability, and user experience**.

---

## 🎯 Core Experience

The application is designed around a simple user journey:

```text
Discover
   ↓
Explore
   ↓
Browse Categories
   ↓
View Book Details
   ↓
Authenticate
   ↓
Read
```

Administrators have an additional management workflow:

```text
Admin Login
    ↓
Manage Books
    ↓
Add / Update Content
    ↓
Automatic Metadata Retrieval
    ↓
Publish
    ↓
Users Receive Notifications
```

---

# 🚀 Features

## 🔐 Authentication & Accounts

A complete authentication layer built around Django's authentication system.

* User registration
* Username/password login
* Logout
* Protected pages
* Login-required workflows
* Redirect-after-login behavior
* CSRF-protected authentication forms
* Email-based password reset
* Styled password reset pages

---

## 🔵 Google Sign-In

Users can authenticate using their Google account through **OAuth 2.0** and `django-allauth`.

### Authentication flow

```text
User
 │
 ├── Username / Password
 │
 └── Google Account
          │
          ▼
      OAuth Flow
          │
          ▼
    Django Authentication
          │
          ▼
       Application
```

The Google authentication integration includes:

* Google OAuth configuration
* OAuth consent configuration
* Authorized redirect URI
* Django Sites framework
* Social Application configuration
* Authentication backend integration
* First-time Google account onboarding

---

## 📚 Intelligent Book Metadata

Adding books doesn't have to mean manually entering every piece of information.

When book metadata is missing, the application can retrieve information automatically using external APIs.

### Metadata pipeline

```text
Admin adds book
      │
      ▼
Check existing metadata
      │
      ├── Description missing ──► Google Books API
      │
      ├── Rating missing ───────► Google Books API
      │
      └── Cover missing ────────► Google Books API
                                      │
                                      ▼
                               No matching cover?
                                      │
                                      ▼
                              Open Library fallback
```

The system follows an important rule:

> **Manually entered administrator data takes precedence over automatically retrieved data.**

This prevents API responses from unexpectedly overwriting curated content.

---

## 🏷️ Dynamic Categories

The library supports category-based book discovery.

Instead of maintaining a hard-coded navigation menu, categories are generated from the application's book-category definitions.

### Benefits

* Centralized category definitions
* Automatically synchronized navigation
* Dedicated category listing pages
* Cleaner browsing experience
* Easier future expansion

---

## 🛡️ Role-Based Administration

Administrative functionality is separated from the regular user experience.

Staff/admin users can access:

* ➕ Add Book
* 🗂️ Manage Books
* Administrative content controls

Regular users cannot access protected management views simply by manually entering their URLs.

Authorization is enforced at the application level using Django's authentication and permission mechanisms.

```text
                    ┌─────────────────┐
                    │      User       │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Authenticated?  │
                    └───────┬─────────┘
                            │
                  ┌─────────┴─────────┐
                  │                   │
                NO                   YES
                  │                   │
                  ▼                   ▼
              Public UI       ┌──────────────┐
                              │ Staff/Admin? │
                              └──────┬───────┘
                                     │
                           ┌─────────┴─────────┐
                           │                   │
                          NO                  YES
                           │                   │
                           ▼                   ▼
                      User Features      Management UI
```

---

## 🔔 Notifications

The application includes a lightweight notification system connected to individual users.

When a new book is added:

```text
New Book Added
      │
      ▼
Notification Created
      │
      ▼
User Notification Center
      │
      ├── Unread Count
      │
      └── Notification Dropdown
```

This provides a foundation for extending the application with richer user-facing events in the future.

---

# 🧠 Technical Architecture

The project follows Django's conventional separation of concerns.

```text
Django
│
├── Hello/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── home/
│   ├── admin.py
│   ├── apps.py
│   ├── context_processors.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── tests.py
│   └── migrations/
│
├── templates/
│
├── static/
│
├── media/
│
├── manage.py
│
└── requirements.txt
```

The repository currently contains the main Django project package, the `home` application, templates, static/media assets, `manage.py`, and dependency configuration.

---

# 🛠️ Technology Stack

| Technology             | Role                                       |
| ---------------------- | ------------------------------------------ |
| 🐍 **Python**          | Core programming language                  |
| 🎯 **Django 5.2**      | Web application framework                  |
| 🔐 **django-allauth**  | Social authentication & account management |
| 🌐 **Requests**        | External API communication                 |
| 🖼️ **Pillow**         | Image processing                           |
| ⚙️ **python-decouple** | Configuration management                   |
| 🎨 **HTML5**           | Application structure                      |
| 🎨 **CSS3**            | Styling                                    |
| 🧩 **Bootstrap**       | Responsive UI components                   |
| 🗄️ **SQLite**         | Development database                       |

The repository currently pins Django 5.2.16, django-allauth 65.4.1, requests 2.32.5, Pillow 11.3.0, and python-decouple 3.8 in `requirements.txt`.

---

# 📁 Project Structure

```text
Django/
│
├── .vscode/
│
├── Hello/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── home/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── context_processors.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── media/
├── static/
├── templates/
│
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

---

# ⚡ Getting Started

## Prerequisites

Make sure you have installed:

* Python 3.x
* Git
* pip
* A virtual-environment tool

---

## 1. Clone the repository

```bash
git clone https://github.com/Hasnain-118/Django.git
```

```bash
cd Django
```

---

## 2. Create a virtual environment

### Windows

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Apply database migrations

```bash
python manage.py migrate
```

---

## 5. Create an administrator

```bash
python manage.py createsuperuser
```

Follow the prompts to configure the admin account.

---

## 6. Start the development server

```bash
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

---

# 🔑 Configuration

For local development, configure environment-specific values rather than committing sensitive credentials.

Typical configuration includes:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-app-password
```

> ⚠️ **Never commit real API credentials, OAuth secrets, email passwords, or production secret keys to Git.**

---

# 🔵 Google OAuth Setup

To enable Google authentication:

1. Create a project in Google Cloud.
2. Configure the OAuth consent screen.
3. Create OAuth client credentials.
4. Configure the authorized redirect URI.
5. Add the credentials to the Django environment.
6. Configure the Django Sites framework.
7. Configure the django-allauth Social Application.
8. Test both existing-user and first-time-user flows.

---

# 📧 Password Reset

The application supports email-based password recovery.

The general flow is:

```text
Forgot Password
      │
      ▼
Enter Email
      │
      ▼
Django Generates Reset Token
      │
      ▼
SMTP Email Delivery
      │
      ▼
Reset Link
      │
      ▼
New Password
```

For local development, configure SMTP credentials through environment variables rather than hardcoding them.

---

# 🔌 External APIs

The application uses external services to enrich book information.

### Google Books API

Used as the primary source for automated book metadata retrieval.

Potentially retrieved information includes:

* Book description.
* Rating
* Cover image

### Open Library

Used as a fallback source specifically for cover images when the Google Books lookup does not provide a suitable result.

---

# 🧪 Development & Testing

Run Django's test suite with:

```bash
python manage.py test
```

For additional development diagnostics:

```bash
python manage.py check
```

Before deployment, verify:

```bash
python manage.py check --deploy
```

---

# 🔒 Security Considerations

Before deploying the application publicly, review:

* `SECRET_KEY`
* `DEBUG`
* `ALLOWED_HOSTS`
* CSRF configuration
* OAuth credentials
* SMTP credentials
* Database configuration
* Static/media handling
* Production WSGI/ASGI configuration

Development credentials should **never** be reused as production secrets.

---

# 🗺️ Roadmap

The project is evolving toward a deployment-ready digital library platform.

### Current direction

* [x] User authentication
* [x] Email password reset
* [x] Google OAuth
* [x] Book browsing
* [x] Category filtering
* [x] Automated book metadata
* [x] Admin-only book management
* [x] Notification foundation
* [x] Responsive interface
* [x] Repository/deployment review

### Next priorities

* [ ] Production deployment
* [ ] Environment-based production configuration
* [ ] Static/media deployment configuration
* [ ] Further notification refinement
* [ ] Additional UI polish
* [ ] Expanded automated testing
* [ ] Production database configuration
* [ ] Deployment documentation

---

# 🧩 Engineering Highlights

This project focuses on practical Django engineering rather than simply presenting a static interface.

### Authentication

Uses Django's authentication infrastructure together with django-allauth for third-party identity providers.

### Authorization

Management functionality is protected both at the UI level and through server-side access checks.

### API Integration

External book APIs are integrated into the application lifecycle to reduce repetitive administrative data entry.

### Data Integrity

Manually supplied book information takes precedence over automatically retrieved metadata.

### Modular Design

Application logic is organized across models, forms, views, URLs, context processors, templates, and migrations.

---

# 📸 Screenshots

> Add project screenshots here as the interface continues to evolve.

Recommended showcase:

| Preview | Feature               |
| ------- | --------------------- |
| 🏠      | Home / Discover       |
| 📚      | Book Library          |
| 🔎      | Search                |
| 🏷️     | Categories            |
| 📖      | Book Details          |
| 🔐      | Sign In               |
| 🔵      | Google Sign-In        |
| 🔑      | Password Reset        |
| 🛠️     | Admin Book Management |
| 🔔      | Notifications         |

Example:

```md
![Home Page](screenshots/home.png)
```

---

# 📊 Project Philosophy

Digital Library is built around a simple idea:

> **A library application should make discovering and managing knowledge feel effortless.**

That means reducing unnecessary administrative work, keeping navigation intuitive, protecting privileged functionality, and creating an authentication experience that feels native rather than bolted on.

---

# 🤝 Contributing

Contributions, ideas, improvements, and bug reports are welcome.

### Development workflow

```bash
# Fork the repository

# Create a feature branch
git checkout -b feature/your-feature

# Make your changes

# Commit
git commit -m "feat: add your feature"

# Push
git push origin feature/your-feature
```

Then open a Pull Request.

### Suggested commit style

```text
feat: add category filtering
fix: resolve password reset email issue
refactor: improve book metadata service
docs: update installation guide
style: refine authentication UI
```

---

# 👨‍💻 Author

## Muhammad Hasnain Iftikhar

**BS Software Engineering Student · Django Developer**

I build web applications with a focus on backend engineering, clean architecture, authentication systems, API integration, and practical user experiences.

<p>
  <a href="https://github.com/Hasnain-118">
    <strong>GitHub</strong>
  </a>
  &nbsp; · &nbsp;
  <a href="https://www.linkedin.com/in/muhammad-hasnain-iftikhar/">
    <strong>LinkedIn</strong>
  </a>
</p>

---

# 📄 License

This project is released under the **MIT License**.

See the repository's license information for details.

---

<div align="center">

### ⭐ If this project helped you, consider starring the repository.

**Built with Python & Django · Designed for learning · Engineered for growth**

</div>
