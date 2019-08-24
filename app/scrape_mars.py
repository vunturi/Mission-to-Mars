# from splinter import Browser
# from bs4 import BeautifulSoup
# import numpy
# import pandas as pd
# import time

# def mars_news(browser, data):
# 	print("mars_news")

# 	# Visit the mars nasa news site

# 	url = "https://mars.nasa.gov/news/"

# 	browser.visit(url)

# 	# Optional delay for loading the page
# 	browser.is_element_present_by_css("ul.item_list li.slide")

# 	# Convert the browser html to a soup object and then quit the browser
# 	html = browser.html
# 	news_soup = BeautifulSoup(html, 'html.parser')

# 	slide_elem = news_soup.select_one('ul.item_list li.slide')

# 	slide_elem.find("div", class_='content_title')

# 	# Use the parent element to find the first a tag and save it as `news_title`
# 	news_title = slide_elem.find("div", class_='content_title').get_text()

# 	# Use the parent element to find the paragraph text
# 	news_p = slide_elem.find('div', class_="article_teaser_body").get_text()

# 	temp_dict = {"news_title": news_title, 
# 				 "news_para": news_p}

# 	data['mars_news'] = temp_dict




# def featured_image(browser, data):
# 	print("featured image")

# 	# Visit URL
# 	url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
# 	browser.visit(url)

# 	# Find and click the full image button
# 	full_image_elem = browser.find_by_id('full_image')
# 	full_image_elem.click()

# 	# Find the more info button and click that
# 	browser.is_element_present_by_text('more info', wait_time=1)
# 	more_info_elem = browser.find_link_by_partial_text('more info')
# 	more_info_elem.click()

# 	# Parse the resulting html with soup
# 	html = browser.html
# 	img_soup = BeautifulSoup(html, 'html.parser')

# 	# find the relative image url
# 	img_url_rel = img_soup.select_one('figure.lede a img').get("src")

# 	# Use the base url to create an absolute url
# 	img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

# 	temp_dict = {"featured_image" : img_url}

# 	data["JPL_featured_image"] = temp_dict


# def hemispheres(browser, data):

# 	url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
# 	browser.visit(url_hemisphere)

# 	hemisphere_image_urls = {}

# 	# First, get a list of all of the hemispheres
# 	links = browser.find_by_css("a.product-item h3")

# 	# Next, loop through those links, click the link, find the sample anchor, return the href
# 	for i in range(len(links)):
# 		#hemisphere = {}

# 		# We have to find the elements on each loop to avoid a stale element exception
# 		browser.find_by_css("a.product-item h3")[i].click()

# 		# Get Hemisphere title
# 		#hemisphere['title'] = browser.find_by_css("h2.title").text

# 		title = browser.find_by_css("h2.title").text

# 		# Next, we find the Sample image anchor tag and extract the href
# 		sample_elem = browser.find_link_by_text('Sample').first
# 		#hemisphere['img_url'] = sample_elem['href']

# 		img_url = sample_elem['href']

# 		# Append hemisphere object to list
# 		#hemisphere_image_urls.append(hemisphere)

# 		hemisphere_image_urls[title] = img_url

# 		# Finally, we navigate backwards
# 		browser.back()

# 	data["hemisphere"] = hemisphere_image_urls


# def twitter_weather(browser, data):

# 	url = 'https://twitter.com/marswxreport?lang=en'
# 	browser.visit(url)

# 	html = browser.html
# 	weather_soup = BeautifulSoup(html, 'html.parser')

# 	# First, find a tweet with the data-name `Mars Weather`
# 	mars_weather_tweet = weather_soup.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})

# 	# Next, search within the tweet for the p tag containing the tweet text
# 	mars_weather = mars_weather_tweet.find('p', 'tweet-text').get_text()

# 	temp_dict = {"twitter_mars_weather": mars_weather}

# 	data["mars_weather"] = temp_dict

# def mars_facts(data):
# 	df = pd.read_html('http://space-facts.com/mars/')[1]
# 	df.columns=['description', 'value']
# 	df.set_index('description', inplace=True)
# 	mars_html_tag = df.to_html()

# 	temp_dict = {"mars_df_html": mars_html_tag}

# 	data["mars_fact"] = temp_dict


# def scrape_all():

# 	print("scrape_all")

# 	# Initiate headless driver for deployment
# 	executable_path = {'executable_path': 'C:\\webdrivers\\chromedriver_win32\\chromedriver.exe'}
# 	browser = Browser('chrome', **executable_path)

# 	# Run all scraping functions and store in dictionary.
# 	data = {}

# 	mars_news(browser, data)
# 	featured_image(browser, data)
# 	twitter_weather(browser, data)
# 	mars_facts(data)
# 	hemispheres(browser, data)

# 	print(data)



# 	# Stop webdriver and return data
# 	browser.quit()

# 	return data


# if __name__ == "__main__":

# 	# If running as script, print scraped data
# 	print(scrape_all())

from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt


def scrape_all():

    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store in dictionary.
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "hemispheres": hemispheres(browser),
        "weather": twitter_weather(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # Get first list item and wait half a second if not immediately present
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=0.5)

    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")

    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        news_title = slide_elem.find("div", class_="content_title").get_text()
        news_p = slide_elem.find(
            "div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id("full_image")
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text("more info", wait_time=0.5)
    more_info_elem = browser.find_link_by_partial_text("more info")
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, "html.parser")

    # Find the relative image url
    img = img_soup.select_one("figure.lede a img")

    try:
        img_url_rel = img.get("src")

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f"https://www.jpl.nasa.gov{img_url_rel}"

    return img_url


def hemispheres(browser):

    # A way to break up long strings
    url = (
        "https://astrogeology.usgs.gov/search/"
        "results?q=hemisphere+enhanced&k1=target&v1=Mars"
    )

    browser.visit(url)

    # Click the link, find the sample anchor, return the href
    hemisphere_image_urls = []
    for i in range(4):

        # Find the elements on each loop to avoid a stale element exception
        browser.find_by_css("a.product-item h3")[i].click()

        hemi_data = scrape_hemisphere(browser.html)

        # Append hemisphere object to list
        hemisphere_image_urls.append(hemi_data)

        # Finally, we navigate backwards
        browser.back()

    return hemisphere_image_urls


def twitter_weather(browser):
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    html = browser.html
    weather_soup = BeautifulSoup(html, "html.parser")

    # First, find a tweet with the data-name `Mars Weather`
    tweet_attrs = {"class": "tweet", "data-name": "Mars Weather"}
    mars_weather_tweet = weather_soup.find("div", attrs=tweet_attrs)

    # Next, search within the tweet for the p tag containing the tweet text
    mars_weather = mars_weather_tweet.find("p", "tweet-text").get_text()

    return mars_weather


def scrape_hemisphere(html_text):

    # Soupify the html text
    hemi_soup = BeautifulSoup(html_text, "html.parser")

    # Try to get href and text except if error.
    try:
        title_elem = hemi_soup.find("h2", class_="title").get_text()
        sample_elem = hemi_soup.find("a", text="Sample").get("href")

    except AttributeError:

        # Image error returns None for better front-end handling
        title_elem = None
        sample_elem = None

    hemisphere = {
        "title": title_elem,
        "img_url": sample_elem
    }

    return hemisphere


def mars_facts():
    try:
        df = pd.read_html("http://space-facts.com/mars/")[1]
    except BaseException:
        return None

    df.columns = ["description", "value"]
    df.set_index("description", inplace=True)

    # Add some bootstrap styling to <table>
    return df.to_html(classes="table table-striped")


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())
