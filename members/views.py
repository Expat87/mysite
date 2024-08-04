from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
#from .forms import RegisterUserForm

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Login success"))
            return redirect('home')
        else:
            messages.success(request, ("Login failed.  Please try again..."))
            return redirect('login')       
    else:
        return render(request, 'authenticate/login.html',
                  {})

def logout_user(request):
    logout(request)
    messages.success(request, ("Successfully Logged Out."))
    return redirect('home')

##def register_user(request):
##    if request.method == "POST":
##        form = RegisterUserForm(request.POST)
##        if form.is_valid():
##            user = form.save()
##            #username = form.cleaned_data['username']
##            #password = form.cleaned_data['password1']
##            user.is_active = False
##            user.save()
##            #user = authenticate(request, username=username, password=password)
##            #login(request, user)
##            messages.success(request, ("Registration successful - awaiting Admin approval"))
##            return redirect('home')
##    else:
##        form = RegisterUserForm()
##    return render(request, 'authenticate/register_user.html', {
##        'form': form,})
##
##def user_list(request):
##    user_count = User.objects.all().count()
##    user_list = User.objects.all().order_by('username')
##    if request.user.is_superuser:
##        return render(request,'authenticate/user_list.html',{
##                 'user_count':user_count,
##                 'user_list':user_list,
##                 })
##    else:
##        messages.success(request, "Only Admin can view this page")
##        return redirect('home')

