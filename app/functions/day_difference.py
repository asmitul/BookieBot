from datetime import datetime
import pytz
from dateutil import parser

def datestr_difference(date_str):
    # 获取上海时区
    shanghai_timezone = pytz.timezone('Asia/Shanghai')
    # 获取今天的日期（带上海时区）
    today = datetime.now(shanghai_timezone)

    try:
        # 尝试将字符串转换为带时区信息的日期对象
        given_date = parser.parse(date_str)
    except ValueError:
        # 如果解析失败，返回错误信息
        return "日期格式错误"

    # 如果给定的日期不包含时区信息，则将其设为上海时区
    if given_date.tzinfo is None:
        given_date = shanghai_timezone.localize(given_date)
    else:
        # 如果给定日期包含时区信息，将其转换为上海时区
        given_date = given_date.astimezone(shanghai_timezone)

    # 计算日期差异
    difference = today - given_date

    # 提取天数差异
    days_difference = difference.days

    return days_difference

# 测试代码
print(datestr_difference("2024-05-10"))  # 传递不带时区信息的日期
print(datestr_difference("2024-05-10 17:31:55+00:00"))  # 传递带时区信息的日期
