from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Department)
admin.site.register(StudentID)
admin.site.register(Student)
admin.site.register(Subject)
from django.db.models import Q,Sum
class SubjectMarksAdmin(admin.ModelAdmin):
    list_display=['student','subject','marks']
admin.site.register(SubjectMarks,SubjectMarksAdmin)
class ReportCardAdmin(admin.ModelAdmin):
    list_display=['student','student_rank','total_marks','date_of_repo_generation']
    ordering=['-student_rank']
    def total_marks(self,obj):
        subject_marks=SubjectMarks.objects.filter(student=obj.student)
        marks=(subject_marks.aggregate(marks=Sum('marks')))
        return marks['marks']

admin.site.register(ReportCard,ReportCardAdmin)
