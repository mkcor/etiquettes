import re

import numpy as np
import pandas as pd


def print_sheet(i):
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

    items = [f'<li>{c}</li>' for c in commande.split(";")]

    with open(file_name, 'x') as f:
        f.write('<!DOCTYPE html>')
        f.write('<html>')
        f.write('<body>')
        f.write('<style>')
        f.write('.top-margin { margin-top: 4cm; }')
        f.write('</style>')

        f.write(f'<h1> {prenom} {nom.upper()} </h1>')
        f.write(f'<h1> {ad1} </h1>')
        f.write(f'<h1> {ad2.upper()} </h1>')

        f.write('<p class="top-margin">Expéditeur :</p>')
        f.write('<p>Lorem ipsum dolor sit amet</p>')
        f.write('<p>67000 CONSECTETUR</p>')

        f.write('<p class="top-margin">Commande :</p>')
        f.write('<ul>')
        for it in items:
            f.write(it)
        f.write('</ul>')

        f.write('</html>')
        f.write('</body>')

if __name__ == '__main__':
    # Load table
    df = pd.read_csv('feuille_commandes.csv')
    # Replace NaN's with empty strings
    df.fillna('', inplace=True)
    for i in range(df.shape[0]):
        file_name = f'etiquette_{i}.html'
        print_sheet(i)
