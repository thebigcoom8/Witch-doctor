import json
import logging
import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper


class DIYHRTScraper(BaseScraper):
    """
    Scraper for DIY HRT Wiki data.
    Provides community-built resources for hormone replacement therapy.
    """

    def __init__(self):
        super().__init__()
        self.diy_hrt_url = "https://diyhrt.wiki"
        self.data = {"medications": [], "protocols": [], "resources": []}

    def start_scraping(self):
        """Start DIY HRT Wiki scraping."""
        self.log_info("Starting DIY HRT Wiki scraper...")
        try:
            medications = self.fetch_medications()
            if medications:
                self.data["medications"] = medications
                self.log_info(f"Fetched {len(medications)} medications")
            
            protocols = self.fetch_protocols()
            if protocols:
                self.data["protocols"] = protocols
                self.log_info(f"Fetched {len(protocols)} protocols")
            
            return self.data
        except Exception as e:
            self.log_error(f"Error during scraping: {e}")
            return None

    def fetch_medications(self):
        """Fetch HRT medications."""
        try:
            url = f"{self.diy_hrt_url}/wiki/index.php/Medications"
            response = self.make_request(url)
            
            if response and response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                return self.parse_medications(soup)
            
            return []
        except Exception as e:
            self.log_error(f"Error fetching medications: {e}")
            return []

    def parse_medications(self, soup):
        """Parse medication data from HTML."""
        medications = []
        try:
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows[1:]:  # Skip header
                    cells = row.find_all('td')
                    if len(cells) >= 3:
                        med = {
                            "name": cells[0].get_text(strip=True),
                            "dosage": cells[1].get_text(strip=True),
                            "notes": cells[2].get_text(strip=True),
                        }
                        medications.append(med)
        except Exception as e:
            self.log_error(f"Error parsing medications: {e}")
        
        return medications

    def fetch_protocols(self):
        """Fetch HRT protocols."""
        try:
            url = f"{self.diy_hrt_url}/wiki/index.php/Protocols"
            response = self.make_request(url)
            
            if response and response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                return self.parse_protocols(soup)
            
            return []
        except Exception as e:
            self.log_error(f"Error fetching protocols: {e}")
            return []

    def parse_protocols(self, soup):
        """Parse protocol data from HTML."""
        protocols = []
        try:
            protocol_sections = soup.find_all('h3')
            for section in protocol_sections:
                protocol_name = section.get_text(strip=True)
                next_sibling = section.find_next('p')
                protocol_description = next_sibling.get_text(strip=True) if next_sibling else ""
                
                protocols.append({
                    "name": protocol_name,
                    "description": protocol_description,
                })
        except Exception as e:
            self.log_error(f"Error parsing protocols: {e}")
        
        return protocols

    def parse_data(self, response):
        """Parse response (required by abstract class)."""
        return response.json() if response else None

    def save_to_file(self, filepath):
        """Save data to JSON file."""
        try:
            with open(filepath, 'w') as f:
                json.dump(self.data, f, indent=2)
            self.log_info(f"Saved to {filepath}")
            return True
        except Exception as e:
            self.log_error(f"Error saving: {e}")
            return False
