import nltk
import json
import requests
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
import warnings
from urllib.parse import urljoin
import os
from collections import defaultdict
import time

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

print("Starting NLTK download check...")
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('taggers/averaged_perceptron_tagger_eng')
except LookupError:
    print("Downloading NLTK data...")
    try:
        nltk.download('punkt_tab')
        nltk.download('averaged_perceptron_tagger_eng')
    except Exception as e:
        print(f"Failed to download NLTK data: {str(e)}")
        raise
print("NLTK download check completed.")

keyword_confidence = {'intelligence': 0.9, 'learning': 0.8, 'ai': 0.9, 'system': 0.6, 'agent': 0.7, 'network': 0.6, 'neural': 0.7}

class ASI:
    def __init__(self):
        print("Initializing ASI...")
        self.log_file = "asi_log.txt"
        self.updates_file = "updates.json"
        self.config_file = "config.json"
        self.knowledge = self._load_knowledge()
        self.memory = self._load_memory()
        self.memory["visits"] = self.memory.get("visits", 0)
        self.config = self._load_config()
        self.agi_keywords = self.config.get("agi_keywords", {"intelligence", "learning", "ai", "system", "agent", "network", "neural"})
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

    def _load_config(self):
        print("Loading config...")
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Failed to load config.json: {str(e)}")
                return {}
        return {}

    def _save_config(self):
        print("Saving config...")
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f)
        except Exception as e:
            print(f"Failed to save config.json: {str(e)}")

    def _load_updates(self):
        print("Loading updates...")
        if os.path.exists(self.updates_file):
            try:
                with open(self.updates_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Failed to load updates.json: {str(e)}")
                return {"timestamp": 0, "perception": {}, "decision": {}}
        return {"timestamp": 0, "perception": {}, "decision": {}}

    def _save_updates(self, perception_data, decision):
        print("Saving updates...")
        updates = {
            "timestamp": time.time(),
            "perception": perception_data,
            "decision": decision
        }
        try:
            with open(self.updates_file, 'w') as f:
                json.dump(updates, f)
        except Exception as e:
            print(f"Failed to save updates.json: {str(e)}")
        return updates

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

    def perceive_agi(self, url=None, max_depth=1):  # Reduced max_depth to 1 for initial test
        print(f"Starting perceive_agi with URL: {url}")
        if url is None:
            url = "https://export.arxiv.org/rss/cs.AI"
        
        visited = set()
        explored = []

        def crawl(current_url, depth):
            print(f"Crawling {current_url} at depth {depth}")
            if depth > max_depth or current_url in visited:
                return
            visited.add(current_url)

            try:
                response = requests.get(current_url, timeout=20)
                print(f"Request to {current_url} completed with status {response.status_code}")
                response.raise_for_status()
                self._log(f"Raw response status: {response.status_code}, content length: {len(response.text)}")
                
                parser = 'lxml' if current_url.endswith('.rss') or 'xml' in response.headers.get('Content-Type', '') else 'html.parser'
                soup = BeautifulSoup(response.text, parser) if parser == 'html.parser' else BeautifulSoup(response.text, 'lxml-xml')
                
                if parser == 'lxml':
                    items = soup.select('item')
                    self._log(f"Found {len(items)} items in {current_url}")
                    if not items:
                        self._log(f"No items found at {current_url}")
                        return
                    # Process only the first item for debugging
                    item = items[0]
                    self._log(f"Raw XML of first item: {str(item)[:200]}...")  # Log first 200 chars of XML
                    title = item.select_one('title')
                    description = item.select_one('description')
                    text_elements = [description] if description else [title] if title else [item]
                    text = ' '.join(elem.get_text() for elem in text_elements if elem and elem.get_text().strip())
                    if not text.strip():
                        text = item.get_text()  # Fallback to entire item text
                    self._log(f"Extracted text from first item: {text[:100]}...")
                    links = [link.text for link in item.select('link') if 'arxiv.org' in link.text][:1]
                    if not text.strip():
                        self._log(f"No usable text in first item at {current_url}")
                        return
                    tokens = nltk.word_tokenize(text.lower())
                    self._log(f"Tokenized text into {len(tokens)} tokens")
                    if not tokens:
                        self._log(f"No tokens extracted from {current_url}")
                        return
                    tagged = nltk.pos_tag(tokens)
                    self._log(f"Tagged {len(tagged)} tokens")
                    keywords = [word for word, pos in tagged if pos.startswith('NN') and word in self.agi_keywords]
                    if not keywords:
                        keywords = [word for word, pos in tagged if pos.startswith('NN')][:2]
                    self._log(f"Extracted keywords: {keywords}")
                    explored.append({
                        "url": current_url,
                        "text": text[:200],
                        "links": links,
                        "keywords": keywords
                    })
                    if links and depth < max_depth:
                        crawl(links[0], depth + 1)
                else:
                    text_elements = soup.select('blockquote.abstract') or soup.select('h1, p')[:3]
                    if not text_elements:
                        self._log(f"No relevant text found at {current_url}")
                        return
                    text = ' '.join(elem.get_text() for elem in text_elements if elem.get_text().strip())
                    if not text.strip():
                        self._log(f"No usable text at {current_url}")
                        return
                    links = [urljoin(current_url, a.get('href')) for a in soup.find_all('a', href=True) 
                             if 'arxiv.org' in a.get('href') and depth < max_depth][:3]
                    tokens = nltk.word_tokenize(text.lower())
                    if not tokens:
                        self._log(f"No tokens extracted from {current_url}")
                        return
                    tagged = nltk.pos_tag(tokens)
                    keywords = [word for word, pos in tagged if pos.startswith('NN') and word in self.agi_keywords]
                    if not keywords:
                        keywords = [word for word, pos in tagged if pos.startswith('NN')][:2]
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
        self.knowledge[url] = explored
        self._save_knowledge()
        keywords = explored[0]["keywords"] if explored else []
        self._log(f"Perceived AGI data from {url}, keywords: {keywords}")
        return {"explored": explored}

    def simulate_decision(self, data):
        print("Simulating decision...")
        if not data or not data.get('explored') or not data['explored']:
            self._log("No data or empty explored list for decision simulation")
            return {"decision": "No action", "reason": "Insufficient data"}
        if not all('keywords' in entry for entry in data['explored']):
            self._log("Missing keywords in explored data for decision simulation")
            return {"decision": "No action", "reason": "Missing keywords"}
        
        all_keywords = set()
        for entry in data['explored']:
            all_keywords.update(entry['keywords'])
        
        relevant_keywords = {kw for kw in all_keywords if kw in self.agi_keywords}
        confidence_score = sum(keyword_confidence.get(kw, 0.7) for kw in relevant_keywords)
        threshold = 1.5

        if relevant_keywords and confidence_score >= threshold:
            decision = "Invest in AGI research"
            reason = f"High relevance of AGI-related keywords detected: {relevant_keywords}, Confidence: {confidence_score:.2f}"
        else:
            decision = "Maintain current operations"
            reason = f"No strong AGI signal detected: {all_keywords}, Confidence: {confidence_score:.2f}"

        self._log(f"Simulated decision: {decision}, Reason: {reason}")
        return {"decision": decision, "reason": reason}

    def latest_updates(self):
        print("Checking for latest updates...")
        updates = self._load_updates()
        current_time = time.time()
        if current_time - updates["timestamp"] > 86400:
            print("Refreshing updates...")
            perception_data = self.perceive_agi()
            decision = self.simulate_decision(perception_data)
            updates = self._save_updates(perception_data, decision)
        else:
            print("Returning cached updates...")
        return updates

    def chat(self, user_input):
        print(f"Processing chat input: {user_input}")
        user_input = user_input.lower().strip()
        if "update me" in user_input or "latest" in user_input:
            updates = self.latest_updates()
            response = f"Here are the latest updates:\nDecision: {updates['decision']['decision']}\nReason: {updates['decision']['reason']}"
        elif "explore" in user_input or "roam" in user_input:
            perception_data = self.perceive_agi()
            response = f"Explored data: {json.dumps(perception_data, indent=2)}"
        elif "decide" in user_input or "simulate" in user_input:
            perception_data = self.perceive_agi()
            decision = self.simulate_decision(perception_data)
            response = f"Decision: {decision['decision']}\nReason: {decision['reason']}"
        elif "add keyword:" in user_input:
            new_keyword = user_input.split("add keyword:")[1].strip()
            if new_keyword:
                self.agi_keywords.add(new_keyword)
                self.config["agi_keywords"] = list(self.agi_keywords)
                self._save_config()
                if new_keyword not in keyword_confidence:
                    keyword_confidence[new_keyword] = 0.7
                response = f"Added keyword '{new_keyword}' to AGI keywords. Current list: {self.agi_keywords}"
            else:
                response = "Please provide a keyword to add (e.g., 'add keyword: neural')."
        else:
            response = "I can help with: 'update me', 'explore data', 'decide', or 'add keyword: <keyword>'. What would you like to do?"
        self._log(f"Chat response: {response}")
        return {"response": response}
