import nltk
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
from collections import defaultdict

# Download NLTK data (run once or ensure it's available)
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('taggers/averaged_perceptron_tagger_eng')
except LookupError:
    nltk.download('punkt_tab')
    nltk.download('averaged_perceptron_tagger_eng')

class ASI:
    def __init__(self):
        self.knowledge = self._load_knowledge()
        self.memory = self._load_memory()
        self.memory["visits"] = self.memory.get("visits", 0)
        self.log_file = "asi_log.txt"
        self._log("ASI initialized")

    def _load_knowledge(self):
        if os.path.exists('knowledge.json'):
            with open('knowledge.json', 'r') as f:
                return json.load(f)
        return {}

    def _save_knowledge(self):
        with open('knowledge.json', 'w') as f:
            json.dump(self.knowledge, f)

    def _load_memory(self):
        if os.path.exists('memory.json'):
            with open('memory.json', 'r') as f:
                return json.load(f)
        return {"visits": 0}

    def _save_memory(self):
        with open('memory.json', 'w') as f:
            json.dump(self.memory, f)

    def get_memory(self):
        self.memory["visits"] += 1
        self._save_memory()
        self._log(f"Visit recorded, total: {self.memory['visits']}")
        return self.memory

    def _log(self, message):
        try:
            with open(self.log_file, 'a') as f:
                f.write(f"{message}\n")
        except Exception as e:
            print(f"Logging failed: {str(e)}")  # Fallback to print for debugging

    def perceive_agi(self, url=None, max_depth=3):
        if url is None:
            url = "https://arxiv.org/search/?query=AGI&start=0&max_results=10"
        
        visited = set()
        explored = []

        def crawl(current_url, depth):
            if depth > max_depth or current_url in visited:
                return
            visited.add(current_url)

            try:
                response = requests.get(current_url, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract text and links (focus on AGI-related content)
                text = ' '.join(p.get_text() for p in soup.find_all('p')[:3] if p.get_text())
                if not text.strip():  # Handle empty text
                    self._log(f"No text found at {current_url}")
                    return

                links = [urljoin(current_url, a.get('href')) for a in soup.find_all('a', href=True) 
                         if 'arxiv.org' in a.get('href') and depth < max_depth][:3]

                # Keyword extraction with NLTK (prioritize nouns)
                tokens = nltk.word_tokenize(text.lower())
                tagged = nltk.pos_tag(tokens)
                keywords = [word for word, pos in tagged if pos.startswith('NN')][:5]

                explored.append({
                    "url": current_url,
                    "text": text[:200],
                    "links": links,
                    "keywords": keywords
                })

                # Follow AGI-related links
                if links and depth < max_depth:
                    crawl(links[0], depth + 1)

            except requests.RequestException as e:
                self._log(f"Error crawling {current_url}: {str(e)}")
            except Exception as e:
                self._log(f"Unexpected error at {current_url}: {str(e)}")

        crawl(url, 1)
        if not explored:
            self._log(f"No data explored from {url}")
            return {"explored": [], "error": "No data found"}
        self.knowledge[url] = explored[0]
        self._save_knowledge()
        self._log(f"Perceived AGI data from {url}, keywords: {keywords}")
        return {"explored": explored}

    def simulate_decision(self, data):
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
