
# coding: utf-8

# In[4]:


from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import tweepy
import time
import pandas as pd


# NASA Mars News

def mars_scrape():

    # Mars News URL# Mars
    url = "https://mars.nasa.gov/news/"

    # Retrieve page with the requests module
    html = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html.text, 'html.parser')

    # Get title & description
    news_title = soup.find('div', 'content_title', 'a').text
    news_p = soup.find('div', 'rollover_description_inner').text


    # In[6]:


    news_title


    # JPL Mars Space Images - Featured Image

    # In[8]:


    # JPL Mars URL# JPL Ma
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    # Setting up splinter
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path)
    browser.visit(url)

    # Moving through the pages
    time.sleep(5)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    browser.click_link_by_partial_text('more info')
    time.sleep(5)

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Get featured image
    results = soup.find('article')
    extension = results.find('figure', 'lede').a['href']
    link = "https://www.jpl.nasa.gov"
    featured_image_url = link + extension


    # Mars Weather

    # In[10]:


    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_weather_url)
    time.sleep(1)
    mars_weather_html = browser.html
    mars_weather_soup = BeautifulSoup(mars_weather_html, 'html.parser')

    tweets = mars_weather_soup.find('ol', class_='stream-items')
    mars_weather = tweets.find('p', class_="tweet-text").text
    print(mars_weather)


    # Mars Facts

    # In[12]:


    # visit space facts and scrap the mars facts table# visit
    mars_facts_url = 'https://space-facts.com/mars/'
    browser.visit(mars_facts_url)
    time.sleep(1)
    mars_facts_html = browser.html
    mars_facts_soup = BeautifulSoup(mars_facts_html, 'html.parser')

    fact_table = mars_facts_soup.find('table', class_='tablepress tablepress-id-mars')
    column1 = fact_table.find_all('td', class_='column-1')
    column2 = fact_table.find_all('td', class_='column-2')

    facets = []
    values = []

    for row in column1:
        facet = row.text.strip()
        facets.append(facet)
    
    for row in column2:
        value = row.text.strip()
        values.append(value)
    
    mars_facts = pd.DataFrame({
        "Facet":facets,
        "Value":values
        })

    mars_facts_html = mars_facts.to_html(header=False, index=False)
    mars_facts


    # Mars Hemispheres

    # In[37]:


    def marsHemisphere():
        hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        driver.get(hemisphere_url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        mars_hemisphere_list = []
        products = soup.find("div", class_ = "result-list" )
        hemispheres = products.find_all("div", class_="item")

        for hemisphere in hemispheres:
            title = hemisphere.find("h3").text
            title = title.replace("Enhanced", "")
            end_link = hemisphere.find("a")["href"]
            image_url = "https://astrogeology.usgs.gov/" + end_link
            mars_hemisphere_list.append({"title": title, "img_url": image_url})

        def get_high_res_url(some_url):
            response = requests.get(some_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all("a")
            tifs = [j for j in links if ".tif" in j.attrs.get('href')]
            return tifs[0].get('href')

        updated_photos = []

        for data in mars_hemisphere_list:
            link_to_check = data.get('img_url')
            title = data.get('title')
            final_image_url = get_high_res_url(link_to_check)
            updated_photos.append({
                'Title': title,
                'Url': final_image_url
            })
        return updated_photos

