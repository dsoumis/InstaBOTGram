import os
import urllib.request
from _socket import timeout
from time import sleep

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


class InstaBOTGram:
    def __facebook_login(self, username, password):
        facebook_login_element_xpath = "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[1]/button"
        # WebDriverWait is used for the app to wait max 10 seconds to make sure that the page is fully loaded.
        # If more than 10 seconds and no response throws timeout exception
        try:
            # Finds and clicks Log In with Facebook
            WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located((By.XPATH, facebook_login_element_xpath))
            ).click()

            try:
                # Writes username in field
                WebDriverWait(self.driver, 10).until(
                    expected_conditions.presence_of_element_located((By.XPATH, "//input[@name=\"email\"]"))
                ).send_keys(username)

                # Writes password in field
                # No need to wait password will be there if username is already there
                self.driver.find_element_by_xpath("//input[@name=\"pass\"]").send_keys(password)

                # Click login button
                # No need to wait
                self.driver.find_element_by_xpath("//*[@id=\"loginbutton\"]").click()

            except timeout:
                print("Timeout facebookuserfield")
        except timeout:
            print("Timeout facebookloginelement")

    def __not_facebook_login(self, username, password):
        login_element_xpath = "/html/body/div[1]/section/main/article/div[2]/div[2]/p/a"  # or ="//a[contains(text(), 'Log in')]"
        # WebDriverWait is used for the app to wait max 10 seconds to make sure that the page is fully loaded.
        # If more than 10 seconds and no response throws timeout exception
        try:
            # Finds and clicks Log In
            WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located((By.XPATH, login_element_xpath))
            ).click()

            try:
                # Writes username in field
                WebDriverWait(self.driver, 10).until(
                    expected_conditions.presence_of_element_located((By.XPATH, "//input[@name=\"username\"]"))
                ).send_keys(username)

                # Writes password in field
                # No need to wait password will be there if username is already there
                self.driver.find_element_by_xpath("//input[@name=\"password\"]").send_keys(password)

                # Click login button
                # No need to wait
                self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div"
                                                  "/article/div/div[1]/div/form/div[4]/button").click()

            except timeout:
                print("Timeout userfield")
        except timeout:
            print("Timeout loginelement")

    def __disable_notifications_popup_window(self):
        try:
            WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, "/html/body/div[4]/div/div/div[3]/button[2]"))
            ).click()
        except Exception:
            try:
                WebDriverWait(self.driver, 10).until(
                    expected_conditions.presence_of_element_located(
                        (By.XPATH, "/html/body/div[3]/div/div/div[3]/button[2]"))
                ).click()
            except Exception:
                print("Timeout notifications popup window")

    def __init__(self, username, password, type_of_login):
        self.driver = webdriver.Firefox()
        self.driver.get("https://www.instagram.com")
        if type_of_login != "F":
            self.__not_facebook_login(username, password)
        else:
            self.__facebook_login(username, password)

        # Presses not now to first popup window of Instagram
        self.__disable_notifications_popup_window()

        #self.driver.quit()

    def __following(self):
        # Click following
        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, "//a[contains(@href, '/following')]"))
        ).click()

        # Wait till following list is shown by checking the existence of hashtag list
        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, "//a[contains(@href, '/hashtag_following')]"))
        )

        try:
            # Scroll the following list
            scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")
        except Exception:
            # Scroll the following list
            scroll_box = self.driver.find_element_by_xpath("/html/body/div[3]/div/div[2]")
        last_height, height = 0, 1
        # Because instagram doesn't load the whole list at once, but buffers as scrolling down fast we use sleep
        # in order to have time to get buffered and load the persons in the list.
        while last_height != height:
            last_height = height
            sleep(1)
            height = self.driver.execute_script("arguments[0].scrollTo(0,arguments[0].scrollHeight);"
                                                "return arguments[0].scrollHeight;", scroll_box)

        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        try:
            self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button").click()
        except Exception:
            self.driver.find_element_by_xpath("/html/body/div[3]/div/div[1]/div/div[2]/button").click()
        return names

    def __followers(self):
        # Click followers
        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, "//a[contains(@href, '/followers')]"))
        ).click()

        try:
            # Wait till followers list is shown by checking the existence of x button
            WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, "/html/body/div[4]/div/div[1]/div/div[2]/button"))
            )
        except Exception:
            WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, "/html/body/div[3]/div/div[1]/div/div[2]/button"))
            )

        try:
            # Scroll the followers list
            scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")
        except Exception:
            # Scroll the followers list
            scroll_box = self.driver.find_element_by_xpath("/html/body/div[3]/div/div[2]")
        last_height, height = 0, 1
        # Because instagram doesn't load the whole list at once, but buffers as scrolling down fast we use sleep
        # in order to have time to get buffered and load the persons in the list.
        while last_height != height:
            last_height = height
            sleep(1)
            height = self.driver.execute_script("arguments[0].scrollTo(0,arguments[0].scrollHeight);"
                                                "return arguments[0].scrollHeight;", scroll_box)

        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        try:
            self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button").click()
        except Exception:
            self.driver.find_element_by_xpath("/html/body/div[3]/div/div[1]/div/div[2]/button").click()
        return names

    def get_unfollowers(self):
        try:
            # Click profile icon left of username
            WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/section/main/section/div[3]/div[1]/div/div[1]"))
            ).click()
            followers = self.__followers()
            following = self.__following()

            not_following_back = [user for user in following if user not in followers]
            print(not_following_back)
            print(len(not_following_back))
        except timeout:
            print("Timeout profile path")

    def download_user_images(self, user):
        # Downloads all images from a users profile.

        self.driver.get("https://www.instagram.com/{}/".format(user))

        img_srcs = []
        last_height = 0
        height = 1
        while last_height != height:
            last_height = height
            sleep(1)
            height = self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);"
                                                "return document.body.scrollHeight;")

            img_srcs.extend(
                [img.get_attribute('src') for img in self.driver.find_elements_by_class_name('FFVAD')])  # scrape srcs

        img_srcs = list(set(img_srcs))  # clean up duplicates

        for idx, src in enumerate(img_srcs):
            # Creates a folder named after a user to to store the image, then downloads the image to the folder.

            folder_path = './{}'.format(user)
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)

            img_filename = 'image_{}.jpg'.format(idx)
            urllib.request.urlretrieve(src, '{}/{}'.format(user, img_filename))


if __name__ == '__main__':
    """
    The main function called when predict.py is run from the command line

    >Execute: python3.7 predict.py -i path_to:nn_representations.csv -m path_to:WindDenseNN.h5 -a path_to:actual.csv
    """
    temp = InstaBOTGram(, , "F")
    #temp.get_unfollowers()
    temp.download_user_images("dimitris_soumis")
