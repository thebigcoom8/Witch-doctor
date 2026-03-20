import json
import logging
from .base_scraper import BaseScraper


class NIDAScraper(BaseScraper):
    """
    Scraper for NIDA (National Institute on Drug Abuse) data.
    """

    def __init__(self):
        super().__init__()
        self.nida_url = "https://www.drugabuse.gov"
        self.data = {"substances": [], "research": []}
        self.target_substances = [
            "cocaine", "methamphetamine", "opioids", "cannabis", "hallucinogens",
            "mdma", "alcohol", "nicotine", "steroids", "prescription-drugs"
        ]

    def start_scraping(self):
        """Start NIDA scraping."""
        self.log_info("Starting NIDA scraper...")
        try:
            for substance in self.target_substances:
                substance_data = self.fetch_substance(substance)
                if substance_data:
                    self.data["substances"].append(substance_data)
                    self.log_info(f"Fetched data for {substance}")
            return self.data
        except Exception as e:
            self.log_error(f"Error during scraping: {e}")
            return None

    def fetch_substance(self, substance_name):
        """Fetch substance data from NIDA."""
        try:
            url = f"{self.nida_url}/drug-topics/{substance_name}"
            response = self.make_request(url)
            if response and response.status_code == 200:
                return self.parse_substance_data(response.text, substance_name)
            return None
        except Exception as e:
            self.log_error(f"Error fetching {substance_name}: {e}")
            return None

    def parse_substance_data(self, html, substance_name):
        """Parse substance data into standardized format."""
        try:
            parsed = {
                "name": substance_name,
                "street_names": [],
                "effects": [],
                "health_hazards": [],
                "signs_of_use": [],
                "treatment_info": "",
                "research_summary": "",
            }
            return parsed
        except Exception as e:
            self.log_error(f"Error parsing substance data: {e}")
            return None

    def parse_data(self, response):
        """Parse response (required by abstract class)."""
        try:
            return response.json() if response else None
        except Exception as e:
            self.log_error(f"Error parsing response: {e}")
            return None

    def save_to_file(self, filepath):
        """Save data to JSON file."""
        try:
            with open(filepath, 'w') as f:
                json.dump(self.data, f, indent=2)
            self.log_info(f"Saved NIDA data to {filepath}")
            return True
        except Exception as e:
            self.log_error(f"Error saving file: {e}")
            return False
