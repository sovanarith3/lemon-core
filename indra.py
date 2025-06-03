import logging
import json
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

logging.basicConfig(level=logging.INFO)
logging.info("IndraAI initialized")

class IndraAI:
    def __init__(self):
        self.counter_file = "counter.json"
        self.counter = self._load_counter()
        self.visited_urls = set()
        self.knowledge_file = "knowledge.json"
        self.knowledge = self._load_knowledge()
        logging.info(f"Initialized with knowledge: {len(self.knowledge)} entries")

    def _load_counter(self):
        if os.path.exists(self.counter_file):
            with open(self.counter_file, 'r') as f:
                data = json.load(f)
                return data.get("visits", 0)
        return 0

    def _save_counter(self):
        with open(self.counter_file, 'w') as f:
            json.dump({"visits": self.counter}, f)
        logging.info(f"Saved counter: {self.counter}")

    def _load_knowledge(self):
        if os.path.exists(self.knowledge_file):
            with open(self.knowledge_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_knowledge(self):
        try:
            with open(self.knowledge_file, 'w') as f:
                json.dump(self.knowledge, f)
            logging.info(f"Saved knowledge with {len(self.knowledge)} entries")
        except Exception as e:
            logging.error(f"Failed to save knowledge: {e}")

    def get_status(self):
        return "Running"

    def get_memory(self):
        self.counter += 1
        self._save_counter()
        return {"visits": self.counter}

    def explore_web(self, url):
        try:
            if url in self.visited_urls:
                return {"url": url, "error": "Already visited"}
            self.visited_urls.add(url)

            response = requests.get(url, timeout=5)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract text
            text = soup.get_text(separator=" ", strip=True)

            # Extract links
            links = []
            for a_tag in soup.find_all('a', href=True):
                link = urljoin(url, a_tag['href'])
                if link.startswith('http') and link not in self.visited_urls:
                    links.append(link)
            result = {"url": url, "text": text[:500], "links": links[:5]}

            # Store knowledge
            self.knowledge[url] = result
            self._save_knowledge()
            logging.info(f"Explored {url}, found {len(links)} links")

            return result
        except Exception as e:
            logging.error(f"Error exploring {url}: {e}")
            return {"url": url, "error": str(e)}

    def roam_next(self):
        logging.info(f"Knowledge contains {len(self.knowledge)} entries")
        if self.knowledge:
            last_url = list(self.knowledge.keys())[-1]
            logging.info(f"Last URL: {last_url}, Links: {self.knowledge[last_url].get('links', [])}")
            if 'links' in self.knowledge[last_url] and self.knowledge[last_url]['links']:
                next_url = random.choice(self.knowledge[last_url]['links'])
                return self.explore_web(next_url)
        return {"error": "No new links to roam"}

if __name__ == "__main__":
    indra = IndraAI()
