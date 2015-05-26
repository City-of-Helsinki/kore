from django.core.management.base import BaseCommand
from schools.models import *
from munigeo.models import Address as MuniAddress
import re
from optparse import make_option


class Command(BaseCommand):
    help = 'Geocodes all addresses in Address.objects'
    option_list = BaseCommand.option_list + (
        make_option('--rewrite-existing',
                    action='store_true',
                    dest='remove',
                    default=False,
                    help='Rewrites all automatically geocoded addresses'),
    )

    def handle(self, *args, **options):
        for address in Address.objects.all():
            if hasattr(address, 'location'):
                if options['remove'] and not address.location.handmade:
                    address.location.delete()
                    self.stdout.write(str(address) + ' geocoding deleted')
                else:
                    continue
            address_street, town = str(address).split(', ')
            address_street_number = re.split('( [0-9]+)', address_street)
            address_street = address_street_number[0]
            if len(address_street_number) > 1:
                address_number = address_street_number[1].strip()
            else:
                continue
            match = MuniAddress.objects.filter(
                street__name=address_street, number=address_number,
                street__municipality__name=town
            ).first()
            if match is not None:
                self.stdout.write(str(address) + ' geocoded as ' + str(match))
                location = AddressLocation(address=address, location=match.location)
                location.save()
            else:
                self.stdout.write(str(address) + ' match not found')
