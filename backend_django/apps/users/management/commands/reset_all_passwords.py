"""
Reset all admin passwords to admin123.
Use this to force password updates on existing accounts.
"""
from django.core.management.base import BaseCommand
from apps.users.models import AdminUser

DEFAULT_ADMINS = [
    'safety_admin',
    'dean_seait',
    'dean_agriculture',
    'dean_criminology',
    'dean_business',
    'dean_ict',
    'dean_civil_eng',
    'dean_teacher_ed',
    'dean_tesda',
    'dean_gen_ed',
    'dean_basic_ed',
    'head_agriculture',
    'head_criminology',
    'head_business',
    'head_ict',
    'head_civil_eng',
    'head_teacher_ed',
    'head_tesda',
    'head_gen_ed',
    'head_basic_ed',
]

class Command(BaseCommand):
    help = 'Reset all admin passwords to admin123'

    def handle(self, *args, **kwargs):
        updated = 0
        for username in DEFAULT_ADMINS:
            try:
                user = AdminUser.objects.get(username=username)
                user.set_password('admin123')
                user.save()
                self.stdout.write(self.style.SUCCESS(f'  Updated: {username}'))
                updated += 1
            except AdminUser.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  Missing: {username}'))
        
        # Also update the default admin user
        try:
            admin_user = AdminUser.objects.get(username='admin')
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(f'  Updated: admin'))
            updated += 1
        except AdminUser.DoesNotExist:
            self.stdout.write(self.style.WARNING(f'  Missing: admin'))
        
        self.stdout.write(self.style.SUCCESS(f'\nDone. {updated} password(s) reset to admin123.'))
