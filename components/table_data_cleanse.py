import logging
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from components.get_webdriver import driver, wait

logging.basicConfig(level=logging.INFO, format='%(lineno)d %(asctime)s - %(levelname)s : %(message)s')


def data_cleanse(data: list[WebElement], cid=None):
    logging.info(cid)
    if not data:
        logging.info('数据为空')
        return []
    logging.info('数据获取成功')
    logging.info('开始数据清洗')
    result = []
    for element in data:
        # 每个tr里面包含好几个td，我们需要获取全部
        # 头像，昵称，标签，简介，分类，关注数
        name =  iselement(element, By.CSS_SELECTOR, '[data-e2e="fbc99397-6043-1b37"]')
        # 獲取詳細頁面數據






        result.append(
            {
                'cid': cid[len(result)],
                'img_url': iselement(element,By.CSS_SELECTOR,'[data-e2e="e81f0ced-c73a-1f08"]',True,'src'),
                # 获取昵称
                'name': name,
                # 获取标签
                'tag': iselement(element,By.CSS_SELECTOR, '[data-e2e="7540492b-7c74-bca5"]'),
                # 获取个性签名
                'signature': iselement(element,By.CSS_SELECTOR, '[data-e2e="3b9caa65-c65a-e9df"]'),
                # 获取分类
                'category': iselement(element,By.CSS_SELECTOR, '[data-e2e="6e905dae-25bf-454b"]'),
                # 获取商店基本信息
                'shop_info': iselement(element,By.CSS_SELECTOR, '[data-e2e="9e8f2473-a87f-db74"]'),
                # 获取视频封面
                'video_img_url': iselement(element,By.CSS_SELECTOR,'[data-e2e="0830b47f-1bbf-a2b4"]', True,'src'),
                # 獲取交易額
                'deal_amount': iselement(element,By.CSS_SELECTOR, '[data-e2e="dfa39213-a263-5c80"]'),
                # 獲取成交量
                'bargain_total': iselement(element,By.CSS_SELECTOR, '[data-e2e="84077312-3e9e-6c5e"]'),
                # 獲取平均播放數
                'video_play_total': iselement(element,By.CSS_SELECTOR, '[data-e2e="ac42cf72-8039-7ab4"]'),
                # 獲取互動率
                'interaction_rate': iselement(element,By.CSS_SELECTOR, '[data-e2e="1ae51110-5bd8-9a32"]'),
                # 獲取詳細頁 個人簡介
                # 'intro': intro,
                # 獲取詳細頁 預發佈率
                # 'Expected_release_rate': kbps,

            }
        )
        logging.info(f'以獲取[ {name} ]的資料')

    logging.info('数据清洗完成')
    logging.info(f'-------本次共采集[{result.__len__()}]個數據-------')
    save_data(result)

def iselement(element,_type, condition, istrue=False, _src=None):
    try:
        a = element.find_element(_type,condition)
        if istrue:
            return a.get_attribute(_src)
        return a.text
    except Exception:
        return ' '


def save_data(data: list):
    # 使用Pandas將資料存入Excel檔案，數據不能重複
    # 我後續需要在裏面添加數據
    import pandas as pd
    df = pd.DataFrame(data)
    df = df.drop_duplicates()
    # 保存到Excel檔案
    df.to_excel('data.xlsx', index=False)
    logging.info('所有數據已保存到本地目錄下的data.xlsx')