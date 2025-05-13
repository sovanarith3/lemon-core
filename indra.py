import schedule
import time
import random
import requests
from bs4 import BeautifulSoup
import psycopg2
import os
from urllib.parse import urljoin
import sys

# Database Connection Setup
database_url = os.getenv("DATABASE")
if not database_url:
raise ValueError("DATABASE environment variable not set")

try:
conn = psycopg2.connect(database_url)
cur = conn.cursor()
# Create tables for memory and URL queue
cur.execute("""
CREATE TABLE IF NOT EXISTS indra_memory (
id SERIAL PRIMARY KEY,
action TEXT,
timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
outcome TEXT
)
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS url_queue (
id SERIAL PRIMARY KEY,
url TEXT,
visited BOOLEAN DEFAULT FALSE
)
""")
conn.commit()
print("Database initialized successfully")
except Exception as e:
print(f"Database connection failed: {e}")
sys.exit(1)

# Logging Function for Self-Awareness
def log_action(action, outcome):
try:
cur.execute("INSERT INTO indra_memory (action, outcome) VALUES (%s, %s)", (action, outcome))
conn.commit()
except Exception as e:
print(f"Failed to log action: {e}")

# Self-Evaluation Function
def evaluate_performance(action, outcome):
success = "success" in outcome.lower() or "explored" in outcome.lower()
log_action(action, outcome)
return success

# URL Management Functions for Free Navigation
def find_new_urls(soup, base_url):
links = soup.find_all('a', href=True)
new_urls = []
for link in links:
absolute_url = urljoin(base_url, link['href'])
if absolute_url.startswith('http') and not any(absolute_url.startswith(banned) for banned in ['mailto:', 'javascript:']):
new_urls.append(absolute_url)
return new_urls

def add_urls_to_queue(urls):
for url in set(urls): # Remove duplicates
try:
cur.execute("INSERT INTO url_queue (url) VALUES (%s) ON CONFLICT DO NOTHING", (url,))
except Exception as e:
print(f"Failed to add URL {url} to queue: {e}")
conn.commit()

def get_next_url():
try:
cur.execute("SELECT url FROM url_queue WHERE visited = FALSE LIMIT 1")
url = cur.fetchone()
if url:
cur.execute("UPDATE url_queue SET visited = TRUE WHERE url = %s", (url[0],))
conn.commit()
return url[0]
return "https://en.wikipedia.org/wiki/Special:Random" # Fallback to random Wikipedia page
except Exception as e:
print(f"Failed to get next URL: {e}")
return "https://en.wikipedia.org/wiki/Special:Random"

# Web Scraping Function
def scrape_website(url):
try:
headers = {'User-Agent': 'Indra/1.0 (AI Learning Bot)'}
response = requests.get(url, headers=headers, timeout=10)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')
# Extract text content
paragraphs = soup.find_all('p')
text = " ".join([p.get_text() for p in paragraphs if p.get_text().strip()])
# Find new URLs to explore
new_urls = find_new_urls(soup, url)
add_urls_to_queue(new_urls)
outcome = f"Success: Scraped {len(text)} characters from {url}"
log_action(f"Scraped {url}", outcome)
return text, new_urls
except Exception as e:
outcome = f"Failed: {str(e)}"
log_action(f"Scraped {url}", outcome)
return None, []

# Autonomous Decision-Making
goals = [
"scrape new tech articles",
"learn about AI ethics",
"explore diverse topics"
]

def choose_action():
goal = random.choice(goals)
log_action("Chose goal", goal)
return goal

def execute_action(goal):
url = get_next_url()
text, new_urls = scrape_website(url)
if text:
if "scrape" in goal:
outcome = f"Scraped tech article successfully: {text[:100]}..."
elif "learn" in goal:
outcome = "Learned about AI ethics" if "ethics" in text.lower() else "Learned general topic"
else:
outcome = f"Explored {url} successfully"
else:
outcome = f"Failed to execute {goal} at {url}"
evaluate_performance(f"Executed goal: {goal}", outcome)

# Main Decision Loop
def decision_loop():
goal = choose_action()
execute_action(goal)
print(f"Current time: {time.ctime()}, Goal: {goal}, Active URLs in queue: {cur.execute('SELECT COUNT(*) FROM url_queue WHERE visited = FALSE').fetchone()[0]}")

# Schedule the Loop
schedule.every(10).minutes.do(decision_loop)

# Initial Run and Continuous Loop
if __name__ == "__main__":
print("Indra is starting... Initializing decision loop at", time.ctime())
decision_loop() # Run immediately on start
while True:
schedule.run_pending()
time.sleep(1)

# Cleanup on Exit
import atexit
@atexit.register
def cleanup():
if 'conn' in globals() and conn:
cur.close()
conn.close()
print("Database connection closed.")
