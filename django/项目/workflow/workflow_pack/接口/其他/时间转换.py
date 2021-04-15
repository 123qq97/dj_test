#获取当前时间转化为UTC时间格式
import time
import pytz
import datetime


# 当前的本地时间转换为UTC
def local_to_utc( utc_format='%Y-%m-%dT%H:%M:%S.%fZ'):
    #设置utc标准时区为上海
    local_tz = pytz.timezone('Asia/Shanghai')
    #设置时间的格式
    local_format = "%Y-%m-%d %H:%M:%S.%f"
    #获取当前的时间
    time_str = str(datetime.datetime.now())
    #将时间转换为时间数组
    dt = datetime.datetime.strptime(time_str, local_format)
    local_dt = local_tz.localize(dt, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    return utc_dt.strftime(utc_format)

#UTC时间格式转换为普通时间格式
def utc_to_localtime(utc_time):
    # utc="2020-05-12T01:15:56.483Z"
    #转换所需的格式
    UTC_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
    #utc转换普通时间
    now_time=datetime.datetime.strptime(utc_time, UTC_FORMAT)

#当前的本地时间转换为时间戳
def local_to_time_stamp():
    #获取当前时间的时间戳(毫秒)
    time_stamp = int(time.time() * 1000)
    return time_stamp


#时间戳（毫秒）转换为普通时间格式（毫秒）
def time_stamp_to_local(time_stamp):
    # 时间戳(毫秒)转换为日期格式（毫秒）
    d = datetime.datetime.fromtimestamp(float(time_stamp) / 1000)
    #转换为此时间格式显示
    have_time = d.strftime("%Y-%m-%d %H:%M:%S.%f")
    return have_time