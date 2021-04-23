import re

import numpy as np
import pandas as pd


def print_one_order(i):
    # Load data for row i
    prenom = df.loc[i, 'Prénom']
    nom = df.loc[i, 'Nom']
    adresse = df.loc[i, 'Adresse']
    commande = df.loc[i, 'Commande']
    # Find postal code in address
    cp_p = re.compile('(([0-8][0-9])|(9[0-5])|(2[ab]))[0-9]{3}')
    search = cp_p.search(adresse)
    if search is None:
        ad1 = ''
        ad2 = ''
    else:
        ad1 = adresse[:search.span()[0]].replace(',','')
        ad2 = adresse[search.span()[0]:].replace('.','')

    items = [f'<li>{c}</li>' for c in commande.split(';')]
    string = (
        f'<h1 class="tiny-margin"> {prenom} {nom.upper()} </h1>'
        f'<h1> {ad1} </h1>'
        f'<h1> {ad2.upper()} </h1>'
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


def print_sheet(i):
    # Print two consecutive orders on one sheet
    with open(file_name, 'x') as f:
        f.write('<!DOCTYPE html>')
        f.write('<html>')
        f.write('<body>')
        f.write('<style>')
        f.write('.tiny-margin { margin-top: 0.8cm; }')
        f.write('.top-margin { margin-top: 2cm; }')
        f.write('</style>')

        f.write(print_one_order(i))
        f.write(print_one_order(i + 1))

        f.write('</html>')
        f.write('</body>')

if __name__ == '__main__':
    # Load table
    df = pd.read_csv('feuille_commandes.csv')
    # Filter for orders to print
    df = df[df['Flag'] == 'P']
    # Replace NaN's with empty strings
    df.fillna('', inplace=True)
    # Reset index
    df.reset_index(drop=True, inplace=True)
    for i in range(0, df.shape[0], 2):
        file_name = f'etiquette_{i}.html'
        print_sheet(i)
