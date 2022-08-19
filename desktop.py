""" 
COMP 593 - Final Project

Description: 
  Downloads NASA's Astronomy Picture of the Day (APOD) from a specified date
  and sets it as the desktop background image.

Usage:
  python apod_desktop.py image_cache_path [apod_date]

Parameters:
  image_cache_path = Full path of the image cache directory
  apod_date = APOD date (format: YYYY-MM-DD)

History:
  Date        Author    Description
  2022-05-09  J.Dalby   Initial creation
"""
from os import path
from sys import argv, exit
from datetime import datetime, date
from hashlib import sha256
from os import path, makedirs
from ctypes import windll
from urllib import request
import requests
import sqlite3
import re

def main():
    # *** DO NOT MODIFY THIS FUNCTION ***

    # Determine the path of image cache directory and SQLite data base file
    image_cache_path = get_image_cache_path()
    db_path = path.join(image_cache_path, 'apod_images.db')

    # Determine the date of the desired APOD
    apod_date = get_apod_date()

    # Create the image cache database, if it does not already exist
    create_apod_image_cache_db(db_path)

    # Get info about the APOD from the NASA API
    apod_info_dict = get_apod_info(apod_date)
    
    # Get the URL of the APOD
    image_url = get_apod_image_url(apod_info_dict)
    image_title = get_apod_image_title(apod_info_dict)
    
    # Determine the path at which the downloaded image would be saved 
    image_path = get_apod_image_path(image_cache_path, image_title, image_url)

    # Download the APOD image data, but do not save to disk
    image_data = download_image_from_url(image_url)

    # Determine the SHA-256 hash value and size of the APOD image data
    image_size = get_image_size(image_data)
    image_sha256 = get_image_sha256(image_data)

    # Print APOD image information
    print_apod_info(image_url, image_title, image_path, image_size, image_sha256)

    # Add image to cache if not already present
    if not apod_image_already_in_cache(db_path, image_sha256):
        save_image_file(image_data, image_path)
        add_apod_to_image_cache_db(db_path, image_title, image_path, image_size, image_sha256)

    # Set the desktop background image to the selected APOD
    set_desktop_background_image(image_path)

def get_image_cache_path():
   
    if len(argv) >= 2:
        dir_path = argv[1]

        if not path.isabs(dir_path):
            print('error: image cache path paramater must be absalute')
            exit('script excution aborted')
        else:
            if path is dir(dir_path):
                print('image cache directory:', dir_path)
                return dir_path
            elif path.isfile(dir_path):
                print('error: path parameter is existing file')
                exit('script excution aborted')
            else:
                print("creating new image directory '" + dir_path + "'...", end='')
                try:
                    makedirs(dir_path)
                    print('sucess')
                except:
                    print('failure')
                return dir_path
    else:
        print('error: missing image path paramater')
        exit('script excution aborted')

def get_apod_date():
    if len(argv) >- 3:
        apod_date = argv[2]  

        try: 
            apod_datetime = datetime.strptime(apod_date, '%Y-%m-%d')
        except ValueError:
            print('error: invalid datad format')
            exit('script aborted')
        if apod_datetime.date() < date(1995,6,16):
            print('error: date too far in past')
            exit("script aborted")
        elif apod_datetime.date() > date.today():
            print('error: date cant be in future')
            exit("script aborted")
    else:
        apod_date = date.today().isoformat()
    print("APOD date:", apod_date)

    return apod_date

def get_apod_image_path(image_cache_path, image_title, image_url):
    file_ext = image_url.split(".")[-1]

    file_name = image_title.strip()
    file_name = file_name.replace(' ', '_')
    file_name = re.sub(r'\W', '', file_name)
    file_name = '.'.join((file_name, file_ext))
    file_path = path.join(image_cache_path, file_name)
    return file_path

def get_apod_info(apod_date):
    print('getting image infor from NASA... Please stand by...', end='') 

    NASA_API_KEY = 'tz6CvXkLfg4etTXfvIZSOFaGDi6Cmm9BT393j05V'
    APOD_URL = "https://api.nasa.gov/planetary/apod"
    apod_params = {
        'api_key': NASA_API_KEY,
        'date': apod_date,
        'thumbs': True
    }
    resp_msg = requests.get(APOD_URL, params=apod_params)

    if resp_msg.status_code == requests.codes.ok:
        print('success')
    else:
        print('failure code', resp_msg.status_code)
        exit('script aborted')
    apod_info_dict = resp_msg.json()
    return apod_info_dict

def get_apod_image_url(apod_info_dict):
    if apod_info_dict['media_type'] == 'image':
        return apod_info_dict['hdurl']
    elif apod_info_dict['media_type'] == 'video':
        return apod_info_dict['thumbnail_url']
    return 'TODO'

def get_apod_image_title(apod_info_dict):
    return apod_info_dict['title']

def print_apod_info(image_url, image_title, image_path, image_size, image_sha256):
   print('apod image information:')
   print('image title:', image_title)
   print('image path', image_path)
   print('image url:', image_url)
   print('image size:', image_size, 'bytes')
   print('hash:', image_sha256)

def create_apod_image_cache_db(db_path):
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    create_table = """
        CREATE TABLE IF NOT EXISTS image(
            info     TEST PRIMARY KEY NOT NULL,
            title    TEXT NOT NULL,
            url      TEXT NOT NULL,
            size     INTEGER,
            hash     NUMERIC
        );
    """
    cur.execute(create_table)
    con.commit()
    con.close()

def add_apod_to_image_cache_db(db_path, image_title, image_path, image_size, image_sha256):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    insert_image = """INSERT INTO image_data
                    (title, file_path, size_bytes, sha256, downloaded_at)
                    VALUES (?,?,?,?,?)"""
    image_data = (image_title, image_path, image_size, image_sha256, datetime.now())
    cur.execute(insert_image, image_data)
    con.commit()
    con.close()

def apod_image_already_in_cache(db_path, image_sha256):
    db_path = sqlite3.connect(db_path)
    cur = db_path.cursor()

    image_sha256 = cur.execute("SELECT image_sha256 FROM apod WHERE image_sha256 = ?", (image_sha256,))
    hashed = cur.fetchall()
    if hashed:
        print('image is being added to the cache')
    else:
        print("image is already in cache")
    db_path.commit()
    db_path.close()
    return False

def get_image_size(image_data):
    return len(image_data)

def get_image_sha256(image_data):
    
    return sha256(image_data).hexdigest.upper()

def download_image_from_url(image_url):
    print('downloading image from NASA...', end='')

    resp_msg = requests.get(image_url)

    if resp_msg.status_code == requests.codes.ok:
        print('success')
    else:
        print('failure code', resp_msg.status_code)
        exit('script aborted')
    
def save_image_file(image_data, image_path):
    try:
        print('saving the image filre to cache...', end='')
        with open(image_path, 'wb') as fp:
            fp.write(image_data)
        print('success')
    except:
        print('failure')
        print('scripte aborted')
    return # TODO

def set_desktop_background_image(image_path):
    print("setting image as background")
    SPI_SETDESKWALLPAPER = 20
    windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 0)
    return # TODO

main()