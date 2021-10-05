from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import random
import sys
import os


def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore


def enablePrint():
    sys.stdout = sys.__stdout__


class SpamBot:
    def __init__(self, proxy=None, headless=False):
        self.proxy = proxy
        self.headless = headless

    def login(self, username, password):
        """Logs to your profile and saves the cookies to send messages without
        accessing your profile every time."""
        blockPrint()
        cookies, result = self._login(username, password)
        enablePrint()
        if result:
            self.cookies = cookies
            print("Logged in correctly.")
        else:
            Exception("Error while logging in.")

    def _login(self, username, password):
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
            if self.headless:
                break
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

    def send(self, user, message):
        """Sends an Instagram DM."""
        if not hasattr(self, 'cookies'):
            print("We require logging in to continue.")
            username = input("Username: ")
            password = input("Password: ")
            self.login(username, password)
        blockPrint()
        result = self._send(user, message)
        enablePrint()
        if result:
            print("DM sended correctly.")
        else:
            print("DM not sent. There was an issue while sending. Try again later.")

    def _send(self, user, message):
        opts = Options()
        if self.proxy is not None:
            opts.add_argument('--proxy-server=%s' % self.proxy)
        opts.headless = self.headless
        opts.add_argument(
            "user-agent=%s" % 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0')
        browser = webdriver.Chrome(
            ChromeDriverManager().install(), options=opts)
        browser.get("https://www.instagram.com")
        try:
            for cookie in self.cookies:
                browser.add_cookie(cookie)
        except:
            browser.quit()
            return False
        browser.get("https://www.instagram.com/direct/new/")
        lock = False
        if not self.headless:
            for j in range(20):
                btns = browser.find_elements_by_tag_name("button")
                for btn in btns:
                    if "Not Now" in btn.text:
                        btn.click()
                        lock = True
                        break
                if lock:
                    break
                else:
                    time.sleep(0.5)
            else:
                browser.quit()
                return False
        browser.find_element_by_name("queryBox").send_keys(user)
        lock = False
        for j in range(20):
            svgs = browser.find_elements_by_tag_name("svg")
            for svg in svgs:
                if "Toggle selection" in svg.get_attribute("aria-label"):
                    svg.click()
                    lock = True
                    break
            if lock:
                break
            else:
                time.sleep(0.5)
        else:
            browser.quit()
            return False
        btns = browser.find_elements_by_tag_name("button")
        for btn in btns:
            try:
                if btn.text.find("Next") != -1:
                    btn.click()
                    break
            except:
                pass
        else:
            browser.quit()
            return False
        old = browser.current_url
        for j in range(10):
            if old == browser.current_url:
                time.sleep(1)
            else:
                break
        else:
            browser.quit()
            return False
        ta = browser.find_element_by_xpath(
            "//textarea[@placeholder='Message...']")
        ta.send_keys(message)
        btns = browser.find_elements_by_tag_name("button")
        for btn in btns:
            try:
                if btn.text.find("Send") != -1:
                    btn.click()
                    break
            except:
                pass
        else:
            browser.quit()
            return False
        time.sleep(3)
        browser.quit()
        return True

    def send_multiple(self, users, message):
        """Sends multiple DMs at a random time distance between 1 and 5 minutes. Advised only for short lists."""
        for user in users:
            self.send(user, message)
            time.sleep(random.randint(60, 300))


class Bot:
    def __init__(self, proxy=None, headless=False):
        self.proxy = proxy
        self.headless = headless

    def login(self, username, password):
        """Logs to your profile and saves the cookies to send messages without
        accessing your profile every time."""
        blockPrint()
        cookies, result = self._login(username, password)
        enablePrint()
        if result:
            self.cookies = cookies
            print("Logged in correctly.")
        else:
            Exception("Error while logging in.")

    def _login(self, username, password):
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
        if not self.headless:
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
        blockPrint()
        result = self._like(link)
        enablePrint()
        if result:
            print("Post liked correctly.")
        else:
            print("Error while trying to like the post.")

    def _like(self, link):
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
        blockPrint()
        result = self._follow("https://www.instagram.com/"+username)
        enablePrint()
        if result:
            print("User followed correctly.")
        else:
            print("Error while following the user.")

    def _follow(self, link):
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
