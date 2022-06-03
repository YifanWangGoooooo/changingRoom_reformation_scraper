from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

def get_all_pro_urls(link):
    try:
        # Set the URL
        base_url = link

        # open up chrome
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        # automatically use the correct chromedriver by using the webdrive-manager.
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(base_url)
        # wait 10 sec
        timeout = 10
    except Exception as e:
        driver.quit()
        print(e)

    # check if the page is loaded by checking the 'Search-Show' appears
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@data-action='Search-Show']")))
    except TimeoutException:
        print("Timed out waiting for page to load")
        driver.quit()

    try:
        ScrollCount = 0
        # getting the number of items on the page. if it is a full page then it will be 30
        results = driver.find_elements_by_xpath('//div[@class="product-grid__item col-6 col-md-3"]')
    except Exception as e:
        driver.quit()
        print(e)

    # we only scroll down 4 times at this point and get all the hyper objects on these 4 pages
    try:
        while (len(results) % 30 == 0) and (ScrollCount < 2):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            ScrollCount += 1
            # wait for the page to load
            time.sleep(10)

        results = driver.find_elements_by_xpath("//a[@href]")

    except Exception as e:
        driver.quit()
        print(e)

    # for each object in results, fetch the link and append it to list
    link_list = list()
    try:
        for result in results:
            link = result.get_attribute("href")
            link_list.append(link)
    except Exception as e:
        driver.quit()
        print(e)

    # filter out the product link including different colors
    link_list = [i for i in link_list if i.startswith('https://www.thereformation.com/products/')]

    # drop duplicate
    link_list = list(set(link_list))
    return link_list


def detail(link_list):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    name_list = list()
    price_list = list()
    color_list = list()
    size_list = list()
    image_list = list()
    description_list = list()
    for link in link_list[0:3]:
        try:
            driver.get(link)
        except:
            continue

        # gathering product name
        try:
            name = driver.find_elements_by_xpath('//div[@class="pdp__title"]')[0].find_element_by_tag_name("h1").text
            name_list.append(name)
        except:
            name_list.append("")

        # gathering product discription
        try:
            description = driver.find_elements_by_xpath('//div[@class="cms-generic-copy"]')[0].text
            description_list.append(description)
        except:
            description_list.append("")

        # gathering product price
        try:
            price = driver.find_elements_by_xpath('//span[@class="price--reduced"]')[0].text
            price_list.append(price)
        except:
            price_list.append("")

        # gathering product color
        try:
            color = driver.find_elements_by_xpath('//span[@class="product-attribute__selected-value"]')[0].text
            color_list.append(color)
        except:
            color_list.append("")

        # gathering product size
        try:
            sizes = driver.find_elements_by_xpath('//div[@data-attr-group="size"]//button')
            all_sizes = list()
            for size in sizes:
                size = size.get_attribute("data-title")
                all_sizes.append(size)
            size_list.append(all_sizes)
        except:
            size_list.append(list())

        # gathering product image link
        try:
            images = driver.find_elements_by_xpath('//div[@class="thumbnails-wrap css-25752b"]//img')

            all_images = list()
            for image in images:
                image = image.get_attribute("src")
                all_images.append(image)
            image_list.append(all_images)
        except:
            image_list.append(list())

    # generate datafram
    product_df = pd.DataFrame(
        {'productName': name_list,
         'productDescription': description_list,
         'productPrice': price_list,
         'productColor': color_list,
         'productSizes': size_list,
         'productCategory': category_list,
         'productUrl': link_list[0:3],
         'imageLinks': image_list

         })
    return product_df