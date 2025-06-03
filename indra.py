import logging
import json
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import random  # Added missing import

logging.basicConfig(level=logging.INFO)
logging.info("IndraAI initialized")

class IndraAI:
    def __init__(self):
        self.counter_file = "counter.json"
        self.counter = self._load_counter()
        self.visited_urls = set()
        self.knowledge_file = "knowledge.json"
        self.knowledge = self._load_knowledge()
        logging.info(f"Initialized with knowledge: {len(self.knowledge)} entries, file exists: {os.path.exists(self.knowledge_file)}")

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
            try:
                with open(self.knowledge_file, 'r') as f:
                    data = json.load(f)
                    # Ensure links are lists
                    for url, info in data.items():
                        if 'links' in info and isinstance(info['links'], str):
                            info['links'] = eval(info['links']) if info['links'] else []
                        elif 'links' not in info:
                            info['links'] = []
                    return data
            except json.JSONDecodeError as e:
                logging.error(f"Invalid JSON in {self.knowledge_file}: {e}")
                return {}
        return {}

    def _save_knowledge(self):
        try:
            with open(self.knowledge_file, 'w') as f:
                json.dump(self.knowledge, f, indent=2)
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
            links = self.knowledge[last_url].get('links', [])
            logging.info(f"Last URL: {last_url}, Links: {links}")
            if links:
                next_url = random.choice(links)
                logging.info(f"Chose next URL: {next_url}")
                return self.explore_web(next_url)
            logging.warning("No valid links found, falling back to default URL")
        else:
            logging.warning("Knowledge is empty, starting fresh")
        return self.explore_web('https://en.wikipedia.org/wiki/Artificial_general_intelligence')

if __name__ == "__main__":
    indra = IndraAI()
