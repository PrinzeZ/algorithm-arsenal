import requests
import time

def naive_crawl(urls):
    results = []
    for url in urls:
        try:
            r = requests.get(url, timeout=5)
            results.append((url, r.status_code, len(r.text)))
        except:
            results.append((url, "ERROR", 0))
    return results

if __name__ == "__main__":
    urls = ["https://httpbin.org/get"] * 10
    start = time.time()
    naive_crawl(urls)
    print(f"Time: {time.time() - start:.2f}s")