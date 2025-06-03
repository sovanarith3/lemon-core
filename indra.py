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
        logging.info(f"Explored {url}, found {len(links)} links, stored links: {links[:5]}")

        return result
    except Exception as e:
        logging.error(f"Error exploring {url}: {e}")
        return {"url": url, "error": str(e)}
