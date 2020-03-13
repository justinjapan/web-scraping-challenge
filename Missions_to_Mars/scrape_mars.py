
#import dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import os
import pandas as pd
import time
import requests as req
from pprint import pprint
import numpy as np


#point to the directory where chromedriver exists
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)



#visit the page
url = "https://mars.nasa.gov/news/"
browser.visit(url)


#using bs to write it into html
html = browser.html
#soup = bs(response.text, 'lxml')
soup = bs(html,"html.parser")



#scrape site to collect latest News Titles and Paragraph Text
news_title = soup.find("div",class_="content_title").text
news_paragraph = soup.find("div", class_="article_teaser_body").text
print(f"Title: {news_title}")
print(f"Para: {news_paragraph}")


#Visit URL for JPL
url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=featured#submit"
browser.visit(url_image)


#Get the base url
from urllib.parse import urlsplit
base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url_image))
print(base_url)


#Grab the image
xpath = "//*[@id=\"page\"]/section[3]/div/ul/li[1]/a/div/div[2]/img"



#Use splinter to click on the mars featured image
#to bring the full resolution image
results = browser.find_by_xpath(xpath)
img = results[0]
img.click()



#get image url using BeautifulSoup
html_image = browser.html
soup = bs(html_image, "lxml")
img_url = soup.find("img", class_="fancybox-image")["src"]
featured_image_url = base_url + img_url
print(featured_image_url)



# Visit Mars Weather Twitter through splinter module
weather_url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(weather_url)


# HTML Object 
html_weather = browser.html

# Parse HTML with Beautiful Soup
soup = bs(html_weather, 'html.parser')

# Find all elements that contain tweets
latest_tweets = soup.find_all('div', class_='js-tweet-text-container')

# Retrieve all elements that contain news title in the specified range
# Look for entries that display weather related words to exclude non weather related tweets 
for tweet in latest_tweets: 
    weather_tweet = tweet.find('p').text
    if 'Sol' and 'pressure' in weather_tweet:
        print(weather_tweet)
        break
    else: 
        pass


# Visit Mars facts url 
facts_url = 'http://space-facts.com/mars/'

# Use Panda's `read_html` to parse the url
mars_facts = pd.read_html(facts_url)

# Find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
mars_df = mars_facts[0]

# Assign the columns `['Description', 'Value']`
mars_df.columns = ['Description','Value']

# Set the index to the `Description` column without row indexing
mars_df.set_index('Description', inplace=True)

# Save html code to folder Assets
mars_df.to_html()

data = mars_df.to_dict(orient='records')  # Here's our added param..

# Display mars_df
mars_df


# Visit hemispheres website through splinter module 
hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(hemispheres_url)


# HTML Object
html_hemispheres = browser.html

# Parse HTML with Beautiful Soup
soup = bs(html_hemispheres, 'html.parser')

# Retreive all items that contain mars hemispheres information
items = soup.find_all('div', class_='item')

# Create empty list for hemisphere urls 
hemisphere_image_urls = []

# Store the main_ul 
hemispheres_main_url = 'https://astrogeology.usgs.gov'

# Loop through the items previously stored
for i in items: 
    # Store title
    title = i.find('h3').text
    
    # Store link that leads to full image website
    partial_img_url = i.find('a', class_='itemLink product-item')['href']
    
    # Visit the link that contains the full image website 
    browser.visit(hemispheres_main_url + partial_img_url)
    
    # HTML Object of individual hemisphere information website 
    partial_img_html = browser.html
    
    # Parse HTML with Beautiful Soup for every individual hemisphere information website 
    soup = bs( partial_img_html, 'html.parser')
    
    # Retrieve full image source 
    img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
    
    # Append the retreived information into a list of dictionaries 
    hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    
    
    

# Display hemisphere_image_urls
hemisphere_image_urls
pprint(hemisphere_image_urls)




