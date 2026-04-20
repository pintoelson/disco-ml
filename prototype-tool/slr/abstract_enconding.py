# Springer and IEEE bib extractions do not provide abstracts, this script scrapes them from the webpages
# Inspired by https://github.com/gabrielmarques/springer-abstracts
import bibtexparser
import requests
from bs4 import BeautifulSoup
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.0 Safari/537.36'}
from utils import get_ieee_abstract


def ieee_abstracts(original_bib, output_bib):
    with open(original_bib, encoding="utf-8") as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
        
    count = 1
    for entry in bib_database.entries:
        print(entry['ID'])
        url = 'https://ieeexplore.ieee.org/document/' + entry['ID']
        entry['abstract'] = get_ieee_abstract(url)
            
            
    with open(output_bib, 'w', encoding="utf-8") as bibtex_file:
        bibtexparser.dump(bib_database, bibtex_file)

def springer_abstracts(original_bib, output_bib):
    with open(original_bib, encoding="utf-8") as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
        
    count = 1
    for entry in bib_database.entries:
        print(entry['ID'])
        url = entry['url']
        print(url)
        if 'abstract' not in entry:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            soup.encode("utf-8")
            # print(soup)
            abstract_container = soup.find('div', id='Abs1-content')
            abstract = abstract_container.get_text(strip=True)
            if abstract is None:
                print('Nothing found, stopping now! Check the URL, connection, tag, or whether the IP has been blocked!')
                break
            else:
                print(count)
                count += 1
                print('abstract collected')
                print('\n')
                entry['abstract'] = abstract
    
    
    with open(output_bib, 'w', encoding="utf-8") as bibtex_file:
        bibtexparser.dump(bib_database, bibtex_file)

if __name__ == "__main__":
    # springer_abstracts("slr/bib/s2/springer-s2.bib", "slr/bib/s2/springer-s2-abstracts.bib")
    ieee_abstracts("slr/bib/s2/ieee-s2.bib", "slr/bib/s2/ieee-s2-abstracts.bib")
    