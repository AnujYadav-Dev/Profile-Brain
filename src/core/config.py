import os
import logging
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Profile-Brain')

@dataclass
class Config:
    access_token: str
    user_name: str
    cache_dir: str
    dark_svg_path: str
    light_svg_path: str
    birth_date: str
    
    @property
    def headers(self) -> dict:
        return {'authorization': f'token {self.access_token}'}

def get_config() -> Config:
    return Config(
        access_token=os.environ.get('ACCESS_TOKEN', ''),
        user_name=os.environ.get('USER_NAME', 'AnujYadav-Dev'),
        cache_dir=os.environ.get('CACHE_DIR', 'cache'),
        dark_svg_path=os.environ.get('DARK_SVG_PATH', 'dark_mode.svg'),
        light_svg_path=os.environ.get('LIGHT_SVG_PATH', 'light_mode.svg'),
        birth_date=os.environ.get('BIRTH_DATE', '')
    )

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'assets', 'templates')
