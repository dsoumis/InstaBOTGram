import os
import urllib.request
from _socket import timeout
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


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
        login_element_xpath = "/html/body/div[1]/section/main/article/div[2]/div[2]/p/a"
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

    def __init__(self, username, password, type_of_login, browser='f'):
        if browser == 'f':
            self.driver = webdriver.Firefox()
        else:
            self.driver = webdriver.Chrome()  # Chrome has not been tested
        self.driver.get("https://www.instagram.com")
        if type_of_login != "F":
            self.__not_facebook_login(username, password)
        else:
            self.__facebook_login(username, password)

        # Presses not now to first popup window of Instagram
        self.__disable_notifications_popup_window()

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
            return not_following_back
        except timeout:
            print("Timeout profile path")

    def unfollow_user(self, user):
        # Navigate to user's page
        self.driver.get("https://www.instagram.com/{}/".format(user))
        try:
            # Check that we are on user's page
            WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, "//h1[contains(text(), '{}')]".format(user)))
            )
            # Click following button
            WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button"))
            ).click()
            # Click unfollow
            WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, "/html/body/div[4]/div/div/div[3]/button[1]"))
            ).click()
        except Exception:
            print(Exception)

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

    def get_followers_from_liking_hashtags(self, hashtag):
        self.driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        # Check that we are on hashtag's page
        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/section/main/header/div[2]/div[1]/div[1]/h1"))
        )
        images = []
        images.extend(self.driver.find_elements_by_class_name('_9AhH0'))

        for image in images[:30]:
            print(image)
            image.click()
            try:
                # Click like button
                WebDriverWait(self.driver, 1).until(
                    expected_conditions.presence_of_element_located(
                        (By.XPATH, "//span[contains(@class, 'fr66n')]//*[@fill='#262626']"))
                ).click()
            except Exception:
                # Click close button
                self.driver.find_elements_by_class_name('ckWGn')[0].click()
                # Check that we are on hashtag's page
                WebDriverWait(self.driver, 10).until(
                    expected_conditions.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/section/main/header/div[2]/div[1]/div[1]/h1"))
                )
                continue

            # Click close button
            self.driver.find_elements_by_class_name('ckWGn')[0].click()
            # Check that we are on hashtag's page
            WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/section/main/header/div[2]/div[1]/div[1]/h1"))
            )

    def like_latest_posts(self, user, number_of_posts):

        # Likes a number of a users latest posts, specified by number_of_posts.

        # Navigate to user's page
        self.driver.get("https://www.instagram.com/{}/".format(user))
        try:
            # Check that we are on user's page
            WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, "//h1[contains(text(), '{}')]".format(user)))
            )
            images = []
            last_height = 0
            height = 1
            while last_height != height:
                last_height = height
                sleep(1)
                height = self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);"
                                                    "return document.body.scrollHeight;")

                images.extend(self.driver.find_elements_by_class_name('_9AhH0'))
            images = list(set(images))  # clean up duplicates

            unique_photos = len(images)
            print("{} len is ".format(unique_photos))
            if unique_photos < number_of_posts:
                number_of_posts = unique_photos
            for image in images[:number_of_posts]:
                print(image)
                image.click()
                try:
                    # Click like button
                    WebDriverWait(self.driver, 1).until(
                        expected_conditions.presence_of_element_located(
                            (By.XPATH, "//span[contains(@class, 'fr66n')]//*[@fill='#262626']"))
                    ).click()
                except Exception:
                    # Click close button
                    self.driver.find_elements_by_class_name('ckWGn')[0].click()
                    # Check that we are on user's page
                    WebDriverWait(self.driver, 10).until(
                        expected_conditions.presence_of_element_located(
                            (By.XPATH, "//h1[contains(text(), '{}')]".format(user)))
                    )
                    continue

                # Click close button
                self.driver.find_elements_by_class_name('ckWGn')[0].click()
                # Check that we are on user's page
                WebDriverWait(self.driver, 10).until(
                    expected_conditions.presence_of_element_located(
                        (By.XPATH, "//h1[contains(text(), '{}')]".format(user)))
                )
        except Exception:
            print(Exception)

    def terminate(self):
        self.driver.quit()


if __name__ == '__main__':
    """
    The main function called when bot.py is run from the command line

    >Execute: python3.7 bot.py
    """
    print("~~~Welcome to InstaBOTGram. "
          "A bot which tampers with your instagram account and provides you with many functionalities.~~~")
    print("\n!!!Creator of this application, Dimitris Soumis, does not take any responsibillity of potential harms "
          "that user's actions through this application may cause.!!!")
    print("\n~~~Please provide your Instagram type of login. "
          "If you login through Facebook prees 'F' and 'ENTER'. "
          "Otherwise just press 'ENTER'.~~~")
    type_of_logino = input('Type of login: ')
    if type_of_logino == 'f' or type_of_logino == 'F':
        type_of_logino = "F"
    else:
        type_of_logino = "NF"
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear terminal
    if type_of_logino == "F":
        print("\nPlease provide your Facebook e-mail/phone and password "
              "(The values which you use to login into Facebook). "
              "\n\n!!!InstaBOTGram does not save this data and your personal information is totally protected.!!!\n"
              )
        usernameo = input('E-mail/Phone: ')
        passwordo = input('Password: ')
    else:
        print("\nPlease provide your Instagram username and password "
              "(The values which you use to login into Instagram). "
              "\n\n!!!InstaBOTGram does not save this data and your personal information is totally protected.!!!\n"
              )
        usernameo = input('Username: ')
        passwordo = input('Password: ')
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear terminal
    print("\nPlease select your browser. Press 'c' and 'ENTER' for Chrome or 'f' and 'ENTER' for Firefox.")
    browsero = input('Browser: ')
    if browsero == 'f' or browsero == 'F':
        browsero = 'f'
    else:
        browsero = 'c'
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear terminal
    print("~~~InstaBOTGram is loading. "
          "Please don't press anything on the newly opened browser as the bot does everything automatically."
          "Just sit back and enjoy :)~~~")
    input('Press ENTER to validate that you have read this message.')
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear terminal
    temp = InstaBOTGram(usernameo, passwordo, type_of_logino, browsero)
    print("~~~Choose what InstaBOTGram should do for you.~~~")
    print("Press a number from the menu and 'ENTER' for an action to take place.")
    while 1:
        print("MENU:\n"
              "1.See who's not following you back."
              "2.Download all images of a user."  # TODO: Test what happens if profile is locked
              "3.Get NEW Followers."
              "4.Spam a user with likes."
              "5.Exit InstaBOTGram")
        action = input('Give a number from above and press ENTER: ')
        while 1:
            if action == 1 or action == 2 or action == 3 or action == 4 or action == 5:
                break
            action = input('No such number. Give a number from the MENU: ')
        if action == 1:
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear terminal
            not_following_backo = temp.get_unfollowers()
            print("Not following you back: {}".format(not_following_backo))
            print("{} users are not following you back.".format(len(not_following_backo)))
            print("Do you want to unfollow these users? Press 'y' and 'ENTER' for yes or 'n' and 'ENTER' for no.")
            while 1:
                answer = input('Y/N: ')
                if answer == 'y' or answer == 'Y' or answer == 'n' or answer == 'N':
                    break
            if answer == 'y' or answer == 'Y':
                for usern in not_following_backo:
                    temp.unfollow_user(usern)
                print('You successfully unfollowed those users.')
        elif action == 2:
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear terminal
            print('Give the username of the user that you want to download pictures from.')
            user2 = input('Username: ')
            temp.download_user_images(user2)
        elif action == 3:
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear terminal
            print('!!!This actions means that your account !likes! a couple of pictures with specific hashtags.!!!')
            print("Do you accept? Press 'y' and 'ENTER' for yes or 'n' and 'ENTER' for no.")
            while 1:
                answer = input('Y/N: ')
                if answer == 'y' or answer == 'Y' or answer == 'n' or answer == 'N':
                    break
            if answer == 'y' or answer == 'Y':
                print('Write three of your favourite hashtags.')
                hashtag1 = input('Hashtag 1: ')
                hashtag2 = input('Hashtag 2: ')
                hashtag3 = input('Hashtag 3: ')
                temp.get_followers_from_liking_hashtags(hashtag1)
                temp.get_followers_from_liking_hashtags(hashtag2)
                temp.get_followers_from_liking_hashtags(hashtag3)
        elif action == 4:
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear terminal
            print('Give the username of the user that you want to spam with likes.')
            user4 = input('Username: ')
            print('How many photos do you want InstaBOTGram to like? (Write number and press \'ENTER\'')
            how_many = input('Number: ')
            temp.like_latest_posts(user4, how_many)
        elif action == 5:
            temp.terminate()
            break
