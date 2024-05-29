import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
path = 'G:/chromedriver/chromedriver.exe'
cService = webdriver.ChromeService(executable_path=path)

website = 'https://x.com'
driver = webdriver.Chrome(service=cService, options=chrome_options)
driver.maximize_window()
driver.get(website)
try:
    signin_btn = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//a[@data-testid="loginButton"]')))
except Exception as e:
    print("Loading took too much time or element not found", str(e))
signin_btn.click()
try:
    username = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
        (By.XPATH, '//input[@autocomplete="username"]')))
except Exception as e:
    print("Loading took too much time or element not found", str(e))
username.send_keys('USERNAME')
try:
    next_button = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//button[@type="button"][2]')))
except Exception as e:
    print("Loading took too much time or element not found", str(e))
next_button.click()
try:
    password = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//input[@name="password"]')))
except Exception as e:
    print("Loading took too much time or element not found", str(e))
password.send_keys('PASSWORD')
try:
    loginbutton = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
        (By.XPATH, '//button[@data-testid="LoginForm_Login_Button"]')))
except Exception as e:
    print("Loading took too much time or element not found", str(e))
loginbutton.click()
try:
    searchbox = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Search"]')))
except Exception as e:
    print("Loading took too much time or element not found", str(e))
searchbox.send_keys('#BreakingNews #HindiNews')
searchbox.send_keys(Keys.ENTER)


def get_article(article):
    try:
        username = article.find_element(
            By.XPATH, './/span[contains(text(), "@")]').text
        text = article.find_element(
            By.XPATH, './/div[@data-testid="tweetText"]').text
        tweets_data = [username, text]

    except Exception as e:
        print("Loading took too much time or element not found", str(e))
        tweets_data = ['user', 'text']

    return tweets_data


user_data = []
text_data = []
article_ids = set()
scrolling = True

while scrolling:

    articles = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.XPATH, '//article[@role="article"]')))

    for article in articles:
        article_list = get_article(article)
        print(article_list)
        article_id = ''.join(article_list)
        if article_id not in article_ids:
            article_ids.add(article_id)
            user_data.append(article_list[0])
            text_data.append(" ".join(article_list[1].split()))

    # Get the initial scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(3)
        # Calculate new scroll height and compare it with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:  # if the new and last height are equal, it means that there isn't any new page to load, so we stop scrolling
            scrolling = False
            break
        else:
            last_height = new_height
            break
driver.quit()
articles_data = pd.DataFrame({"Name": user_data, "Text": text_data})
articles_data.to_csv("x-articles.csv", index=False)
