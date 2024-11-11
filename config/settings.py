from pathlib import Path

SETTINGS_DATA = {
    'FIND_ALL_DATA_URL' : "https://affiliate.tiktokglobalshop.com/connection/creator?enter_from=affiliate_find_creators&shop_region=US",
    'DETAIL_DATA_URL' : 'https://affiliate.tiktokglobalshop.com/connection/creator/detail?cid={}',
    'USER_UPLOAD_URL': 'https://affiliate.tiktokglobalshop.com/connection/creator-management?shop_region=US',
    'File_name' : 'request_data',
    'Time_out' : 20,
    'EMAIL' : 'shop09202@woworldtech.com',
    'PASSWORD' : 'bingshui123.',
    'edge_driver_path': r'D:\edge_driver\msedgedriver.exe',
    'USER_FILE_PATH': str(Path(__file__).parent.parent) + r'\edge_user_data',
    'COLLECT_COUNT_DATA': 1500,
    'PAGE_COUNT': 800
}