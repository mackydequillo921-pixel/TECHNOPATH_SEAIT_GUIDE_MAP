from django.core.management.base import BaseCommand
from apps.users.models import AdminUser

# All admin accounts to reset password to '123'
ADMIN_ACCOUNTS = [
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
    help = 'Reset all SEAIT admin account passwords to 123'

    def handle(self, *args, **kwargs):
        reset_count = 0
        for username in ADMIN_ACCOUNTS:
            try:
                user = AdminUser.objects.get(username=username)
                user.set_password('123')
                user.save()
                self.stdout.write(self.style.SUCCESS(f'  Password reset: {username}'))
                reset_count += 1
            except AdminUser.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  Not found: {username}'))
        
        self.stdout.write(self.style.SUCCESS(f'\nDone! {reset_count} admin account(s) password reset to "123".'))
        self.stdout.write('\nAll accounts now use password: 123')
