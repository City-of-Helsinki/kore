#!/usr/bin/env python

import re
import sys

CLASS_REPLACE = {
    'Aineistotyyppi': 'DataType',
    'Ala': 'Field',
    'Arkistoaineisto': 'ArchiveData',
    'Elinkaaritapahtuma': 'LifecycleEvent',
    'ElinkaaritapahtumanLaji': 'LifecycleEventType',
    'Kaupunginosa': 'Neighborhood',
    'Kieli': 'Language',
    'Koulu': 'School',
    'KoulunKieli': 'SchoolLanguage',
    'KoulunOmistussuhde': 'SchoolOwnership',
    'KoulunPerustajat': 'SchoolFounder',
    'KoulunSukupuoli': 'SchoolGender',
    'Koulutyyppi': 'SchoolType',
    'NimenTyyppi': 'NameType',
    'Nimi': 'Name',
    'OmistajaPerustaja': 'OwnerFounder',
    'OmistajaPerustajatyyppi': 'OwnerFounderType',
    'Osoite': 'Address',
    'RakennuksenNimi': 'BuildingName',
    'RakennuksenOmistussuhde': 'BuildingOwnership',
    'RakennuksenOsoite': 'BuildingAddress',
    'RakennuksenStatus': 'BuildingStatus',
    'Rakennus': 'Building',
    'Rehtori': 'Principal',
    'Tyosuhde': 'Employership',
}

PROP_REPLACE = {
    'alkamispaiva': 'begin_day',
    'alkamiskuukausi': 'begin_month',
    'alkamisvuosi': 'begin_year',
    'paattymispaiva': 'end_day',
    'paattymiskuukausi': 'end_month',
    'paattymisvuosi': 'end_year',
    'viite': 'reference',
    'noin_a': 'approx_begin',
    'noin_p': 'approx_end',
    'sukunimi': 'surname',
    'etunimi': 'first_name',
    'arkkitehti': 'architect',
    'kiineistonumero': 'property_id',
    'kommentti': 'comment',
    'noin': 'approx',
    'omistus': 'ownership',
    'nimi': 'name',
    'kadun_nimi_suomeksi': 'street_name_fi',
    'kadun_nimi_ruotsiksi': 'street_name_sv',
    'postitoimipaikka': 'zip_code',
    'kunnan_nimi_suomeksi': 'municipality_fi',
    'kunnan_nimi_ruotsiksi': 'municipality_sv',
    'selite': 'description',
    'nimen_tyyppi': 'type',
    'sijainti': 'location',
    'paiva': 'day',
    'kuukausi': 'month',
    'vuosi': 'year',
    'paatoksen_tekija': 'decisionmaker',
    'paatoksen_paiva': 'decision_day',
    'paatoksen_kuukausi': 'decision_month',
    'paatoksen_vuosi': 'decision_year',
    'lis_tietoja': 'extra_info',
}

def modify_lines(f):
    for line in f:
        if 'db_table' in line:
            yield line
            continue
        for src, dest in CLASS_REPLACE.items():
            line = re.sub(r'\b' + src + r'\b', dest, line)
        if 'db_column' in line:
            yield line
            continue
        m = re.match(r'\s+([\w_]+)\s+=\s+models\.', line)
        if not m:
            yield line
            continue
        name = m.groups()[0]
        add = ''
        if '()' not in line:
            if 'ForeignKey' in line:
                name += '_id'
                m = re.search(r'models.ForeignKey\(\'?([\w]+)\'?[,)]', line)
                assert m is not None
                cls_name = m.groups()[0]
                if 'koulun_a' not in line and 'koulun_b' not in line:
                    line = re.sub(r'^(\s+)[\w_]+', r'\1' + cls_name.lower(), line)
            add = ', '
        line = line.replace(')', add + "db_column='" + name + "')", 1)
        if name in PROP_REPLACE:
            line = line.replace(name, PROP_REPLACE[name], 1)
        yield line

f = open('schools/models.py.old', 'r')
for l in modify_lines(f):
    sys.stdout.write(l)
