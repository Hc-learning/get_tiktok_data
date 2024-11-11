


# 讀取xlsx檔案

# 加载Excel文件
# workbook = load_workbook('../data.xlsx')
#
# # 选择工作表
# sheet = workbook.active  # 或者使用 workbook['工作表名']
# a = 0
# datas = ['https://affiliate.tiktokglobalshop.com/connection/creator/detail?cid=7495344726565423350',
#          'https://affiliate.tiktokglobalshop.com/connection/creator/detail?cid=7494227701041957519',
#          'https://affiliate.tiktokglobalshop.com/connection/creator/detail?cid=7494008919956489925',
#          'https://affiliate.tiktokglobalshop.com/connection/creator/detail?cid=7495155741722184578',
#          'https://affiliate.tiktokglobalshop.com/connection/creator/detail?cid=7494001242412779805',
#          'https://affiliate.tiktokglobalshop.com/connection/creator/detail?cid=7495519059014224725',
#          'https://affiliate.tiktokglobalshop.com/connection/creator/detail?cid=7494019419359643757',
#          'https://affiliate.tiktokglobalshop.com/connection/creator/detail?cid=7493991856232433905',
#          'https://affiliate.tiktokglobalshop.com/connection/creator/detail?cid=7494246429697280709',
#          'https://affiliate.tiktokglobalshop.com/connection/creator/detail?cid=7495190556016544190',
#          'https://affiliate.tiktokglobalshop.com/connection/creator/detail?cid=7495279983602338736',
#          'https://affiliate.tiktokglobalshop.com/connection/creator/detail?cid=7495208385472203441']

# 读取数据
# for row in sheet.iter_rows(values_only=True):
#     if a != 0:
#         datas.append(row[-1])
#     a += 1
# print(datas)
# driver.get('https://affiliate.tiktokglobalshop.com/connection/creator?enter_from=affiliate_find_creators&shop_region=US')
# wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'table tbody tr')))
# driver.find_element(By.CSS_SELECTOR, 'table tbody tr').click()
# b = 0
# flag = True

# c = copy.deepcopy(datas)
# @retry(stop=stop_after_attempt(len(datas) * 2))
# def a(_datas):
#     global b
#     for i in _datas[b:]:
#         ee = int(input('輸入數字：'))
#         print('retry')
#         ert = 1 / ee
#         c[b] = b
#         b += 1
#     return c
#
#
# print(a(datas))
# dict_data = [
#     {'name': 'test1\ntest2'},
#     {'name': 'test2'},
#     {'name': 'test3'}
# ]
#
# df = pd.DataFrame(dict_data)
# df.to_excel('test.xlsx', index=False)

# def get_data():
#     dict_data[0] = dict_data[0] | {'age': 18}
# get_data()
# print(dict_data)
# count = 0

# def get_data(_datas):
#     copy_datas = copy.deepcopy(_datas)
#     for i in _datas:
#         detail_url = i
#         # 打開一個新標簽頁面
#         driver.get(detail_url)
#         # 等待頁面載入完成
#         try:
#             wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.pcm-pc-content .pcm-pc-legend')))
#             deal_amount = driver.find_element(By.CSS_SELECTOR, '.pcm-pc-content .pcm-pc-legend').find_elements(
#                 By.CSS_SELECTOR, '.ecom-data-overflow-text-container')
#             deal_list = [i.text for i in deal_amount]
#             _list = driver.find_elements(By.CSS_SELECTOR, '[data-e2e="0bc7b49d-b8b3-02d5"]')
#             dict_data = {
#                 # 獲取詳細頁 個人簡介
#                 'intro': iselement(driver, By.CSS_SELECTOR, '[data-e2e="2e9732e6-4d06-458d"]'),
#                 # 獲取詳細頁 預發佈率
#                 'kbps': _list[4].text,
#                 # 獲取粉絲數,
#                 'follower_count': iselement(driver, By.CSS_SELECTOR, '[data-e2e="7aed0dd7-48ba-6932"]'),
#                 # 獲取佣金率
#                 'commission': _list[5].text,
#                 # 獲取每个销售渠道的商品交易总额
#                 'deal_amount': deal_list
#             }
#             global count
#             _datas = _datas[count + 1:]
#             copy_datas[count] = dict_data
#             count += 1
#         except TimeoutException as e:
#             print('頁面載入超時')
#             print('無法取得資料,出現滑塊驗證')
#     return copy_datas
#
#
# print(get_data(datas))
# print(datas)

# df = pd.read_excel('../data.xlsx')
# df = df.drop_duplicates(subset=['name'])
# df.to_excel('../data1.xlsx', index=False)
# print(len(df))
# 当前日期
# today = datetime.date.today()
# # 创建一个 timedelta 对象，表示 10 天
# ten_days = datetime.timedelta(days=10)
# # 加上 10 天
# future_date = today + ten_days
# print(future_date.strftime('%m/%d/%Y') + '1111')  # 输出: 当前日期加 10 天

# 數據切片
# a = [
#     {'name':'xiao1'},
#     {'age':'12'}
# ]

# b = [
#     {'name':'xiao2', 'age':'99', 'city':'beijing'},
#     {'name': 'xiao2', 'age': '88', 'city': 'beijing'},
# ]
#
# da = pd.DataFrame(a)
# db = pd.DataFrame(b)
#
# # 合并数据
# df = pd.concat([db, da], ignore_index=True)
# # df.drop_duplicates(subset=['name'], inplace=True)
# print(df)


# driver.get('https://www.baidu.com')
# time.sleep(5)
# driver.find_element(By.ID, 'kw').send_keys('selenium')
# time.sleep(2)
# driver.find_element(By.ID, 'kw').clear()

# driver.execute_script("Array.from(document.querySelectorAll('[role=region]')).forEach(item => item.style.display = 'block')")
# driver.execute_script("document.querySelector('#target_complete_details_message_input').value = 'adawdawd'")
# driver.find_element(By.ID, 'target_complete_details_message_input').send_keys('我是输入的内容')

# input()


from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
import json
import time

# 官方文档地址
# https://doc2.bitbrowser.cn/jiekou/ben-di-fu-wu-zhi-nan.html

# 此demo仅作为参考使用，以下使用的指纹参数仅是部分参数，完整参数请参考文档
class BrowserApi:
    def __init__(self, name):
        self.url = "http://127.0.0.1:54345"
        self.headers = {'Content-Type': 'application/json'}
        self.name = name


    def createBrowser(self):  # 创建或者更新窗口，指纹参数 browserFingerPrint 如没有特定需求，只需要指定下内核即可，如果需要更详细的参数，请参考文档
        json_data = {
            'name': self.name,  # 窗口名称
            'remark': '',  # 备注
            'proxyMethod': 2,  # 代理方式 2自定义 3 提取IP
            # 代理类型  ['noproxy', 'http', 'https', 'socks5', 'ssh']
            'proxyType': 'noproxy',
            'host': '',  # 代理主机
            'port': '',  # 代理端口
            'proxyUserName': '',  # 代理账号
            "browserFingerPrint": {  # 指纹对象
                'coreVersion': '124'  # 内核版本，注意，win7/win8/winserver 2012 已经不支持112及以上内核了，无法打开
            }
        }

        res = requests.post(f"{self.url}/browser/update",
                            data=json.dumps(json_data), headers=self.headers).json()
        browserId = res['data']['id']
        print(browserId)
        return browserId


    def updateBrowser(self):  # 更新窗口，支持批量更新和按需更新，ids 传入数组，单独更新只传一个id即可，只传入需要修改的字段即可，比如修改备注，具体字段请参考文档，browserFingerPrint指纹对象不修改，则无需传入
        json_data = {'ids': ['93672cf112a044f08b653cab691216f0'],
                     'remark': '我是一个备注', 'browserFingerPrint': {}}
        res = requests.post(f"{self.url}/browser/update/partial",
                            data=json.dumps(json_data), headers=self.headers).json()
        print(res)


    def openBrowser(self, id_):  # 直接指定ID打开窗口，也可以使用 createBrowser 方法返回的ID
        json_data = {"id": f'{id_}'}
        res = requests.post(f"{self.url}/browser/open",
                            data=json.dumps(json_data), headers=self.headers).json()
        return res


    def closeBrowser(self, _id):  # 关闭窗口
        json_data = {'id': f'{_id}'}
        requests.post(f"{self.url}/browser/close",
                      data=json.dumps(json_data), headers=self.headers).json()


    def deleteBrowser(self, _id):  # 删除窗口
        json_data = {'id': f'{_id}'}
        print(requests.post(f"{self.url}/browser/delete",
              data=json.dumps(json_data), headers=self.headers).json())


if __name__ == '__main__':
    # browser_id = createBrowser()
    # openBrowser(browser_id)
    #
    # time.sleep(10)  # 等待10秒自动关闭窗口
    #
    # closeBrowser(browser_id)
    #
    # time.sleep(10)  # 等待10秒自动删掉窗口

    # deleteBrowser('12e9e766145c4e889efec6ccb057c3b0')
    pass
# # /browser/open 接口会返回 selenium使用的http地址，以及webdriver的path，直接使用即可
# res = openBrowser("15724e57fc0e490baeaa5ab853abfe54") # 窗口ID从窗口配置界面中复制，或者api创建后返回
#
# print(res)
#
# driverPath = res['data']['driver']
# debuggerAddress = res['data']['http']
#
# # selenium 连接代码
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_experimental_option("debuggerAddress", debuggerAddress)
#
# chrome_service = Service(driverPath)
# driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
#
# # 以下为PC模式下，打开baidu，输入 BitBrowser，点击搜索的案例
# driver.get('https://www.baidu.com/')
#
# input = driver.find_element(By.CLASS_NAME, 's_ipt')
# input.send_keys('BitBrowser')
#
# print('before click...')
#
# btn = driver.find_element(By.CLASS_NAME, 's_btn')
# btn.click()
#
# print('after click')