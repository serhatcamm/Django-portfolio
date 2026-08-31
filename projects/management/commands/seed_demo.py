import os
import shutil

from django.conf import settings
from django.core.files import File
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand

from projects.models import (
    AboutContent,
    HeroContent,
    Project,
    Reference,
    SiteConfiguration,
    Skill,
    SkillCategory,
    SocialLink,
    Stat,
    ThemeSettings,
)


class Command(BaseCommand):
    help = "Populate the site with demo content (idempotent). Copies seed media into MEDIA_ROOT and seeds content models."

    projects = [
        ("E-Commerce API", "e-commerce-api",
         "A robust REST API for e-commerce built with Django Rest Framework. Features product listings, cart, orders, user authentication and Stripe payments.",
         "Python, Django, DRF", "p1.webp", "https://example.com/e-commerce-api"),
        ("AI Image Generator", "ai-image-generator",
         "Web app that generates images using the DALL-E API and React. Includes prompt history, gallery, and one-click downloads.",
         "Python, React, OpenAI", "p2.webp", "https://example.com/ai-image-generator"),
        ("Task Management System", "task-management-system",
         "Real-time task tracking with WebSockets and Redis. Live project boards, notifications, and team collaboration.",
         "Django, Channels, Redis", "p3.webp", "https://example.com/task-management"),
        ("Portfolio Template", "portfolio-template",
         "Modern, responsive portfolio with a dynamic theme engine and full admin panel (this very project).",
         "Django, Vanilla CSS", "p4.webp", "https://example.com/portfolio-template"),
        ("Finance Tracker", "finance-tracker",
         "Personal finance app with data visualization and CSV export. Track budgets, expenses and monthly trends.",
         "Python, Pandas, Chart.js", "p5.webp", "https://example.com/finance-tracker"),
        ("Blog Platform", "blog-platform",
         "SEO-optimized blog with markdown support and commenting. Includes tags, categories and an RSS feed.",
         "Django, PostgreSQL", "p6.webp", "https://example.com/blog-platform"),
        ("Job Board Platform", "job-board-platform",
         "Full-featured job board with recruiter and candidate portals, smart search, filters and email alerts.",
         "Django, PostgreSQL, Elasticsearch", "p7.webp", "https://example.com/job-board"),
        ("Real-Time Chat App", "real-time-chat-app",
         "Instant messaging app with WebSockets, read receipts, typing indicators and group channels.",
         "Django, Channels, Redis", "p8.webp", "https://example.com/chat-app"),
    ]

    skill_categories = {
        "Backend Development": ["Python", "Django", "FastAPI"],
        "Frontend": ["Vanilla JS", "CSS3"],
        "Databases & Tools": ["PostgreSQL", "Redis", "Docker"],
    }

    themes = [
        ("Modern Dark", "#0c0c0e", "#a78bfa", "#161619", "#f4f4f5", "#a1a1aa", "#b5b5b5", 1.2),
        ("Midnight Deep", "#020617", "#38bdf8", "#0f172a", "#f1f5f9", "#94a3b8", "#38bdf8", 1.0),
        ("Emerald Forest", "#061a11", "#10b981", "#0a2619", "#ecfdf5", "#a7f3d0", "#10b981", 0.8),
        ("Soft Rose", "#1a1215", "#fb7185", "#2e1d23", "#fef2f2", "#fecdd3", "#fb7185", 0.9),
    ]

    references = [
        ("John Doe", "Senior Dev", "TechCorp",
         "Serhat is an exceptional engineer with a deep understanding of Django. He delivered our APIs ahead of schedule.", 1),
        ("Jane Smith", "Product Manager", "InnovateUI",
         "The attention to detail in the dynamic theme engine is impressive. Our clients love the polished look.", 2),
        ("Mike Ross", "Lead Architect", "CloudScale",
         "Reliable, fast, and writes very clean code. Highly recommended for any backend-heavy project.", 3),
        ("Emily Chen", "CTO", "DataForge Labs",
         "A rare mix of solid engineering and great communication. Serhat owns every task he takes on.", 4),
        ("Ahmed Al-Farsi", "Startup Founder", "NovaTech",
         "Superb execution from design to deployment. The final product exceeded what we asked for.", 5),
        ("Sofia Rossi", "Design Lead", "PixelWorks",
         "Working with Serhat is seamless — he cares about the details and ships on time, every time.", 6),
    ]

    def copy_seed_media(self):
        media_root = settings.MEDIA_ROOT
        seed_root = settings.BASE_DIR / 'seed_media'
        if not seed_root.is_dir():
            self.stdout.write(self.style.WARNING('seed_media/ not found, skipping media copy'))
            return
        for sub in ['project_images', 'logos']:
            src_dir = seed_root / sub
            dst_dir = os.path.join(str(media_root), sub)
            if src_dir.is_dir():
                os.makedirs(dst_dir, exist_ok=True)
                for f in src_dir.iterdir():
                    if f.is_file():
                        shutil.copy2(str(f), dst_dir)
                        self.stdout.write(f"  copied {sub}/{f.name}")

    def open_seed(self, rel):
        return open(os.path.join(str(settings.BASE_DIR), 'seed_media', rel), 'rb')

    def handle(self, *args, **options):
        self.copy_seed_media()

        # ---- Projects ----
        for title, slug, desc, tech, img, link in self.projects:
            if Project.objects.filter(slug=slug).exists():
                continue
            # Pre-copying the file makes Django append a random suffix on save
            # (e.g. p1_AbC123x.webp), which is unstable across rebuilds and
            # breaks DB->media consistency. Remove the base-named copy first so
            # the field is stored under its stable base name (e.g. p1.webp).
            rel = os.path.join('project_images', img)
            if default_storage.exists(rel):
                default_storage.delete(rel)
            obj = Project(title=title, slug=slug, description=desc, technology=tech, link=link)
            obj.image.save(img, File(self.open_seed(os.path.join('project_images', img))))
            obj.save()
            self.stdout.write(self.style.SUCCESS(f"  project: {title}"))

        # ---- Skill Categories & Skills ----
        for name, skills in self.skill_categories.items():
            cat, _ = SkillCategory.objects.get_or_create(
                name=name, defaults={'order': SkillCategory.objects.count()})
            for s in skills:
                Skill.objects.get_or_create(name=s, category=cat)

        # ---- Hero Content ----
        HeroContent.objects.filter(is_active=True).update(is_active=False)
        hero, created = HeroContent.objects.get_or_create(
            name="Your Name",
            defaults={
                "greeting": "Hi, I'm",
                "titles": "Software Engineer, Maker, Designer",
                "description": "Building high-performance, dynamic web applications with Python & Django.",
                "primary_cta_text": "Explore Work",
                "secondary_cta_text": "Let's Talk",
                "is_active": True,
            },
        )
        if not created:
            hero.is_active = True
            hero.save()

        # ---- About Content ----
        AboutContent.objects.filter(is_active=True).update(is_active=False)
        about, created = AboutContent.objects.get_or_create(
            title="About Your Name",
            defaults={
                "subtitle": "Software Engineer & Creative Problem Solver",
                "summary": "Passionate about building scalable web applications and intuitive user experiences.",
                "biography": "With over 3 years of experience in the Python ecosystem, I specialize in Django and FastAPI for backend architecture, while maintaining a keen eye for clean, modern frontend design. My approach combines technical rigor with a user-centric mindset to deliver high-performance digital products.",
                "years_of_experience": 3,
                "is_active": True,
            },
        )
        if not created:
            about.is_active = True
            about.save()

        # ---- Stats ----
        if Stat.objects.count() == 0:
            for value, label, order in [
                ("6+", "Projects Completed", 1),
                ("10+", "Happy Clients", 2),
                ("3+", "Years Experience", 3),
            ]:
                Stat.objects.create(value=value, label=label, order=order)

        # ---- Themes ----
        ThemeSettings.objects.all().update(is_active=False)
        for i, (name, bg, accent, card, text, sec, pat, anim) in enumerate(self.themes):
            obj, created = ThemeSettings.objects.get_or_create(
                name=name,
                defaults={
                    "bg_color": bg, "accent_color": accent, "card_color": card,
                    "text_color": text, "text_secondary_color": sec,
                    "bg_pattern_color": pat, "anim_speed": anim,
                    "bg_pattern": "dots", "bg_pattern_opacity": 0.11,
                    "is_active": (i == 0),
                },
            )
            if not created:
                obj.bg_color = bg
                obj.accent_color = accent
                obj.card_color = card
                obj.text_color = text
                obj.text_secondary_color = sec
                obj.bg_pattern_color = pat
                obj.anim_speed = anim
                obj.bg_pattern = "dots"
                obj.bg_pattern_opacity = 0.11
                obj.is_active = (i == 0)
                obj.save()
            if i == 0 and not obj.logo:
                obj.logo.save('logo.svg', File(self.open_seed(os.path.join('logos', 'logo.svg'))))
                obj.favicon.save('favicon.svg', File(self.open_seed(os.path.join('logos', 'logo.svg'))))
                obj.save()

        # ---- Site Configuration ----
        SiteConfiguration.objects.filter(is_active=True).update(is_active=False)
        site, created = SiteConfiguration.objects.get_or_create(
            id=1,
            defaults={
                "container_width": 1640, "grid_column_width": 380, "card_border_radius": 24,
                "glass_blur": 15, "nav_padding_y": 0.8, "section_padding_y": 0.0,
                "hero_gap": 0.0, "container_padding_top": 0.0,
                "footer_copyright": "SERHAT \u00c7AM", "footer_tagline": "Crafted with Django & Passion.",
                "is_active": True,
            },
        )
        if not created:
            site.is_active = True
            site.save()

        # ---- References ----
        if Reference.objects.count() == 0:
            for name, position, company, testimonial, order in self.references:
                Reference.objects.create(
                    name=name, position=position, company=company,
                    testimonial=testimonial, order=order)

        # ---- Social Links ----
        if SocialLink.objects.count() == 0:
            SocialLink.objects.create(platform="GitHub", url="https://github.com/serhatcamm", icon_class="fa-github")
            SocialLink.objects.create(platform="LinkedIn", url="https://www.linkedin.com/in/serhatcammm/", icon_class="fa-linkedin")

        self.stdout.write(self.style.SUCCESS("Demo content seeded successfully."))
