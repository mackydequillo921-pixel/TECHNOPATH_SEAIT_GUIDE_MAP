"""
Seed initial navigation data into the database.
Run this to create default paths, nodes, and admin user.
"""
from django.core.management.base import BaseCommand
from apps.navigation.models import SVGPath, NavigationNode
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed initial navigation data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding navigation data...')
        
        # Create default nodes (campus locations)
        nodes_data = [
            {'node_id': 'gate', 'name': 'College Gate', 'x': 100, 'y': 100, 'type': 'entrance'},
            {'node_id': 'admin', 'name': 'Admin Building', 'x': 200, 'y': 150, 'type': 'building'},
            {'node_id': 'library', 'name': 'Library', 'x': 300, 'y': 200, 'type': 'building'},
            {'node_id': 'canteen', 'name': 'Canteen', 'x': 250, 'y': 300, 'type': 'facility'},
            {'node_id': 'gym', 'name': 'Gymnasium', 'x': 400, 'y': 250, 'type': 'facility'},
            {'node_id': 'ict', 'name': 'ICT Building', 'x': 350, 'y': 400, 'type': 'building'},
            {'node_id': 'engineering', 'name': 'Engineering Building', 'x': 450, 'y': 350, 'type': 'building'},
            {'node_id': 'nursing', 'name': 'Nursing Building', 'x': 500, 'y': 450, 'type': 'building'},
            {'node_id': 'educ', 'name': 'Education Building', 'x': 550, 'y': 300, 'type': 'building'},
            {'node_id': 'parking', 'name': 'Parking Area', 'x': 150, 'y': 250, 'type': 'facility'},
        ]
        
        for node_data in nodes_data:
            NavigationNode.objects.get_or_create(
                node_id=node_data['node_id'],
                defaults=node_data
            )
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(nodes_data)} nodes'))
        
        # Create paths between nodes
        paths_data = [
            {'path_id': 'gate-to-admin', 'name': 'Gate to Admin', 'from_node': 'gate', 'to_node': 'admin'},
            {'path_id': 'admin-to-library', 'name': 'Admin to Library', 'from_node': 'admin', 'to_node': 'library'},
            {'path_id': 'library-to-canteen', 'name': 'Library to Canteen', 'from_node': 'library', 'to_node': 'canteen'},
            {'path_id': 'canteen-to-gym', 'name': 'Canteen to Gym', 'from_node': 'canteen', 'to_node': 'gym'},
            {'path_id': 'gym-to-ict', 'name': 'Gym to ICT', 'from_node': 'gym', 'to_node': 'ict'},
            {'path_id': 'ict-to-engineering', 'name': 'ICT to Engineering', 'from_node': 'ict', 'to_node': 'engineering'},
            {'path_id': 'engineering-to-nursing', 'name': 'Engineering to Nursing', 'from_node': 'engineering', 'to_node': 'nursing'},
            {'path_id': 'nursing-to-educ', 'name': 'Nursing to Education', 'from_node': 'nursing', 'to_node': 'educ'},
            {'path_id': 'gate-to-parking', 'name': 'Gate to Parking', 'from_node': 'gate', 'to_node': 'parking'},
        ]
        
        for path_data in paths_data:
            from_node = NavigationNode.objects.filter(node_id=path_data['from_node']).first()
            to_node = NavigationNode.objects.filter(node_id=path_data['to_node']).first()
            
            if from_node and to_node:
                SVGPath.objects.get_or_create(
                    path_id=path_data['path_id'],
                    defaults={
                        'name': path_data['name'],
                        'from_node': from_node,
                        'to_node': to_node,
                        'svg_d': f'M {from_node.x} {from_node.y} L {to_node.x} {to_node.y}'
                    }
                )
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(paths_data)} paths'))
        
        # Create default admin user if none exists
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@technopath.edu',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('Created default admin user: admin / admin123'))
        
        self.stdout.write(self.style.SUCCESS('Data seeding complete!'))
