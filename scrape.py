import os

import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from credential import userName, password
from count import count
import time

count = count

class IG_Scraper:
    def __init__(self, inputUserName="", inputPassword=""):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

        if inputUserName != "" and inputPassword != "":
            self.userName = inputUserName
            self.password = inputPassword
        else:
            self.userName = userName
            self.password = password

        self.checked = []
        self.count = 0
        self.folder_name = userName

        self.duplicates_found = 0
        self.allowed_duplicates = 200

        self.driver.get('https://instagram.com')
        time.sleep(4)
        # Input Username

        self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(self.userName)
        # Input Password

        self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(self.password)
        # Click Login

        self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button').click()
        time.sleep(4)

        # Deny remember login info
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
        time.sleep(4)

        # Don't show notifications
        self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[2]').click()
        time.sleep(2)

    def all_saved(self):
        time.sleep(4)
        # Click on profile
        # self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]/span/img').click()
        # self.driver.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[6]/span').click()
        self.driver.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[6]/span').click()
        time.sleep(2)
        # Click on 'Saved'
        # self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]/div[2]/div[2]/div[2]/a[2]/div').click()
        self.driver.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[6]/div[2]/div[2]/div[2]/a[2]/div').click()
        time.sleep(4)
        # Click on 'All Posts'
        self.driver.find_element_by_css_selector('div.Nt8m2').click()
        # self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[3]/div[2]/div/div/div[1]/div/div').click()
        time.sleep(4)

    def has_duplicate(self, file_name):
        files = os.listdir(self.folder_name)
        return file_name in files

    def is_checked(self, file_name):
        return file_name in self.checked

    def download(self):
        global count

        try:
            if not os.path.exists(self.folder_name):
                os.makedirs(self.folder_name)

            path = os.getcwd()
            path = os.path.join(path, self.folder_name)

            images = self.driver.find_elements_by_class_name("FFVAD")
            # images = self.driver.find_elements_by_tag_name('img')
            picture_name_list = [image.get_attribute('alt') for image in images]
            images = [image.get_attribute('srcset') for image in images]

            # Take only first link (highest resolution link)
            for i in range(len(images)):

                images[i] = images[i].split(" ")
                images[i] = images[i][0]
                if picture_name_list[i] != "":
                    # Sanitize String
                    picture_name_list[i] = picture_name_list[i].replace("\n", "")
                    picture_name_list[i] = picture_name_list[i].replace("#", "")
                    picture_name_list[i] = picture_name_list[i].replace("%", "")
                    picture_name_list[i] = picture_name_list[i].replace("&", "")
                    picture_name_list[i] = picture_name_list[i].replace("{", "")
                    picture_name_list[i] = picture_name_list[i].replace("}", "")
                    picture_name_list[i] = picture_name_list[i].replace("\\", "")
                    picture_name_list[i] = picture_name_list[i].replace("<", "")
                    picture_name_list[i] = picture_name_list[i].replace(">", "")
                    picture_name_list[i] = picture_name_list[i].replace("*", "")
                    picture_name_list[i] = picture_name_list[i].replace("?", "")
                    picture_name_list[i] = picture_name_list[i].replace("/", "")
                    picture_name_list[i] = picture_name_list[i].replace("$", "")
                    picture_name_list[i] = picture_name_list[i].replace("!", "")
                    picture_name_list[i] = picture_name_list[i].replace("'", "")
                    picture_name_list[i] = picture_name_list[i].replace('"', "")
                    picture_name_list[i] = picture_name_list[i].replace(":", "")
                    picture_name_list[i] = picture_name_list[i].replace("@", "")
                    picture_name_list[i] = picture_name_list[i].replace("+", "")
                    picture_name_list[i] = picture_name_list[i].replace("`", "")
                    picture_name_list[i] = picture_name_list[i].replace("|", "")
                    picture_name_list[i] = picture_name_list[i].replace("=", "")
                    picture_name_list[i] = picture_name_list[i].replace(".", "")

                    string = ""
                    for c in picture_name_list[i]:
                        if c.isalnum():
                            string += c
                    picture_name_list[i] = string

                    picture_name_list[i] = picture_name_list[i].replace(" ", "_") + ".jpg"
                else:
                    """
                    picture_name_list[i] = str(self.count) + ".jpg"
                    self.count += 1
                    """
                    picture_name_list[i] = str(count) + ".jpg"
                    count += 1

            for counter in range(len(images)):
                url = images[counter]
                file_name = picture_name_list[counter]

                if not self.is_checked(file_name):
                    if self.has_duplicate(file_name):
                        self.duplicates_found += 1
                        print("Duplicates Found: " + str(self.duplicates_found))
                        print("Duplicate Name", file_name)
                        print(url)
                        if (self.duplicates_found >= self.allowed_duplicates):
                            return True
                    else:
                        response = requests.get(url)
                        file = open(self.folder_name + "/" + file_name, "wb")
                        file.write(response.content)
                        file.close()
                        self.checked.append(file_name)
            return False
        except:
            return False

    def automatic_scroll(self):
        self.download()
        lenOfPage = self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight); lenOfPage = document.body.scrollHeight; return lenOfPage;")
        match = False
        while not match:
            if self.download():
                return
            lastCount = lenOfPage
            # Wait for instagram to load
            time.sleep(4)
            lenOfPage = self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight); lenOfPage = document.body.scrollHeight; return lenOfPage;")
            if lastCount == lenOfPage or self.download():
                match = True



if __name__ == '__main__':
    # Create scraper object
    scrape = IG_Scraper()

    try:
        # Take all saved photos
        scrape.all_saved()
    except:
        print("Unable to go to all saved")
        pass

    # Download Images
    # scrape.download()

    # Automatic Scroll
    scrape.automatic_scroll()
    print(count)

    count_file = open("count.py", "w")
    count_file.write("count = " + str(count))

# Example picture: https://www.instagram.com/p/CMcdUvBDfiK/

"""
https://scontent-yyz1-1.cdninstagram.com/v/t51.2885-15/e35/p1080x1080/161019502_474326766931529_6965239171372591638_n.jpg?tp=1&_nc_ht=scontent-yyz1-1.cdninstagram.com&_nc_cat=1&_nc_ohc=GcInOHEFfIIAX_R5VB9&oh=8bf45325c627933b6e91bf0f968ebc72&oe=607A5CC4&ig_cache_key=MjUzMDAyNjA1NTE0NzUxNTk5Nw%3D%3D.2 1080w,
https://scontent-yyz1-1.cdninstagram.com/v/t51.2885-15/sh0.08/e35/p750x750/161019502_474326766931529_6965239171372591638_n.jpg?tp=1&_nc_ht=scontent-yyz1-1.cdninstagram.com&_nc_cat=1&_nc_ohc=GcInOHEFfIIAX_R5VB9&oh=46dd9d512be04d284e961a8ff36b5272&oe=60774543&ig_cache_key=MjUzMDAyNjA1NTE0NzUxNTk5Nw%3D%3D.2 750w,
https://scontent-yyz1-1.cdninstagram.com/v/t51.2885-15/sh0.08/e35/p640x640/161019502_474326766931529_6965239171372591638_n.jpg?tp=1&_nc_ht=scontent-yyz1-1.cdninstagram.com&_nc_cat=1&_nc_ohc=GcInOHEFfIIAX_R5VB9&oh=928931e79d92ebf711cc8154215427a5&oe=607A8287&ig_cache_key=MjUzMDAyNjA1NTE0NzUxNTk5Nw%3D%3D.2 640w,
https://scontent-yyz1-1.cdninstagram.com/v/t51.2885-15/e35/p480x480/161019502_474326766931529_6965239171372591638_n.jpg?tp=1&_nc_ht=scontent-yyz1-1.cdninstagram.com&_nc_cat=1&_nc_ohc=GcInOHEFfIIAX_R5VB9&oh=38aab0d0699a853391ff68f53469f8dd&oe=607816BD&ig_cache_key=MjUzMDAyNjA1NTE0NzUxNTk5Nw%3D%3D.2 480w,
https://scontent-yyz1-1.cdninstagram.com/v/t51.2885-15/e35/p320x320/161019502_474326766931529_6965239171372591638_n.jpg?tp=1&_nc_ht=scontent-yyz1-1.cdninstagram.com&_nc_cat=1&_nc_ohc=GcInOHEFfIIAX_R5VB9&oh=b8a042403764bfa72ffeafed2041a1fa&oe=6078D27C&ig_cache_key=MjUzMDAyNjA1NTE0NzUxNTk5Nw%3D%3D.2 320w,
https://scontent-yyz1-1.cdninstagram.com/v/t51.2885-15/e35/p240x240/161019502_474326766931529_6965239171372591638_n.jpg?tp=1&_nc_ht=scontent-yyz1-1.cdninstagram.com&_nc_cat=1&_nc_ohc=GcInOHEFfIIAX_R5VB9&oh=b1a984797aa61f0996b2ab3a315ddcf2&oe=60782B86&ig_cache_key=MjUzMDAyNjA1NTE0NzUxNTk5Nw%3D%3D.2 240w,
https://scontent-yyz1-1.cdninstagram.com/v/t51.2885-15/e35/c0.180.1440.1440a/s1080x1080/161019502_474326766931529_6965239171372591638_n.jpg?tp=1&_nc_ht=scontent-yyz1-1.cdninstagram.com&_nc_cat=1&_nc_ohc=GcInOHEFfIIAX_R5VB9&oh=737cd3f72caef11a044e3c161ced232d&oe=607A22AB&ig_cache_key=MjUzMDAyNjA1NTE0NzUxNTk5Nw%3D%3D.2 1080w,
https://scontent-yyz1-1.cdninstagram.com/v/t51.2885-15/sh0.08/e35/c0.180.1440.1440a/s750x750/161019502_474326766931529_6965239171372591638_n.jpg?tp=1&_nc_ht=scontent-yyz1-1.cdninstagram.com&_nc_cat=1&_nc_ohc=GcInOHEFfIIAX_R5VB9&oh=746cb3d63d6306d4cb2f2639469ebff7&oe=6077DF24&ig_cache_key=MjUzMDAyNjA1NTE0NzUxNTk5Nw%3D%3D.2 750w,
https://scontent-yyz1-1.cdninstagram.com/v/t51.2885-15/sh0.08/e35/c0.180.1440.1440a/s640x640/161019502_474326766931529_6965239171372591638_n.jpg?tp=1&_nc_ht=scontent-yyz1-1.cdninstagram.com&_nc_cat=1&_nc_ohc=GcInOHEFfIIAX_R5VB9&oh=7a4b614c2fb8e72d2c8e77f56bb7ceed&oe=60793F68&ig_cache_key=MjUzMDAyNjA1NTE0NzUxNTk5Nw%3D%3D.2 640w,
https://scontent-yyz1-1.cdninstagram.com/v/t51.2885-15/e35/c0.180.1440.1440a/s480x480/161019502_474326766931529_6965239171372591638_n.jpg?tp=1&_nc_ht=scontent-yyz1-1.cdninstagram.com&_nc_cat=1&_nc_ohc=GcInOHEFfIIAX_R5VB9&oh=3234f0eea74a2d0b2ad33d0fe7c3a950&oe=6078A269&ig_cache_key=MjUzMDAyNjA1NTE0NzUxNTk5Nw%3D%3D.2 480w,
https://scontent-yyz1-1.cdninstagram.com/v/t51.2885-15/e35/c0.180.1440.1440a/s320x320/161019502_474326766931529_6965239171372591638_n.jpg?tp=1&_nc_ht=scontent-yyz1-1.cdninstagram.com&_nc_cat=1&_nc_ohc=GcInOHEFfIIAX_R5VB9&oh=ccf140ae69b46d81298c1078439c63aa&oe=6077AFB0&ig_cache_key=MjUzMDAyNjA1NTE0NzUxNTk5Nw%3D%3D.2 320w,
https://scontent-yyz1-1.cdninstagram.com/v/t51.2885-15/e35/c0.180.1440.1440a/s240x240/161019502_474326766931529_6965239171372591638_n.jpg?tp=1&_nc_ht=scontent-yyz1-1.cdninstagram.com&_nc_cat=1&_nc_ohc=GcInOHEFfIIAX_R5VB9&oh=1744d1d75cdbd299575f1c5d3e1d5a45&oe=60775FD2&ig_cache_key=MjUzMDAyNjA1NTE0NzUxNTk5Nw%3D%3D.2 240w,
https://scontent-yyz1-1.cdninstagram.com/v/t51.2885-15/e35/c0.180.1440.1440a/s150x150/161019502_474326766931529_6965239171372591638_n.jpg?tp=1&_nc_ht=scontent-yyz1-1.cdninstagram.com&_nc_cat=1&_nc_ohc=GcInOHEFfIIAX_R5VB9&oh=a4fe880eeb478b76c627739b7cc19a75&oe=607737D8&ig_cache_key=MjUzMDAyNjA1NTE0NzUxNTk5Nw%3D%3D.2 150w
"""
