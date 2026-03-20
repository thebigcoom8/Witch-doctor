import requests

class PubChemScraper:
    def __init__(self, compound_name):
        self.compound_name = compound_name
        self.base_url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug'

    def fetch_data(self):
        url = f'{self.base_url}/compound/name/{self.compound_name}/JSON'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

# Example usage
if __name__ == '__main__':
    scraper = PubChemScraper('aspirin')
    data = scraper.fetch_data()
    print(data)