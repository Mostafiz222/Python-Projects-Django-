from faker import Faker
fake =Faker()
import random
from .models import *
from django.db.models import Sum
def seed_db(n=10)->None:
    try:
        for i in range (0,n):
            department_obj=Department.objects.all()
            random_index=random.randint(0,len(department_obj)-1)
            department=department_obj[random_index]
            studentid=f'STU-0{random.randint(100,999)}'
            student_name=fake.name()
            student_email=fake.email()
            student_age=random.randint(20,30)
            student_addr=fake.address()

            student_id_obj=StudentID.objects.create(studentid= studentid)
            stundent_obj=Student.objects.create(
                department=department,
                StudentID=student_id_obj,
                Student_name=student_name,
                Student_email=student_email,
                Student_age=student_age,
                Student_address=student_addr,
            )
    except Exception as e:
        print(e)
def create_sub_marks(n):
    try:
        student_obj=Student.objects.all()
        for student in student_obj:
            subjects=Subject.objects.all()
            for subject in subjects:
                SubjectMarks.objects.create(
                    subject=subject,
                    student=student,
                    marks=random.randint(0,100)
                )
    except Exception as e:
        print(e)

def generate_report_card():
    cur_rank=-1
    i=1
    ranks=Student.objects.annotate(marks=Sum('studentmarks__marks')).order_by('-marks','-Student_age')
    for rank in ranks:
         ReportCard.objects.create(
            student =rank,
            student_rank=i
           )
         i=i+1
