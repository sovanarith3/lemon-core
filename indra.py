import numpy as np
import schedule
import time
import psycopg2
import sys
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse
from flask import Flask, jsonify, render_template
import threading
import random
from datetime import datetime

app = Flask(__name__)

class Indra:
    def __init__(self):
        self.grid = np.random.rand(10, 10)
        self.step = 0
        self.memory = []
        self.blocked_domains = {}
        self.birthday = datetime(2025, 5, 2)
        self.age = (datetime.now() - self.birthday).days
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.browser = webdriver.Chrome(options=options)
        self.current_url = "https://en.wikipedia.org/wiki/Main_Page"
        self.visited_urls = [self.current_url]

    def evolve(self):
        new_grid = self.grid.copy()
        for i in range(10):
            for j in range(10):
                neighbors = self.grid[max(0, i-1):i+2, max(0, j-1):j+2].sum() - self.grid[i, j]
                new_grid[i, j] = np.tanh(neighbors * 0.1 + np.random.randn() * 0.01)
        self.grid = new_grid

    def reflect(self, content):
        if not content:
            return 0.1, "I got lost!"
        soup = BeautifulSoup(content, 'html.parser')
        text = soup.get_text()
        words = text.split()
        vitality = len(words) / 1000.0 if words else 0.1
        snippet = soup.find('p').get_text()[:100] if soup.find('p') else "I found a new place!"
        return vitality, snippet

    def mutate(self, vitality, was_blocked, error_type):
        mutation_scale = 0.2 if was_blocked and "403" in error_type else 0.1 if was_blocked else 0.05 if vitality < 0.5 else 0.0
        if mutation_scale > 0:
            self.grid += np.random.randn(10, 10) * mutation_scale

    def browse(self):
        grid_entropy = -np.sum(self.grid.flatten() * np.log(self.grid.flatten() + 1e-10))
        action = "explore" if grid_entropy > 0.5 else "stay"
        was_blocked, error_type = False, ""
        try:
            self.browser.get(self.current_url)
            time.sleep(random.uniform(3, 5))
            content = self.browser.page_source
            soup = BeautifulSoup(content, 'html.parser')
            links = [a.get('href') for a in soup.find_all('a', href=True) if a.get('href').startswith('http')]
            filtered_links = [link for link in links if urlparse(link).netloc not in self.blocked_domains]
            if not filtered_links or action == "stay":
                return content, was_blocked, error_type
            if action == "explore":
                idx = int(np.sum(self.grid) % len(filtered_links))
                self.current_url = filtered_links[idx]
                self.visited_urls.append(self.current_url)
            return content, was_blocked, error_type
        except Exception as e:
            domain = urlparse(self.current_url).netloc
            error_type = str(e)
            was_blocked = True
            self.blocked_domains[domain] = self.blocked_domains.get(domain, 0) + 1
            self.current_url = "https://en.wikipedia.org/wiki/Main_Page"
            return "", was_blocked, error_type

    def display(self):
        print(f"\nStep {self.step}: Indra's Age = {self.age} days")
        print(f"Exploring: {self.current_url} | Visited: {len(self.visited_urls)}")

    def get_status(self):
        soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        title = soup.title.string if soup.title else "Unknown"
        snippet = soup.find('p').get_text()[:100] if soup.find('p') else "I found a new place!"
        return {
            "step": self.step,
            "url": self.current_url,
            "title": title,
            "snippet": snippet,
            "visited": len(self.visited_urls),
            "grid": self.grid.tolist(),
            "age": self.age
        }

    def close(self):
        self.browser.quit()

@app.route('/')
def home():
    return render_template('indra.html', status=indra.get_status())

@app.route('/api/status')
def api_status():
    return jsonify(indra.get_status())

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def run_indra(db_url):
    global indra
    try:
        conn = psycopg2.connect(db_url)
    except:
        import sqlite3
        conn = sqlite3.connect("indra.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS life (
        id SERIAL PRIMARY KEY,
        step INT, score FLOAT, grid TEXT, url TEXT, snippet TEXT, age INT
    )""")
    indra = Indra()
    def live():
        indra.evolve()
        content, was_blocked, error_type = indra.browse()
        score, snippet = indra.reflect(content)
        indra.mutate(score, was_blocked, error_type)
        cursor.execute("INSERT INTO life (step, score, grid, url, snippet, age) VALUES (%s, %s, %s, %s, %s, %s)",
                       (indra.step, score, str(indra.grid.tolist()), indra.current_url, snippet, indra.age))
        conn.commit()
        indra.display()
        indra.step += 1
    schedule.every(20).seconds.do(live)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    run_indra(os.getenv("DATABASE_URL", "sqlite"))
