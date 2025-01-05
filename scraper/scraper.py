
import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor
import time
import random

# import sys
# sys.path.append('../input')
# from urls import urls
class MyntraScraper:
    def __init__(self, urls):
        self.urls = urls
        self.results = []

    @staticmethod
    def scrape_product(url):
        """Scrape product details from a single Myntra product page."""
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }
        try:
            session = requests.Session()
            Initial_response = session.get("https://www.myntra.com", headers=headers)
            cookies = session.cookies.get_dict()
            
            response = session.get(url, headers=headers, cookies=cookies, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "lxml")

            script = None
            for s in soup.find_all("script"):
                if 'pdpData' in s.text:
                    script = s.get_text(strip=True)
                    break

            if not script:
                raise ValueError("Product data script not found on the page.")

            data = json.loads(script[script.index('{'):])['pdpData']

            name = data['brand']['name']
            rating = int(data['ratings']['averageRating'])
            discounted_price = None
            discription = data['name']

            if "sizes" in data and data["sizes"]:
                size_data = data["sizes"][0]
                if "sizeSellerData" in size_data and size_data["sizeSellerData"]:
                    discounted_price = size_data["sizeSellerData"][0].get("discountedPrice")

            return {
                "name": name,
                "price": discounted_price,
                "rating": rating,
                "description": discription,
                "url": url
            }

        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None

    def scrape_all(self):
        """Scrape all product URLs using parallelization."""
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(self.scrape_product, url) for url in self.urls]
            for future in futures:
                result = future.result()
                if result:
                    self.results.append(result)
                    time.sleep(random.uniform(1, 3))
        print(f"Scraped {len(self.results)} products.")
    def save_to_json(self, output_path):
        """Save the scraped data to a JSON file."""
        with open(output_path, "w") as f:
            json.dump(self.results, f, indent=4)


if __name__ == "__main__":
    
    # urls = [
    #     "https://www.myntra.com/casual-shoes/roadster/the-roadster-lifestyle-co-men-black-round-toe-comfort-insole-lightweight-slip-on-sneakers/29812388/buy",
    #     "https://www.myntra.com/watch-gift-set/joker+%26+witch/joker--witch-unisex-james--claire-couple-watches-jwcw215/24295998/buy",
    #     "https://www.myntra.com/sunglasses/wrogn/wrogn-men-other-sunglasses-with-uv-protected-lens-wrnsg-07-sl/28422486/buy",
    #     "https://www.myntra.com/sports-shoes/hrx+by+hrithik+roshan/hrx-by-hrithik-roshan-unisex-colourblocked-running-non-marking-shoes/32085906/buy",
    #     "https://www.myntra.com/sandals/mast+%26+harbour/mast--harbour-men-comfort-sandals/28886982/buy",
    #     "https://www.myntra.com/casual-shoes/u.s.+polo+assn./u-s-polo-assn-men-navy-blue-monton-40-sneakers/18843486/buy",
    #     "https://www.myntra.com/sports-shoes/hrx+by+hrithik+roshan/hrx-by-hrithik-roshan-men-black-and-grey-non-marking-running-sports-shoes/22799380/buy",
    #     "https://www.myntra.com/duffel-bag/gear/gear-unisex-black--grey-colourblocked-cross-training-duffel-bag/13512466/buy"
    # ]
    
    input_file = "input/urls.txt"  
    try:
        with open(input_file, "r") as f:
            urls = f.read().strip().split("\n")
        
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_file}")
        exit(1)
    
    scraper = MyntraScraper(urls)
    scraper.scrape_all()
    scraper.save_to_json("output/scraped_data.json")
