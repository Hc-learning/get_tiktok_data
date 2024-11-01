import time

from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By

from components.get_webdriver import driver

driver.get("https://www.baidu.com")
time.sleep(2)
driver.find_element(By.XPATH, '//*[@id="s-top-left"]/a[6]').click()
_windows = driver.window_handles
driver.switch_to.window(_windows[-1])
print(driver.current_url)
time.sleep(5)
content = driver.page_source
print(content)
driver.switch_to.window(_windows[0])
time.sleep(2)
driver.find_element(By.XPATH, '//*[@id="s-top-left"]/a[5]').click()
time.sleep(2)
driver.switch_to.window(_windows[1])
driver.close()
time.sleep(5)
