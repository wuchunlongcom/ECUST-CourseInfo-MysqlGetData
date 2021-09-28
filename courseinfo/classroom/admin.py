from django.contrib import admin

from .models import Campus, Building, ClassroomType, Classroom, Teacher, Term, Course


@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
    list_display = ('name', 'show_schedule', 'show_classroom')
    list_editable = ['show_schedule', 'show_classroom']


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('campus', 'name', 'show_schedule', 'show_classroom')
    list_editable = ['show_schedule', 'show_classroom']


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'building', 'name', 'classroomType', 'show_schedule',
        'show_classroom')
    list_editable = ['show_schedule', 'show_classroom']


@admin.register(ClassroomType)
class ClassroomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'show_schedule', 'show_classroom')
    list_editable = ['show_schedule', 'show_classroom']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ('name', 'firstMonday', 'start', 'end')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'courseid', 'name', 'teacher', 'term', 'classroom', 'CLASS_TIME',
        'START_TIME', 'XQ', 'KS', 'JS', 'ZC1', 'ZC2', 'SJBZ', 'showtext')
