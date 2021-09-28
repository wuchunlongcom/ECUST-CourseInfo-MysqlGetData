# -*- coding: utf-8 -*-
import time
import datetime

def get_date(n):
    """获得日期字符串
       ...
       n=-2  2019-09-24  上二天
       n=-1  2019-09-25  上一天
       n=0   2019-09-26  当天
       n=1   2019-09-27  后一天
       n=2   2019-09-28  后二天 
       ...  
    """
    return str(datetime.date.today() + datetime.timedelta(days=n))

def get_year_weekday(date_str):
    """date_str:'2019-01-31'
       返回（年号，第几周，星期几）(2019, 5, 4) 
    """
    return datetime.datetime.fromisoformat(date_str).isocalendar()

def get_weekday(date_str):
    """date_str:'2019-01-31'
       返回 星期4
    """
    return datetime.datetime.fromisoformat(date_str).isocalendar()[2]