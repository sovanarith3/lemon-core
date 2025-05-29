import requests
from bs4 import BeautifulSoup
import json
import time
import schedule
import logging
import os

# Configure logging to stdout
logging.basicConfig(level=logging.INFO)

class IndraAI:
    def __init__(self):
        self.memory = []
        self.state = "idle"
        print("IndraAI initialized")
        logging.info("IndraAI initialized")

    def log_state(self, action):
        self.memory.append({"action": action, "timestamp": time.time()})
        logging.info(f"Action: {action}, State: {self.state}, Time: {time.time()}")
        print(f"Memory updated: {self.memory}")
        try:
            with open('/tmp/memory.json', 'w') as f:
                json.dump(self.memory, f)
        except Exception as e:
            logging.error(f"Failed to write memory.json: {str(e)}")

    def scrape_web(self, url):
        logging.info(f"Attempting to scrape {url}")
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            self.log_state(f"Scraped {url}")
            return text
        except Exception as e:
            self.log_state(f"Error scraping {url}: {str(e)}")
            return None

    def make_decision(self):
        logging.info("Making decision")
        if self.state == "idle":
            self.state = "active"
            # Temporarily disable scraping
            # data = self.scrape_web("https://example.com")
            self.log_state("Skipped scraping for debugging")
            self.state = "idle"
            logging.info("Decision completed")
            return None
        return None

    def get_status(self):
        return f"State: {self.state}, Memory size: {len(self.memory)}"

    def get_memory(self):
        return self.memory

def run_indra():
    try:
        print("Starting Indra worker")
        logging.info("Starting Indra worker")
        indra = IndraAI()
        # Temporarily disable scheduler
        # schedule.every(60).seconds.do(indra.make_decision)
        # logging.info("Scheduler started")
        # while True:
        #     try:
        #         schedule.run_pending()
        #         logging.info("Scheduler tick")
        #     except Exception as e:
        #         logging.error(f"Error in scheduler loop: {str(e)}")
        #     time.sleep(1)
        logging.info("Worker running in debug mode without scheduler")
        while True:
            indra.make_decision()
            time.sleep(60)
    except Exception as e:
        logging.error(f"Worker error: {str(e)}")
        raise

if __name__ == "__main__":
    run_indra()
