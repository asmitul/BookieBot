from datetime import datetime
import pytz


def get_beijing_time():
    # 定义北京时区
    beijing_tz = pytz.timezone('Asia/Shanghai')
    
    # 获取当前时间，并转换为北京时区
    beijing_time = datetime.now(beijing_tz)
    
    # 格式化时间
    formatted_time = beijing_time.strftime('%Y-%m-%d %H:%M:%S+08:00')
    
    return formatted_time

if __name__ == '__main__':
    print(get_beijing_time())