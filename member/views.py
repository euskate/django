from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from .models import Table2
from django.db.models import Sum, Max, Min, Count, Avg
import random

# django에서 제공하는 User 모델
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as a_login, logout as a_logout


cursor = connection.cursor()

# Create your views here.


def exam_select(request):
    if request.method == 'GET':
        n = request.GET.get("no",0)

        # sum = Table2.objects.raw('SELECT SUM(math) FROM MEMBER_TABLE2')
        print(sum)

        # SELECT SUM(math) FROM MEMBER_TABLE2
        # list = Table2.objects.aggregate(Sum('math'))

        # SELECT NO, NAME FROM MEMBER_TABLE2
        # list = Table2.objects.all().values(['no', 'name'])
        
        # SELECT * FROM MEMBER_TABLE2 ORDER BY name ASC
        # list = Table2.objects.all().order_by('name')
        # list = Table2.objects.raw("SELECT * FROM MEMBER_TABLE2 ORDER BY name ASC")

        # 반별 국어, 영어, 수학 합계
        # SELECT SUM(kor) AS kor, SUM(eng) AS eng, SUM(math) AS math FROM MEMBER_TABLE2 GROUP BY CLASSROOM
        # list = Table2.objects.values('classroom').annotate(kor=Sum('kor'),eng=Sum('eng'),math=Sum('math'))

        list = Table2.objects.all()
        # return render(request, 'member/exam_select.html', {"list":rows}, {"sum":sum})

        # list = Table2.objects.values('classroom').annotate(kor=Sum('kor'),eng=Sum('eng'),math=Sum('math'))   
    
        return render(request, 'member/exam_select.html',{"list":list}) 
    elif request.method == 'POST':
        return redirect('/member/exam_select')

def exam_insert(request):
    if request.method == 'GET':
        return render(request, 'member/exam_insert.html')
    elif request.method == 'POST':
        obj = Table2()
        obj.name = request.POST['name']     # 변수에 값
        obj.kor = request.POST['kor']
        obj.eng = request.POST['eng']
        obj.math = request.POST['math']
        obj.classroom = request.POST['cr']
        obj.save()     
        return redirect('/member/exam_select')

def exam_insert_all(request):
    if request.method == 'GET':
        no = int(request.GET['num'])
        ran = [[random.randint(0, 100) for j in range(3)] for i in range(no)]
        print(ran)
        return render(request, 'member/exam_insert_all.html', {'cnt':range(no), 'ran':ran})
    elif request.method == 'POST':
        na = request.POST.getlist('name[]')
        ko = request.POST.getlist('kor[]')
        en = request.POST.getlist('eng[]')
        ma = request.POST.getlist('math[]')
        cr = request.POST.getlist('cr[]')
        
        objs = []

        for i in range(0, len(na), 1):
            obj = Table2()
            obj.name = na[i]
            obj.kor  = ko[i]
            obj.eng  = en[i]
            obj.math = ma[i]
            obj.classroom = cr[i]
            objs.append(obj)

        # print(objs)
        Table2.objects.bulk_create(objs)
        return redirect("/member/exam_select")

def exam_update_all(request):
    if request.method == 'GET':
        n = request.session['no']
        print(n)
        # SELECT * FROM BOARD_TABLE2 WHERE NO=8 OR NO=5 OR NO=3
        # SELECT * FROM BOARD_TABLE2 WHERE NO IN (8,5,3)
        rows =  Table2.objects.filter(no__in=n)

        return render(request, 'member/exam_update_all.html', {"list":rows})
    elif request.method == 'POST':
        menu = request.POST['menu']
        if menu == '1':
            no = request.POST.getlist("chk[]")
            request.session['no'] = no
            print(no)
            return redirect("/member/exam_update_all")
        elif menu == '2':
            no = request.POST.getlist('no[]')
            na = request.POST.getlist('name[]')
            ko = request.POST.getlist('kor[]')
            en = request.POST.getlist('eng[]')
            ma = request.POST.getlist('math[]')
            cr = request.POST.getlist('cr[]')

            objs = []
            for i in range(0, len(no), 1):
                obj = Table2.objects.get(no=no[i])
                obj.name = na[i]
                obj.kor  = ko[i]
                obj.eng  = en[i]
                obj.math = ma[i]
                obj.classroom = cr[i]
                objs.append(obj)
            Table2.objects.bulk_update(objs, ["name","kor","eng","math","classroom"])
            return redirect("/member/exam_select")

def exam_update(request):
    if request.method == 'GET':
        n = request.GET.get("no",0)
        row = Table2.objects.get(no=n)
        return render(request, 'member/exam_update.html', {"one":row})
    elif request.method == 'POST':
        n = request.POST['no']
        obj = Table2.objects.get(no=n)
        obj.name = request.POST['name']     # 변수에 값
        obj.kor = request.POST['kor']
        obj.eng = request.POST['eng']
        obj.math = request.POST['math']
        obj.classroom = request.POST['cr']

        obj.save()
        return redirect('/member/exam_select')

def exam_delete(request):
    if request.method == 'POST':
        n = request.GET.get("no", 0)
        row = Table2.objects.get(no=n)
        row.delete()
        return redirect('/member/exam_select')



def auth_join(request):
    if request.method == 'GET':
        return render(request, 'member/auth_join.html')
    elif request.method == 'POST':
        id = request.POST['username']
        pw = request.POST['password']
        na = request.POST['first_name']
        em = request.POST['email']

        obj = User.objects.create_user(
            username=id,
            password=pw,
            first_name=na,
            email=em
        )
        obj.save()

        return redirect('/member/auth_index')

def auth_index(request):
    if request.method == 'GET':
        return render(request, 'member/auth_index.html')
    elif request.method == 'POST':
        pass

def auth_login(request):
    if request.method == 'GET':
        return render(request, 'member/auth_login.html')
    elif request.method == 'POST':
        id = request.POST['username']
        pw = request.POST['password']

        # DB에 인증
        obj = authenticate(request, username=id, password=pw)

        if obj:
            # 세션에 추가
            a_login(request, obj)
        return redirect('/member/auth_index')

def auth_logout(request):
    if request.method == 'GET' or request.method == 'POST':
        a_logout(request)
        return redirect('/member/auth_index')

def auth_edit(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return redirect('/member/auth_login')
        obj = User.objects.get(username=request.user)
        return render(request, 'member/auth_edit.html', {"obj":obj})
    elif request.method == 'POST':
        id = request.POST['username']
        na = request.POST['first_name']
        em = request.POST['email']

        obj = User.objects.get(username=id)
        obj.first_name = na
        obj.email = em
        obj.save()
        return redirect('/member/auth_index')

def auth_pw(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return redirect('/member/auth_login')

        return render(request, 'member/auth_pw.html')
    elif request.method == 'POST':
        pw = request.POST['pw'] # 기존 암호
        pw1 = request.POST['pw1'] # 기존 암호
        obj = authenticate(request, username=request.user, password=pw)
        if obj:
            obj.set_password(pw1)
            obj.save()
            return redirect('/member/auth_index')
        return redirect('/member/auth_pw')

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
