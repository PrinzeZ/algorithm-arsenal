import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

class ConcurrentCrawler:
    def __init__(self, max_workers=5, delay=0.5):
        self.max_workers = max_workers
        self.delay = delay
        self.seen = set()
    
    def fetch(self, url):
        if url in self.seen:
            return (url, "DUPLICATE", 0)
        self.seen.add(url)
        time.sleep(self.delay)
        try:
            r = requests.get(url, timeout=5)
            return (url, r.status_code, len(r.text))
        except Exception as e:
            return (url, "ERROR", str(e))
    
    def crawl(self, urls):
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.fetch, url): url for url in urls}
            for future in as_completed(futures):
                results.append(future.result())
        return results

if __name__ == "__main__":
    urls = ["https://httpbin.org/get"] * 10
    crawler = ConcurrentCrawler(max_workers=5)
    start = time.time()
    results = crawler.crawl(urls)
    print(f"Time: {time.time() - start:.2f}s")
    print(f"Unique crawled: {len(crawler.seen)}")