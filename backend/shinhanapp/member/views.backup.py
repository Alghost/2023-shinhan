from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password
from .models import Member

# Create your views here.

# 로그인 페이지
# 기능 1: 로그인 화면 출력
# 기능 2: 아이디, 비밀번호 입력받아서 로그인되는것.
def login(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')

        if Member.objects.filter(user_id=user_id).exists():
            member = Member.objects.get(user_id=user_id)

            if check_password(password, member.password):
                request.session['user_pk'] = member.id
                request.session['user_id'] = member.user_id
                return redirect('/')
        
        # 로그인 실패!
    return render(request, 'login.html')

def logout(request):
    if 'user_pk' in request.session:
        del(request.session['user_pk'])
    if 'user_id' in request.session:
        del(request.session['user_id'])

    return redirect('/')

# 회원가입 페이지 노출
# 회원가입 기능 개발
def register(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        age = request.POST.get('age')
        name = request.POST.get('name')

        if not Member.objects.filter(user_id=user_id).exists():
            member = Member(
                user_id=user_id,
                password=make_password(password),
                age=age,
                name=name
            )
            member.save()
            return redirect('/member/login/')

    return render(request, 'register.html')