from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import schedule
import yagmail


def get_gas_price():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    try:
        print("initialising Chrome Driver...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("going to the website...")
        driver.get('https://etherscan.io/gastracker')
        
        print("loading...")
        wait = WebDriverWait(driver, 20)  # 增加等待时间到20秒
        gas_element = wait.until(
            EC.presence_of_element_located((By.ID, "spanAvgPrice"))
        )
        
        gas_price = float(gas_element.text)
        print(f"current gas price is: {gas_price} Gwei")
        
        if gas_price < 5:
            send_alert_email(gas_price)
            print("gas price is less than 5 gwei")
        return gas_price
            
    except Exception as e:
        print(f"error: {str(e)}")
        print("error_type:", type(e).__name__)
        import traceback
        print("error_info:", traceback.format_exc())
        return None
            
    finally:
        try:
            if 'driver' in locals():
                driver.quit()
        except Exception as e:
            print(f"error occured when closing the driver: {str(e)}")
    
def send_alert_email(self, price):
    """sending email alert"""
    try:
        # Please substitute the following email address and auth code
        sender_email = "xxx"
        sender_password = "xxx"
        receiver_email = "xxx"
            
        yag = yagmail.SMTP(user=sender_email, 
                          password=sender_password, 
                          host='smtp.qq.com')
        subject = 'Gas price alert'
        content = f'current gas price is: {price} Gwei，lower than 5 Gwei！'
        yag.send(receiver_email, subject, content)
        print(f"email alert sent，current gas price: {price} Gwei")
    except Exception as e:
        print(f"error occured while sending email: {e}")


def job():
    print("Starting job: checking gas price...")
    get_gas_price()
    print("Job completed.")


job()

# set the program to run every 1 hour
schedule.every(1).hour.do(job)
    
# keep the program running
while True:
    schedule.run_pending()
    time.sleep(60)
