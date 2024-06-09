import re
from datetime import datetime, timedelta
import pytz

BEIJING_TZ = pytz.timezone('Asia/Shanghai')

def str_to_datastr(user_input: str):
    now = datetime.now(BEIJING_TZ)
    
    # 匹配“今天”关键字
    if '今天' in user_input:
        match = re.search(r'今天(\d{1,2})点', user_input)
        if match:
            hour = int(match.group(1))
            return now.replace(hour=hour, minute=0, second=0, microsecond=0)
    
    # 匹配“明天”关键字
    if '明天' in user_input:
        match = re.search(r'明天(\d{1,2})点', user_input)
        if match:
            hour = int(match.group(1))
            return (now + timedelta(days=1)).replace(hour=hour, minute=0, second=0, microsecond=0)

    # 匹配“后天”关键字
    if '后天' in user_input:
        match = re.search(r'后天(\d{1,2})点', user_input)
        if match:
            hour = int(match.group(1))
            return (now + timedelta(days=2)).replace(hour=hour, minute=0, second=0, microsecond=0)

    # 匹配具体日期：月-日-小时
    match = re.search(r'(\d{1,2})月(\d{1,2})号(\d{1,2})点', user_input)
    if match:
        month = int(match.group(1))
        day = int(match.group(2))
        hour = int(match.group(3))
        year = now.year
        # 考虑到跨年的情况
        if month < now.month or (month == now.month and day < now.day):
            year += 1
        return now.replace(year=year, month=month, day=day, hour=hour, minute=0, second=0, microsecond=0)
    
    # 匹配“几分钟后”
    match = re.search(r'(\d+)分钟后', user_input)
    if match:
        minutes = int(match.group(1))
        return (now + timedelta(minutes=minutes)).replace(microsecond=0)
    
    # 匹配“几小时后”
    match = re.search(r'(\d+)小时后', user_input)
    if match:
        hours = int(match.group(1))
        return (now + timedelta(hours=hours)).replace(microsecond=0)
    
    # 匹配“几个小时后”
    match = re.search(r'(\d+)个小时后', user_input)
    if match:
        hours = int(match.group(1))
        return (now + timedelta(hours=hours)).replace(microsecond=0)
    
    # 匹配“几天后”
    match = re.search(r'(\d+)天后', user_input)
    if match:
        days = int(match.group(1))
        return (now + timedelta(days=days)).replace(microsecond=0)
    
    # 匹配“几个月后”
    match = re.search(r'(\d+)个月后', user_input)
    if match:
        months = int(match.group(1))
        new_month = now.month + months
        new_year = now.year + (new_month - 1) // 12
        new_month = (new_month - 1) % 12 + 1
        return now.replace(year=new_year, month=new_month, microsecond=0)
    
    return None

if __name__ == '__main__':
    print(str_to_datastr("今天12点"))
    print(str_to_datastr("明天12点"))
    print(str_to_datastr("后天12点"))
    print(str_to_datastr("6月5号12点"))
    print(str_to_datastr("12月31号23点"))
    print(str_to_datastr("1月1号0点"))
    print(str_to_datastr("4月1号1点"))
    print(str_to_datastr("30分钟后"))
    print(str_to_datastr("5小时后"))
    print(str_to_datastr("3天后"))
    print(str_to_datastr("2个月后"))
    print(str_to_datastr("1小时后"))
    print(str_to_datastr("1个小时后"))

