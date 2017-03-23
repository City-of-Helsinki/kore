import re
from munigeo.models import Address as MuniAddress


def geocode_address(address_street, town):
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
    return match
