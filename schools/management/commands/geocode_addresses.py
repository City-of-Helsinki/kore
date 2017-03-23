from django.core.management.base import BaseCommand
from schools.models import *
from munigeo.models import Address as MuniAddress
import re
from optparse import make_option

from schools.utils import geocode_address


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

            match = geocode_address(address.street_name_fi, address.municipality_fi)

            if match is not None:
                self.stdout.write(str(address) + ' geocoded as ' + str(match))
                location.location = match.location
            else:
                location.location = None
                self.stdout.write(str(address) + ' match not found')
            location.save()
