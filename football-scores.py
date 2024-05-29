import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
path = 'G:/chromedriver/chromedriver.exe'
cService = webdriver.ChromeService(executable_path=path)
driver = webdriver.Chrome(service=cService, options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(2)
website = 'https://www.adamchoi.co.uk/overs/detailed'

driver.get(website)
all_matches_button = driver.find_element(By.XPATH, 
    '//label[@analytics-event="All matches"]')
all_matches_button.click()
dropdown = Select(driver.find_element(By.ID, 'country'))
dropdown.select_by_visible_text('Japan')
time.sleep(3)
matches = driver.find_elements(By.TAG_NAME, 'tr')

date = []
home_team = []
score = []
away_team = []

for match in matches:
    # print(match)
    date.append(match.find_element(By.XPATH, './td[1]').text)
    home = match.find_element(By.XPATH, './td[2]').text
    home_team.append(home)
    score.append(match.find_element(By.XPATH, './td[3]').text)
    away_team.append(match.find_element(By.XPATH, './td[4]').text)

driver.quit()
df = pd.DataFrame({'Date': date, 'Home Team': home_team,
                    'Score': score, 'Away Team': away_team})
df.to_csv('football-Japan.csv', index=False)

