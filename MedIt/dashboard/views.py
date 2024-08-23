from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render

@login_required
def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html')

@permission_required('dashboard.add_data', raise_exception=True)
def dashboard_admin_view(request):
    return render(request, 'dashboard/dashboard_admin.html')
