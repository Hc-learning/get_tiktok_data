import logging
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from components.gei_webdriver import wait, wd
from components.gei_webdriver import SETTINGS_DATA
from selenium.webdriver.support import expected_conditions as EC

# 达人按钮
# button[data-tid="m4b_button"].arco-btn span.m4b-button-icon
# 达人机构
# div.arco-form-item-control-children div.arco-typography:nth-child(5)
# 表格
# table tbody tr

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
        wd.get(url)
        wait.until(condition(element))
    except TimeoutException as e:
        logging.info(f'错误：{e}')
    except Exception as e:
        logging.info(f'错误：{e}')


def login_():
    try:
        # 登陆账号
        # 切换邮箱登入
        wd.find_element(By.CSS_SELECTOR, '#TikTok_Ads_SSO_Login_Email_Panel_Button').click()
        # 输入邮箱号
        email_element = wd.find_element(By.CSS_SELECTOR, '#TikTok_Ads_SSO_Login_Email_Input')
        email_element.send_keys(SETTINGS_DATA.get('EMAIL'))
        # 输入密码
        pwd_element = wd.find_element(By.CSS_SELECTOR, '#TikTok_Ads_SSO_Login_Pwd_Input')
        pwd_element.send_keys(SETTINGS_DATA.get('PASSWORD'))
        # 点击登陆按钮
        wd.find_element(By.CSS_SELECTOR, '#TikTok_Ads_SSO_Login_Btn').click()
        # 等待页面加载完成
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.arco-table-body table tbody')))
    except TimeoutException as e:
        logging.info(f'错误：数据没有加载成功，{e}')


def click_btn():
    pass


def run():
    wd.get(SETTINGS_DATA.get('FIND_ALL_URL'))
    time.sleep(10)
    wd.delete_all_cookies()
    wd.add_cookie({
        'name': 'cookie_name',
        'value': 'cookie_value',
        'sessionid': '68ac918d876c74fe4cc2d830e4a121ed'
    })
    wd.refresh()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.arco-table-body table tbody')))


if __name__ == '__main__':
    run()
