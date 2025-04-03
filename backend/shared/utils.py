from datetime import datetime, timedelta
import pytz
from shared.models.paste import Paste

local_tz = pytz.timezone("Asia/Bangkok")

def is_expired(paste: Paste, total_views: int = None) -> bool:
    if paste.expiration == "Never":
        return False
    if paste.expiration == "Burn After Read":
        return total_views > 0 if total_views is not None else paste.views > 0
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
        expire_time = created_at_local + expiration_map[paste.expiration]
        return datetime.now(local_tz) > expire_time
    return False