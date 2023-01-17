from django.shortcuts import render, redirect
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

            if member.password == password:
                request.session['user_pk'] = member.id
                request.session['user_id'] = member.user_id
                return redirect('/')
        
        # 로그인 실패!

    return render(request, 'login.html')