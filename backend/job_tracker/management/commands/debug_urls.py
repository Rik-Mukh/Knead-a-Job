from django.core.management.base import BaseCommand
from django.urls import get_resolver
from job_tracker.urls import router

class Command(BaseCommand):
    help = 'Debug URL patterns for job tracker'

    def handle(self, *args, **options):
        self.stdout.write("🔍 DEBUG: Job Tracker Router URLs:")
        for pattern in router.urls:
            self.stdout.write(f"  - {pattern.pattern} -> {pattern.name}")
        
        self.stdout.write("\n🔍 DEBUG: All URL patterns:")
        resolver = get_resolver()
        for pattern in resolver.url_patterns:
            if hasattr(pattern, 'url_patterns'):
                for sub_pattern in pattern.url_patterns:
                    self.stdout.write(f"  - {sub_pattern.pattern} -> {sub_pattern.name}")
            else:
                self.stdout.write(f"  - {pattern.pattern} -> {pattern.name}")
