import plotly.express as px
import plotly.io as pio
from datetime import datetime, timedelta
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RevenueForm
from .models import Revenue
from .models import Clinic, PaymentType
from django.contrib.auth.decorators import permission_required
from .models import KnowledgeBaseSection, KnowledgeBaseArticle
from .forms import KnowledgeBaseSectionForm, KnowledgeBaseArticleForm
from django.shortcuts import get_object_or_404


import plotly.express as px
import plotly.io as pio

def generate_graph_html(dates, revenue_values):
    # Создаем график с помощью Plotly
    fig = px.line(x=dates, y=revenue_values, labels={'x': 'Дата', 'y': 'Доход'}, title='Доход по дням')

    # Возвращаем HTML код графика
    graph_html = pio.to_html(fig, full_html=False)
    return graph_html

@login_required
def dashboard_view(request):
    # Устанавливаем текущую дату и дату за полгода назад по умолчанию
    end_date = datetime.today()
    start_date = end_date - timedelta(days=182)

    # Получаем параметры фильтров из GET-запроса (или используем значения по умолчанию)
    clinic_filter = request.GET.get('clinic', '')
    payment_type_filter = request.GET.get('payment_type', '')
    start_date = request.GET.get('start_date', start_date.strftime('%Y-%m-%d'))
    end_date = request.GET.get('end_date', end_date.strftime('%Y-%m-%d'))

    # Преобразуем даты в нужный формат
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

    # Фильтрация данных
    revenues = Revenue.objects.filter(date__range=[start_date_obj, end_date_obj])

    # Применяем фильтр по клинике, если выбран
    if clinic_filter:
        revenues = revenues.filter(clinic__id=clinic_filter)

    # Применяем фильтр по виду оплаты, если выбран
    if payment_type_filter:
        revenues = revenues.filter(payment_type__id=payment_type_filter)

    # Группировка данных по дате и суммирование доходов
    revenues_by_date = revenues.values('date').annotate(total_revenue=Sum('revenue')).order_by('date')

    # Подготовка данных для графика
    dates = [entry['date'].strftime('%Y-%m-%d') for entry in revenues_by_date]
    revenue_values = [entry['total_revenue'] for entry in revenues_by_date]

    # Генерация графика
    graph_html = generate_graph_html(dates, revenue_values)

    # Получение всех клиник и типов оплат для фильтров
    clinics = Clinic.objects.all()
    payment_types = PaymentType.objects.all()

    context = {
        'dates': dates,
        'revenue_values': revenue_values,
        'clinic_filter': clinic_filter,  # Передаем выбранный фильтр
        'payment_type_filter': payment_type_filter,  # Передаем выбранный фильтр
        'start_date': start_date,  # Передаем выбранную начальную дату
        'end_date': end_date,  # Передаем выбранную конечную дату
        'clinics': clinics,  # Передаем список клиник в шаблон
        'payment_types': payment_types,  # Передаем список типов оплат
        'graph_html': graph_html  # Передаем HTML графика в шаблон
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

def knowledge_base_view(request):
    sections = KnowledgeBaseSection.objects.all()
    return render(request, 'knowledge_base/knowledge_base.html', {'sections': sections})

def add_section_view(request):
    if request.method == 'POST':
        form = KnowledgeBaseSectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('knowledge_base')
    else:
        form = KnowledgeBaseSectionForm()
    return render(request, 'knowledge_base/add_section.html', {'form': form})

from django.shortcuts import render, redirect
from .forms import KnowledgeBaseArticleForm

def add_article_view(request):
    if request.method == 'POST':
        form = KnowledgeBaseArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('knowledge_base')
    else:
        form = KnowledgeBaseArticleForm()
    return render(request, 'knowledge_base/add_article.html', {'form': form})

def view_article(request, id):
    article = get_object_or_404(KnowledgeBaseArticle, id=id)
    return render(request, 'knowledge_base/view_article.html', {'article': article})

def edit_article_view(request, id):
    article = get_object_or_404(KnowledgeBaseArticle, id=id)
    if request.method == 'POST':
        form = KnowledgeBaseArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('view_article', id=article.id)
    else:
        form = KnowledgeBaseArticleForm(instance=article)
    return render(request, 'knowledge_base/edit_article.html', {'form': form, 'article': article})

def stationary_view(request):
    return render(request, 'stationary/stationary.html')

@permission_required('dashboard.add_stationary_data', raise_exception=True)
def stationary_admin_view(request):
    return render(request, 'stationary/stationary_admin.html')