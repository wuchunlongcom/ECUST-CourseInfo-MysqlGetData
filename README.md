
### ECUST-CourseInfo-MysqlGetData

```
快速 进入py375  
$ source  /Users/wuchunlong/local/env375/bin/activate
$ cd /Users/wuchunlong/local/github/ECUST-CourseInfo-MysqlGetData/courseinfo
$ ./start.sh

http://localhost:9000/admin/
admin/admin
```

### 主要功能
```
先运行一下工程 ECUST-CourseInfo-ExcelToMysql（$ ./start.sh ）； 确保mysql数据库中有数据；

1、从mysql数据库中获得数据，更新到本例的数据库sqlite3；
2、部署到远程机后，本例的数据库sqlite3与mysql数据库，每分钟同步更新一次；

备注已经关闭的功能：
1、initdb.py
关闭了 从classrooms, schedules两个excel中获得数据，写入本工程的数据库sqlite3；
2、sync_db.py
关闭了 部署到远程机后，本例的数据库sqlite3与Oracle数据库，每分钟同步更新一次；

```
### mysql 常用命令
```
$ mysql -u root -p
mysql> create database studb;  # 创建数据库 一定要有分号；！
mysql> show databases;  # 显示数据库
mysql> use mystudb;   # 使用数据库mystudb   必须！！！
mysql> show tables;  # 显示表
mysql>select * from account_student;  # 显示表数据
mysql> drop database studb; # 删除数据库studb
mysql> quit # 退出

```
### 验证mysql获得的数据
```
(env375) wuchunlongdeMacBook-Pro:courseinfo wuchunlong$ mysql -u root -p
Enter password: 12345678
...
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| mysqldb            |
| mystudb            |
| performance_schema |
| studb              |
| sys                |
| test_db_test       |
+--------------------+
8 rows in set (0.01 sec)

mysql> use mystudb;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> show tables;
+----------------------------+
| Tables_in_mystudb          |
+----------------------------+
| auth_group                 |
| auth_group_permissions     |
| auth_permission            |
| auth_user                  |
| auth_user_groups           |
| auth_user_user_permissions |
| classroom_building         |
| classroom_campus           |
| classroom_classroom        |
| classroom_classroomtype    |
| classroom_course           |
| classroom_teacher          |
| classroom_term             |
| django_admin_log           |
| django_content_type        |
| django_migrations          |
| django_session             |
+----------------------------+
17 rows in set (0.00 sec)

mysql> select * from classroom_campus;
+--------------+---------------+----------------+
| name         | show_schedule | show_classroom |
+--------------+---------------+----------------+
| 奉贤校区     |             1 |              1 |
| 徐汇校区     |             1 |              1 |
| 金山校区     |             1 |              1 |
+--------------+---------------+----------------+
3 rows in set (0.00 sec)

mysql> select * from classroom_building;
+----+-----------------------+---------------+----------------+--------------+
| id | name                  | show_schedule | show_classroom | campus_id    |
+----+-----------------------+---------------+----------------+--------------+
|  1 | 商学院大楼            |             1 |              1 | 徐汇校区     |
|  2 | X                     |             1 |              1 | 奉贤校区     |
|  3 | 三教室                |             1 |              1 | 徐汇校区     |
...
| 28 | 理化楼                |             1 |              1 | 金山校区     |
| 29 | 实验二楼              |             1 |              1 | 奉贤校区     |
+----+-----------------------+---------------+----------------+--------------+
29 rows in set (0.00 sec)

mysql> select * from classroom_classroom;
+----------------------------------+---------------------------+---------------+----------------+-------------+------------------+
| id                               | name                      | show_schedule | show_classroom | building_id | classroomType_id |
+----------------------------------+---------------------------+---------------+----------------+-------------+------------------+
| 017C98D2C9454F17882C62DEAD49D204 | 实四401                   |             1 |              1 |           4 | 实验室           |
|
...
| FC4C726BB28147B5B3B0D0ADEB169FBB | 信息楼505                 |             1 |              1 |           2 | 一般教室         |
| FD3FF785ADB842F4B6E96620C3099D3A | 实验六楼341               |             1 |              1 |          17 | 实验室           |
+----------------------------------+---------------------------+---------------+----------------+-------------+------------------+
606 rows in set (0.00 sec)

mysql> select * from classroom_classroomtype;
+-----------------+---------------+----------------+
| name            | show_schedule | show_classroom |
+-----------------+---------------+----------------+
| 一般教室        |             1 |              1 |
| 体育场          |             1 |              1 |
| 制图室          |             1 |              1 |
| 办公室          |             1 |              1 |
| 多媒体教室      |             1 |              1 |
| 实验室          |             1 |              1 |
| 录像教室        |             1 |              1 |
| 活动中心        |             1 |              1 |
| 电化教室        |             1 |              1 |
| 计算机房        |             1 |              1 |
| 语音室          |             1 |              1 |
+-----------------+---------------+----------------+
11 rows in set (0.00 sec)

mysql> select * from classroom_course;
+------+-------------+-------------+----------------------------+------------+------------------------------+------+----+----+-----+-----+------+----------------------------------+---------------+-------------+
| id   | courseid    | name        | CLASS_TIME                 | START_TIME | showtext                     | XQ   | KS | JS | ZC1 | ZC2 | SJBZ | classroom_id                     | teacher_id    | term_id     |
+------+-------------+-------------+----------------------------+------------+------------------------------+------+----+----+-----+-----+------+----------------------------------+---------------+-------------+
|    1 | 19113275001 | 制          | 20910                      | 3-12|全    | 制药工程专业概论|3-12|虞心红|全|  | 2    |  9 | 10 |   3 |  12 |    0 | 2040206                          | 04053         | 2019-2020-1 |
|    2 | 19110401004 | 化工原理     | 30506                      | 1-17|单    | 化工原理|1-17|吴艳阳|单|         | 3    |  5 |  6 |   1 |  17 |    1 | 2030404                          | 07556         | 2019-2020-1 |
|    3 | 19110401003 | 化工原理     | 10506                      | 1-17|全    | 化工原理|1-17|赵世成|全|         | 1    |  5 |  6 |   1 |  17 |    0 | 2030202                          | 07607         | 2019-2020-1 |
|    4 | 19110736001 | 化工设备设计  | 20506                      | 1-8|全     | 化工设备设计|1-8|周帼彦|全|      | 2    |  5 |  6 |   1 |   8 |    0 | 1070401                          | 07405         | 2019-2020-1 |
...
| 7661 |             | 借用         | 3030405050607081009101112 | 16-16|全   | 借用|16-16|徐书克|全|图书馆901   | 3    |  3 | 12 |  16 |  16 |    0 | EC1304D4A1C34AB892CB4E4054D0A87E | 11157         | 2019-2020-1 |
| 7662 |             | 借用         | 503040505060708           | 16-16|全   | 借用|16-16|邓自洋|全|图书馆901   | 5    |  3 |  8 |  16 |  16 |    0 | EC1304D4A1C34AB892CB4E4054D0A87E | 07940         | 2019-2020-1 |
+------+-------------+-------------+---------------------------+-----------+-------------------------------+------+----+----+-----+-----+------+----------------------------------+-------------- +-------------+
7662 rows in set (0.01 sec)

mysql> 

classroom_teacher;
+----------------------------------+--------------+
| id                               | name         |
+----------------------------------+--------------+
|                                  |              |
| 00B0D1A039B84A0A9CEF6FA27F4271C4 | 张凯丽       |
| 02998                            | 唐颂超       |
...
| S0034                            | 王俊杰       |
| S0036                            | 邱穆青       |
+----------------------------------+--------------+
994 rows in set (0.00 sec)

mysql> select * from classroom_term;
+-------------+-------------+------------+------------+
| name        | firstMonday | start      | end        |
+-------------+-------------+------------+------------+
| 2018-2019-1 | 2018-09-01  | 2018-09-01 | 2019-01-15 |
...
| 2020-2021-2 | 2021-02-10  | 2021-02-10 | 2021-06-30 |
+-------------+-------------+------------+------------+
6 rows in set (0.00 sec)

```

### 问题
```
django.db.utils.IntegrityError: NOT NULL constraint failed: classroom_classroom.building_id
解决方法    
building = models.ForeignKey(Building, on_delete=models.CASCADE) # 增加 null=True, blank=True, default=None
building = models.ForeignKey(Building, on_delete=models.CASCADE, null=True, blank=True, default=None)


2021.09.28
```
