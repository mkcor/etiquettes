import re
import sys

import numpy as np
import pandas as pd


def find_address_France(adresse):
    # Find postal code in address
    cp_p = re.compile('(([0-8][0-9])|(9[0-5])|(2[ab]))[0-9]{3}')
    search = cp_p.search(adresse)
    if search is None:
        return ''
    else:
        ad1 = adresse[:search.span()[0]].replace(',', '')
        ad2 = adresse[search.span()[0]:].replace('.', '').upper()
        return [ad1, ad2]


def find_address_intnl(adresse):
    ad_lines = adresse.split('\n')
    ad_lines = [a.rstrip('\r') for a in ad_lines]
    ad_lines = [a.rstrip(',') for a in ad_lines]
    ad_lines[-1] = ad_lines[-1].upper()
    return ad_lines


def print_one_order(i, flag):
    # Load data for row i
    prenom = df.loc[i, 'Prénom']
    nom = df.loc[i, 'Nom']
    adresse = df.loc[i, 'Adresse']
    if flag == 'P':
        ad = find_address_France(adresse)
    elif flag == 'PE':
        ad = find_address_intnl(adresse)
    else:
        pass
    ad_lines = [f'<h1>{a}</h1>' for a in ad]
    commande = df.loc[i, 'Commande']
    items = [f'<li>{c}</li>' for c in commande.split(';')]
    string = f'<h1 class="tiny-margin"> {prenom.title()} {nom.upper()} </h1>'
    for al in ad_lines:
        string += al
    string += (
        '<p class="top-margin">Expéditeur :</p>'
        '<p>Lorem ipsum dolor sit amet</p>'
        '<p>67000 CONSECTETUR</p>'
        '<p class="top-margin">Commande :</p>'
        '<ul>'
    )
    for it in items:
        string += it
    string += (
        '</ul>'
        '</html>'
        '</body>'
    )

    return string


def print_sheet(i, flag):
    # Print two consecutive orders on one sheet
    with open(file_name, 'x', encoding='utf-8') as f:
        f.write('<!DOCTYPE html>')
        f.write('<html>')
        f.write('<body>')
        f.write('<style>')
        f.write('.tiny-margin { margin-top: 0.8cm; }')
        f.write('.top-margin { margin-top: 2cm; }')
        f.write('</style>')

        f.write(print_one_order(i, flag))
        f.write(print_one_order(i + 1, flag))

        f.write('</html>')
        f.write('</body>')

if __name__ == '__main__':
    # Load table
    df = pd.read_csv('feuille_commandes.csv')
    # Filter for orders to print
    flag = sys.argv[1]
    if flag not in ['P', 'PE']:
        raise ValueError('Donner la valeur P ou PE au paramètre flag')
    df = df[df['Flag'] == flag]
    # Replace NaN's with empty strings
    df.fillna('', inplace=True)
    # Reset index
    df.reset_index(drop=True, inplace=True)
    for i in range(0, df.shape[0], 2):
        file_name = f'etiquette_{i}.html'
        print_sheet(i, flag)
