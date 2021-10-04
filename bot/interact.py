from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time


class Bot:
    def __init__(self, proxy=None, headless=False):
        self.proxy = proxy
        self.headless = headless

    def login(self, username, password):
        """Logs to your profile and saves the cookies to send messages without
        accessing your profile every time."""

        cookies, result = self.__login(username, password)
        if result:
            self.cookies = cookies
            print("Logged in correctly.")
        else:
            Exception("Error while logging in.")

    def __login(self, username, password):
        """A specific method for advanced users, that returns the cookies to let you handle
        them yourself."""
        opts = Options()
        if self.proxy is not None:
            opts.add_argument('--proxy-server=%s' % self.proxy)
        opts.headless = self.headless
        browser = webdriver.Chrome(
            ChromeDriverManager().install(), options=opts)
        try:
            browser.get("https://www.instagram.com")
        except:
            browser.quit()
            return None, False
        btns = browser.find_elements_by_tag_name("button")
        for btn in btns:
            if "Accept All" in btn.text:
                btn.click()
                break
        else:
            browser.quit()
            return None, False
        for j in range(10):
            try:
                browser.find_element_by_name("username").send_keys(username)
            except:
                time.sleep(0.5)
            else:
                break
        else:
            browser.quit()
            return None, False
        browser.find_element_by_name("password").send_keys(password)
        for j in range(10):
            try:
                browser.find_element_by_xpath(
                    "//button[@type='submit']").click()
            except:
                time.sleep(0.5)
            else:
                break
        else:
            browser.quit()
            return None, False
        old = browser.current_url
        for j in range(10):
            if old == browser.current_url:
                time.sleep(1)
            else:
                cookies = browser.get_cookies()
                browser.quit()
                return cookies, True
        else:
            browser.quit()
            return None, False

    def like(self, link):
        """Like an Instagram post."""
        if not hasattr(self, 'cookies'):
            print("We require logging in to continue.")
            username = input("Username: ")
            password = input("Password: ")
            self.login(username, password)
        result = self.__like(link)
        if result:
            print("Post liked correctly.")
        else:
            print("Error while trying to like the post.")

    def __like(self, link):
        """A more specific method that lets you handle yourself the result
        of the like attempt."""
        opts = Options()
        if self.proxy is not None:
            opts.add_argument('--proxy-server=%s' % self.proxy)
        opts.headless = self.headless
        browser = webdriver.Chrome(
            ChromeDriverManager().install(), options=opts)
        browser.get("https://www.instagram.com")
        for cookie in self.cookies:
            browser.add_cookie(cookie)
        try:
            browser.get(link)
        except:
            browser.quit()
            return False
        done = False
        for i in range(5):
            svgs = browser.find_elements_by_tag_name("svg")
            for svg in svgs:
                try:
                    if "Like" in svg.get_attribute("aria-label") and svg.get_attribute("height") == "24":
                        svg.click()
                        done = True
                        break
                except:
                    pass
            else:
                time.sleep(0.5)
        if done:
            browser.quit()
            return True
        browser.quit()
        return False

    def follow(self, username):
        if not hasattr(self, 'cookies'):
            print("We require logging in to continue.")
            username = input("Username: ")
            password = input("Password: ")
            self.login(username, password)
        result = self.__follow("https://www.instagram.com/"+username)
        if result:
            print("User followed correctly.")
        else:
            print("Error while following the user.")

    def __follow(self, link):
        opts = Options()
        opts.headless = self.headless
        if self.proxy is not None:
            opts.add_argument('--proxy-server=%s' % self.proxy)
        browser = webdriver.Chrome(
            ChromeDriverManager().install(), options=opts)
        try:
            browser.get("https://www.instagram.com")
        except:
            browser.quit()
            return False
        for cookie in self.cookies:
            browser.add_cookie(cookie)
        try:
            browser.get(link)
        except:
            browser.quit()
            return False
        for i in range(10):
            btns = browser.find_elements_by_tag_name("button")
            lock = False
            for btn in btns:
                if "Follow" in btn.text:
                    lock = True
                    btn.click()
                    break
            else:
                time.sleep(0.5)
            if lock:
                break
        else:
            browser.quit()
            return False
        browser.quit()
        return True
