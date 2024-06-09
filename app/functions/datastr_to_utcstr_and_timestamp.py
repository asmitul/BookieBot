from datetime import datetime
import pytz

def convert_to_utc_and_timestamp(beijing_time_str):
    # 创建一个北京时区的datetime对象
    beijing_tz = pytz.timezone('Asia/Shanghai')
    beijing_time = datetime.strptime(beijing_time_str, '%Y-%m-%d %H:%M:%S%z')
    
    # 转换为UTC时间
    utc_time = beijing_time.astimezone(pytz.utc)
    
    # 转换为时间戳
    timestamp = int(utc_time.timestamp())
    
    return utc_time, timestamp

if __name__ == '__main__':
    beijing_time_str = '2024-05-17 19:23:40+08:00'
    utc_time, timestamp = convert_to_utc_and_timestamp(beijing_time_str)
    print("UTC Time:", utc_time)
    print("Timestamp:", timestamp)
