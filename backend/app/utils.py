from datetime import datetime, timedelta
import logging
import pytz
from app.models.paste import Paste

local_tz = pytz.timezone("Asia/Bangkok")

logging.basicConfig(
    filename="app.log", 
    level=logging.DEBUG, 
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

def is_expired(paste: Paste) -> bool:
    if paste.expiration == "Never":
        return False
    if paste.expiration == "Burn After Read":
        return paste.views > 0  

    expiration_map = {
        "1 Minute": timedelta(minutes=1), 
        "10 Minutes": timedelta(minutes=10),
        "1 Hour": timedelta(hours=1),
        "1 Day": timedelta(days=1),
        "1 Week": timedelta(weeks=1),
        "2 Weeks": timedelta(weeks=2),
        "1 Month": timedelta(days=30),
        "6 Months": timedelta(days=180),
        "1 Year": timedelta(days=365),
    }

    if paste.expiration in expiration_map:
        created_at_local = local_tz.localize(paste.created_at)  
        logging.info(f"Created at Local: {created_at_local}")
        
        expire_time = created_at_local + expiration_map[paste.expiration]
        logging.info(f"Expire time: {expire_time}")
        
        return datetime.now(local_tz) > expire_time

    return False