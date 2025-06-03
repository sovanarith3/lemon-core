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
    nltk.data.find('averaged_perceptron_tagger')
except LookupError:
    nltk.download('punkt_tab')
    nltk.download('averaged_perceptron_tagger')

class IndraAI:
    def __init__(self):
        self.knowledge = self._load_knowledge()
        self.memory = self._load_memory()
        self.memory["visits"] = self.memory.get("visits", 0)

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
        return self.memory

    def explore_web(self, url=None, max_depth=5):
        if url is None:
            url = "https://en.wikipedia.org/wiki/Special:Random"
        
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
                
                # Extract text and links
                text = ' '.join(p.get_text() for p in soup.find_all('p')[:3])
                links = [urljoin(current_url, a.get('href')) for a in soup.find_all('a', href=True) if a.get('href').startswith('/wiki/')][:5]

                # Keyword extraction with NLTK
                tokens = nltk.word_tokenize(text.lower())
                tagged = nltk.pos_tag(tokens)
                keywords = [word for word, pos in tagged if pos.startswith('NN')][:5]  # Prioritize nouns

                explored.append({
                    "url": current_url,
                    "text": text[:200],  # Limit text length
                    "links": links,
                    "keywords": keywords
                })

                # Follow one link for deeper exploration
                if links and depth < max_depth:
                    crawl(links[0], depth + 1)

            except requests.RequestException:
                return

        crawl(url, 1)
        self.knowledge[url] = explored[0]
        self._save_knowledge()
        return {"explored": explored}

    def roam_auto(self):
        return self.explore_web()

    def roam_next(self):
        if not self.knowledge:
            return self.explore_web()
        last_url = list(self.knowledge.keys())[-1]
        return self.explore_web(last_url)

# Example usage (for testing)
if __name__ == "__main__":
    indra = IndraAI()
    print(indra.roam_auto())
