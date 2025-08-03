from django.core.management.base import BaseCommand

from app.portfolio.models import DeveloperSkill


class Command(BaseCommand):
    help = "Populate DeveloperSkill instances with sample data"

    def handle(self, *args, **options):
        # Clear existing skills
        DeveloperSkill.objects.all().delete()
        self.stdout.write("Cleared existing developer skills")

        # Comprehensive developer skills dataset (200+ items)
        skills_data = [
            # Programming Languages
            {"name": "Python", "level": "advanced"},
            {"name": "JavaScript", "level": "advanced"},
            {"name": "TypeScript", "level": "intermediate"},
            {"name": "Java", "level": "intermediate"},
            {"name": "C#", "level": "intermediate"},
            {"name": "C++", "level": "beginner"},
            {"name": "C", "level": "beginner"},
            {"name": "Go", "level": "intermediate"},
            {"name": "Rust", "level": "beginner"},
            {"name": "PHP", "level": "intermediate"},
            {"name": "Ruby", "level": "intermediate"},
            {"name": "Swift", "level": "beginner"},
            {"name": "Kotlin", "level": "beginner"},
            {"name": "Scala", "level": "beginner"},
            {"name": "R", "level": "intermediate"},
            {"name": "MATLAB", "level": "beginner"},
            {"name": "Perl", "level": "beginner"},
            {"name": "Lua", "level": "beginner"},
            {"name": "Dart", "level": "beginner"},
            {"name": "Elixir", "level": "beginner"},
            # Web Technologies - Frontend
            {"name": "HTML5", "level": "advanced"},
            {"name": "CSS3", "level": "advanced"},
            {"name": "SASS/SCSS", "level": "advanced"},
            {"name": "LESS", "level": "intermediate"},
            {"name": "Stylus", "level": "beginner"},
            {"name": "PostCSS", "level": "intermediate"},
            {"name": "Tailwind CSS", "level": "advanced"},
            {"name": "Bootstrap", "level": "advanced"},
            {"name": "Bulma", "level": "intermediate"},
            {"name": "Foundation", "level": "intermediate"},
            {"name": "Material-UI", "level": "intermediate"},
            {"name": "Ant Design", "level": "intermediate"},
            {"name": "Chakra UI", "level": "intermediate"},
            # JavaScript Frameworks & Libraries
            {"name": "React", "level": "advanced"},
            {"name": "Vue.js", "level": "intermediate"},
            {"name": "Angular", "level": "intermediate"},
            {"name": "Svelte", "level": "beginner"},
            {"name": "jQuery", "level": "advanced"},
            {"name": "Alpine.js", "level": "intermediate"},
            {"name": "Lit", "level": "beginner"},
            {"name": "Stimulus", "level": "intermediate"},
            {"name": "Ember.js", "level": "beginner"},
            {"name": "Backbone.js", "level": "beginner"},
            # React Ecosystem
            {"name": "Next.js", "level": "advanced"},
            {"name": "Gatsby", "level": "intermediate"},
            {"name": "React Router", "level": "advanced"},
            {"name": "Redux", "level": "intermediate"},
            {"name": "MobX", "level": "beginner"},
            {"name": "React Query", "level": "intermediate"},
            {"name": "SWR", "level": "intermediate"},
            {"name": "Recoil", "level": "beginner"},
            {"name": "Zustand", "level": "intermediate"},
            # Vue Ecosystem
            {"name": "Nuxt.js", "level": "intermediate"},
            {"name": "Vuex", "level": "intermediate"},
            {"name": "Pinia", "level": "beginner"},
            {"name": "Vue Router", "level": "intermediate"},
            {"name": "Quasar", "level": "beginner"},
            # Backend Frameworks
            {"name": "Django", "level": "advanced"},
            {"name": "Django REST Framework", "level": "advanced"},
            {"name": "FastAPI", "level": "intermediate"},
            {"name": "Flask", "level": "intermediate"},
            {"name": "Express.js", "level": "intermediate"},
            {"name": "Koa.js", "level": "beginner"},
            {"name": "Fastify", "level": "beginner"},
            {"name": "NestJS", "level": "intermediate"},
            {"name": "ASP.NET Core", "level": "intermediate"},
            {"name": "Spring Boot", "level": "intermediate"},
            {"name": "Ruby on Rails", "level": "intermediate"},
            {"name": "Laravel", "level": "intermediate"},
            {"name": "Symfony", "level": "beginner"},
            {"name": "CodeIgniter", "level": "beginner"},
            # Content Management Systems
            {"name": "Wagtail CMS", "level": "advanced"},
            {"name": "WordPress", "level": "intermediate"},
            {"name": "Drupal", "level": "beginner"},
            {"name": "Joomla", "level": "beginner"},
            {"name": "Strapi", "level": "intermediate"},
            {"name": "Contentful", "level": "intermediate"},
            {"name": "Sanity", "level": "intermediate"},
            {"name": "Ghost", "level": "intermediate"},
            # Databases
            {"name": "PostgreSQL", "level": "advanced"},
            {"name": "MySQL", "level": "intermediate"},
            {"name": "SQLite", "level": "advanced"},
            {"name": "MongoDB", "level": "intermediate"},
            {"name": "Redis", "level": "intermediate"},
            {"name": "Elasticsearch", "level": "intermediate"},
            {"name": "InfluxDB", "level": "beginner"},
            {"name": "CouchDB", "level": "beginner"},
            {"name": "Neo4j", "level": "beginner"},
            {"name": "DynamoDB", "level": "beginner"},
            {"name": "Cassandra", "level": "beginner"},
            {"name": "MariaDB", "level": "intermediate"},
            # Cloud Platforms
            {"name": "AWS", "level": "intermediate"},
            {"name": "Google Cloud Platform", "level": "intermediate"},
            {"name": "Microsoft Azure", "level": "beginner"},
            {"name": "DigitalOcean", "level": "intermediate"},
            {"name": "Linode", "level": "intermediate"},
            {"name": "Vultr", "level": "intermediate"},
            {"name": "Heroku", "level": "advanced"},
            {"name": "Vercel", "level": "advanced"},
            {"name": "Netlify", "level": "advanced"},
            {"name": "Railway", "level": "intermediate"},
            {"name": "Render", "level": "intermediate"},
            # DevOps & Infrastructure
            {"name": "Docker", "level": "advanced"},
            {"name": "Kubernetes", "level": "intermediate"},
            {"name": "Docker Compose", "level": "advanced"},
            {"name": "Ansible", "level": "intermediate"},
            {"name": "Terraform", "level": "intermediate"},
            {"name": "Vagrant", "level": "intermediate"},
            {"name": "Chef", "level": "beginner"},
            {"name": "Puppet", "level": "beginner"},
            {"name": "Helm", "level": "beginner"},
            {"name": "Jenkins", "level": "intermediate"},
            {"name": "GitLab CI/CD", "level": "intermediate"},
            {"name": "GitHub Actions", "level": "advanced"},
            {"name": "CircleCI", "level": "intermediate"},
            {"name": "Travis CI", "level": "intermediate"},
            # Version Control
            {"name": "Git", "level": "advanced"},
            {"name": "GitHub", "level": "advanced"},
            {"name": "GitLab", "level": "intermediate"},
            {"name": "Bitbucket", "level": "intermediate"},
            {"name": "SVN", "level": "beginner"},
            {"name": "Mercurial", "level": "beginner"},
            # Testing
            {"name": "Jest", "level": "intermediate"},
            {"name": "Pytest", "level": "advanced"},
            {"name": "Unittest", "level": "advanced"},
            {"name": "Cypress", "level": "intermediate"},
            {"name": "Selenium", "level": "intermediate"},
            {"name": "Playwright", "level": "intermediate"},
            {"name": "Testing Library", "level": "intermediate"},
            {"name": "Mocha", "level": "beginner"},
            {"name": "Chai", "level": "beginner"},
            {"name": "PHPUnit", "level": "intermediate"},
            {"name": "JUnit", "level": "intermediate"},
            {"name": "RSpec", "level": "beginner"},
            # Build Tools & Bundlers
            {"name": "Webpack", "level": "intermediate"},
            {"name": "Vite", "level": "advanced"},
            {"name": "Rollup", "level": "intermediate"},
            {"name": "Parcel", "level": "intermediate"},
            {"name": "esbuild", "level": "intermediate"},
            {"name": "Gulp", "level": "intermediate"},
            {"name": "Grunt", "level": "beginner"},
            {"name": "Snowpack", "level": "beginner"},
            # Package Managers
            {"name": "npm", "level": "advanced"},
            {"name": "Yarn", "level": "advanced"},
            {"name": "pnpm", "level": "intermediate"},
            {"name": "pip", "level": "advanced"},
            {"name": "Poetry", "level": "intermediate"},
            {"name": "Pipenv", "level": "intermediate"},
            {"name": "Composer", "level": "intermediate"},
            {"name": "Bundler", "level": "beginner"},
            # Mobile Development
            {"name": "React Native", "level": "intermediate"},
            {"name": "Flutter", "level": "beginner"},
            {"name": "Ionic", "level": "beginner"},
            {"name": "Cordova/PhoneGap", "level": "beginner"},
            {"name": "Xamarin", "level": "beginner"},
            {"name": "Native iOS", "level": "beginner"},
            {"name": "Native Android", "level": "beginner"},
            # Desktop Development
            {"name": "Electron", "level": "intermediate"},
            {"name": "Tauri", "level": "beginner"},
            {"name": "Qt", "level": "beginner"},
            {"name": "GTK", "level": "beginner"},
            {"name": "WPF", "level": "beginner"},
            {"name": "WinForms", "level": "beginner"},
            # Data Science & ML
            {"name": "NumPy", "level": "intermediate"},
            {"name": "Pandas", "level": "intermediate"},
            {"name": "Matplotlib", "level": "intermediate"},
            {"name": "Seaborn", "level": "intermediate"},
            {"name": "Scikit-learn", "level": "beginner"},
            {"name": "TensorFlow", "level": "beginner"},
            {"name": "PyTorch", "level": "beginner"},
            {"name": "Keras", "level": "beginner"},
            {"name": "Jupyter", "level": "intermediate"},
            {"name": "Apache Spark", "level": "beginner"},
            # Monitoring & Analytics
            {"name": "Google Analytics", "level": "intermediate"},
            {"name": "Sentry", "level": "intermediate"},
            {"name": "New Relic", "level": "beginner"},
            {"name": "Datadog", "level": "beginner"},
            {"name": "Prometheus", "level": "beginner"},
            {"name": "Grafana", "level": "beginner"},
            {"name": "Mixpanel", "level": "beginner"},
            # Communication & Project Management
            {"name": "Slack", "level": "advanced"},
            {"name": "Discord", "level": "intermediate"},
            {"name": "Microsoft Teams", "level": "intermediate"},
            {"name": "Zoom", "level": "advanced"},
            {"name": "Jira", "level": "intermediate"},
            {"name": "Trello", "level": "advanced"},
            {"name": "Asana", "level": "intermediate"},
            {"name": "Notion", "level": "advanced"},
            {"name": "Confluence", "level": "intermediate"},
            # Design & Prototyping
            {"name": "Figma", "level": "intermediate"},
            {"name": "Adobe XD", "level": "beginner"},
            {"name": "Sketch", "level": "beginner"},
            {"name": "InVision", "level": "beginner"},
            {"name": "Photoshop", "level": "intermediate"},
            {"name": "Illustrator", "level": "beginner"},
            # API Technologies
            {"name": "REST APIs", "level": "advanced"},
            {"name": "GraphQL", "level": "intermediate"},
            {"name": "gRPC", "level": "beginner"},
            {"name": "WebSockets", "level": "intermediate"},
            {"name": "Socket.io", "level": "intermediate"},
            {"name": "Postman", "level": "advanced"},
            {"name": "Insomnia", "level": "intermediate"},
            {"name": "Swagger/OpenAPI", "level": "intermediate"},
            # Security
            {"name": "OAuth", "level": "intermediate"},
            {"name": "JWT", "level": "intermediate"},
            {"name": "SSL/TLS", "level": "intermediate"},
            {"name": "OWASP", "level": "intermediate"},
            {"name": "Penetration Testing", "level": "beginner"},
            {"name": "Cryptography", "level": "beginner"},
        ]

        created_skills = []
        for skill_data in skills_data:
            skill = DeveloperSkill.objects.create(
                name=skill_data["name"], level=skill_data["level"]
            )
            created_skills.append(skill)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {len(created_skills)} developer skills: "
                f'{", ".join([skill.name for skill in created_skills])}'
            )
        )
