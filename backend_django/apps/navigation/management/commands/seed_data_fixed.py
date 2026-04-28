"""
Seed initial navigation data into the database.
Uses correct model structure: NavigationNode, NavigationEdge, Path, PathPoint
"""
from django.core.management.base import BaseCommand
from apps.navigation.models import NavigationNode, NavigationEdge, Path, PathPoint
from apps.facilities.models import Facility
from apps.rooms.models import Room
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed initial navigation data with correct model structure'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding navigation data...')
        
        # Create default nodes (campus locations)
        nodes_data = [
            {'map_svg_id': 'gate', 'name': 'College Gate', 'x': 100, 'y': 100, 'node_type': 'entrance', 'floor': 1},
            {'map_svg_id': 'admin', 'name': 'Admin Building', 'x': 200, 'y': 150, 'node_type': 'building', 'floor': 1},
            {'map_svg_id': 'library', 'name': 'Library', 'x': 300, 'y': 200, 'node_type': 'building', 'floor': 1},
            {'map_svg_id': 'canteen', 'name': 'Canteen', 'x': 250, 'y': 300, 'node_type': 'facility', 'floor': 1},
            {'map_svg_id': 'gym', 'name': 'Gymnasium', 'x': 400, 'y': 250, 'node_type': 'facility', 'floor': 1},
            {'map_svg_id': 'ict', 'name': 'ICT Building', 'x': 350, 'y': 400, 'node_type': 'building', 'floor': 1},
            {'map_svg_id': 'engineering', 'name': 'Engineering Building', 'x': 450, 'y': 350, 'node_type': 'building', 'floor': 1},
            {'map_svg_id': 'nursing', 'name': 'Nursing Building', 'x': 500, 'y': 450, 'node_type': 'building', 'floor': 1},
            {'map_svg_id': 'educ', 'name': 'Education Building', 'x': 550, 'y': 300, 'node_type': 'building', 'floor': 1},
            {'map_svg_id': 'parking', 'name': 'Parking Area', 'x': 150, 'y': 250, 'node_type': 'facility', 'floor': 1},
        ]
        
        created_nodes = 0
        for node_data in nodes_data:
            node, created = NavigationNode.objects.get_or_create(
                map_svg_id=node_data['map_svg_id'],
                defaults=node_data
            )
            if created:
                created_nodes += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {created_nodes} new nodes'))
        
        # Create navigation edges (connections between nodes)
        edges_data = [
            ('gate', 'admin', 100),
            ('admin', 'library', 150),
            ('library', 'canteen', 100),
            ('canteen', 'gym', 150),
            ('gym', 'ict', 150),
            ('ict', 'engineering', 100),
            ('engineering', 'nursing', 100),
            ('nursing', 'educ', 150),
            ('gate', 'parking', 150),
        ]
        
        created_edges = 0
        for from_id, to_id, distance in edges_data:
            from_node = NavigationNode.objects.filter(map_svg_id=from_id).first()
            to_node = NavigationNode.objects.filter(map_svg_id=to_id).first()
            
            if from_node and to_node:
                edge, created = NavigationEdge.objects.get_or_create(
                    from_node=from_node,
                    to_node=to_node,
                    defaults={'distance': distance}
                )
                if created:
                    created_edges += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {created_edges} new edges'))
        
        # Create default admin user if none exists
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@technopath.edu',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('Created default admin user: admin / admin123'))
        
        self.stdout.write(self.style.SUCCESS('Navigation data seeding complete!'))
