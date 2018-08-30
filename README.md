# Scraper for cars.com with concurrent, non-blocking image download

> This project is a simple web scraper built using Selenium Web Driver. The majority of the logic is build in Python, but the image downloader is an executable built using the Golang toolchain for MacOS. The source code for the image downloader can be found [here](https://github.com/chousemath/concurrent-image-download). The images will be downloaded into a `car-specific directory` inside the `images` directory, which will be created automatically by the image-download binary if it does not yet exist.

### Executing this script

```bash
# First, populate cars.csv with all the car metadata you want to scrape
# The csv file must be structured in the following way...
# YEAR,MAKE,MODEL,TRIM,LINK
$ python scraper.py
```