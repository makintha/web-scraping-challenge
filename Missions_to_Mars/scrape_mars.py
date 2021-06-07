from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
# from selenium import Browser 
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd

def scrape_info():
    # Set up Splinter        
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    urls = [
        "https://redplanetscience.com/",
        "https://spaceimages-mars.com/",
        "https://galaxyfacts-mars.com/",
        "https://marshemispheres.com/"
        ]

    # setting dictionary
    mars={}

    for i in range(len(urls)):
        browser.visit(urls[i])
        html = browser.html
        # Create a Beautiful Soup object
        soup = bs(html, 'html.parser')

        if i == 0:
            # Scrapping latest news
            
            mars['title'] = soup.find("div", class_="content_title").text
            mars['para'] = soup.find("div", class_="article_teaser_body").text


        elif i == 1:
            # Scrapping image
            head = soup.find('div', class_="floating_text_area")
            image_url = head.find('a')['href']
            mars['featured_image_url'] = urls[i] + image_url

            # print(featured_image_url)

        elif i == 2:
            # scrapping table

            # import to Pandas
            table = pd.read_html(urls[i])
            df = table[0]
            df.columns=['Desciptions','Mars', 'Earth']
            mars['table'] = df.to_html(index=False, classes=['table', 'table-striped'])


        elif i == 3:
            # Scrapping Mars Hemisphere Titles and Images
            temp = soup.find_all('div', class_="description")
        
            hemisphere_title = []
            for x in temp:
                hemisphere_title.append(x.find('h3').text)
        
            # print(hemisphere_title)
        
            image_full_url = []
            for hemis in hemisphere_title:
        
                html = browser.html
                soup = bs(html, 'html.parser')
        
                browser.links.find_by_partial_text(f'{hemis}').click()
        
                html = browser.html
                soup = bs(html, 'html.parser')
        
                tt = soup.find('img', class_="wide-image")
                image_full_url.append(tt['src'])
        
                browser.links.find_by_partial_text('Back').click()
            


            hemis_image_url = [urls[i] + url for url in image_full_url]
            hemisphere_image_urls = []
            for i in range(len(hemisphere_title)):
                hemisphere_image_urls.append(
                    {"title": hemisphere_title[i],
                    "img_url" : hemis_image_url[i]
                    }
                )
            
            mars['hemisphere_image_urls'] = hemisphere_image_urls
        

    browser.quit()

    return mars

# print(scrape_info())