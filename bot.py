import time
import logging
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config import Config

class RollerCoinBot:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.driver = None
        self.last_run = None
        self.total_runs = 0
        self.error_count = 0
        self.current_action = 'Initializing'
        self.running = True

    def setup_driver(self):
        try:
            self.current_action = 'Setting up browser'
            options = Options()
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.binary_location = "/usr/bin/google-chrome"
            self.logger.info("Using Chrome binary at /usr/bin/google-chrome")

            service = Service("/usr/local/bin/chromedriver")
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.implicitly_wait(10)
            self.driver.get("data:text/html,<html><body><h1>Test</h1></body></html>")
            self.logger.info("Chrome driver test successful")
            return True
        except Exception as e:
            self.logger.error(f'Failed to setup Chrome driver: {e}')
            self.current_action = f'Error: {str(e)}'
            return False

    def login(self):
        try:
            if not self.driver:
                self.logger.error('Driver not initialized')
                return False
            self.current_action = 'Navigating to login page'
            self.driver.get(Config.LOGIN_URL)
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            email_input.clear()
            email_input.send_keys(Config.get_email())
            password_input = self.driver.find_element(By.NAME, "password")
            password_input.clear()
            password_input.send_keys(Config.get_password())
            signin_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign in') or contains(@type, 'submit')]"))
            )
            signin_btn.click()
            time.sleep(10)
            if "login" not in self.driver.current_url.lower():
                self.logger.info('Login successful')
                return True
            self.logger.warning('Login may have failed')
            return False
        except Exception as e:
            self.logger.error(f'Login failed: {e}')
            self.current_action = f'Login error: {str(e)}'
            return False

    def perform_activities(self):
        try:
            if not self.driver:
                return False
            self.logger.info('Performing activities')
            return True
        except Exception as e:
            self.logger.error(f'Activities failed: {e}')
            return False

    def run_cycle(self):
        if not self.running:
            return
        try:
            self.logger.info('Starting new bot cycle')
            if not self.setup_driver():
                raise Exception("Failed to setup driver")
            if not self.login():
                raise Exception("Login failed")
            if not self.perform_activities():
                self.logger.warning("Some activities failed")
            self.total_runs += 1
            self.last_run = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.logger.info(f'Bot cycle completed successfully (Total runs: {self.total_runs})')
        except Exception as e:
            self.error_count += 1
            self.logger.error(f'Bot cycle failed: {e}')
        finally:
            self.cleanup_driver()

    def cleanup_driver(self):
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
                self.logger.info('Driver cleanup completed')
        except Exception as e:
            self.logger.error(f'Error during driver cleanup: {e}')

    def stop(self):
        self.running = False
        self.cleanup_driver()
        self.logger.info('Bot stopped')
