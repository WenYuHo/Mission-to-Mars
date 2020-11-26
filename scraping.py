# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

# Set the executable path and initialize the chrome browser in splinter


# Scrape First topic, featured IMG, Mars fact and return dictionary of data.
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': 'C:\\Users\\tony5\\.wdm\\drivers\\chromedriver\\win32\\87.0.4280.20\\chromedriver.exe'}
    browser = Browser("chrome", **executable_path, headless=True)
    
    # Run all scraping functions and store results in dictionary
    news_title, news_paragraph = mars_news(browser)

    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now(),
      "hemispheres" : scrape_hd(browser)
    }
    
    # Stop webdriver and return data
    browser.quit()
    return data

# Scrape first topic title and its teaser paragraph
def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


    # Featured Title/Teaser Paragraph
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')

        # # Use the parent element to find the first <a> tag and save it as  `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None

    return news_title, news_p

# Scrape Featured Images
def featured_image(browser):
    # Visit url
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    # full_image_elem = browser.links.find_by_partial_text('FULL IMAGE')
    full_image_elem.click()


    # Find the more info button and click that
    # browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()


    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    
    return img_url

# Scrape Mars Facts
def mars_facts():
    try:
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)

    return df.to_html()

# Scrape Hemisphere Data

def scrape_hd(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    hemis_soup = soup(html, 'html.parser')
    hemisphere_image_urls = []
    all_hemis = hemis_soup.select("div.description a")
    try:
        for hemis in all_hemis:
            hemis_link = "https://astrogeology.usgs.gov" + hemis.get("href")
            browser.visit(hemis_link)
            html = browser.html
            one_hemis_soup = soup(html, 'html.parser')
            
            title = one_hemis_soup.select_one("h2.title").text
            image = one_hemis_soup.select_one("div.downloads a").get("href")
            
            hemispheres = {"img_url":image, "title":title}       
            hemisphere_image_urls.append(hemispheres)
        return hemisphere_image_urls
    except:
        return None




# script is complete and ready for action.
# The print statement will print out the results of our scraping
# to our terminal after executing the code.

if __name__ == "__main__":
    # If running as script, print scraped data
    # https://thepythonguru.com/what-is-if-__name__-__main__/
    print("Executing as main program")
    print(scrape_all())