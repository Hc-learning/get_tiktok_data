from pathlib import Path

SETTINGS_DATA = {
    'FIND_ALL_DATA_URL' : "https://affiliate.tiktokglobalshop.com/connection/creator?enter_from=affiliate_find_creators&shop_region=US",
    'DETAIL_DATA_URL' : 'https://affiliate.tiktokglobalshop.com/connection/creator/detail?cid={%s}',
    'File_name' : 'request_data',
    'Time_out' : 9920,
    'EMAIL' : 'shop09202@woworldtech.com',
    'PASSWORD' : 'bingshui123.',
    'chrome_driver_path': r'D:\chrome_driver\chromedriver-win64\chromedriver.exe',
    'COOKIES_PATH': r'D:\Project\get_tiktok_data\components\cookies.json',
    'USER_FILE_PATH': str(Path(__file__).parent.parent) + r'\chrome_user_data',
    'COLLECT_TOTAL_DATA': 12
}