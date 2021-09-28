from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('classroominfo/', views.campusInfo, name='campusInfo'),
    path('classroominfo/<str:campus>/', views.buildingInfo),
    path('classroominfo/<str:campus>/<str:building>/', views.classroomInfo),

    path('courseinfo/', views.courseInfo, name='courseinfo'),
    path('courseinfo/coursename/<int:page>/', views.courseNameSearch),
    path('courseinfo/teachername/<int:page>/', views.teacherNameSearch),
    path('courseinfo/classroom/', views.courseCampus, name='courseinfo/classroom'),
    path('courseinfo/classroom/<str:campus>/', views.courseBuilding),
    path('courseinfo/classroom/<str:campus>/<str:building>/', views.courseClassroom),
    path('courseinfo/classroom/<str:campus>/<str:building>/<str:classroom>/', views.classroomDetails),
    path('courseinfo/<str:id>/', views.courseDetails),

    path('syncdb/', views.syncdb),  # 数据更新中...
]
