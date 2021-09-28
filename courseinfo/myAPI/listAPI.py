from decimal import Decimal
from pypinyin import lazy_pinyin

#     拼音排序
#     mylist = ['鑫','鹭','榕','柘','珈','骅','孚','迦','瀚','濮','浔','沱','泸','恺','怡','岷','萃','兖','a','x']
#              ['a', '萃', '孚', '骅', '瀚', '珈', '迦', '恺', '鹭', '泸', '岷', '濮', '榕', '沱', '鑫', '浔', 'x', '怡', '兖', '柘']
#     """

def is_chinese(uchar):
   """判断一个unicode是否是汉字"""
   return uchar >= u'\u4e00' and uchar<=u'\u9fa5'


def is_list_chinese(mylist):
    return any(is_chinese(i) for i in mylist)


def pinyinSort(mylist):
    if is_list_chinese(mylist):
        """如果有中文,按拼音排序"""
        return sorted(mylist, key=lazy_pinyin)
    return sorted(mylist)


def get_sum(mylist):
    '''获得列表元素和 返回浮点数字字符串，保留2位小数。[1,2,3] --> '6.00' '''
    return str(Decimal(sum(mylist)).quantize(Decimal('0.00')))


def get_average(mylist):
    '''获得列表元素平均值 返回浮点数字字符串，保留2位小数。[4,3,4] --> '3.67' '''
    return str(Decimal(sum(mylist)*1.0/(len(mylist))).quantize(Decimal('0.00')))


#单元测试
import unittest
class TestFunc(unittest.TestCase):
    def test_get_sum(self):
        self.assertEqual(get_sum([1,2,3]), '6.00')
    def test_get_value(self):
        self.assertEqual(get_average([4,3,4]), '3.67')
