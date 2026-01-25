import time
import json
import random
import pickle
import os
import shutil
import tempfile

from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def get_random_delay(start, end):
    return random.choice([start, end])


def wait_with_random_delay(start, end):
    random_delay = random.choice([start, end])
    time.sleep(random_delay)


def get_page_soup(driver):
    return BeautifulSoup(driver.page_source, "html5lib")


def save_to_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f)

def load_cookies_in_driver_before_site_load(driver, cookies_pkl_file):
    cookies = pickle.load(open(cookies_pkl_file, "rb"))

    # Enables network tracking so we may use Network.setCookie method
    driver.execute_cdp_cmd("Network.enable", {})

    for cookie in cookies:
        expiry = cookie.get("expiry", None)

        if expiry:
            cookie["expiry"] = int(expiry * 1000)

        # Replace domain 'apple.com' with 'microsoft.com' cookies
        # cookie['domain'] = cookie['domain'].replace('apple.com', 'microsoft.com')

        # Set the actual cookie
        driver.execute_cdp_cmd("Network.setCookie", cookie)

    # Disable network tracking
    driver.execute_cdp_cmd("Network.disable", {})


def load_cookies_in_driver(
        driver,
        cookies_pkl_file,
):
    for cookie in pickle.load(open(cookies_pkl_file, "rb")):
        expiry = cookie.get("expiry", None)

        if expiry:
            cookie["expiry"] = int(expiry * 1000)
        driver.add_cookie(cookie)


def save_cookies(cookies_pkl_file, cookies_data):
    pickle.dump(cookies_data, open(cookies_pkl_file, "wb"))


def remove_temp_folders():
    # path = "C:/Users/ADMINI~1/AppData/Local/Temp/2"
    path = str(tempfile.gettempdir()).replace("\\", "/")
    # Check if the given path exists
    if os.path.exists(path):
        # Iterate over all items in the directory
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            # Check if the item is a directory
            if os.path.isdir(item_path):
                try:
                    # Remove the directory and all its contents
                    shutil.rmtree(item_path)
                    print(f"Successfully removed the directory: {item_path}")
                except Exception as e:
                    # pass
                    print(f"Error removing directory {item_path}: {str(e)}")
            else:
                print(f"{item_path} is not a directory, skipping.")
    else:
        print(f"Error: The path {path} does not exist.")


def delete_old_files_by_name(folder_path, days=7):
    # Calculate the cutoff date
    cutoff_date = datetime.now() - timedelta(days=days)

    # Loop through all files in the specified folder
    for filename in os.listdir(folder_path):
        # Check if the file name matches the date format
        try:
            file_date = datetime.strptime(filename[:10], "%Y-%m-%d")
        except ValueError:
            # Skip files that don't follow the YYYY-MM-DD.txt format
            continue

        # Delete the file if its date is older than the cutoff date
        if file_date < cutoff_date:
            file_path = os.path.join(folder_path, filename)

            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")


def generate_log(directory_name, data):
    # Format the date and time for use in a file name
    log_filename_date = datetime.now().strftime("%Y-%m-%d")

    # Format the date and time for use in a file name
    if not os.path.exists(f'ZkekeLogs/{directory_name}'):
        os.makedirs(f'ZkekeLogs/{directory_name}')

    # Get current date and time
    with open(f'ZkekeLogs/{directory_name}/{log_filename_date}.txt', 'a', encoding="utf-8") as f:
        # Write some content to the file
        f.write(str(data) + '\n')

    # # it will delete files older then 7 days
    # delete_old_files_by_name(f'ScrapperLogs/{directory_name}')
