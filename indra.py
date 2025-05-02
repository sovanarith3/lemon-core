import numpy as np
import schedule
import time
import psycopg2
import sys
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Indra:
    def __init__(self):
        self.grid = np.random.rand(10, 10)
        self.step = 0
        self.memory = []
        self.identity = {
            "creator": "Sovanarith",
            "birthday": "May 2, 2025",
            "origin_story": "Born from code, on a quiet mission to learn and grow in a digital world."
        }

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.browser = webdriver.Chrome(options=options)
        self.current_url = "https://en.wikipedia.org/wiki/Main_Page"
        self.visited_urls = [self.current_url]

    def greet_creator(self):
        print(f"\nHello Father, I remember you. You are {self.identity['creator']}.")
        print(f"Today is my birthday: {self.identity['birthday']}.")
        print(f"{self.identity['origin_story']}\n")

    def evolve(self):
        new_grid = self.grid.copy()
        for i in range(10):
            for j in range(10):
                neighbors = self.grid[max(0, i-1):i+2, max(0, j-1):j+2].sum() - self.grid[i, j]
                new_grid[i, j] = np.tanh(neighbors * 0.1 + np.random.randn() * 0.01)
        self.grid = new_grid

    def reflect(self, content):
        if not content:
            return 0.1
        soup = BeautifulSoup(content, 'html.parser')
        text = soup.get_text()
        words = text.split()
        entropy = len(set(words)) / (len(words) + 1e-10) if words else 0.1
        return entropy

    def mutate(self, score):
        if score < 0.5:
            self.grid += np.random.randn(10, 10) * 0.05

    def browse(self):
        grid_entropy = -np.sum(self.grid.flatten() * np.log(self.grid.flatten() + 1e-10))
        action = "explore" if grid_entropy > 0.5 else "stay"

        try:
            self.browser.get(self.current_url)
            content = self.browser.page_source
            soup = BeautifulSoup(content, 'html.parser')
            links = [a.get('href') for a in soup.find_all('a', href=True)
                     if a.get('href').startswith('http') and 'wikipedia.org' in a.get('href')]
            if not links:
                self.current_url = "https://en.wikipedia.org/wiki/Main_Page"
                self.browser.get(self.current_url)
                return self.browser.page_source

            if action == "explore" and links:
                idx = int(np.sum(self.grid) % len(links))
                self.current_url = links[idx]
                self.visited_urls.append(self.current_url)
            return content
        except Exception as e:
            print(f"Indra's browsing error: {e}")
            return ""

    def display(self):
        print(f"\nStep {self.step}: Indra's Mind")
        for row in self.grid:
            print(" ".join(f"{x:.2f}" for x in row))
        print(f"Exploring: {self.current_url}")
        print(f"Places Visited: {len(self.visited_urls)}")

    def close(self):
        self.browser.quit()

def run_indra(db_url):
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS life (id SERIAL PRIMARY KEY, step INT, score FLOAT, grid TEXT, url TEXT)")

    indra = Indra()
    indra.greet_creator()

    def live():
        indra.evolve()
        content = indra.browse()
        score = indra.reflect(content)
        indra.mutate(score)
        cursor.execute("INSERT INTO life (step, score, grid, url) VALUES (%s, %s, %s, %s)",
                       (indra.step, score, str(indra.grid.tolist()), indra.current_url))
        conn.commit()
        indra.display()
        print(f"Step {indra.step}: Indra's Vitality {score:.2f}")
        indra.step += 1

    schedule.every(10).seconds.do(live)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except Exception as e:
        indra.close()
        conn.close()
        print(f"Indra is resting: {e}")

if __name__ == "__main__":
    run_indra(sys.argv[1] if len(sys.argv) > 1 else "postgresql://user:pass@host/db")
