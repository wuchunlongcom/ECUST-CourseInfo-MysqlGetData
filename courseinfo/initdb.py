#!/usr/bin/env python

import os
import django
import datetime
from data.sync_db import syncdb, readWorkbook, syncdb_MysqlGetData

BASE_DIR = os.path.dirname(__file__)


if __name__ == "__main__":
    """
    # 关闭 从classrooms, schedules两个excel中获得数据，写入本工程的数据库sqlite3 
    classroomExcel = os.path.join(BASE_DIR, 'excel', 'classroom.xls')
    classrooms = readWorkbook(classroomExcel)
    scheduleExcel = os.path.join(BASE_DIR, 'excel', 'schedule.xls')
    schedules = readWorkbook(scheduleExcel, x=1)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "courseinfo.settings")
    django.setup()
    from classroom.models import Term

    [i.delete() for i in Term.objects.all()]
    terms = [
        ('2018-2019-1', datetime.date(2018, 9, 1), datetime.date(2018, 9, 1), datetime.date(2019, 1, 15)),
        ('2018-2019-2', datetime.date(2019, 2, 10), datetime.date(2019, 2, 10), datetime.date(2019, 6, 30)),
        ('2019-2020-1', datetime.date(2019, 9, 2), datetime.date(2019, 9, 2), datetime.date(2020, 1, 25)),
        ('2019-2020-2', datetime.date(2020, 1, 26), datetime.date(2020, 2, 10), datetime.date(2020, 6, 30)),
        ('2020-2021-1', datetime.date(2020, 9, 1), datetime.date(2020, 9, 1), datetime.date(2021, 1, 15)),
        ('2020-2021-2', datetime.date(2021, 2, 10), datetime.date(2021, 2, 10), datetime.date(2021, 6, 30))
    ]
    items = [Term(name=i[0], firstMonday=i[1], start=i[2], end=i[3]) for i in terms]
    Term.objects.bulk_create(items, batch_size=20)

    syncdb(classrooms, schedules)
    """
    # 开放从mysql数据库中获得数据，再写入本工程的数据库sqlite3
    syncdb_MysqlGetData()
