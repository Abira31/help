from django.core.management.base import BaseCommand
from core.create_fake_data import CreateFakeData

class Command(BaseCommand):
    help = 'Create facke data'
    def handle(self, *args, **kwargs):
       CreateFakeData.create()






