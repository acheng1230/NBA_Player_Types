# Load packages
import re
import pandas as pd
import numpy as np

# Load selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chrome webdriver
driver = webdriver.Chrome('/Users/alexcheng/Downloads/chromedriver')

def get_player_name(url):
    """
    takes in a specific player page and scrapes the player name.
    """
    driver.get(url)
    name = driver.find_elements_by_xpath("""//*[@id="meta"]/div[2]/h1""")
    for value in name:
        name = value.text
        name = str(name.encode('ascii', 'ignore'))
    return name

def get_per_game(url):
    """
    takes in a specific url and scrapes the career averages from the per game table.
    """
    driver.get(url)

    # share & more
    driver.find_element_by_xpath("""//*[@id="all_per_game"]/div[1]/div/ul/li[1]/span""").click()

    # get table as csv (for excel)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, """//*[@id="all_per_game"]/div[1]/div/ul/li[1]/div/ul/li[3]/button"""))).click()

    # table
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME, """table_outer_container""")))

    # capture csv text
    per_game = driver.find_element_by_id("csv_per_game")

    # data cleaning
    per_game = per_game.text.encode('ascii', 'ignore').split()

    for stats in per_game:
        if stats.startswith('Career'):
            per_game = re.findall('(\d[\d.,-]+)$', stats)[0]

    per_game_list = []
    for i in per_game.split(','):
        if i == '':
            per_game_list.append(0.0)
        else:
            i = float(i)
            per_game_list.append(i)

    return per_game_list


def get_shooting(url):
    """
    takes in a specific player page and scrapes the career averages from the shooting table.
    """
    driver.get(url)

    # share & more
    driver.find_element_by_xpath("""//*[@id="all_shooting"]/div[1]/div/ul/li[2]/span""").click()

    # get table as csv (for excel)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, """//*[@id="all_shooting"]/div[1]/div/ul/li[2]/div/ul/li[3]/button"""))).click()

    # table
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME, """table_outer_container""")))

    # capture csv text
    shooting = driver.find_element_by_id("csv_shooting")

    # data cleaning
    shooting = shooting.text.encode('ascii', 'ignore').split()

    for stats in shooting:
        if stats.startswith('Career'):
            shooting = re.findall('(\d[\d.,-]+)$', stats)[0]

    shooting_list = []
    for i in shooting.split(','):
        if i == '':
            shooting_list.append(0.0)
        else:
            i = float(i)
            shooting_list.append(i)

    return shooting_list


def get_advanced(url):
    """
    takes in a specific player page and scrapes the career averages from the advanced table.
    """
    driver.get(url)
    # scraping advanced table
    driver.find_element_by_xpath("""//*[@id="all_advanced"]/div[1]/div/ul/li[1]/span""").click()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, """//*[@id="all_advanced"]/div[1]/div/ul/li[1]/div/ul/li[3]/button"""))).click()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.CLASS_NAME, """table_outer_container""")))

    # capture csv text
    advanced = driver.find_element_by_id("csv_advanced")

    # data cleaning
    advanced = advanced.text.encode('ascii').split()

    for stats in advanced:
        if stats.startswith('Career'):
            advanced = re.findall('(\d[\d.,-]+)$', stats)[0]

    advanced_list = []
    for i in advanced.split(','):
        if i == '':
            advanced_list.append(0.0)
        else:
            i = float(i)
            advanced_list.append(i)

    del advanced_list[14]
    del advanced_list[19]

    return advanced_list

def get_columns():
    """
    grabs column headers from the shooting and advanced tables (in that order).
    """

    # per_game_cols = ['Player', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%',
    #                  '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB',
    #                  'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']

    shooting_cols = ['Games', 'Min_Played', 'FG%', 'AVG_DIST_FGA', '%FGA_2P', '%FGA_0-3ft',
                     '%FGA_3-10ft','%FGA_10-16ft', '%FGA_16ft<3', '%FGA_3P', '2P%',
                     '0-3_FG%', '3-10_FG%', '10-16_FG%', '16<3_FG%', '3P%', '%ASTd_2P',
                     '%FGA_DUNK', 'DUNKS', '%ASTd_3P', '%_CORNER3PA', '3P%_CORNER3',
                     'HEAVE_ATT', 'HEAVE_MD']

    advanced_cols = ['Games_', 'Minutes_Played', 'PER', 'TS%', '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%',
                     'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%', 'OWS', 'DWS', 'WS',
                     'WS/48', 'OBPM', 'DPM', 'BPM', 'VORP']

    cols = shooting_cols + advanced_cols
    return cols


def advanced_stats(url):
    """
    scrapes the entire advanced stats table for the season.
    """
    driver.get(url)

    # share & more
    driver.find_element_by_xpath("""//*[@id="all_per_game"]/div[1]/div/ul/li[1]/span""").click()

    # get table as csv (for excel)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, """//*[@id="all_per_game"]/div[1]/div/ul/li[1]/div/ul/li[3]/button"""))).click()

    # table
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME, """table_outer_container""")))

    # capture csv text
    per_game = driver.find_element_by_id("csv_per_game")
