import logging
import datetime
import os
formatter = '[%(asctime)s] %(levelname)8s --- %(message)s (%(filename)s:%(lineno)s)'
logging.basicConfig(
    filename=f'bot-from-{datetime.datetime.now().date()}.log',
    filemode='w',
    format=formatter,
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.WARNING
)

vk_token = 'a056c6b27e410777977abd7cd5ad0d83950a546447eff5b05b28cba07d1f8cd627e9c6c21c8e49bf8b6f3'