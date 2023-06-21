from selenium import webdriver

# Caminho para o driver do chrome
webdriver_path = "Driver/chromedriver.exe"

# Initialize the WebDriver instance (e.g., ChromeDriver)
driver = webdriver.Chrome()

# Example usage: Open a webpage
driver.get("https://www.google.com.br/")

# Prompt user input to keep the window open
input("Press Enter to close the browser window...")

# Clean up: Close the WebDriver instance
driver.quit()