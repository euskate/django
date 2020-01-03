from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from base64 import b64encode    # byte 배열을 base64로 변경함

# Create your views here.

cursor = connection.cursor()    #sql문 수행을 위한 cursor 객체

# 127.0.0.1:8000/board/content?no=3
@csrf_exempt
def edit(request):
    return render (request, 'board/edit.html')

@csrf_exempt
def delete(request):
    return render (request, 'board/delete.html')

@csrf_exempt
def content(request):
    if request.method == 'GET':
        no = request.GET.get('no',0)    #프로그램이 꺼지지 않게하는 함수
        if no == 0:
            return redirect("/board/list")
        
        if request.session['hit'] == 1:
            # 조회수 1증가시킴
            sql = """
                UPDATE BOARD_TABLE1 SET HIT=HIT+1
                WHERE NO = %s
            """
            cursor.execute(sql, [no])
            request.session['hit'] = 0
        
        sql = """
            SELECT NVL(MAX(NO), 0)
            FROM board_table1
            WHERE NO < %s
        """
        cursor.execute(sql, [no])
        prev = cursor.fetchone()

        sql = """
            SELECT NVL(MIN(NO), 0)
            FROM board_table1
            WHERE NO > %s
        """
        cursor.execute(sql, [no])
        next = cursor.fetchone()



        # 가져오기
        sql = """
            SELECT
                NO, TITLE, CONTENT, WRITER, HIT, TO_CHAR(REGDATE, 'YYYY-MM-DD HH:MI:SS'), BOARD_IMG
            FROM
                BOARD_TABLE1
            WHERE
                NO = %s
        """
        cursor.execute(sql, [no])
        data = cursor.fetchone()
        # print(data)

        if data[6]:
            img = data[6].read()        #바이트 배열을 img에 넣음
            img64 = b64encode(img).decode("utf-8")
        else:
            file = open('./static/img/default_image.jpg', 'rb')
            img = file.read()
            img64 = b64encode(img).decode("utf-8")

        # print(no)
        return render (request, 'board/content.html', {"one":data, "image":img64, "prev":prev[0], "next":next[0]})

@csrf_exempt
def list(request):
    if request.method == 'GET':
        request.session['hit'] = 1 # 세션에 hit=1

        sql = """
            SELECT
                NO, TITLE, WRITER, HIT, TO_CHAR(REGDATE, 'YYYY-MM-DD HH:MI:SS')
            FROM
                BOARD_TABLE1
            ORDER BY NO DESC
        """

        cursor.execute(sql)
        data = cursor.fetchall()

        # print( type(data) )
        # print( data )           #[(   ), (   )]
        return render (request, 'board/list.html', {"list":data})

@csrf_exempt
def write(request):
    if request.method == 'GET':
        return render (request, 'board/write.html')
    elif request.method == 'POST':
        tmp = None
        if 'img' in request.FILES:
            img = request.FILES['img']  #name값 img
            tmp = img.read()

        arr = [
            request.POST['title'],
            request.POST['contents'],
            request.POST['writer'],
            tmp
        ]

        try:
            # print(arr)
            sql = """
                INSERT INTO BOARD_TABLE1(TITLE, CONTENT, WRITER, HIT, REGDATE, BOARD_IMG)
                VALUES(%s, %s, %s, 234, SYSDATE, %s)
            """
            cursor.execute(sql, arr)
        except Exception as e:
            print(e)

        return redirect("/board/list")
    