import json
import logging
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from components.get_webdriver import wait, driver
from components.get_webdriver import SETTINGS_DATA
from selenium.webdriver.support import expected_conditions as EC
from components.table_data_cleanse import data_cleanse

# 爬取思路
"""
    1、 打开网页，登陆账号（这里使用selenium模拟登陆，验证码由人工识别）
        找到达人按钮点击 --> 找到达人机构点击 --> 选择独立达人
        表格筛选出数据后，我们继续获取数据
    页面数据加载方式：
        网页通过Ajax加载数据，当页面滑倒一定程度后，加载后面的数据，每次加载12个数据
        数据会加载到表格的最后所以属性都是一样
    2、我们可以在获取完第一轮数据后通过滚动屏幕来获取第二轮数据
    3、在获取数据的同时可以继续获取详细页的数据
    4、防止重复元素，我们可以设置一个列表来保存已经爬取过的元素，避免重复爬取
    5、数据存储方式：
        我们可以将数据存储到csv文件中，每一行代表一个数据，每一列代表一个属性
        这样可以方便后续分析数据
    后续工作：
        1、我们可以将数据写入数据当中
        2、创建一个api接口用于返回数据
        3、可以编写一个小前端项目，用于显示数据
"""

logging.basicConfig(level=logging.INFO, format='%(lineno)d %(asctime)s - %(levelname)s : %(message)s')


# 页面的跳转
def scrape_page(url, condition, element):
    try:
        driver.get(url)
        wait.until(condition(element))
    except TimeoutException as e:
        logging.info(f'错误：{e}')
    except Exception as e:
        logging.info(f'错误：{e}')


def login_():
    try:
        # 登陆账号
        # 切换邮箱登入
        driver.find_element(By.CSS_SELECTOR, '#TikTok_Ads_SSO_Login_Email_Panel_Button').click()
        logging.info('切换到邮箱登入')
        # 输入邮箱号
        email_element = driver.find_element(By.CSS_SELECTOR, '#TikTok_Ads_SSO_Login_Email_Input')
        email_element.send_keys(SETTINGS_DATA.get('EMAIL'))
        logging.info('输入邮箱号')
        # 输入密码
        pwd_element = driver.find_element(By.CSS_SELECTOR, '#TikTok_Ads_SSO_Login_Pwd_Input')
        pwd_element.send_keys(SETTINGS_DATA.get('PASSWORD'))
        logging.info('输入密码')
        # 点击登陆按钮
        driver.find_element(By.CSS_SELECTOR, '#TikTok_Ads_SSO_Login_Btn').click()
        logging.info('点击登陆按钮')
        logging.info('出现验证码，请手动完成')
        # 等待页面加载完成
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[data-e2e="e9e98bcf-9e15-8681"] span')))
        logging.info('登陆成功')
    except TimeoutException as e:
        logging.info(f'错误：数据没有加载成功，{e}')

# 点击按钮
def click_btn():
    try:
        # 点击达人按钮
        driver.find_element(By.CSS_SELECTOR, 'button[data-e2e="e9e98bcf-9e15-8681"] span').click()
        # 点击达人机构
        driver.find_element(By.XPATH, '//*[@id="creatorAgency"]/div/button/div').click()
        # 点击独立达人
        driver.find_element(By.XPATH, '//*[@id="arco-select-popup-2"]/div/div/li[3]').click()
        logging.info('數據已篩選')
        return get_data()
    except TimeoutException as e:
        logging.info(f'未找到元素：{e}')
    except Exception as e:
        logging.info(f'错误：{e}')

# 获取数据
def get_data():
    try:
        # 等待页面加载完成
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content-container"]/main/div/div/div/div/div[5]/div/div/div/div/div[2]/div/div/div/div/div/div[2]/table/tbody')))
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-e2e="e81f0ced-c73a-1f08"]')))
        # 获取表格数据
        time.sleep(5)
        return driver.find_elements(By.XPATH, '//*[@id="content-container"]/main/div/div/div/div/div[5]/div/div/div/div/div[2]/div/div/div/div/div/div[2]/table/tbody/tr')
    except TimeoutException as e:
        logging.info(f'未找到元素：{e}')
    except Exception as e:
        logging.info(f'错误：{e}')

def run():
    try:
        # 打开网页
        driver.get(SETTINGS_DATA.get('FIND_ALL_DATA_URL'))
        # 查看是否登录
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#TikTok_Ads_SSO_Login_Email_Panel_Button')))
        logging.info('检测到还没有登录，开始登陆')
        login_()
    except TimeoutException:
        logging.info('检测到已经登录')
    except Exception as e:
        logging.info(f'错误：{e}')
    finally:
        data = click_btn()
        result = data_cleanse(data)
        json.dump(result, open('data.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=4)

if __name__ == '__main__':
    run()
