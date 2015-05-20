from django.core.management.base import BaseCommand
from schools.models import *
from munigeo.models import Address as MuniAddress
import re


class Command(BaseCommand):
    help = 'Geocodes all addresses in Address.objects'

    def handle(self, *args, **options):
        for address in Address.objects.all():
            if hasattr(address, 'location'):
                continue
            address_street_town = str(address).split(', ')
            address_street_number = re.split('( [0-9]+)', address_street_town[0])
            address_street = address_street_number[0]
            if len(address_street_number) > 1:
                address_number = address_street_number[1].strip()
            match = MuniAddress.objects.filter(
                street__name=address_street, number=address_number,
                street__municipality__name=address_street_town[1]
            ).first()
            self.stdout.write(str(address) + ' geocoded as ' + str(match))
            if match is not None:
                location = AddressLocation(address=address, location=match.location)
                location.save()
