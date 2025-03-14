#!/usr/bin/python3
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class session_get:
    def __init__(self, url):
        self.url = url
        self.browser = self._init_browser()
    
    def _init_browser(self):
        # 다양한 User-Agent 리스트
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36",
        ]
        random_user_agent = random.choice(user_agents)

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument(f"user-agent={random_user_agent}")
        
        browser = webdriver.Chrome(options=options)
        browser.get(self.url)
        return browser
    
    def get_browser(self): # 객체 반환
        return self.browser

    def close(self): # 브라우저 종료
        if self.browser:
            self.browser.quit()
            self.browser = None # 객체 초기화
