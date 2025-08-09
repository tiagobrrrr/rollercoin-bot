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
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from config import Config

class RollerCoinBot:
    """RollerCoin automation bot with enhanced error handling"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.driver = None
        self.last_run = None
        self.total_runs = 0
        self.error_count = 0
        self.current_action = 'Initializing'
        self.running = True
        
    def setup_driver(self):
        """Setup Chrome WebDriver with optimal settings"""
        try:
            self.current_action = 'Setting up browser'
            options = Options()
            
            # Enhanced Chrome options for Replit environment
            options.add_argument("--headless=new")  # Use new headless mode
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-software-rasterizer")
            options.add_argument("--disable-background-timer-throttling")
            options.add_argument("--disable-backgrounding-occluded-windows")
            options.add_argument("--disable-renderer-backgrounding")
            options.add_argument("--disable-features=TranslateUI")
            options.add_argument("--disable-ipc-flooding-protection")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--remote-debugging-port=9222")
            options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36")
            
            # Find and set Chromium binary
            import glob
            chromium_matches = glob.glob("/nix/store/*/bin/chromium")
            if chromium_matches:
                chromium_binary = chromium_matches[0]
                options.binary_location = chromium_binary
                self.logger.info(f'Using Chromium binary: {chromium_binary}')
            else:
                self.logger.warning('Chromium binary not found')
                return False
            
            # Try different approaches to get a working driver
            driver_created = False
            
            # Method 1: Try static chromedriver
            static_driver_path = "/home/runner/.local/bin/chromedriver-static"
            if os.path.exists(static_driver_path):
                try:
                    service = Service(static_driver_path)
                    self.driver = webdriver.Chrome(service=service, options=options)
                    driver_created = True
                    self.logger.info('Using static chromedriver')
                except Exception as static_error:
                    self.logger.warning(f'Static chromedriver failed: {static_error}')
            
            # Method 2: Use Chrome in remote debugging mode (as fallback)
            if not driver_created:
                try:
                    # Start Chrome in remote debugging mode manually
                    import subprocess
                    import time
                    import requests
                    
                    # Start Chrome process with remote debugging
                    chrome_cmd = [
                        chromium_binary,
                        '--headless=new',
                        '--no-sandbox',
                        '--disable-dev-shm-usage',
                        '--remote-debugging-port=9222',
                        '--disable-gpu',
                        '--disable-software-rasterizer'
                    ]
                    
                    chrome_process = subprocess.Popen(chrome_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    time.sleep(3)  # Wait for Chrome to start
                    
                    # Check if remote debugging is available
                    try:
                        response = requests.get('http://localhost:9222/json/version', timeout=5)
                        if response.status_code == 200:
                            # Use remote debugging
                            options.add_experimental_option("debuggerAddress", "localhost:9222")
                            options.add_argument("--remote-debugging-port=9222")
                            
                            # Create driver without service (using remote debugging)
                            self.driver = webdriver.Chrome(options=options)
                            driver_created = True
                            self.logger.info('Using Chrome remote debugging mode')
                    except Exception as remote_error:
                        self.logger.warning(f'Remote debugging failed: {remote_error}')
                        chrome_process.terminate()
                        
                except Exception as fallback_error:
                    self.logger.warning(f'Chrome process fallback failed: {fallback_error}')
            
            if not driver_created:
                self.logger.error('All Chrome driver methods failed')
                return False
            
            if self.driver:
                self.driver.implicitly_wait(10)
                # Test driver with a simple operation
                try:
                    self.driver.get("data:text/html,<html><body><h1>Test</h1></body></html>")
                    self.logger.info('Chrome driver test successful')
                    return True
                except Exception as test_error:
                    self.logger.error(f'Chrome driver test failed: {test_error}')
                    self.cleanup_driver()
                    return False
            else:
                self.logger.error('Failed to create driver instance')
                return False
            
        except Exception as e:
            self.logger.error(f'Failed to setup Chrome driver: {e}')
            self.current_action = f'Error: {str(e)}'
            return False
    
    def login(self):
        """Login to RollerCoin with enhanced error handling"""
        try:
            if not self.driver:
                self.logger.error('Driver not initialized')
                return False
                
            self.current_action = 'Navigating to login page'
            self.driver.get(Config.LOGIN_URL)
            self.logger.info('Navigated to RollerCoin login page')
            
            # Wait for page to load
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            self.current_action = 'Looking for login button'
            # Try to find and click login button if it exists
            try:
                login_btn = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login') or contains(text(), 'Log in')]"))
                )
                login_btn.click()
                self.logger.info('Clicked login button')
                time.sleep(3)
            except TimeoutException:
                self.logger.info('Login button not found or not needed')
            
            self.current_action = 'Entering credentials'
            # Find and fill email field
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            email_input.clear()
            email_input.send_keys(Config.get_email())
            self.logger.info('Email entered')
            
            # Find and fill password field
            password_input = self.driver.find_element(By.NAME, "password")
            password_input.clear()
            password_input.send_keys(Config.get_password())
            self.logger.info('Password entered')
            
            self.current_action = 'Submitting login'
            # Find and click sign in button
            signin_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign in') or contains(text(), 'Sign In') or contains(@type, 'submit')]"))
            )
            signin_btn.click()
            self.logger.info('Login form submitted')
            
            # Wait for login to complete
            self.current_action = 'Waiting for login completion'
            time.sleep(15)
            
            # Check if login was successful by checking URL or looking for common elements
            try:
                # Check if we're redirected away from login page
                current_url = self.driver.current_url
                if "login" not in current_url.lower():
                    self.logger.info('Login successful - redirected from login page')
                    return True
                else:
                    self.logger.warning('Login may have failed - still on login page')
                    return False
            except Exception as url_check_error:
                self.logger.warning(f'Could not verify login success: {url_check_error}')
                return False
                
        except Exception as e:
            self.logger.error(f'Login failed: {e}')
            self.current_action = f'Login error: {str(e)}'
            return False
    
    def perform_activities(self):
        """Perform various activities on RollerCoin"""
        try:
            if not self.driver:
                self.logger.error('Driver not initialized')
                return False
                
            self.current_action = 'Performing activities'
            
            # Add your specific RollerCoin activities here
            # For example: claiming rewards, playing games, etc.
            
            # Placeholder for activities - customize based on RollerCoin features
            self.logger.info('Performing basic site activities')
            
            # Navigate around the site
            try:
                # Look for common elements or activities
                activities = [
                    "//a[contains(text(), 'Mine')]",
                    "//a[contains(text(), 'Games')]",
                    "//button[contains(text(), 'Claim')]"
                ]
                
                for activity_xpath in activities:
                    try:
                        element = self.driver.find_element(By.XPATH, activity_xpath)
                        if element.is_displayed():
                            element.click()
                            time.sleep(2)
                            self.logger.info(f'Clicked on activity: {activity_xpath}')
                            break
                    except NoSuchElementException:
                        continue
                        
            except Exception as e:
                self.logger.warning(f'Error during activities: {e}')
            
            return True
            
        except Exception as e:
            self.logger.error(f'Activities failed: {e}')
            self.current_action = f'Activities error: {str(e)}'
            return False
    
    def run_cycle(self):
        """Run a complete bot cycle"""
        if not self.running:
            return
            
        try:
            self.logger.info('Starting new bot cycle')
            self.current_action = 'Starting cycle'
            
            # Setup driver
            if not self.setup_driver():
                raise Exception("Failed to setup driver")
            
            # Login
            if not self.login():
                raise Exception("Login failed")
            
            # Perform activities
            if not self.perform_activities():
                self.logger.warning("Some activities failed")
            
            # Update statistics
            self.total_runs += 1
            self.last_run = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.current_action = 'Cycle completed'
            
            self.logger.info(f'Bot cycle completed successfully (Total runs: {self.total_runs})')
            
        except Exception as e:
            self.error_count += 1
            self.current_action = f'Cycle error: {str(e)}'
            self.logger.error(f'Bot cycle failed: {e}')
            
        finally:
            # Always cleanup driver
            self.cleanup_driver()
    
    def cleanup_driver(self):
        """Cleanup WebDriver resources"""
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
                self.logger.info('Driver cleanup completed')
        except Exception as e:
            self.logger.error(f'Error during driver cleanup: {e}')
    
    def stop(self):
        """Stop the bot"""
        self.running = False
        self.current_action = 'Stopping'
        self.cleanup_driver()
        self.logger.info('Bot stopped')
