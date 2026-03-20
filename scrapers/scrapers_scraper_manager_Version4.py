import os
import json
import logging
from datetime import datetime


class ScraperManager:
    """
    Orchestrates all scrapers and manages the data collection pipeline.
    """

    def __init__(self, output_dir="data/raw"):
        self.output_dir = output_dir
        self.logger = logging.getLogger(__name__)
        self.scrapers = {}
        os.makedirs(output_dir, exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def register_scraper(self, name, scraper):
        """Register a scraper instance."""
        self.scrapers[name] = scraper
        self.logger.info(f"Registered scraper: {name}")

    def run_all_scrapers(self):
        """Run all registered scrapers and collect data."""
        self.logger.info("Starting all scrapers...")
        all_data = {}
        
        for scraper_name, scraper in self.scrapers.items():
            try:
                self.logger.info(f"Running {scraper_name}...")
                data = scraper.start_scraping()
                if data:
                    all_data[scraper_name] = data
                    self.save_scraper_data(scraper_name, data)
                    self.logger.info(f"{scraper_name} completed successfully")
                else:
                    self.logger.warning(f"{scraper_name} returned no data")
            except Exception as e:
                self.logger.error(f"Error running {scraper_name}: {e}")
        
        self.save_combined_data(all_data)
        self.logger.info("All scrapers completed")
        return all_data

    def run_specific_scraper(self, scraper_name):
        """Run a specific scraper."""
        if scraper_name not in self.scrapers:
            self.logger.error(f"Scraper {scraper_name} not found")
            return None
        
        try:
            self.logger.info(f"Running {scraper_name}...")
            scraper = self.scrapers[scraper_name]
            data = scraper.start_scraping()
            if data:
                self.save_scraper_data(scraper_name, data)
                self.logger.info(f"{scraper_name} completed successfully")
            return data
        except Exception as e:
            self.logger.error(f"Error running {scraper_name}: {e}")
            return None

    def save_scraper_data(self, scraper_name, data):
        """Save data from a specific scraper."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(self.output_dir, f"{scraper_name}_{timestamp}.json")
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            self.logger.info(f"Saved {scraper_name} data to {filepath}")
        except Exception as e:
            self.logger.error(f"Error saving {scraper_name} data: {e}")

    def save_combined_data(self, all_data):
        """Save all scraped data combined."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(self.output_dir, f"combined_{timestamp}.json")
        try:
            with open(filepath, 'w') as f:
                json.dump(all_data, f, indent=2)
            self.logger.info(f"Saved combined data to {filepath}")
        except Exception as e:
            self.logger.error(f"Error saving combined data: {e}")

    def get_scraper_status(self):
        """Get status of all registered scrapers."""
        return {name: scraper.__class__.__name__ for name, scraper in self.scrapers.items()}