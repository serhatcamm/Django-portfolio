# Dynamic Django Portfolio Website

A modern, highly customizable personal portfolio website built with Python/Django. Features an extensive admin panel that allows full control over branding, themes, global layout, and content without touching code.

LIVE DEMO: https://serhatcamm.github.io/Python-Django-Personal-Website-with-Admin-Panel/

## Features
- **Dynamic Theme Management:** Switch between pre-defined color schemes or create your own.
- **Global Layout Control:** Adjust spacing, container widths, and gaps globally from the admin panel.
- **Admin-Driven Content:** Manage your bio, projects, skills, and contact info directly in the Django Admin.
- **Static Export:** Fully exportable as a static site for GitHub Pages or other hosting services.

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/serhatcamm/Django-portfolio
   cd Python-Django-Personal-Website-with-Admin-Panel
   ```

2. **Create and activate a virtual environment:**
   - **Windows:**
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server:**
   ```bash
   python manage.py runserver
   ```
   Access the site at `http://127.0.0.1:8000` and the Admin panel at `http://127.0.0.1:8000/admin`.

## Deploying to GitHub Pages

To export your site as a static build for deployment:
```bash
python generate_static.py
```
This will generate the site in the `docs/` folder. Commit and push these changes to your `main` branch:
```bash
git add docs/
git commit -m "Deploy static site"
git push origin main
```
*Ensure your GitHub repository settings are configured to serve pages from the `/docs` folder.*

## Optional: HTTPS Development
If you need to test features that require HTTPS (e.g., service workers, geolocation), you can use the included `proxy_server.py`. 

**Requirements:**
1. Generate your own SSL certificate (`cert.crt`) and key (`cert.key`) on your machine:
   ```bash
   openssl req -x509 -newkey rsa:4096 -keyout cert.key -out cert.crt -days 365 -nodes
   ```
2. Update the file paths in `proxy_server.py` to point to your new `cert.crt` and `cert.key` files.
3. Run the proxy:
   ```bash
   python proxy_server.py
   ```
This will start your Django server on port 8000 and expose it via HTTPS on port 443.
