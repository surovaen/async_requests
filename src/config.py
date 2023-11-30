import os
from pathlib import Path

from dotenv import load_dotenv


dotenv_path = '.env'
load_dotenv(dotenv_path)


class Config:
    """Настройки."""

    FAKE_API = os.environ.get('FAKE_API', 'https://jsonplaceholder.typicode.com/todos/')
    BASE_DIR = Path(__file__).resolve().parent
    RESULT_JSON = Path(BASE_DIR / 'result.json')
    WORKERS = int(os.environ.get('WORKERS', '5'))
    REQUESTS_COUNT = int(os.environ.get('REQUESTS_COUNT', '100'))


Config.RESULT_JSON.touch(exist_ok=True)
