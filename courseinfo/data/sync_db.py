#!/usr/bin/env python

import os
import django
import datetime
import xlrd

def list_sub(list1,list2):
    """
    二个列表相减，序列不发生了变化
    list1 = [[3,4],[5, 6],[1, 2],[7, 8]] 
    list2 = [[3, 4],[7, 8]]
    return： [[5, 6], [1, 2]]
    """
    return  [i for i in list1 if i not in list2] 

# Oracle
def getData(sql):
    import cx_Oracle
    db = cx_Oracle.connect("jw_user", "Hdlgdx18", "172.20.8.37:1521/orcl", encoding="UTF-8")
    cur = db.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    ret = [[j or '' for j in i] for i in result]
    cur.close
    db.close()
    return ret

# mysql
def getMysqlData(sql):
    import pymysql
    db = pymysql.Connect(host="127.0.0.1",
                         user="root",
                         password="12345678",
                         port=3306,
                         db="mystudb",
                         charset="utf8")
    
    cur = db.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    ret = [[j or '' for j in i] for i in result]
    cur.close
    db.close()
    return ret    


def readWorkbook(workbookPath, x=0, index=0):
    ''' 电子表格
        workbookPath: os.path.join(BASE_DIR, 'excel', 'classroom.xls')
        x: 从x行开始 0,1,2...
        index: 工作表序号
    '''

    workbook = xlrd.open_workbook(filename=workbookPath)
    sheet = workbook.sheet_by_index(index)

    myList = []
    for row_num in range(x, sheet.nrows):
        row = sheet.row(row_num)  # row -- [empty:'', empty:'', text:'HZ-616S', number:10000.0]
        v = [r.value.strip() for r in row]
        myList.append(v)

    return myList


def syncdb(classrooms, schedules):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "courseinfo.settings")
    django.setup()
    from django.contrib.auth.models import User, Group, Permission
    if not User.objects.filter(username='admin'):
        user = User.objects.create_superuser('admin', 'admin@test.com', 'admin')
        user.save()

    from classroom.models import Campus, Building, ClassroomType, Classroom, Teacher, Term, Course

    """
    从classrooms, schedules两个列表中获得数据，写入本工程的数据库sqlite3  
    """
    # Import classroom
    items = set(i[4] for i in classrooms) # 从classrooms中获得校区{'徐汇校区', '金山校区', '奉贤校区'}    
    # 下面两条语句，确保校区不会被重复写入到数据库Campus
    [i.delete() for i in Campus.objects.all() if i.name not in items] #  删除数据库Campus记录 （不是校区{'徐汇校区', '金山校区', '奉贤校区'}的记录） 
    items = items - set(Campus.objects.all().values_list('name', flat=True))  # items = {'a','b','c'} - set(['b','c']) --> {'a'}
    items = [Campus(name=i) for i in items]
    Campus.objects.bulk_create(items, batch_size=20)
 
    items = set(i[3] for i in classrooms)
    [i.delete() for i in ClassroomType.objects.all() if i.name not in items]
    items = items - set(ClassroomType.objects.all().values_list('name', flat=True))
    items = [ClassroomType(name=i) for i in items]
    ClassroomType.objects.bulk_create(items, batch_size=20)
 
    items = set((i[4], i[2]) for i in classrooms)
    [i.delete() for i in Building.objects.all() if (i.campus.name, i.name) not in items]
    items = items - set(Building.objects.all().values_list('campus__name', 'name'))
    items = [Building(campus=Campus.objects.get(name=k), name=v) for (k,v) in items]
    Building.objects.bulk_create(items, batch_size=20)
 
    items = {i[0]:i for i in classrooms}
     
    [i.delete() for i in Classroom.objects.all() if i.id not in items]
    items = {i:items[i] for i in set(items)-set(Classroom.objects.all().values_list('id', flat=True))}   
     
    items = [(v, Campus.objects.get(name=v[4])) for (k,v) in items.items()]
 
    items = [(i[0], Building.objects.get(campus=i[1], name=i[0][2])) for i in items] # 添加 Building
    items = [(i[0], i[1], ClassroomType.objects.get(name=i[0][3])) for i in items] # 添加 ClassroomType
    items = [Classroom(id=i[0][0], name=i[0][1], building=i[1], classroomType=i[2]) for i in items]
    Classroom.objects.bulk_create(items, batch_size=20)
 
    # Import schedule
    items = set((i[3], i[4]) for i in schedules)
    [i.delete() for i in Teacher.objects.all() if (i.id, i.name) not in items]
    items = items - set(Teacher.objects.all().values_list('id', 'name'))
    items = [Teacher(id=i[0], name=i[1]) for i in items]
    Teacher.objects.bulk_create(items, batch_size=20)
 
    items = set(i[1] for i in schedules)
    items = items - set(Term.objects.all().values_list('name', flat=True))
    today = datetime.date.today()
    items = [Term(name=i, firstMonday=today, start=today, end=today) for i in items]
    Term.objects.bulk_create(items, batch_size=20)
 
 
    [i.delete() for i in Course.objects.all()]
    items = [i for i in schedules if i[5].isdigit()]
    for i in range(len(items)):
        if items[i][12] and not items[i][13]:
            items[i][13] = items[i][12]
    items = [(
        i, Term.objects.get(name=i[1]), Teacher.objects.get(id=i[3]),
        Classroom.objects.get(id=i[8])) for i in items]
    items = [Course(
        courseid=i[0][0], term=i[1], name=i[0][2], teacher=i[2], CLASS_TIME=i[0][5],
        START_TIME=i[0][6], classroom=i[3], XQ=i[0][9], KS=i[0][10] or 0,
        JS=i[0][11] or 0, ZC1=i[0][12] or 0, ZC2=i[0][13] or 0,
        SJBZ=i[0][14] or 0, showtext=i[0][15] or 0) for i in items]
    Course.objects.bulk_create(items, batch_size=20)


def syncdb_MysqlGetData():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "courseinfo.settings")
    django.setup()
    from django.contrib.auth.models import User, Group, Permission
    if not User.objects.filter(username='admin'):
        user = User.objects.create_superuser('admin', 'admin@test.com', 'admin')
        user.save()

    from classroom.models import Campus, Building, ClassroomType, Classroom, Teacher, Term, Course

    """
    从mysql数据库获得数据，再写入本工程的数据库sqlite3
    """
    # Import Campus
    """
    mysql> select * from classroom_campus;
    +--------------+---------------+----------------+
    | name         | show_schedule | show_classroom |
    +--------------+---------------+----------------+
    | 奉贤校区      |             1 |              1 |
    | 徐汇校区      |             1 |              1 |
    | 金山校区      |             1 |              1 |
    +--------------+---------------+----------------+
    3 rows in set (0.00 sec)      
    """
    # [['奉贤校区', 1, 1], ['徐汇校区', 1, 1], ['金山校区', 1, 1]]
    items = getMysqlData('select * from classroom_campus') 
    items = [i[0] for i in items]     
    # 下面两条语句，确保校区名称是最新的
    [i.delete() for i in Campus.objects.all() if i.name not in items]  
    items = list_sub(items,list(Campus.objects.all().values_list('name', flat=True)))  
    items = [Campus(name=i) for i in items]
    Campus.objects.bulk_create(items, batch_size=20)    
    
    # Import ClassroomType
    """
    mysql> select * from classroom_classroomtype;
    +-----------------+---------------+----------------+
    | name            | show_schedule | show_classroom |
    +-----------------+---------------+----------------+
    | 一般教室         |             1 |              1 |
    ...
    | 语音室           |             1 |              1 |
    +-----------------+---------------+----------------+
    11 rows in set (0.00 sec)    
    """
    items = getMysqlData('select * from classroom_classroomtype')
    items = [i[0] for i in items]  
    [i.delete() for i in ClassroomType.objects.all() if i.name not in items]  
    items = list_sub(items,list(ClassroomType.objects.all().values_list('name', flat=True)))   
    items = [ClassroomType(name=i) for i in items]
    ClassroomType.objects.bulk_create(items, batch_size=20)    

    # Import Building
    """
    mysql> select * from classroom_building;
    +----+-----------------------+---------------+----------------+--------------+
    | id | name                  | show_schedule | show_classroom | campus_id    |
    +----+-----------------------+---------------+----------------+--------------+
    |  1 | 商学院大楼              |             1 |              1 | 徐汇校区      |
    ...
    | 29 | 实验二楼                |             1 |              1 | 奉贤校区      |
    +----+-----------------------+---------------+----------------+--------------+
    29 rows in set (0.00 sec)    
    """
    # [[1, '商学院大楼', 1, 1, '徐汇校区'],...]
    items = getMysqlData('select * from classroom_building') 
    items = [(i[4], i[1]) for i in items]
    [i.delete() for i in Building.objects.all() if (i.campus.name, i.name) not in items]    
    items = list_sub(items,list(Building.objects.all().values_list('campus__name', 'name')))    
    items = [Building(campus=Campus.objects.get(name=i[0]), name=i[1]) for i in items]
    Building.objects.bulk_create(items, batch_size=20)
    

    # Import Teacher
    """
    classroom_teacher;
    +----------------------------------+--------------+
    | id                               | name         |
    +----------------------------------+--------------+
    | 00B0D1A039B84A0A9CEF6FA27F4271C4 | 张凯丽        |
    ...
    | S0036                            | 邱穆青        |
    +----------------------------------+--------------+
    994 rows in set (0.00 sec)    
    """
    items = getMysqlData('select * from classroom_teacher') # [['S0032', '杨薇'],...]]
    items = [(i[0], i[1]) for i in items]
    [i.delete() for i in Teacher.objects.all() if (i.id, i.name) not in items]
    items = list_sub(items,list(Teacher.objects.all().values_list('id', 'name')))  
    items = [Teacher(id=i[0], name=i[1]) for i in items]
    Teacher.objects.bulk_create(items, batch_size=20)

    # Import Term
    """
    mysql> select * from classroom_term;
    +-------------+-------------+------------+------------+
    | name        | firstMonday | start      | end        |
    +-------------+-------------+------------+------------+
    | 2018-2019-1 | 2018-09-01  | 2018-09-01 | 2019-01-15 |
    ...
    | 2020-2021-2 | 2021-02-10  | 2021-02-10 | 2021-06-30 |
    +-------------+-------------+------------+------------+
    6 rows in set (0.00 sec)    
    """
    #[['2018-2019-1', datetime.date(2018, 9, 1)], datetime.date(2019, 01, 15)]]
    items = getMysqlData('select * from classroom_term') 
    items = [i[0] for i in items]
    items = list_sub(items,list(Term.objects.all().values_list('name', flat=True)))  
    today = datetime.date.today()
    items = [Term(name=i, firstMonday=today, start=today, end=today) for i in items] 
    Term.objects.bulk_create(items, batch_size=20)
    
    # Import Classroom
    """
    mysql> select * from classroom_classroom;
    +----------------------------------+--------------+---------------+----------------+-------------+------------------+
    | id                               | name         | show_schedule | show_classroom | building_id | classroomType_id |
    +----------------------------------+--------------+---------------+----------------+-------------+------------------+
    | 017C98D2C9454F17882C62DEAD49D204 | 实四401       |             1 |              1 |          23 | 实验室           |
    ...
    | FD3FF785ADB842F4B6E96620C3099D3A | 实验六楼341    |             1 |              1 |          17 | 实验室           |
    +-------------------------------------------------+---------------+----------------+-------------+------------------+
    606 rows in set (0.00 sec)    
    """ 
                                                            
    classrooms = getMysqlData('select * from classroom_classroom') 
         
    items = {i[0]:i for i in classrooms}     
    [i.delete() for i in Classroom.objects.all() if i.id not in items]        
    items = list_sub(classrooms,list(Classroom.objects.all().values_list()))
 
    items = [Classroom(id=v[0], name=v[1], 
                    building=Building.objects.get(
                        campus=Campus.objects.get(name=Building.objects.get(id=v[4]).campus.name),
                        name=Building.objects.get(id=v[4]).name                       
                        ),                        
                    classroomType=ClassroomType.objects.get(name=v[5])) for v in items]      
    Classroom.objects.bulk_create(items, batch_size=20)


    # Import Course
    """
       0       1             2             3                 4                   5                     6     7    8    9      10    11               12                          13              14
    +------+-------------+-------------+----------------+------------+------------------------------+------+----+----+-----+-----+------+----------------------------------+---------------+-------------+
    | id   | courseid    | name        | CLASS_TIME     | START_TIME | showtext                     | XQ   | KS | JS | ZC1 | ZC2 | SJBZ | classroom_id                     | teacher_id    | term_id     |
    +------+-------------+-------------+----------------+------------+------------------------------+------+----+----+-----+-----+------+----------------------------------+---------------+-------------+
    |    1 | 19113275001 | 制          | 20910          | 3-12|全    | 制药工程专业概论|3-12|虞心红|全|  | 2    |  9 | 10 |   3 |  12 |    0 | 2040206                          | 04053         | 2019-2020-1 |
    ...
    | 7662 |             | 借用        | 503040505060708| 16-16|全   | 借用|16-16|邓自洋|全|图书馆901   | 5    |  3 |  8 |  16 |  16 |    0 | EC1304D4A1C34AB892CB4E4054D0A87E | 07940         | 2019-2020-1 |
    +------+-------------+-------------+---------------+------- ----+-------------------------------+------+----+----+-----+-----+------+----------------------------------+-------------- +-------------+
    7662 rows in set (0.01 sec)
    """
    # [[1, '19113275001', '制药工程专业概论', '20910', '3-12|全', '制药工程专业概论|3-12|虞心红|全|', '2', 9, 10, 3, 12, '', '2040206', '04053', '2019-2020-1'],..]
    items = getMysqlData('select * from classroom_course')
    [i.delete() for i in Course.objects.all()]

    items = [Course(
        courseid=i[1], term=Term.objects.get(name=i[14]), 
        name=i[2], teacher=Teacher.objects.get(id=i[13]), CLASS_TIME=i[3],
        START_TIME=i[4], classroom=Classroom.objects.get(id=i[12]), XQ=i[6], KS=i[7] or 0,
        JS=i[8] or 0, ZC1=i[9] or 0, ZC2=i[10] or 0,
        SJBZ=i[11] or 0, showtext=i[5] or 0) for i in items]
    Course.objects.bulk_create(items, batch_size=20)    
    # items = Course.objects.all().values_list() 
    # print(items[0:2]) 


def main():
    # import os
    # BASE_DIR = os.path.dirname(__file__)
    # classroomExcel = os.path.join(BASE_DIR, 'excel', 'classroom.xls')
    # classrooms = readWorkbook(classroomExcel)
    # scheduleExcel = os.path.join(BASE_DIR, 'excel', 'schedule.xls')
    # schedules = readWorkbook(scheduleExcel, x=1)

    # 从Oracle数据库VIEW_DJZX_CLASSROOM、VIEW_DJZX_SCHEDULE两张表中获得数据，写入本工程的数据库sqlite3  
    classrooms = getData('select * from VIEW_DJZX_CLASSROOM')
    # print(type(classrooms[0]), classrooms[0:10])
    schedules = getData("select * from VIEW_DJZX_SCHEDULE where TERMNAME='2019-2020-1'")       
    # print(type(schedules[0]), schedules[0:10])
    syncdb(classrooms, schedules)

    
if __name__ == "__main__":
    #main()  # 关闭从Oracle数据库获得数据，更新数据
    syncdb_MysqlGetData() # 开放从mysql数据库获得数据，更新数据
    
