import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class WhatsAppAutomation:
    def __init__(self):
        self.driver = None
        self.wait = None
        
    def setup_driver(self):
        """Initialize the Chrome driver"""
        options = webdriver.ChromeOptions()
        options.add_argument('--user-data-dir=./User_Data')  # Save session to avoid scanning QR every time
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 20)
        
    def open_whatsapp(self):
        """Open WhatsApp Web"""
        self.driver.get("https://web.whatsapp.com")
        print("Please scan the QR code if needed and press Enter when ready.")
        input()  # Wait for user to scan QR code and press Enter
        
    def search_contact(self, contact_name):
        """Search for a contact"""
        try:
            search_box = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
            )
            search_box.clear()
            search_box.send_keys(contact_name)
            time.sleep(2)  # Wait for search results
        except (NoSuchElementException, TimeoutException):
            print("Search box not found")
            
    def select_contact(self, contact_name):
        """Select a contact from the search results"""
        try:
            contact = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f'//span[@title="{contact_name}"]'))
            )
            contact.click()
        except (NoSuchElementException, TimeoutException):
            print(f"Contact '{contact_name}' not found")
            
    def send_message(self, message):
        """Send a message to the selected contact"""
        try:
            message_box = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )
            message_box.send_keys(message + Keys.ENTER)
            print(f"Message sent: {message}")
            time.sleep(2)  # Wait for message to be sent
        except (NoSuchElementException, TimeoutException):
            print("Message box not found")
            
    def send_multiple_messages(self, contact_name, messages, delay=2):
        """Send multiple messages to a contact"""
        self.search_contact(contact_name)
        self.select_contact(contact_name)
        
        for message in messages:
            self.send_message(message)
            time.sleep(delay)  # Delay between messages
            
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            
def main():
    # Initialize the automation
    wa = WhatsAppAutomation()
    wa.setup_driver()
    
    try:
        # Open WhatsApp Web
        wa.open_whatsapp()
        
        # Contact and messages
        contact_name = "Friend's Name"  # Replace with actual contact name
        messages = [
            "Hello! This is an automated message.",
            "This is the second message.",
            "And this is the third one.",
            "Have a great day!"
        ]
        
        # Send messages
        wa.send_multiple_messages(contact_name, messages)
        
        print("Messages sent successfully!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
    finally:
        # Close the browser
        wa.close()

if __name__ == "__main__":
    main()