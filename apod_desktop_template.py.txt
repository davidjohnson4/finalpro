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
    """
    Gets the path of the image cache directory in which all APOD
    images are saved. Creates the image cache directory if it 
    does not already exist.
    
    Exits script execution if no image cache directory path is 
    specified as a command line parameter or the specified path
    is not a valid full path.

    :returns: Path of the image cache directory
    """
    return 'TODO'

def get_apod_date():
    """
    Validates the command line parameter that specifies the APOD date.
    Script exits if the date is invalid or formatted incorrectly.
    Returns today's date if no date is provided on the command line. 

    :returns: APOD date as a string in 'YYYY-MM-DD' format
    """    
    return 'TODO'

def get_apod_image_path(image_cache_path, image_title, image_url):
    """
    Determines the path at which the APOD image is saved in the image cache. 
    
    The image file name is constructed as follows:
    - The file extension is taken from the image URL
    - The file name is taken from the image title, where:
        - Leading and trailing spaces are removed
        - Inner spaces are replaced with underscores
        - Characters other than letters, numbers, and underscores are removed

    For example, suppose:
    - The image cache directory path is 'C:\\temp\\APOD'
    - The image URL is 'https://apod.nasa.gov/apod/image/2205/NGC3521LRGBHaAPOD-20.jpg'
    - The image title is ' NGC #3521: Galaxy in a Bubble '

    The image path will be 'C:\\temp\\APOD\\NGC_3521_Galaxy_in_a_Bubble.jpg'

    :param image_url: APOD image URL
    :param image_cache_path: Path of the image cache directory
    :returns: Path at which image is saved in the image cache
    """
    return 'TODO'

def get_apod_info(apod_date):
    """
    Gets information from the NASA API for the Astronomy 
    Picture of the Day (APOD) from a specified date.

    :param apod_date: APOD date formatted as YYYY-MM-DD
    :returns: Dictionary of APOD info
    """    
    return 'TODO'

def get_apod_image_url(apod_info_dict):
    """
    Gets the URL of the APOD image from the dictionary of APOD information.
    If the APOD is a video, gets the URL of the video thumbnail. 

    :param apod_info_dict: Dictionary of APOD info
    :returns: APOD image URL
    """   
    return 'TODO'

def get_apod_image_title(apod_info_dict):
    """
    Gets the title of the APOD image from the dictionary of APOD information.

    :param apod_info_dict: Dictionary of APOD info
    :returns: APOD image title
    """   
    return 'TODO'

def print_apod_info(image_url, image_title, image_path, image_size, image_sha256):
    """
    Prints the following information about the APOD:
    - Image URL
    - Path at which image is saved in the image cache
    - Image size in bytes
    - Image SHA-256 hash value 

    :param image_url: URL of the APOD image
    :param image_title: Title of the APOD image
    :param image_path: Path of the APOD image file saved locally
    :param image_size: Size of APOD image in bytes
    :param image_sha256: SHA-256 hash value of APOD image
    :returns: None
    """    
    return #TODO

def create_apod_image_cache_db(db_path):
    """
    Creates the APOD image cache SQLite database if it 
    doesn't already exist.

    :param db_path: Path of APOD image cache .db file
    :returns: None
    """
    return #TODO

def add_apod_to_image_cache_db(db_path, image_title, image_path, image_size, image_sha256):
    """
    Adds a specified APOD image to the image cache database.

    :param db_path: Path of APOD image cache .db file
    :param image_title: Title of the APOD image
    :param image_path: Path of the APOD image file saved locally
    :param image_size: Size of APOD image in bytes
    :param image_sha256: SHA-256 hash value of APOD image
    :returns: None
    """
    return #TODO

def apod_image_already_in_cache(db_path, image_sha256):
    """
    Determines whether an image with a specified SHA-256 hash value
    is already present in the image cache.

    :param db_path: Path of APOD image cache .db file
    :param image_sha256: SHA-256 hash value of APOD image
    :returns: True if image is already in the cache; False otherwise
    """ 
    return False #TODO

def get_image_size(image_data):
    """
    Determines the size of an image in bytes

    :param image_data: Image data binary string
    :returns: Size of image in bytes
    """
    return 'TODO'

def get_image_sha256(image_data):
    """
    Calculates the SHA-256 hash value of an image

    :param image_data: Image data binary string
    :returns: SHA-256 hash value of image (hexadecimal string)
    """
    return 'TODO'

def download_image_from_url(image_url):
    """
    Downloads an image from a specified URL.
    ** DOES NOT SAVE THE IMAGE TO DISK **

    :param image_url: URL of image
    :returns: Image data binary string (content of response message)
    """
    return 'TODO'

def save_image_file(image_data, image_path):
    """
    Saves image data as a file on disk.
    ** DOES NOT DOWNLOAD THE IMAGE **

    :param image_data: Image data binary string
    :param image_path: Path to save image file
    :returns: None
    """
    return # TODO

def set_desktop_background_image(image_path):
    """
    Changes the desktop wallpaper to a specific image.

    :param image_path: Path of image file
    :returns: None
    """
    return # TODO

main()