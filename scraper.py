

import requests
import pandas as pd

from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time


#website URL that we want to scrape from
BASE_URL = "https://books.toscrape.com/"


#function to scrape one page
def scrape_page(url):

    print(f"Scraping: {url}")

    response = requests.get( #to get access to the website and retrieve the HTML content    
        url,
        timeout=15, #stop after 15s
        headers={
            "User-Agent": "EducationalProductScraper/1.0"
        }
    )

    response.raise_for_status() #check if it works

    soup = BeautifulSoup(response.text, "lxml") #convert everything to text

    products = [] #store the product information

    # Extract product information
    for product in soup.select("article.product_pod"):

        name = product.select_one("h3 a")["title"]

        price = product.select_one(
            ".price_color"
        ).get_text(strip=True)

        rating_element = product.select_one(
            ".star-rating"
        )

        rating = next(
            (x for x in rating_element.get("class", [])
             if x != "star-rating"),
            None
        )

        relative_url = product.select_one(
            "h3 a"
        )["href"]

        product_url = urljoin(BASE_URL, relative_url)

        products.append({
            "name": name,
            "price": price,
            "rating": rating,
            "url": product_url
        })

    return products, soup


# Function to scrape all pages
def scrape_all_pages():

    current_url = BASE_URL

    all_products = []

    while current_url:

        products, soup = scrape_page(current_url)

        all_products.extend(products)

        # Find next page
        next_button = soup.select_one("li.next a")

        if next_button:

            current_url = urljoin(
                current_url,
                next_button["href"]
            )

            # Wait 1 second between pages
            time.sleep(1)

        else:
            current_url = None

    return all_products


# Main program
if __name__ == "__main__":

    data = scrape_all_pages()

    # Convert results into DataFrame
    df = pd.DataFrame(data)

    # Export to CSV
    df.to_csv("products.csv", index=False)

    print("\n--------------------------")
    print("SCRAPING COMPLETED!")
    print("--------------------------")

    print("Total products:", len(df))

    print("\nFirst 5 products:")
    print(df.head())

    print("\nSaved to products.csv")

