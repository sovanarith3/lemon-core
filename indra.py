import logging
import json
import os
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logging.info("IndraAI initialized")

class IndraAI:
    def __init__(self):
        self.counter_file = "counter.json"
        self.counter = self._load_counter()

    def _load_counter(self):
        if os.path.exists(self.counter_file):
            with open(self.counter_file, 'r') as f:
                data = json.load(f)
                return data.get("visits", 0)
        return 0

    def _save_counter(self):
        with open(self.counter_file, 'w') as f:
            json.dump({"visits": self.counter}, f)

    def get_status(self):
        return "Running"

    def get_memory(self):
        self.counter += 1
        self._save_counter()
        return {"visits": self.counter}

    def explore_web(self, url):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract text from the page
            text = soup.get_text(separator=" ", strip=True)
            return {"url": url, "text": text[:500]}  # Limit to 500 chars for now
        except Exception as e:
            return {"url": url, "error": str(e)}

if __name__ == "__main__":
    indra = IndraAI()
