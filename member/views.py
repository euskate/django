from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

cursor = connection.cursor()

# Create your views here.

def index(request):
    # return HttpResponse("index page <hr />") # 이렇게 작업하면 힘들다.
    return render(request, 'member/index.html') # 파일을 만들어 render 한다.

def list(request):
    sql = "SELECT * FROM MEMBER ORDER BY ID ASC"
    cursor.execute(sql)     # sql 문 실행
    data = cursor.fetchall()    # 결과값을 가져옴
    print(type(data))       # list (DB 종류마다 다르다. ex)mySQL의 경우 튜플)
    print(data)             # [( ),( ),...]

    # list.html을 표시하기 전에
    # list변수에 data값을, title변수에 "회원목록" 문자를
    return render(request, 'member/list.html', {"list":data, "title":"회원목록"})

@csrf_exempt    #post로 값을 전달 받는 곳은 필수, 보안상의 이유
def login(request):
    if request.method == 'GET':
        return render(request, 'member/login.html')
    elif request.method == 'POST':
        ar = [request.POST['id'], request.POST['pw']]
        sql = """
            SELECT ID as MEMBER_ID, NAME as MEMBER_NAME FROM MEMBER
            WHERE ID=%s AND PW=%s
            """
        cursor.execute(sql, ar)
        data = cursor.fetchone()
        print(type(data))
        print(data) #('a','b')

        if data:
            request.session['userid'] = data[0]
            request.session['username'] = data[1]
            return redirect('/member/index')

        return redirect('/member/login')

@csrf_exempt    #post로 값을 전달 받는 곳은 필수, 보안상의 이유
def logout(request):
    if request.method == 'GET' or request.method == 'POST':
        del request.session['userid']
        del request.session['username']
        return redirect('/member/index')

@csrf_exempt    #post로 값을 전달 받는 곳은 필수, 보안상의 이유
def join(request):
    if request.method == 'GET':
        return render(request, 'member/join.html')
    elif request.method == 'POST':
        id = request.POST['id']
        na = request.POST['name']
        em = request.POST['email']
        pw = request.POST['pw']

        ar = [id, na, em, pw]   # list로 만듬
        print(ar)
        # DB에 추가함

        # Model을 쓸 경우 사용하지 않는 부분 (DB로 직접 보낸다.)
        sql = """
            INSERT INTO MEMBER(ID,NAME,EMAIL,PW,JOINDATE)
            VALUES (%s, %s, %s, %s, SYSDATE)
            """
        cursor.execute(sql, ar)

        # 크롬에서 127.0.0.1:800/member/index   엔터키를 자동화한 것
        return redirect('/member/index')

@csrf_exempt
def edit(request):
    if request.method == 'GET':
        ar = [ request.session['userid'] ]
        sql = """
            SELECT * FROM MEMBER WHERE ID=%s
        """
        cursor.execute(sql, ar)
        data = cursor.fetchone()
        print(data)
        return render(request, 'member/edit.html', {"one":data})
    elif request.method == 'POST':
        ar = [
            request.POST['name'],
            request.POST['email'],
            request.POST['tel'],
            request.POST['img'],
            request.POST['id']
        ]

        sql = """
            UPDATE MEMBER SET NAME=%s, EMAIL=%s, TEL=%s, IMG=%s
            WHERE ID=%s
            """

        cursor.execute(sql, ar)
        return redirect("/member/index")

@csrf_exempt
def delete(request):
    if request.method == 'GET' or request.method == 'POST':
        ar = [ request.session['userid'] ]
        sql = """DELETE FROM MEMBER WHERE ID=%s"""
        cursor.execute(sql, ar)
        
        return redirect("/member/logout")

    

@csrf_exempt
def join1(request):
    if request.method == 'GET':
        return render(request, 'member/join1.html')
