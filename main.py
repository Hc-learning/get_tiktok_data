import json
import logging
import re
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from tenacity import retry, stop_after_attempt

from components.get_webdriver import wait, driver
from components.get_webdriver import SETTINGS_DATA
from selenium.webdriver.support import expected_conditions as EC
from components.table_data_cleanse import data_cleanse
from components.utils import wait_for, progress_bar, save_data, clear_data

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
_ids = []


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
        wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'table tbody tr')))
        wait_for(By.CSS_SELECTOR, '[data-e2e="e81f0ced-c73a-1f08"]')
        # 点击达人按钮
        driver.find_element(By.CSS_SELECTOR, 'button[data-e2e="e9e98bcf-9e15-8681"] span').click()
        # 點擊内容類型
        driver.find_element(By.XPATH, '//*[@id="contentType"]/div/button').click()
        driver.find_element(By.XPATH, '//*[@id="arco-select-popup-1"]/div/div/li[2]').click()
        # 点击达人机构
        driver.find_element(By.XPATH, '//*[@id="creatorAgency"]/div/button/div').click()
        # 点击独立达人
        driver.find_element(By.XPATH, '//*[@id="arco-select-popup-2"]/div/div/li[3]').click()

        # 點擊表現tag
        driver.find_element(By.XPATH,
                            '//*[@id="content-container"]/main/div/div/div/div/div[3]/div/div/div/div[2]/div[1]/div[1]/div[2]/div/label[3]/button').click()
        # 成交件數
        driver.find_element(By.XPATH, '//*[@id="unitsSold"]/div/span/button').click()
        driver.find_element(By.XPATH, '//*[@id="arco-select-popup-6"]/div/div/li[2]/span').click()
        # driver.find_element(By.XPATH, '//*[@id="arco-select-popup-6"]/div/div/li[3]/span').click()
        driver.find_element(By.XPATH, '//*[@id="unitsSold"]/div/span/button').click()
        # 預發佈率
        # driver.find_element(By.XPATH, '//*[@id="SampleFulfillmentRate"]/div/button').click()
        # driver.find_element(By.XPATH, '//*[@id="arco-select-popup-7"]/div/div/li[4]').click()
        logging.info('數據已篩選')
    except TimeoutException as e:
        logging.info(f'未找到元素：{e}')
        driver.refresh()
    except Exception as e:
        logging.info(f'错误：{e}')


# 获取数据
def get_data():
    try:
        # 等待页面加载完成
        wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'table tbody tr')))
        wait_for(By.CSS_SELECTOR, '[data-e2e="e81f0ced-c73a-1f08"]')

        return driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')
    except TimeoutException as e:
        logging.info(f'未找到元素：{e}')
    except Exception as e:
        logging.info(f'错误：{e}')


cid_count = 0


# 獲取cid
@retry(stop=stop_after_attempt(100))
def get_cid(_trs):
    driver.execute_script("arguments[0].scrollIntoView();", trs[0])
    global cid_count
    for tr in _trs[cid_count:]:
        tr.click()
        all_tags = driver.window_handles
        driver.switch_to.window(all_tags[-1])  # 切换到新窗口
        url = driver.current_url
        _id = re.search(r'cid=(\d+)', url, re.S).group(1)
        if _id not in _ids:
            _ids.append(_id)
        if len(all_tags) > 2:
            driver.switch_to.window(all_tags[1])  # 切换回要關閉的窗口
            driver.close()  # 關閉新窗口
        driver.switch_to.window(all_tags[0])  # 切换回主窗口\

    # 向下滾動


page = 1
trs = []
@retry(stop=stop_after_attempt(100))
def scroll_down():
    global page, trs
    # 每一 輪數據為12個
    # 當前第幾輪
    count = 12
    _total_page = (SETTINGS_DATA.get("PAGE_COUNT") // count) * count
    # 循环滚动
    logging.info(f'本次采集數據一共-[ {SETTINGS_DATA.get("PAGE_COUNT")}條 ]數據-')
    try:
        while (count * page) <= SETTINGS_DATA.get("PAGE_COUNT"):
            trs = get_data()
            if len(trs) >= (count * page):
                progress_bar('頁面獲取進度', SETTINGS_DATA.get("PAGE_COUNT") // count, page)
                # 向下滚动表格
                driver.execute_script("arguments[0].scrollIntoView();", trs[-1])
                page += 1
        print()
        logging.info('數據加載完成')
        # get_cid(trs)
    except Exception as e:
        logging.info(f'错误：數據獲取終止,{e}')
        logging.info(f'保存已爬取的數據')
        save_data(trs)
        raise e
    return trs


_count = 100


def run():
    try:
        # 打开网页
        driver.get(SETTINGS_DATA.get('FIND_ALL_DATA_URL'))
        # 查看是否登录
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#TikTok_Ads_SSO_Login_Email_Panel_Button')))
        logging.info('检测到还没有登录，开始登陆')
        logging.info('登陆成功')
        login_()
    except TimeoutException:
        logging.info('检测到已经登录')
    except Exception as e:
        logging.info(f'错误：{e}')
    finally:
        global page
        _page = 1
        while True:
            click_btn()
            data = scroll_down()
            data_cleanse(data,_page = _page)
            driver.refresh()
            len_data = clear_data()
            logging.info(f'去除重複數據，剩餘數據【{len_data}】條')
            if len_data > SETTINGS_DATA.get("COLLECT_COUNT_DATA"):
                break
            page = 1
            _page += 1


if __name__ == '__main__':
    run()
    driver.quit()
