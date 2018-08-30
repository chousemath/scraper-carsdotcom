import argparse
from selenium import webdriver
import os
import random
import string
import subprocess
import csv


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Enforce `Incognito` mode for the Chrome browser
CHROME_OPTIONS = webdriver.ChromeOptions()
CHROME_OPTIONS.add_argument("--incognito")


def extract_link(element) -> str:
    try:
        return element.find_elements_by_tag_name('a')[0].get_attribute('href')
    except:
        print('link not found...')
        return ''


with open('cars.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        # Manually define the folder name
        DIR_NAME = f'{row[0]}_{row[1]}_{row[2]}_{row[3]}'
        driver = webdriver.Chrome(chrome_options=CHROME_OPTIONS)
        driver.implicitly_wait(10)
        # Open the encar website page in an incognito Chrome window
        driver.get(row[4])
        # collect the surface level listings
        CARS = driver.find_elements_by_class_name('listing-row__details')
        # collect all the LINKS for the CARS on that page
        LINKS = []
        for car in CARS:
            # extract only the vehicle details page link
            LINKS.append(extract_link(car))
        IMAGES = []
        for link in LINKS:
            print(f'{bcolors.OKBLUE}Visiting {link}{bcolors.ENDC}')
            print(
                f'{bcolors.OKGREEN}====================================={bcolors.ENDC}')
            driver.get(link)
            divs = driver.find_elements_by_tag_name('div')
            for div in divs:
                data_image = div.get_attribute('data-image')
                if data_image:
                    IMAGES.append(data_image)
        # activate the concurrent image downloader
        bashCommand = f"./concurrent-image-download {DIR_NAME} {' '.join(IMAGES)}"
        # subprocess.Popen ensures that this is a non-blocking system call
        subprocess.Popen(['bash', '-c', bashCommand])
        # destroy this driver session and move on to the next one
        driver.quit()
