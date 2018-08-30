import argparse
from selenium import webdriver
import os
import random
import string
import subprocess


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


combinations = [
    ('2014', 'astonmartin', 'random', 'rr', 'https://www.cars.com/for-sale/searchresults.action/?localVehicles=true&mkId=20003&page=1&perPage=10&rd=99999&searchSource=GN_REFINEMENT&showMore=true&sort=relevance&yrId=51683&zc=21043'),
    ('2014', 'astonmartin', 'random', 'rr', 'https://www.cars.com/for-sale/searchresults.action/?localVehicles=true&mkId=20003&page=2&perPage=10&rd=99999&searchSource=GN_REFINEMENT&showMore=true&sort=relevance&yrId=51683&zc=21043'),
]

for combo in combinations:
    # Manually define the folder name
    YEAR = combo[0]
    MAKE = combo[1]
    MODEL = combo[2]
    TRIM = combo[3]
    DIR_NAME = f'{YEAR}_{MAKE}_{MODEL}_{TRIM}'
    PAGE_URL = combo[4]

    driver = webdriver.Chrome(chrome_options=CHROME_OPTIONS)
    driver.implicitly_wait(10)
    # Open the encar website page in an incognito Chrome window
    driver.get(PAGE_URL)
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
        print(f'{bcolors.OKGREEN}====================================={bcolors.ENDC}')
        driver.get(link)
        divs = driver.find_elements_by_tag_name('div')
        for div in divs:
            data_image = div.get_attribute('data-image')
            if data_image:
                IMAGES.append(data_image)

    bashCommand = f"./concurrent-image-download {DIR_NAME} {' '.join(IMAGES)}"
    subprocess.Popen(['bash', '-c', bashCommand])

    driver.quit()
