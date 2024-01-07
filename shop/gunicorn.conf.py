import os

from pathlib import Path



BASE_DIR = Path(__file__).resolve().parent

reload = True

bind = '0.0.0.0:8000'

max_request = 1000

workers = 9

accesslog = os.path.join(BASE_DIR, 'logs/access.log')
errorlog = os.path.join(BASE_DIR, 'logs/error.log')




