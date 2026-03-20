import requests
from bs4 import BeautifulSoup

class TripSitScraper:
    def __init__(self):
        self.base_url = 'https://tripsit.me/'

    def get_drug_info(self, drug_name):
        url = f'{self.base_url}drugs/{drug_name}'
        response = requests.get(url)

        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        info = {'name': drug_name, 'interactions': [], 'safer_use_practices': []}

        # Scrape drug interactions
        interactions_section = soup.find('div', {'id': 'interactions'})
        if interactions_section:
            for li in interactions_section.find_all('li'):
                info['interactions'].append(li.get_text())

        # Scrape safer use practices
        practices_section = soup.find('div', {'id': 'safer_use'})
        if practices_section:
            for li in practices_section.find_all('li'):
                info['safer_use_practices'].append(li.get_text())

        return info

# Example usage:
# scraper = TripSitScraper()
# drug_info = scraper.get_drug_info('alprazolam')
# print(drug_info)