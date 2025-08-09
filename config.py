import os
import logging

class Config:
    """Configuration management for RollerCoin bot"""
    
    LOGIN_URL = "https://rollercoin.com"
    DEFAULT_CYCLE_INTERVAL = 300  # 5 minutes between cycles
    
    @staticmethod
    def get_email():
        """Get email from environment variable or default"""
        return os.getenv("ROLLERCOIN_EMAIL", "tiagoh736@gmail.com")
    
    @staticmethod
    def get_password():
        """Get password from environment variable or default"""
        return os.getenv("ROLLERCOIN_PASSWORD", "Loko@137955")
    
    @staticmethod
    def set_credentials(email, password):
        """Set credentials (in a real app, this would save to secure storage)"""
        # In a production environment, you would save these securely
        # For now, we'll just log that they were updated
        logging.info(f"Credentials updated for email: {email}")
        # You could implement file-based or database storage here
    
    @staticmethod
    def get_cycle_interval():
        """Get the interval between bot cycles in seconds"""
        try:
            return int(os.getenv("CYCLE_INTERVAL", Config.DEFAULT_CYCLE_INTERVAL))
        except ValueError:
            return Config.DEFAULT_CYCLE_INTERVAL
    
    @staticmethod
    def get_debug_mode():
        """Check if debug mode is enabled"""
        return os.getenv("DEBUG", "True").lower() == "true"
