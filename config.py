import os
import logging

class Config:
    LOGIN_URL = "https://rollercoin.com"
    DEFAULT_CYCLE_INTERVAL = 300
    
    @staticmethod
    def get_email():
        return os.getenv("ROLLERCOIN_EMAIL", "")
    
    @staticmethod
    def get_password():
        return os.getenv("ROLLERCOIN_PASSWORD", "")
    
    @staticmethod
    def set_credentials(email, password):
        logging.info(f"Credentials updated for email: {email}")
    
    @staticmethod
    def get_cycle_interval():
        try:
            return int(os.getenv("CYCLE_INTERVAL", Config.DEFAULT_CYCLE_INTERVAL))
        except ValueError:
            return Config.DEFAULT_CYCLE_INTERVAL
    
    @staticmethod
    def get_debug_mode():
        return os.getenv("DEBUG", "True").lower() == "true"
