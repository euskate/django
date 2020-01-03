from django.db import models

class Table1(models.Model):
    object  = models.Manager() # vs code 오류 제거용

    no      = models.AutoField(primary_key=True)        # 글 번호
    title   = models.CharField(max_length=200)          # 글 제목
    content = models.TextField()                        # 글 내용
    writer  = models.CharField(max_length=50)           # 작성자
    hit     = models.IntegerField()                     # 조회수
    board_img = models.BinaryField(null=True)                      # 바이너리 필드
    regdate = models.DateTimeField(auto_now_add=True)   # 등록시간

