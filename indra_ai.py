import nltk
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
from collections import defaultdict

# Download NLTK data (run once or ensure it's available)
print("Starting NLTK download check...")
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('taggers/averaged_perceptron_tagger_eng')
except LookupError:
    print("Downloading NLTK data...")
    nltk.download('punkt_tab')
    nltk.download('averaged_perceptron_tagger_eng')
print("NLTK download check completed.")

class ASI:
    def __init__(self):
        print("Initializing ASI...")
        self.knowledge = self._load_knowledge()
        self.memory = self._load_memory()
        self.memory["visits"] = self.memory.get("visits", 0)
        self.log_file = "asi_log.txt"
        self._log("ASI initialized")
        print("ASI initialization completed.")

    def _load_knowledge(self):
        print("Loading knowledge...")
        if os.path.exists('knowledge.json'):
            try:
                with open('knowledge.json', 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Failed to load knowledge.json: {str(e)}")
                return {}
        return {}

    def _save_knowledge(self):
        print("Saving knowledge...")
        try:
            with open('knowledge.json', 'w') as f:
                json.dump(self.knowledge, f)
        except Exception as e:
            print(f"Failed to save knowledge.json: {str(e)}")

    def _load_memory(self):
        print("Loading memory...")
        if os.path.exists('memory.json'):
            try:
                with open('memory.json', 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Failed to load memory.json: {str(e)}")
                return {"visits": 0}
        return {"visits": 0}

    def _save_memory(self):
        print("Saving memory...")
        try:
            with open('memory.json', 'w') as f:
                json.dump(self.memory, f)
        except Exception as e:
            print(f"Failed to save memory.json: {str(e)}")

    def get_memory(self):
        print("Getting memory...")
        self.memory["visits"] += 1
        self._save_memory()
        self._log(f"Visit recorded, total: {self.memory['visits']}")
        return self.memory

    def _log(self, message):
        print(f"Attempting to log: {message}")
        try:
            with open(self.log_file, 'a') as f:
                f.write(f"[{os.times()[0]}] {message}\n")
        except Exception as e:
            print(f"Logging failed: {str(e)} - Message: {message}")

    def perceive_agi(self, url=None, max_depth=3):
        print(f"Starting perceive_agi with URL: {url}")
        if url is None:
            url = "https://arxiv.org/search/?query=AGI&start=0&max_results=10"
        
        visited = set()
        explored = []

        def crawl(current_url, depth):
            print(f"Crawling {current_url} at depth {depth}")
            if depth > max_depth or current_url in visited:
                return
            visited.add(current_url)

            try:
                response = requests.get(current_url, timeout=10)
                print(f"Request to {current_url} completed with status {response.status_code}")
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract text and links
                text_elements = soup.find_all('p')[:3]
                if not text_elements:
                    self._log(f"No paragraphs found at {current_url}")
                    return
                text = ' '.join(p.get_text() for p in text_elements if p.get_text().strip())
                if not text.strip():
                    self._log(f"No usable text at {current_url}")
                    return

                links = [urljoin(current_url, a.get('href')) for a in soup.find_all('a', href=True) 
                         if 'arxiv.org' in a.get('href') and depth < max_depth][:3]

                # Keyword extraction
                tokens = nltk.word_tokenize(text.lower())
                if not tokens:
                    self._log(f"No tokens extracted from {current_url}")
                    return
                tagged = nltk.pos_tag(tokens)
                keywords = [word for word, pos in tagged if pos.startswith('NN')][:5]

                explored.append({
                    "url": current_url,
                    "text": text[:200],
                    "links": links,
                    "keywords": keywords
                })

                if links and depth < max_depth:
                    crawl(links[0], depth + 1)

            except requests.RequestException as e:
                self._log(f"Network error at {current_url}: {str(e)}")
            except Exception as e:
                self._log(f"Unexpected error at {current_url}: {str(e)}")

        crawl(url, 1)
        if not explored:
            self._log(f"No data explored from {url}")
            return {"explored": [], "error": "No data found"}
        self.knowledge[url] = explored[0]
        self._save_knowledge()
        # Fix: Use the keywords from the first explored entry
        keywords = explored[0]["keywords"] if explored else []
        self._log(f"Perceived AGI data from {url}, keywords: {keywords}")
        return {"explored": explored}

    def simulate_decision(self, data):
        print("Simulating decision...")
        if not data or 'keywords' not in data.get('explored', [{}])[0]:
            self._log("No data or keywords for decision simulation")
            return {"decision": "No action", "reason": "Insufficient data"}

        keywords = data['explored'][0]['keywords']
        if "intelligence" in keywords or "learning" in keywords:
            decision = "Invest in AGI research"
            reason = "High relevance of AGI-related keywords"
        else:
            decision = "Maintain current operations"
            reason = "No strong AGI signal detected"

        self._log(f"Simulated decision: {decision}, Reason: {reason}")
        return {"decision": decision, "reason": reason}

# Example usage (for testing)
if __name__ == "__main__":
    asi = ASI()
    perception_data = asi.perceive_agi()
    decision = asi.simulate_decision(perception_data)
    print(decision)
