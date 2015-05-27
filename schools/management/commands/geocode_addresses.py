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
                    dest='rewrite_existing',
                    default=False,
                    help='Rewrites all automatically geocoded addresses'),
    )

    def handle(self, *args, **options):
        for address in Address.objects.all():
            if hasattr(address, 'location'):
                location = address.location
            else:
                location = AddressLocation(address=address, handmade=False)

            # Skip all manually geocoded locations
            if location.handmade:
                continue

            if location.location is not None and not options['rewrite_existing']:
                continue

            address_street, town = str(address).split(', ')
            address_street_number = re.split('( [0-9]+)', address_street)
            address_street = address_street_number[0]
            if len(address_street_number) > 1:
                address_number = address_street_number[1].strip()
            else:
                address_number = None

            if address_number is not None:
                match = MuniAddress.objects.filter(
                    street__name=address_street, number=address_number,
                    street__municipality__name=town
                ).first()
            else:
                match = None

            if match is not None:
                self.stdout.write(str(address) + ' geocoded as ' + str(match))
                location.location = match.location
            else:
                location.location = None
                self.stdout.write(str(address) + ' match not found')
            location.save()
