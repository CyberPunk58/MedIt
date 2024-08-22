from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.http import HttpResponse

@login_required
def home(request):
    return render(request, 'home.html')

@permission_required('myapp.special_permission', raise_exception=True)
def special_page(request):
    return render(request, 'special.html')
