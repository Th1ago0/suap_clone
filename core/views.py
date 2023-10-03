from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'pages/home.html')
    
@login_required
def logout_view(request):
    logout(request)
    return redirect('login_view')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST or None)
        if form.is_valid():
            user_code = form.cleaned_data['user_code']
            password = form.cleaned_data['password']
            default_message = 'Por favor, entre com um usuário e senha corretos. Note que ambos os campos diferenciam maiúsculas e minúsculas.'
            try:
                user = authenticate(request, user_code=user_code, password=password)
                if user is not None:
                    login(request, user)
                    #error_message = None
                    return redirect('home')
                else:
                    error_message = default_message
            except User.DoesNotExist:
                error_message = default_message
        else:
            error_message = default_message
    else:
        form = LoginForm()
        error_message = None
    return render(request, 'account/login.html', {'error_message':error_message, 'form':form})

def change_pass(request):
    return render(request, 'account/change_pass.html');