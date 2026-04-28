"""
Seed initial navigation paths for AdminPathManager.
Creates Path and PathPoint objects that the frontend expects.
"""
from django.core.management.base import BaseCommand
from apps.navigation.models import Path, PathPoint
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed navigation paths for AdminPathManager'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding navigation paths...')
        
        # Get or create a system user for the paths
        system_user, _ = User.objects.get_or_create(
            username='system',
            defaults={
                'email': 'system@technopath.edu',
                'is_staff': True,
                'is_active': True
            }
        )
        if not system_user.password:
            system_user.set_password('system123')
            system_user.save()
        
        # Define paths with their points (element_ids from the SVG map)
        paths_data = [
            {
                'name': 'Gate to Admin Building',
                'description': 'Main entrance to administration',
                'from_element': 'gate',
                'to_element': 'admin',
                'points': [
                    {'element_id': 'gate', 'x': 100, 'y': 100},
                    {'element_id': 'path-gate-admin', 'x': 150, 'y': 125},
                    {'element_id': 'admin', 'x': 200, 'y': 150},
                ]
            },
            {
                'name': 'Admin to Library',
                'description': 'Administration building to library',
                'from_element': 'admin',
                'to_element': 'library',
                'points': [
                    {'element_id': 'admin', 'x': 200, 'y': 150},
                    {'element_id': 'path-admin-lib', 'x': 250, 'y': 175},
                    {'element_id': 'library', 'x': 300, 'y': 200},
                ]
            },
            {
                'name': 'Library to Canteen',
                'description': 'Library to school canteen',
                'from_element': 'library',
                'to_element': 'canteen',
                'points': [
                    {'element_id': 'library', 'x': 300, 'y': 200},
                    {'element_id': 'path-lib-canteen', 'x': 275, 'y': 250},
                    {'element_id': 'canteen', 'x': 250, 'y': 300},
                ]
            },
            {
                'name': 'Canteen to Gym',
                'description': 'Canteen to gymnasium',
                'from_element': 'canteen',
                'to_element': 'gym',
                'points': [
                    {'element_id': 'canteen', 'x': 250, 'y': 300},
                    {'element_id': 'path-canteen-gym', 'x': 325, 'y': 275},
                    {'element_id': 'gym', 'x': 400, 'y': 250},
                ]
            },
            {
                'name': 'Gym to ICT Building',
                'description': 'Gymnasium to ICT building',
                'from_element': 'gym',
                'to_element': 'ict',
                'points': [
                    {'element_id': 'gym', 'x': 400, 'y': 250},
                    {'element_id': 'path-gym-ict', 'x': 375, 'y': 325},
                    {'element_id': 'ict', 'x': 350, 'y': 400},
                ]
            },
            {
                'name': 'ICT to Engineering',
                'description': 'ICT to Engineering building',
                'from_element': 'ict',
                'to_element': 'engineering',
                'points': [
                    {'element_id': 'ict', 'x': 350, 'y': 400},
                    {'element_id': 'path-ict-eng', 'x': 400, 'y': 375},
                    {'element_id': 'engineering', 'x': 450, 'y': 350},
                ]
            },
            {
                'name': 'Engineering to Nursing',
                'description': 'Engineering to Nursing building',
                'from_element': 'engineering',
                'to_element': 'nursing',
                'points': [
                    {'element_id': 'engineering', 'x': 450, 'y': 350},
                    {'element_id': 'path-eng-nurse', 'x': 475, 'y': 400},
                    {'element_id': 'nursing', 'x': 500, 'y': 450},
                ]
            },
            {
                'name': 'Nursing to Education',
                'description': 'Nursing to Education building',
                'from_element': 'nursing',
                'to_element': 'educ',
                'points': [
                    {'element_id': 'nursing', 'x': 500, 'y': 450},
                    {'element_id': 'path-nurse-educ', 'x': 525, 'y': 375},
                    {'element_id': 'educ', 'x': 550, 'y': 300},
                ]
            },
            {
                'name': 'Gate to Parking',
                'description': 'Main entrance to parking area',
                'from_element': 'gate',
                'to_element': 'parking',
                'points': [
                    {'element_id': 'gate', 'x': 100, 'y': 100},
                    {'element_id': 'path-gate-park', 'x': 125, 'y': 175},
                    {'element_id': 'parking', 'x': 150, 'y': 250},
                ]
            },
        ]
        
        created_paths = 0
        for path_data in paths_data:
            path, created = Path.objects.get_or_create(
                name=path_data['name'],
                defaults={
                    'description': path_data['description'],
                    'is_active': True,
                    'created_by': system_user
                }
            )
            
            if created:
                # Create PathPoints for this path
                for i, point_data in enumerate(path_data['points']):
                    PathPoint.objects.create(
                        path=path,
                        sequence=i,
                        element_id=point_data['element_id'],
                        x=point_data['x'],
                        y=point_data['y']
                    )
                created_paths += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {created_paths} new paths with {sum(len(p["points"]) for p in paths_data)} points'))
        
        # Create default admin user if none exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@technopath.edu',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('Created default admin user: admin / admin123'))
        
        self.stdout.write(self.style.SUCCESS('Navigation path seeding complete!'))
