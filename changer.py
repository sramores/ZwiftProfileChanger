import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import sys


def setup():
    driver_location = "/opt/selenium/chromedriver"
    options = Options()
    options.add_argument("--start-maximized")
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')

    return webdriver.Chrome(driver_location, options=options)


def load_json():
    with open('data.json') as json_file:
        return json.load(json_file)


def main():
    profile = sys.argv[1]
    print("Load", profile, "profile.")

    login(data['email'], data['password'])
    change_profile(data['profiles'][profile])
    connection(data['profiles'][profile]['user'], data['profiles'][profile]['password'])
    close()


def login(email, password):
    print("Login page.")

    driver.get("https://my.zwift.com/profile/edit")

    ema = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "username")))
    ema.clear()
    ema.send_keys(email)

    psw = driver.find_element_by_id("password")
    psw.clear()
    psw.send_keys(password)
    psw.send_keys(Keys.RETURN)


def change_profile(profile):
    print("Edit profile page.")

    first_name = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "firstName")))
    first_name.clear()
    first_name.send_keys(profile['firstName'])

    last_name = driver.find_element_by_id("lastName")
    last_name.clear()
    last_name.send_keys(profile['lastName'])

    if profile['gender'] == 'Male':
        driver.find_element_by_xpath("/html/body/my-zwift/profile-component/div/div/div[2]/settings-general-component/div[2]/form/div[2]/div/label[1]/span[1]").click()
    elif profile['gender'] == 'Female':
        driver.find_element_by_xpath("/html/body/my-zwift/profile-component/div/div/div[2]/settings-general-component/div[2]/form/div[2]/div/label[2]/span[1]").click()

    flag = Select(driver.find_element_by_id("flag"))
    flag.select_by_visible_text(profile['flag'])

    metricHeight = driver.find_element_by_id("metricHeight")
    metricHeight.clear()
    metricHeight.send_keys(profile['height'])

    metricWeight = driver.find_element_by_id("metricWeight")
    metricWeight.clear()
    metricWeight.send_keys(profile['weight'])

    driver.find_element_by_xpath("/html/body/my-zwift/profile-component/div/div/div[2]/settings-general-component/div[2]/form/div[7]/div/button").click()


def garmin_connect(usr, psw):
    print("Garmin Connect.")

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "garmin-connection-button")))

    garmin_connection_button = driver.find_element_by_id("garmin-connection-button")
    ActionChains(driver).move_to_element(garmin_connection_button).click(garmin_connection_button).perform()

    driver.switch_to.default_content()
    driver.switch_to.frame("gauth-widget-frame-gauth-component")

    username = driver.find_element_by_id("username")
    username.clear()
    username.send_keys(usr)

    password = driver.find_element_by_id("password")
    password.clear()
    password.send_keys(psw)
    password.send_keys(Keys.RETURN)

    driver.switch_to.default_content()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "authorize-group")))
    auth_button = driver.find_element_by_id("auth-app-gdpr")
    ActionChains(driver).move_to_element(auth_button).perform()
    auth_button.click()


def connection(user, password):
    print("Connection page.")

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "settings-profile-connections"))).click()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # TODO Add all connections
    try:
        if driver.find_element_by_id("garmin-disconnection-button").is_displayed():
            driver.find_element_by_id("garmin-disconnection-button").click()
            garmin_connect(user, password)

    except NoSuchElementException:
        garmin_connect(user, password)


def close():
    print("Exit Zwift page.")
    driver.close()


if __name__ == "__main__":
    if len(sys.argv[1:]) > 0:
        driver = setup()
        data = load_json()
        main()
    else:
        print("Configuration Error! Missing Parameter.")


