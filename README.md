# Portfolio

A modern, highly customizable personal portfolio website built with Python/Django. Features an extensive admin panel that allows full control over branding, themes, global layout, and content without touching code.

Fully containerized with **Docker** so you can run it (demo content included) in a single command.

## ✨ Features

- **Dynamic Theme Management** — switch between built-in color schemes (Modern Dark, Midnight Deep, Emerald Forest, Soft Rose) or create your own from the admin.
- **Global Layout Control** — adjust spacing, container widths, gaps, animation speeds, and more globally from the admin panel.
- **Admin-Driven Content** — manage your bio, hero, projects, skills, stats, references, social links, and contact info directly in Django Admin.
- **Light / Dark Mode** — instant theme toggle with per-theme light & dark palettes.
- **Dockerized** — self-contained image with auto-migrate, demo content seeding, and an admin superuser.
- **Static Export** — export the whole site as a static build for GitHub Pages or any static host.

## 🚀 Quick Start with Docker (recommended)

No Python/venv setup needed — just Docker.

```bash
git clone https://github.com/serhatcamm/django-portfolio.git
cd django-portfolio
docker compose up --build
```

Open **http://localhost:8000** — the site comes pre-seeded with demo content.

**Admin panel:** http://localhost:8000/admin
- Username: `admin`
- Password: `admin123`

> Set a real `DJANGO_SECRET_KEY` (in `.env`) — the container refuses to start with DEBUG off if one isn't provided. Change the admin password before any public deployment.

### Customizing via environment (optional)
| Variable | Default | Purpose |
| --- | --- | --- |
| `DJANGO_DEBUG` | `False` | Turns debug mode on/off (leave off in production) |
| `DJANGO_SECRET_KEY` | *(required)* | Django secret key — must be set when DEBUG is off |
| `DJANGO_SUPERUSER_USERNAME` | `admin` | Auto-created admin username |
| `DJANGO_SUPERUSER_PASSWORD` | `admin123` | Auto-created admin password |

Example:

```bash
DJANGO_SUPERUSER_USERNAME=me DJANGO_SUPERUSER_PASSWORD=s3cret docker compose up --build
```

## 🐍 Local Development (without Docker)

Requires **Python 3.12+** (Django 6.x).

```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo        # optional: load demo content
python manage.py runserver
```

- Site: http://127.0.0.1:8000
- Admin: http://127.0.0.1:8000/admin
- Auto-created superuser: `admin` / `admin123`

To create your own admin user instead:

```bash
python manage.py createsuperuser
```

## 📁 Project Structure

```
portfolio/            # Django project package (settings, urls, wsgi/asgi)
projects/             # main app: projects, hero, about, skills, stats, themes, references
pages/                # page views + base context
contact/              # contact form + messages API
templates/            # HTML templates
staticfiles/          # static assets served in development
seed_media/           # demo images copied to media/ when seeding
media/                # user-uploaded content (gitignored)
Dockerfile            # container image definition
docker-compose.yml    # one-command run
docker-entrypoint.sh  # migrate + seed + superuser, then start server
```

## 📸 Deploying as a Static Site (GitHub Pages)

To export the site as a static build:

```bash
python manage.py migrate
python generate_static.py
```

This generates the site into the `docs/` folder. Commit and push `docs/`, then configure your GitHub repository to serve Pages from the `/docs` folder.

## 🔒 Security Notes

- `DJANGO_SECRET_KEY` has a development fallback so the app runs out-of-the-box. **Always set a real, random secret key in production.**
- Docker runs with `DJANGO_DEBUG=True` for demo purposes. For production, set `DJANGO_DEBUG=False`, set a real secret key, and serve static/media via a web server (e.g., Nginx) or WhiteNoise.

## ✅ Admin Panel Capabilities

Manage every part of the site without code:

- **Hero Content** — greeting, name, cycling titles, bio, CTA buttons
- **About Content** — title, subtitle, summary, biography, photo, years of experience
- **Projects** — title, description, technology, image, link
- **Skills** — categorized skill tags
- **Stats** — animated counters (projects, clients, experience)
- **References** — testimonials with author/company
- **Social Links** — GitHub, LinkedIn, etc.
- **Theme Settings** — full color/branding/layout/animation control
- **Site Configuration** — nav labels, footer, section titles, contact info

## 📄 License

See the [LICENSE](LICENSE) file.
