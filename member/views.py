from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from .models import Table2
from django.db.models import Sum, Max, Min, Count, Avg
import random
import pandas as pd

# django에서 제공하는 User 모델
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as a_login, logout as a_logout

# 그래프 관련
import matplotlib.pyplot as plt
import io       # byte로 변환
import base64   # byte를 base64로 변경
from matplotlib import font_manager, rc     # 한글 폰트 적용


cursor = connection.cursor()

# Create your views here.

def graph_test(request):
    # dataframe을 활용하여 반별 점수 합계 그래프 그리기
    ### 한글 적용  ###
    font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
    rc('font', family=font_name)
    ### 한글 적용 ###

    # 반별 국영수 데이터 가져오기
    sum_cls = Table2.objects.values("classroom").annotate(Sum("kor"), Sum("eng"), Sum("math")).order_by("classroom")
    
    # 데이터프레임으로 형식 변화
    df = pd.DataFrame(sum_cls)
    print(df)
    print(df.columns)
    # x축의 index를 classroom으로 변경
    df = df.set_index('classroom')
    df.plot(kind="bar")
    # setting the title and label 
    plt.title("반별 과목 점수 합계")
    plt.xlabel("반별")
    plt.ylabel("반 점수 합계")
    
    plt.draw()      # 안보이게 그림을 캡쳐
    img = io.BytesIO()    # img에 byte 배열로 보관
    plt.savefig(img, format="png")  # png파일 포맷으로 저장
    img_url = base64.b64encode(img.getvalue()).decode() # 주소 저장
    plt.close() 

    ######### 연습 : 반별인원수 #############
    cnt_cls = Table2.objects.values("classroom").annotate(Count("classroom")).order_by("classroom")
    df2 = pd.DataFrame(cnt_cls)
    print(df2)
    df2 = df2.set_index('classroom')
    df2.plot(kind="bar")
    # plt.bar(x,y)
    plt.title("반별 인원")
    plt.xlabel("반")
    plt.ylabel("인원")

    plt.draw()      # 안보이게 그림을 캡쳐
    img2 = io.BytesIO()    # img에 byte 배열로 보관
    plt.savefig(img2, format="png")  # png파일 포맷으로 저장
    img2_url = base64.b64encode(img2.getvalue()).decode() # 주소 저장
    plt.close() 
    ######### 연습 : 반별인원 #############

    ######### 연습 : 반별평균 #############
    avg_cls = Table2.objects.values("classroom").annotate(Avg("kor"), Avg("eng"), Avg("math")).order_by("classroom")
    df3 = pd.DataFrame(avg_cls)
    # x축의 index를 classroom으로 변경
    df3 = df3.set_index('classroom')
    df3.plot(kind="bar")
    # setting the title and label 
    plt.title("반별 / 과목 평균")
    plt.xlabel("반별")
    plt.ylabel("평균점수")
    
    plt.draw()      # 안보이게 그림을 캡쳐
    img3 = io.BytesIO()    # img에 byte 배열로 보관
    plt.savefig(img3, format="png")  # png파일 포맷으로 저장
    img3_url = base64.b64encode(img3.getvalue()).decode() # 주소 저장
    plt.close() 
    ######### 연습 : 반별평균 #############

    return render(request, 'member/graph_test.html', {"graph1":'data:;base64,{}'.format(img_url), "graph2":'data:;base64,{}'.format(img2_url), "graph3":'data:;base64,{}'.format(img3_url)})

    # x = ['딸기라떼', '딸기스무디', '딸기스무디Up', '밀크쉐이크', '블루베리스무디', '블루베리요거트스무디', '블루베리요거트스무디Up', '아이스아메리카노', '자바 프라푸치노', '조리퐁쉐이크', '청포도스무디Up', '초코민트자스치노', '초코자바칩 자스치노', '카페모카Hot', '카페모카Ice']
    # y = [ 1,2,2,2,2,1,2,1,1,1,1,1,1,1,1 ]

def graph(request):
    # SELECT SUM("kor") FROM MEMBER_TABLE2
    sum_kor = Table2.objects.aggregate(Sum("kor"))
    sum_eng = Table2.objects.aggregate(Sum("eng"))
    sum_math = Table2.objects.aggregate(Sum("math"))

    print(sum_kor, sum_eng, sum_math)
    
    # SELECT SUM("kor") AS kSum FROM MEMBER_TABLE2
    sum_kor_1 = Table2.objects.aggregate(kSum=Sum("kor"))
    print(sum_kor_1)

    # SELECT SUM("kor") AS kSum FROM MEMBER_TABLE2 WHERE CLASSROOM=102
    sum_kor_102 = Table2.objects.filter(classroom='102').aggregate(kSum=Sum("kor"))
    print(sum_kor_102)

    # SELECT SUM("kor") AS kSum FROM MEMBER_TABLE2 WHERE KOR > 80
    # > gt, >= gte, < lt, <=lte
    sum_kor_gt80 = Table2.objects.filter(kor__gt=10).aggregate(kSum=Sum("kor"))
    print(sum_kor_gt80)

    # 반별 합계
    # SELECT SUM("kor") sum1, SUM("eng") sum2, 
    #       SUM("math") sum3
    # FROM MEMBER_TABLE2
    # GROUP BY CLASSROOM
    sum_cls = Table2.objects.values("classroom").annotate(sumK=Sum("kor"), sumE=Sum("eng"), sumM=Sum("math"))
    print(sum_cls)
    print(sum_cls.query)
    li_sum_cls = list(sum_cls)
    print(li_sum_cls)
    
    # SELECT "MEMBER_TABLE2"."CLASSROOM", SUM("MEMBER_TABLE2"."KOR") AS "SUMK", SUM("MEMBER_TABLE2"."ENG") AS "SUME", SUM("MEMBER_TABLE2"."MATH") AS "SUMM" FROM "MEMBER_TABLE2" GROUP BY "MEMBER_TABLE2"."CLASSROOM"

    x = ['국어', '영어', '수학']
    y = [sum_kor['kor__sum'], sum_eng['eng__sum'], sum_math['math__sum']]

    font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
    rc('font', family=font_name)

    ######### 처음 그려본 그래프 세팅 #########
    # x = list(range(10, 100, 10))
    # y = [ 2,3,4,9,2,5,3,4,7]
    
    # plt.title("AGES & PERSON")
    # plt.xlabel("연령대")
    # plt.ylabel("사람수")
    ######### 처음 그려본 그래프 세팅 #########

    plt.bar(x,y)
    plt.title("과목 & 합계")
    plt.xlabel("과목")
    plt.ylabel("합계")

    # plt.show()    # 표시
    plt.draw()      # 안보이게 그림을 캡쳐
    img = io.BytesIO()    # img에 byte 배열로 보관
    plt.savefig(img, format="png")  # png파일 포맷으로 저장
    img_url = base64.b64encode(img.getvalue()).decode()
    plt.close()     # 그래프 종료


    ########## 평균 구하기 ##############
    avg_kor = Table2.objects.aggregate(Avg("kor"))
    avg_eng = Table2.objects.aggregate(Avg("eng"))
    avg_math = Table2.objects.aggregate(Avg("math"))

    print(avg_kor, avg_eng, avg_math)

    avg_x = ['kor', 'eng', 'math']
    avg_y = [avg_kor['kor__avg'], avg_eng['eng__avg'], avg_math['math__avg']]

    plt.bar(avg_x,avg_y)
    plt.title("과목 & 평균")
    plt.xlabel("과목")
    plt.ylabel("평균")
    plt.draw()      # 안보이게 그림을 캡쳐
    avg_img = io.BytesIO()    # img에 byte 배열로 보관
    plt.savefig(avg_img, format="png")  # png파일 포맷으로 저장
    avg_img_url = base64.b64encode(avg_img.getvalue()).decode()
    # plt.close()     # 그래프 종료
    ########## 평균 구하기 ##############

    return render(request, 'member/graph.html', {"graph1":'data:;base64,{}'.format(img_url), "graph2":'data:;base64,{}'.format(avg_img_url)})  

def dataframe(request):
    # SELECT * FROM MEMBER_TABLE2
    # rows = Table2.objects.all()


    # SELECT NO, NAME, KOR FROM MEMBER_TABLE2
    rows = list(Table2.objects.all().values("no", "name", "kor"))[0:10]
    print(rows)
    # print(type(rows))   # QuerySet -> list로 변경
    # 1. QuerySet -> list로 변경 [{  }, {  }, {  } ... ]
    
    # 2. list -> dataframe으로 변경
    df = pd.DataFrame(rows)
    print(df)

    # 2. dataframe -> list로 변경 [[   ], [   ], [   ] ... ]
    rows1 = df.values.tolist()

    print(rows1)
    return render(request, 'member/dataframe.html', {"df_table":df.to_html(),"list":rows})

def js_chart(request):
    str = '100'
    return render(request, 'member/js_chart.html', {"str":str})

def js_index(request):
    return render(request, 'member/js_index.html')
    

def exam_select(request):
    # sum = Table2.objects.raw("SELECT  1 as no, SUM(math) smath FROM MEMBER_TABLE2")
    # print(type(sum))
    # print(sum.columns)
    # print(sum[0].smath)
    #     # SELECT SUM(math) FROM MEMBER_TABLE2 WHERE CLASS_ROOM=101
    # list = Table2.objects.aggregate(Sum('math'))

    # # SELECT NO, NAME FROM MEMBER_TABLE2
    # list = Table2.objects.all().values('no','name')

    # # SELECT * FROM MEMBER_TABLE2 ORDER BY name ASC
    # list = Table2.objects.all().order_by('name')
    # #list = Table2.objects.raw("SELECT * FROM MEMBER_TABLE2 ORDER BY name ASC")

    # # 반별 국어, 영어, 수학 합계
    # # SELECT SUM(kor) AS kor, SUM(eng) AS eng, SUM(math) AS math FROM MEMBER_TABLE2 GROUP BY CLASSROOM
    # list = Table2.objects.values('classroom').annotate(kor=Sum('kor'),eng=Sum('eng'),math=Sum('math'))   
    
    if request.method == 'GET':
        n = request.GET.get("no",0)

        # sum = Table2.objects.raw('SELECT SUM(math) FROM MEMBER_TABLE2')
        # print(sum)

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

        # return render(request, 'member/exam_select.html', {"list":rows}, {"sum":sum})

        # list = Table2.objects.values('classroom').annotate(kor=Sum('kor'),eng=Sum('eng'),math=Sum('math'))   
        
        txt     = request.GET.get("txt","")
        page    = int(request.GET.get("page",1))

        if not txt:   # 검색어가 없는 경우 전체 출력

            # SQL : SELECT * FROM MEMEBER_TALBE2
            list    = Table2.objects.all()[(page-1)*10:page*10]

            # SQL : SELECT COUNT(*) FROM MEMEBER_TALBE2
            cnt     = Table2.objects.all().count()
            tot     = (cnt-1)//10+1
            # 10 => 1
            # 13 => 2
            # 20 => 2
            # 31 => 4
        else:           # 검색어가 있는 경우
            # SELECT * FROM MT2 WHERE name LIKE '%홍길동%'
            list    = Table2.objects.filter(name__contains=txt)[(page-1)*10:page*10]

            # SELECT COUNT(*) FROM MT2 WHERE name LIKE '%홍길동%'
            cnt     = Table2.objects.filter(name__contains=txt).count()
            tot     = (cnt-1)//10+1
    
        return render(request, 'member/exam_select.html', {"list":list, "pages":range(1,tot+1,1)}) 
    # elif request.method == 'POST':
    #     return redirect('/member/exam_select')

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
    if request.method == 'GET':
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

def list1(request):
    sql = "SELECT * FROM MEMBER ORDER BY ID ASC"
    cursor.execute(sql)     # sql 문 실행
    data = cursor.fetchall()    # 결과값을 가져옴
    print(type(data))       # list (DB 종류마다 다르다. ex)mySQL의 경우 튜플)
    print(data)             # [( ),( ),...]

    # list1.html을 표시하기 전에
    # list변수에 data값을, title변수에 "회원목록" 문자를
    return render(request, 'member/list1.html', {"list":data, "title":"회원목록"})

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
