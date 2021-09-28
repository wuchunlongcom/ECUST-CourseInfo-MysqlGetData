from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import os
import datetime

from courseinfo.settings import BASE_DIR
from .models import Campus, Building, Classroom, Term, Course
from myAPI.pageAPI import djangoPage, PAGE_NUM
from myAPI.listAPI import pinyinSort


def _getDateInfo(date):      
    terms = [i for i in Term.objects.all() if i.start <= date <= i.end]    
    if not terms:
        return '','',''  # add
        raise Http404("Term does not exist")    
    term = terms[0]    
    isocalendar = date.isocalendar()
    week = (date - term.firstMonday).days // 7 + 1
    weekday = isocalendar[2]
    #print(date, "-->", term.name, week, weekday) #2020-10-08 --> 2020-2021-1 6 4  (2020/10/8 -- 第 6 周 -- 星期 4 
    return term.name, week, weekday


def index(request):
    return render(request, 'classroom/index.html', context=locals())


def campusInfo(request):
    baseUrl = '/classroominfo'
    campuses = Campus.objects.filter(show_classroom=True).values_list('name', flat=True)
    return render(request, 'classroom/info-campus.html', context=locals())


def buildingInfo(request, campus):
    baseUrl = '/classroominfo'
    buildings = Building.objects.filter(
        campus=campus,
        campus__show_classroom=True,
        show_classroom=True
    ).values_list('name', flat=True)
    buildings = pinyinSort(buildings)
    return render(request, 'classroom/info-building.html', context=locals())


def classroomInfo(request, campus, building):
    cleanData = request.GET.dict()
    date = cleanData.get('date', '').strip()
    try:
        date = datetime.date.fromisoformat(date)
    except Exception as ex:
        # print('err: %s' % ex)
        date = datetime.date.today()
    
    term, week, weekday = _getDateInfo(date)
    
    # add   2020.10.05 有数据
    if not term:
        return render(request, 'classroom/info-classroom.html', context=locals())

    classrooms = Classroom.objects.filter(
        building__campus=campus,
        building__campus__show_classroom=True,
        building__name=building,
        building__show_classroom=True,
        classroomType__show_classroom=True,
        show_classroom=True
    ).order_by("name")

    classroomList = []
    for i in classrooms:
        courses = Course.objects.filter(
            classroom__id=i.id,
            term=term,
            ZC1__lte=week,
            ZC2__gte=week,
            XQ=weekday,
        )
        # print(i, i.id, list(courses))
        courses = list(courses.filter(SJBZ=0)) + list(courses.filter(SJBZ=(week%2)))

        # print(i, [(j, j.KS, j.JS) for j in courses])
        idles = [[j, True] for j in range(1, 13)]
        for j in courses:
            for k in range(j.KS-1, j.JS):
                idles[k] = [k+1, False]
        idles = [['%02d' % x, y] for (x,y) in idles]
        idles = [idles[:4], idles[4:8], idles[8:]]
        classroomList.append((i, idles))

    return render(request, 'classroom/info-classroom.html', context=locals())


def courseInfo(request):
    return render(request, 'classroom/info-course.html', context=locals())


def courseCampus(request):
    baseUrl = '/courseinfo/classroom'
    campuses = Campus.objects.filter(show_schedule=True).values_list('name', flat=True)
    return render(request, 'classroom/info-campus.html', context=locals())


def courseBuilding(request, campus):
    baseUrl = '/courseinfo/classroom'
    buildings = Building.objects.filter(
        campus=campus,
        campus__show_schedule=True,
        show_schedule=True
    ).values_list('name', flat=True)
    buildings = pinyinSort(buildings)
    return render(request, 'classroom/info-building.html', context=locals())


def courseClassroom(request, campus, building):
    baseUrl = '/courseinfo/classroom'
    classrooms = Classroom.objects.filter(
        building__campus=campus,
        building__campus__show_schedule=True,
        building__name=building,
        building__show_schedule=True,
        classroomType__show_schedule=True,
        show_schedule=True,
    ).order_by("name").values_list('name', flat=True)
    return render(request, 'classroom/info-classroom-list.html', context=locals())


def classroomDetails(request, campus, building, classroom): 
    cleanData = request.GET.dict()
    date = cleanData.get('date', '').strip()
    try:
        date = datetime.date.fromisoformat(date)
    except:
        date = datetime.date.today()
    term, week, weekday = _getDateInfo(date)
    
    # add   2020.10.05 有数据
    if not term:
        return render(request, 'classroom/info-classroom-details.html', context=locals())


    room = Classroom.objects.get(
        building__campus=campus,
        building__campus__show_schedule=True,
        building__name=building,
        building__show_schedule=True,
        classroomType__show_schedule=True,
        show_schedule=True,
        name=classroom,
    )

    # print(room.name, room.id)
    if classroom:
        courses = Course.objects.filter(
            classroom__id=room.id,
            term=term,
            ZC1__lte = week,
            ZC2__gte = week,
            XQ=weekday,
        )
        courses = list(courses.filter(SJBZ=0)) + list(courses.filter(SJBZ=(week%2)))
        courses = {(j.KS,j.JS):j for j in courses}
        courses = sorted(courses.values(), key=lambda x: x.name)
        # print(courses)

    mylist = []
    for n in range(0,12):
        mylist.append(['','','',''])

    for model in courses:  
        ks = model.KS
        js = model.JS              
        for n in range(ks-1,js):
            mylist[n] = [model.id, model.name, model.teacher, model.classroom]

    mlist = []
    k = ['j', 'id', 'KCMC', 'TEACHER_NAME', 'CLASSROOM_ID']
    for (index,m) in enumerate(mylist):
        v = ['第%s节'%(index+1)] + m
        d = dict(zip(k,v))
        mlist.append(d)
    return render(request, 'classroom/info-classroom-details.html', context=locals())


def courseDetails(request, id):
    courses = Course.objects.filter(id=id)
    return render(request, 'classroom/info-course-details.html', context=locals())


def courseNameSearch(request, page):
    cleanData = request.GET.dict()
    coursename = cleanData.get('coursename', '').strip()

    queryString = '?'+'&'.join(['%s=%s' % (k,v) for (k,v) in cleanData.items()])
    baseUrl = '/courseinfo/coursename'

    courses = Course.objects.filter()
    if coursename:
        courses = courses.filter(name__icontains = coursename)
    data_list, pageList, num_pages, page = djangoPage(courses, page, PAGE_NUM)
    offset = PAGE_NUM * (page - 1)
    return render(request, 'classroom/search-coursename.html', context=locals())


def teacherNameSearch(request, page):
    cleanData = request.GET.dict()
    teachername = cleanData.get('teachername', '').strip()

    queryString = '?'+'&'.join(['%s=%s' % (k,v) for (k,v) in cleanData.items()])
    baseUrl = '/courseinfo/teachername'

    courses = Course.objects.filter()
    if teachername:
        courses = courses.filter(teacher__name__icontains = teachername)
    data_list, pageList, num_pages, page = djangoPage(courses, page, PAGE_NUM)
    offset = PAGE_NUM * (page - 1)
    return render(request, 'classroom/search-teachername.html', context=locals())


@login_required
def syncdb(request):
    '''
    1. 文件不存在：显示"同步数据库"按钮，点击按钮，创建一个文件
    2. 文件存在：显示"数据库同步中，请稍等..."文本
    '''
    if not request.user.is_superuser:
        return HttpResponseRedirect('/')

    filepath = os.path.join(BASE_DIR, 'data', 'syncdbstatus.txt')
    change_list_template = "classroom/syncdb.html"

    if request.method == 'POST' and not os.path.exists(filepath):
        with open(filepath, 'w+') as fp:
            fp.write('0')

    syncingdb = os.path.exists(filepath)
    return render(request, 'classroom/syncdb.html', context=locals())
