from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

# Create your views here.
def login_controler(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin')

        else:
            return render(request, 'login.html', {'error':'Credenciales Incorrectos!!'})
    
    return render(request, 'login.html') 

