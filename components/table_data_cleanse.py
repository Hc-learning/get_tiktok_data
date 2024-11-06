import logging
import os.path
import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from tenacity import retry, stop_after_attempt

from components.get_webdriver import driver, wait
from components.utils import progress_bar, save_data
from config.settings import SETTINGS_DATA
import copy

logging.basicConfig(level=logging.INFO, format='%(lineno)d %(asctime)s - %(levelname)s : %(message)s')

copy_data = []
_count = 0
retry_count = 0
table_count = 0


@retry(stop=stop_after_attempt(10))
def data_cleanse(data: list[WebElement],_page = None, cid=None):
    global table_count
    if not data:
        logging.info('数据为空')
        return []
    logging.info('数据获取成功')
    logging.info('开始数据清洗')
    result = []
    try:
        for element in data[table_count:]:
            # 每个tr里面包含好几个td，我们需要获取全部
            # 头像，昵称，标签，简介，分类，关注数
            name = iselement(element, By.CSS_SELECTOR, '[data-e2e="fbc99397-6043-1b37"]')
            # _cid = cid[len(result) - 1]
            # detail_url = SETTINGS_DATA.get('DETAIL_DATA_URL').format(_cid)
            result.append(
                {
                    # 'cid': _cid,
                    # 获取昵称
                    'name': name,
                    'img_url': iselement(element, By.CSS_SELECTOR, '[data-e2e="e81f0ced-c73a-1f08"]', True, 'src'),
                    # 获取标签
                    'tag': iselement(element, By.CSS_SELECTOR, '[data-e2e="7540492b-7c74-bca5"]'),
                    # 获取个性签名
                    'signature': iselement(element, By.CSS_SELECTOR, '[data-e2e="3b9caa65-c65a-e9df"]'),
                    # 获取分类
                    'category': iselement(element, By.CSS_SELECTOR, '[data-e2e="6e905dae-25bf-454b"]'),
                    # 获取商店基本信息
                    'shop_info': iselement(element, By.CSS_SELECTOR, '[data-e2e="9e8f2473-a87f-db74"]'),
                    # 获取视频封面
                    'video_img_url': iselement(element, By.CSS_SELECTOR, '[data-e2e="0830b47f-1bbf-a2b4"]', True,
                                               'src'),
                    # 獲取交易額
                    'deal_amount': iselement(element, By.CSS_SELECTOR, '[data-e2e="dfa39213-a263-5c80"]'),
                    # 獲取成交量
                    'bargain_total': iselement(element, By.CSS_SELECTOR, '[data-e2e="84077312-3e9e-6c5e"]'),
                    # 獲取平均播放數
                    'video_play_total': iselement(element, By.CSS_SELECTOR, '[data-e2e="ac42cf72-8039-7ab4"]'),
                    # 獲取互動率
                    'interaction_rate': iselement(element, By.CSS_SELECTOR, '[data-e2e="1ae51110-5bd8-9a32"]'),
                    # 獲取詳細頁 個人簡介
                    # 'intro': intro,
                    # # 獲取詳細頁 預發佈率
                    # 'Expected_release_rate': kbps,
                    # # 獲取詳細頁 url
                    # 'detail_url': detail_url,
                    # 'address': address,
                }
            )
            table_count += 1
            progress_bar('數據采取進度', len(data), table_count)
        print()
        logging.info('列表数据清洗完成，準備清洗詳細頁')
        global copy_data
        copy_data = copy.deepcopy(result)
        # data_cleanse_detail(result)
        save_data(result, _page)
        table_count = 0
        logging.info(f'-------本次共采集[{result.__len__()}]個數據-------')
    except Exception as e:
        logging.info(f'清洗列表出錯，原因：{e}')
        logging.info('開始備份當數據。。。')
        save_data(result)
        raise e


@retry(stop=stop_after_attempt(1000))
def data_cleanse_detail(_datas: list[dict]):
    try:
        global _count
        for data in _datas[_count:]:
            # 獲取詳細頁面數據
            detail_url = data.get('detail_url')
            # 打開一個新標簽頁面
            driver.get(detail_url)
            # 等待頁面載入完成
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.pcm-pc-content .pcm-pc-legend')))
            deal_amount = driver.find_element(By.CSS_SELECTOR, '.pcm-pc-content .pcm-pc-legend').find_elements(
                By.CSS_SELECTOR, '.ecom-data-overflow-text-container')
            deal_list = [i.text for i in deal_amount]
            deal_list_title = []
            deal_list_percent = []
            for i in deal_list:
                if i.find('%') == -1:
                    deal_list_title.append(i)
                else:
                    deal_list_percent.append(i)
            _list = driver.find_elements(By.CSS_SELECTOR, '[data-e2e="e4af3b5a-a87c-dfbd"]')[1].find_elements(
                By.CSS_SELECTOR, '[data-e2e="0bc7b49d-b8b3-02d5"]')
            dict_data = {
                # 獲取詳細頁 個人簡介
                'intro': iselement(driver, By.CSS_SELECTOR, '[data-e2e="2e9732e6-4d06-458d"]'),
                # 獲取詳細頁 預發佈率
                'kbps': _list[0].text,
                # 獲取粉絲數,
                'follower_count': iselement(driver, By.CSS_SELECTOR, '[data-e2e="7aed0dd7-48ba-6932"]'),
                # 獲取佣金率
                'commission': _list[1].text,
                # 獲取每个销售渠道的商品交易总额
                'deal_amount': f'{str(deal_list_title)},{str(deal_list_percent)}'
            }
            driver.execute_script("arguments[0].scrollIntoView();", _list[0])
            copy_data[_count] = copy_data[_count] | dict_data
            progress_bar('詳細頁采取進度', _datas.__len__(), _count + 1)
            _count += 1
            time.sleep(3)
        print()
        logging.info('詳細頁數據清洗完成')
        logging.info('開始保存數據。。。')
    except Exception as e:
        logging.info(f'清洗詳細頁出錯，原因：{e}')
        logging.info('開始備份當數據。。。')
        # save_and_clear_data()
        raise e


def iselement(element, _type, condition, istrue=False, _src=None):
    try:
        a = element.find_element(_type, condition)
        if istrue:
            return a.get_attribute(_src)
        return a.text
    except Exception:
        return ' '

