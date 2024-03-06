from bs4 import BeautifulSoup
import requests
import pandas as pd

all_url = []

for i in range(2, 12):
    url = f"https://www.airlinequality.com/airline-reviews/british-airways/page/{i}/?sortby=post_date%3ADesc&pagesize=100"
    all_url.append(url) 
    
list_of_tables = [] 

for url in all_url:
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    reviews = soup.find_all('div', {'class': 'review-stats'})
    # print(url)
    # print(len(reviews))
   
    prototype= {}
      

    for div in reviews:
        table_rows = div.find_all('tr')
        for row in table_rows:
            prototype[row.find('td').string] = None
                
    for div in reviews:
        table_rows = div.find_all('tr')
        new_dic = prototype.copy()
        for row in table_rows:
            review_key = row.find('td')
            review_value = row.find('td', {'class': 'review-value'})
            if review_value is not None:
                new_dic[review_key.string] = review_value.string
                continue
                        
            review_stars = row.find('td', {'class': 'stars'})
            # print(review_stars)
            if review_stars is not None:
                new_dic[review_key.string] = len(review_stars.find_all("span", {'class': 'fill'}))
                            
        list_of_tables.append(new_dic)
            
# print(list_of_tables)                                                                            
print(len(list_of_tables))    

# Now you can work with 'all_reviews' which contains the data from all pages.

df = pd.DataFrame(list_of_tables)

# Specify the path where you want to save the CSV file
csv_path = "BA_reviews.csv"

# Save the DataFrame as a CSV file
df.to_csv(csv_path, index=False)

print(f"Data saved to {csv_path}")

