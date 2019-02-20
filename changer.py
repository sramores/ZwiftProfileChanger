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
import ast


def setup():

    driver_location = 'D:/webdriver/chromedriver.exe'

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    
    return webdriver.Chrome(executable_path=driver_location, chrome_options=options)


def load_json():
    with open('data.json') as json_file:
        return json.load(json_file)


def main():
    profile = sys.argv[1]
    print("Load", profile, "profile.")

    login(data['email'], data['password'])
    change_profile(data['profiles'][profile])
    connection(data['profiles'][profile]['connections'])
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

    #assert()
    # TODO Assert Login


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

    driver.find_element_by_xpath("/html/body/my-zwift/profile-component/div/div/div[2]/settings-general-component/div[2]/form/div[8]/div/button").click()


def connection(connections):
    print("Connection page.")

    driver.execute_script("window.scrollTo(0, 0);")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "settings-profile-connections"))).click()

    for connection in connections:
        try:
            connection_name = connection
            globals()[connection_name](connections[connection_name]['username'], connections[connection_name]['password'])
        
        except KeyError:
            print("Connection %s not defined." % (connection))


def Garmin(userData, passData):
    disconnection("garmin-disconnection-button")

    print("Garmin connection page.")

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "garmin-partner-connection")))

    garmin_connection_button = driver.find_element_by_id("garmin-connection-button")
    ActionChains(driver).move_to_element(garmin_connection_button).click(garmin_connection_button).perform()

    driver.switch_to.default_content()
    driver.switch_to.frame("gauth-widget-frame-gauth-component")

    username = driver.find_element_by_id("username")
    username.clear()
    username.send_keys(userData)

    password = driver.find_element_by_id("password")
    password.clear()
    password.send_keys(passData)
    password.send_keys(Keys.RETURN)

    driver.switch_to.default_content()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "authorize-group")))
    auth_button = driver.find_element_by_id("auth-app-gdpr")
    ActionChains(driver).move_to_element(auth_button).perform()
    auth_button.click()



def Strava(userData, passData):
    disconnection("strava-disconnection-button")

    print("Strava connection page.")

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "strava-partner-connection")))

    strava_connection_button = driver.find_element_by_id("strava-connection-button")
    ActionChains(driver).move_to_element(strava_connection_button).click(strava_connection_button).perform()

    #driver.switch_to.default_content()
    #driver.switch_to.frame("gauth-widget-frame-gauth-component")

    username = driver.find_element_by_id("email")
    username.clear()
    username.send_keys(userData)

    password = driver.find_element_by_id("password")
    password.clear()
    password.send_keys(passData)
    password.send_keys(Keys.RETURN)

    driver.switch_to.default_content()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "authorize")))
    auth_button = driver.find_element_by_id("authorize")
    ActionChains(driver).move_to_element(auth_button).perform()
    auth_button.click()

def TrainingPeaks(userData, passData):
    disconnection("trainingpeaks-disconnection-button")

    print("TrainingPeaks connection page.")


def disconnection(button):

    try:
        button = driver.find_element_by_id(button)
        if button.is_displayed():
            actions = ActionChains(driver)
            actions.move_to_element(button).perform()
            button.click()

    except NoSuchElementException:
        return False
    
    return True


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




