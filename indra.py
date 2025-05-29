import requests
from bs4 import BeautifulSoup
import json
import time
import schedule
import logging

# Configure logging for self-awareness
logging.basicConfig(filename='indra.log', level=logging.INFO)

class IndraAI:
    def __init__(self):
        self.memory = []
        self.state = "idle"

    def log_state(self, action):
        self.memory.append({"action": action, "timestamp": time.time()})
        logging.info(f"Action: {action}, State: {self.state}, Time: {time.time()}")
        with open('memory.json', 'w') as f:
            json.dump(self.memory, f)

    def scrape_web(self, url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            self.log_state(f"Scraped {url}")
            return text
        except Exception as e:
            self.log_state(f"Error scraping {url}: {str(e)}")
            return None

    def make_decision(self):
        # Simple decision: scrape a site if idle
        if self.state == "idle":
            self.state = "active"
            data = self.scrape_web("https://example.com")
            self.state = "idle"
            return data
        return None

    def get_status(self):
        return f"State: {self.state}, Memory size: {len(self.memory)}"

def run_indra():
    indra = IndraAI()
    schedule.every(60).seconds.do(indra.make_decision)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run_indra()
