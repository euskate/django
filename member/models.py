from django.db import models
from mpmath import clsin

# Create your models here.

# $ python manage.py check
# $ python manage.py makemigrations member
# $ python manage.py migrate member

# 1. 회원을 20명 정도 추가하시오.
#     calssroom ex) 101 102 506 409
# urls.py
# exam_insert
# exam_update
# exam_delete
# exam_select

class Table2(models.Model):
    objects = models.Manager() # vs code 오류 제거용

    no        = models.AutoField(primary_key=True)
    name      = models.CharField(max_length=30)
    kor       = models.IntegerField()
    eng       = models.IntegerField()
    math      = models.IntegerField()
    classroom = models.CharField(max_length=3)
    regdate   = models.DateTimeField(auto_now_add=True)