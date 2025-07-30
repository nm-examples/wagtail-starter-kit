from django.core.management.base import BaseCommand
from app.portfolio.models import DeveloperSkill


class Command(BaseCommand):
    help = 'Populate DeveloperSkill instances with sample data'

    def handle(self, *args, **options):
        # Clear existing skills
        DeveloperSkill.objects.all().delete()
        self.stdout.write('Cleared existing developer skills')

        # Sample developer skills
        skills_data = [
            {'name': 'Python', 'level': 'advanced'},
            {'name': 'JavaScript', 'level': 'intermediate'},
            {'name': 'React', 'level': 'intermediate'},
            {'name': 'Django', 'level': 'advanced'},
            {'name': 'Wagtail CMS', 'level': 'advanced'},
            {'name': 'HTML/CSS', 'level': 'advanced'},
            {'name': 'Git', 'level': 'intermediate'},
            {'name': 'Docker', 'level': 'intermediate'},
            {'name': 'PostgreSQL', 'level': 'intermediate'},
            {'name': 'AWS', 'level': 'beginner'},
            {'name': 'TypeScript', 'level': 'beginner'},
            {'name': 'Vue.js', 'level': 'beginner'},
        ]

        created_skills = []
        for skill_data in skills_data:
            skill = DeveloperSkill.objects.create(
                name=skill_data['name'],
                level=skill_data['level']
            )
            created_skills.append(skill)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {len(created_skills)} developer skills: '
                f'{", ".join([skill.name for skill in created_skills])}'
            )
        ) 
