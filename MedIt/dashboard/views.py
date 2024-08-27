from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RevenueForm
from .models import Revenue

@login_required
def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html')

@permission_required('dashboard.add_revenue', raise_exception=True)
def dashboard_admin_view(request):
    overwrite = False  # Инициализируем переменную

    if request.method == 'POST':
        form = RevenueForm(request.POST)
        if form.is_valid():
            clinic = form.cleaned_data['clinic']
            date = form.cleaned_data['date']
            payment_type = form.cleaned_data['payment_type']
            revenue = form.cleaned_data['revenue']

            try:
                existing_revenue = Revenue.objects.get(clinic=clinic, date=date, payment_type=payment_type)
                if 'overwrite' in request.POST:
                    existing_revenue.revenue = revenue
                    existing_revenue.save()
                    messages.success(request, 'Запись успешно обновлена.')
                    return redirect('dashboard_admin')
                else:
                    messages.warning(
                        request,
                        f'Запись на {date} для {clinic.name} с типом платежа {payment_type.type} уже существует.'
                    )
                    overwrite = True  # Устанавливаем флаг для отображения кнопки "Перезаписать"
            except Revenue.DoesNotExist:
                form.save()
                messages.success(request, 'Запись успешно добавлена.')
                return redirect('dashboard_admin')
    else:
        form = RevenueForm()

    return render(request, 'dashboard/dashboard_admin.html', {'form': form, 'overwrite': overwrite})
