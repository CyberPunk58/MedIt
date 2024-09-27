from django.shortcuts import render
from django.contrib.auth.decorators import permission_required

def stationary_view(request):
    return render(request, 'stationary/stationary.html')

@permission_required('stationary.change_stationary', raise_exception=True)
def stationary_admin_view(request):
    return render(request, 'stationary/stationary_admin.html')