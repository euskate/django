import matplotlib.pyplot as plt
from matplotlib import font_manager, rc     # 한글 폰트 적용
# x = list(range(10, 100, 10))
# y = [ 2,3,4,9,2,5,3,4,7]


# plt.bar(x,y)
# plt.title("AGES & PERSON")
# plt.xlabel("AGES")
# plt.ylabel("PERSON")

# plt.show()

font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)
x = ['딸기라떼', '딸기스무디', '딸기스무디Up', '밀크쉐이크', '블루베리스무디', '블루베리요거트스무디', '블루베리요거트스무디Up', '아이스아메리카노', '자바 프라푸치노', '조리퐁쉐이크', '청포도스무디Up', '초코민트자스치노', '초코자바칩 자스치노', '카페모카Hot', '카페모카Ice']
y = [ 1,2,2,2,2,1,2,1,1,1,1,1,1,1,1 ]

plt.bar(x,y)
plt.title("DRINKS & PERSON")
plt.xlabel("DRINKS")
plt.ylabel("PERSON")

plt.show()
