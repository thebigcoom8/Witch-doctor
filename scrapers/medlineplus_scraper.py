import json
import logging
from .base_scraper import BaseScraper


class MedlinePlusScraper(BaseScraper):
    """
    Scraper for MedlinePlus medication and drug interaction data.
    """

    def __init__(self):
        super().__init__()
        self.medlineplus_url = "https://medlineplus.gov/api/medication"
        self.data = {"medications": [], "interactions": []}

    def start_scraping(self):
        """Start scraping MedlinePlus."""
        self.log_info("Starting MedlinePlus scraper...")
        try:
            medications = self.fetch_medications()
            if medications:
                self.data["medications"] = medications
                self.log_info(f"Fetched {len(medications)} medications")
            return self.data
        except Exception as e:
            self.log_error(f"Error during scraping: {e}")
            return None

    def fetch_medications(self):
        """Fetch medication list from MedlinePlus API."""
        try:
            response = self.make_request(f"{self.medlineplus_url}/info")
            if response and response.status_code == 200:
                data = response.json()
                return self.parse_medication_data(data)
            return []
        except Exception as e:
            self.log_error(f"Error fetching medications: {e}")
            return []

    def parse_medication_data(self, data):
        """Parse medication data into standardized format."""
        parsed_medications = []
        try:
            medications = data.get("results", [])
            for med in medications:
                parsed_med = {
                    "name": med.get("name", ""),
                    "description": med.get("description", ""),
                    "brand_names": med.get("brandNames", []),
                    "side_effects": med.get("sideEffects", []),
                    "warnings": med.get("warnings", []),
                    "interactions": med.get("interactions", []),
                }
                parsed_medications.append(parsed_med)
        except Exception as e:
            self.log_error(f"Error parsing medication data: {e}")
        return parsed_medications

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
            self.log_info(f"Saved MedlinePlus data to {filepath}")
            return True
        except Exception as e:
            self.log_error(f"Error saving file: {e}")
            return False
