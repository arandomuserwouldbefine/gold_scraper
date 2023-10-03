import requests
import re
import time
import sqlite3
from bs4 import BeautifulSoup

website_url = "https://www.mkspamp.com.my/m/prices.xhtml"

market_url = "https://www.buysilvermalaysia.com/gold-silver-price-today/"


def extract_data_from_html():
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()
    r = requests.get(market_url)
    html_content= r.text
    # Define a regular expression pattern to match the data
    pattern = r'<td style="[^"]*">([^<]+)</td>\s*<td style="[^"]*"><strong>([^<]+)</strong></td>'
    
    # Find all matches using the pattern
    matches = re.findall(pattern, html_content)
    
    # Initialize a list to store the formatted data
    formatted_data = []
    
    # Iterate over the matches and format the data
    for match in matches:
        static_var = match[0].strip()
        price = match[1].strip()
        
        # Extract product name and price without "/gram" or "/公克" part
        product_name = re.sub(r'/gram$|/公克$', '', static_var).strip()
        price_value = re.sub(r'RM\s*', '', price).strip()
        
        cursor.execute(f"UPDATE marketPrice set price = ? WHERE product = ?",(price_value,product_name,))
        conn.commit()
        product_info = {
            "product_name": product_name,
            "price": price_value
        }
        
        formatted_data.append(product_info)

extract_data_from_html()

def scrape_website(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch {url}. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def extract_data(html):
    row_pattern = r'<tr>.*?<label\s+for="pricesForm:productID">(.*?)<\/label>.*?' \
                  r'<label\s+class="royalblue"[^>]*>(.*?)<\/label>.*?' \
                  r'<label\s+class="darkteal"[^>]*>(.*?)<\/label>.*?<\/tr>'
    
    extracted_data = []
    matches = re.finditer(row_pattern, html, re.DOTALL)
    for match in matches:
        product_name = match.group(1).strip()
        price_royalblue = match.group(2).strip()
        price_darkteal = match.group(3).strip()
        extracted_data.append({
            "product_name": product_name,
            "price_royalblue": price_royalblue,
            "price_darkteal": price_darkteal
        })
    return extracted_data



def update_or_insert_into_database(data):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    price_royalblue = 0
    price_darkteal = 0
    existing_data = cursor.fetchone()

    
    for info in data:
        cursor.execute('''SELECT * FROM products WHERE product_name = ?''', (info['product_name'],))
        price_royalblue = info['price_royalblue'].replace(" ","")
        price_darkteal = info['price_darkteal'].replace(" ","")  
        gram500Price = 0
        if info["product_name"] == "Gold   : 100 GM 999.9 (MYR)":
            price_darkteal_numeric = float(price_darkteal)
            gram500Price = price_darkteal_numeric * 5
            cursor.execute('''UPDATE products SET price_darkteal = ? WHERE id = ?''', (gram500Price, 2))

        cursor.execute('''UPDATE products
                                            SET price_royalblue = ?, price_darkteal = ?
                                            WHERE product_name = ?''', (price_royalblue, price_darkteal, info['product_name']))



        cursor.execute('''UPDATE ourRates
                                            SET price_royalblue = ?, price_darkteal = ?
                                            WHERE product_name = ?''', (price_royalblue, price_darkteal, info['product_name']))
    
    print("Price Updating!")
    conn.commit()
    conn.close()




def graph_data_insert():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT price_darkteal, additional_price FROM products WHERE id=?", (1,))

    
    html_content = scrape_website(website_url)
    extractions = extract_data(html_content)    
    
    price = extractions[0]['price_darkteal'].replace(" ", "")
    additional_price = 2000
    result = float(price) + float(additional_price)
    cursor.execute("INSERT INTO price_graph (price) VALUES (?)", (result,))
    print("Data inserted into graph!")
    conn.commit()
    conn.close()


def extract_product_info(url):
    try:
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        product_titles = soup.find_all('span', class_='product-title')

        sell_colors = soup.find_all('span', class_='sellcolor')

        buy_colors = soup.find_all('span', class_='buycolor')

        product_titles_list = [title.get_text() for title in product_titles]
        sell_colors_list = [sell.get_text() for sell in sell_colors]
        buy_colors_list = [buy.get_text() for buy in buy_colors]

        product_info_list = []
        for i in range(len(product_titles_list)):
            product_info = {
                "Product": product_titles_list[i],
                "Sell": sell_colors_list[i],
                "Buy": buy_colors_list[i]
            }
            product_info_list.append(product_info)
            cursor.execute("UPDATE products SET price_darkteal = ? WHERE ids = ?",(product_info["Buy"],product_info["Product"]))
            conn.commit()
        print("Fortuna inserted")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None



# Example usage:
u = "https://pampmalaysia.mkspamp.com.my/PricingClient/pages/product-catalog.xhtml"

if __name__ == "__main__":
    
    
    while True:
        html_content = scrape_website(website_url)
        product_info_list = extract_product_info(u)
        time.sleep(4)



        if html_content:

            graph_data_insert()
            extracted_data = extract_data(html_content)            

            update_or_insert_into_database(extracted_data) 
        time.sleep(5)  