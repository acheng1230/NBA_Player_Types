import re
import glob
import numpy as np
import pandas as pd

# Load selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# Chrome webdriver
driver = webdriver.Chrome('/Users/alexcheng/Downloads/chromedriver')

# Read files
file_location = "/Users/alexcheng/Desktop/advanced_stats/*.csv"

def load_and_clean_csv(file_location):
    for csv in glob.glob(file_location):
        adv_stats = pd.read_csv(csv)

        # Drop columns
        adv_stats.drop(['Rk', 'Tm', 'Unnamed: 20','Unnamed: 25'], axis=1, inplace=True)

        # Create list
        player_list = list(adv_stats['Player'])

        # Consolidate dataframe
        adv_stats_df = adv_stats.groupby([adv_stats.Player, adv_stats.Pos, adv_stats.Player_ID]).mean()

        # Save CSV
        adv_stats_df.to_csv(csv)

file_loc = "/Users/alexcheng/Desktop/cleaned/*.csv"

def add_url(file_loc):
    for csv in glob.glob(file_loc):
        stats = pd.read_csv(csv)

        player_list = list(stats['Player'])

        # Create last_letter column
        last_letter = []
        for player in player_list:
            temp = []
            temp = player.split()
            last_letter.append(temp[1][0].lower())
        stats['last_letter'] = last_letter

        # Create url column
        for i in stats:
            url = "http://www.basketball-reference.com/players/" + stats['last_letter'] + "/" + stats['Player_ID'] + ".html"

        stats['url'] = url

        # Drop last_letter column
        stats.drop('last_letter', axis=1, inplace=True)

        # Save CSV
        stats.to_csv(csv)


def get_shooting(season, url):
    """
    takes in a specific player page and scrapes the career averages from the shooting table.
    """
    driver.get(url)

    # share & more
    driver.find_element_by_xpath("""//*[@id="all_shooting"]/div[1]/div/ul/li[2]/span""").click()

    # get table as csv (for excel)
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable(
            (By.XPATH, """//*[@id="all_shooting"]/div[1]/div/ul/li[2]/div/ul/li[3]/button"""))).click()

    # table
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME, """table_outer_container""")))

    # capture csv text
    shooting = driver.find_element_by_id("csv_shooting")

    # data cleaning
    shooting = shooting.text.encode('ascii', 'ignore').split()

    for stats in shooting:
        if stats.startswith(season):
            shooting = re.findall('(\d[\d.,-]+)$', stats)[0]

    player_id = re.findall('(\w+\d)', url)

    shooting_list = [player_id[0]]
    for i in shooting.split(','):
        if i == '':
            shooting_list.append(0.0)
        else:
            i = float(i)
            shooting_list.append(i)

    return shooting_list


def get_attributes(url):
    driver.get(url)
    try:
        height = driver.find_element_by_css_selector("""#meta > div:nth-of-type(2) > p:nth-of-type(1) > span:nth-of-type(1)""")
        weight = driver.find_element_by_css_selector("""#meta > div:nth-of-type(2) > p:nth-of-type(1) > span:nth-of-type(2)""")
        height = height.text.encode('ascii')
        weight = weight.text.encode('ascii')
        feet = float(re.findall('(\d+)-', height)[0])
        inches = float(re.findall('-(\d+)', height)[0])
        pounds = float(re.findall('(\d+)lb', weight)[0])
        player_id = re.findall('(\w+\d)', url)
        total_inches = feet * 12 + inches
        final_list = [player_id[0], total_inches, pounds]
        return final_list
    except NoSuchElementException:
        try:
            height = driver.find_element_by_css_selector("""#meta > div:nth-of-type(2) > p:nth-of-type(2) > span:nth-of-type(1)""")
            weight = driver.find_element_by_css_selector("""#meta > div:nth-of-type(2) > p:nth-of-type(2) > span:nth-of-type(2)""")
            height = height.text.encode('ascii')
            weight = weight.text.encode('ascii')
            feet = float(re.findall('(\d+)-', height)[0])
            inches = float(re.findall('-(\d+)', height)[0])
            pounds = float(re.findall('(\d+)lb', weight)[0])
            player_id = re.findall('(\w+\d)', url)
            total_inches = feet * 12 + inches
            final_list = [player_id[0], total_inches, pounds]
            return final_list
        except NoSuchElementException:
            try:
                height = driver.find_element_by_css_selector("""#meta > div:nth-of-type(2) > p:nth-of-type(3) > span:nth-of-type(1)""")
                weight = driver.find_element_by_css_selector("""#meta > div:nth-of-type(2) > p:nth-of-type(3) > span:nth-of-type(2)""")
                height = height.text.encode('ascii')
                weight = weight.text.encode('ascii')
                feet = float(re.findall('(\d+)-', height)[0])
                inches = float(re.findall('-(\d+)', height)[0])
                pounds = float(re.findall('(\d+)lb', weight)[0])
                player_id = re.findall('(\w+\d)', url)
                total_inches = feet * 12 + inches
                final_list = [player_id[0], total_inches, pounds]
                return final_list
            except NoSuchElementException:
                try:
                    height = driver.find_element_by_css_selector("""#meta > div:nth-of-type(2) > p:nth-of-type(4) > span:nth-of-type(1)""")
                    weight = driver.find_element_by_css_selector("""#meta > div:nth-of-type(2) > p:nth-of-type(4) > span:nth-of-type(2)""")
                    height = height.text.encode('ascii')
                    weight = weight.text.encode('ascii')
                    feet = float(re.findall('(\d+)-', height)[0])
                    inches = float(re.findall('-(\d+)', height)[0])
                    pounds = float(re.findall('(\d+)lb', weight)[0])
                    player_id = re.findall('(\w+\d)', url)
                    total_inches = feet * 12 + inches
                    final_list = [player_id[0], total_inches, pounds]
                    return final_list
                except:
                    try:
                        height = driver.find_element_by_css_selector("""#meta > div:nth-of-type(2) > p:nth-of-type(5) > span:nth-of-type(1)""")
                        weight = driver.find_element_by_css_selector("""#meta > div:nth-of-type(2) > p:nth-of-type(5) > span:nth-of-type(2)""")
                        height = height.text.encode('ascii')
                        weight = weight.text.encode('ascii')
                        feet = float(re.findall('(\d+)-', height)[0])
                        inches = float(re.findall('-(\d+)', height)[0])
                        pounds = float(re.findall('(\d+)lb', weight)[0])
                        player_id = re.findall('(\w+\d)', url)
                        total_inches = feet * 12 + inches
                        final_list = [player_id[0], total_inches, pounds]
                        return final_list
                    except:
                        try:
                            height = driver.find_element_by_css_selector("""#meta > div:nth-of-type(2) > p:nth-of-type(6) > span:nth-of-type(1)""")
                            weight = driver.find_element_by_css_selector("""#meta > div:nth-of-type(2) > p:nth-of-type(6) > span:nth-of-type(2)""")
                            height = height.text.encode('ascii')
                            weight = weight.text.encode('ascii')
                            feet = float(re.findall('(\d+)-', height)[0])
                            inches = float(re.findall('-(\d+)', height)[0])
                            pounds = float(re.findall('(\d+)lb', weight)[0])
                            player_id = re.findall('(\w+\d)', url)
                            total_inches = feet * 12 + inches
                            final_list = [player_id[0], total_inches, pounds]
                            return final_list
                        except:
                            print("Shit's broken, yo")
