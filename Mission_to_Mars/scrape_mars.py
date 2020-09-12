def scrape():
    # Import dependencies
    from splinter import Browser
    from bs4 import BeautifulSoup as bs
    import pandas as pd
    ## NASA Mars News
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = bs(html, 'html.parser')
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        print("not found")

    ## JPL Mars Space Images
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    
    # Scrape the JPL images site
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Add try/except for error handling
    try:
        # Open the full image link
        browser.click_link_by_partial_text('FULL IMAGE')
    except:
        print("FULL IMAGE link not found")

    # Optional delay for loading the page
    browser.is_element_present_by_css(".fancybox-image", wait_time=1)
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    image_soup = bs(html, 'html.parser')

    try:
        # grab image src and add onto site domain
        image_link = image_soup.find(class_="fancybox-image")['src']
        featured_image_url = 'https://www.jpl.nasa.gov' + image_link
    except:
        print("image not found")
    
    ## Mars Facts
    # scrape all tables from url
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    # grab the first table, the one we are interesed in using
    tabel = tables[0]
    # save the table as a file
    tabel.to_html('table.html',header=False,index=False)
    # store the table as a string
    tabel_html = tabel.to_html(header=False,index=False).replace('\n','')

    ## Mars Hemispheres
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    # Scrape Mars News
    # Visit the astrogeology site
    domain = 'https://astrogeology.usgs.gov'
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css(".description .pubDate", wait_time=1)
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    astro_soup = bs(html, 'html.parser')
    # get links to all 4 hemispheres
    hemi_links_slides = astro_soup.find_all('div',class_='description')
    # get url links to all 4 hemispheres' pages
    hemi_links = []
    for slide in hemi_links_slides:
        hemi_links.append(domain + slide.find('a')['href'])

    hemi_image_urls_titles = [] # for storing image info dictionaries
    # loop through each hemisphere url
    for url in hemi_links:
        # connect to url
        browser.visit(url)

        # Optional delay for loading the page
        browser.is_element_present_by_css(".wide-image", wait_time=1)
        # Convert the browser html to a soup object and then quit the browser
        html = browser.html
        hemi_soup = bs(html, 'html.parser')
        
        # store title and link into list as a dicitonary
        link = domain + hemi_soup.find(class_='wide-image')['src']
        title = hemi_soup.find(class_='title').text
        hemi_image_urls_titles.append({"title":title,"img_url":link})

    # return all outputs in a dictionary
    return {"news_title": news_title,
            "news_p": news_p,
            "featured_image_url": featured_image_url,
            "mars_table": tabel_html,
            "hemisphere_images": hemi_image_urls_titles
            }
