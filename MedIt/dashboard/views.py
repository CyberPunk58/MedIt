from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum  # Добавлено для суммирования
from .forms import RevenueForm
from .models import Revenue, Clinic, PaymentType  # Добавлены модели Clinic и PaymentType
from datetime import datetime, timedelta

@login_required
def dashboard_view(request):
    # Получаем текущую дату и дату полугодия назад
    end_date = datetime.today()
    start_date = end_date - timedelta(days=182)

    # Получаем параметры фильтров из GET-запроса
    clinic_filter = request.GET.get('clinic')
    payment_type_filter = request.GET.get('payment_type')
    start_date = request.GET.get('start_date', start_date.strftime('%Y-%m-%d'))
    end_date = request.GET.get('end_date', end_date.strftime('%Y-%m-%d'))

    # Фильтрация данных
    revenues = Revenue.objects.filter(date__range=[start_date, end_date])

    if clinic_filter:
        revenues = revenues.filter(clinic__id=clinic_filter)

    if payment_type_filter:
        revenues = revenues.filter(payment_type__id=payment_type_filter)

    # Группировка данных по дате и суммирование revenue
    revenues_by_date = revenues.values('date').annotate(total_revenue=Sum('revenue')).order_by('date')

    # Подготовка данных для графика
    dates = [entry['date'].strftime('%Y-%m-%d') for entry in revenues_by_date]
    revenue_values = [entry['total_revenue'] for entry in revenues_by_date]

    # Получаем все клиники и типы платежей для фильтров
    clinics = Clinic.objects.all()
    payment_types = PaymentType.objects.all()

    context = {
        'dates': dates,
        'revenue_values': revenue_values,
        'clinic_filter': clinic_filter,
        'payment_type_filter': payment_type_filter,
        'start_date': start_date,
        'end_date': end_date,
        'clinics': clinics,  # Добавлено для списка клиник в фильтре
        'payment_types': payment_types,  # Добавлено для списка типов платежей в фильтре
    }

    return render(request, 'dashboard/dashboard.html', context)

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
