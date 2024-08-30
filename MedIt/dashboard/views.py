import plotly.express as px
import plotly.io as pio
from datetime import datetime, timedelta
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RevenueForm
from .models import Revenue
from django.contrib.auth.decorators import permission_required
from .models import KnowledgeBaseSection, KnowledgeBaseArticle
from .forms import KnowledgeBaseSectionForm, KnowledgeBaseArticleForm


@login_required
def dashboard_view(request):
    # Получаем текущую дату и дату полугодия назад
    end_date = datetime.today()
    start_date = end_date - timedelta(days=365)

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
    dates = [entry['date'] for entry in revenues_by_date]
    revenue_values = [entry['total_revenue'] for entry in revenues_by_date]

    # Создание интерактивного графика с помощью Plotly
    fig = px.line(x=dates, y=revenue_values, labels={'x': 'Дата', 'y': 'Выручка'},
                  title='Выручка за период', markers=True)

    fig.update_traces(mode='lines+markers', hoverinfo='text+name', marker=dict(size=8))

    graph_html = pio.to_html(fig, full_html=False)

    context = {
        'graph_html': graph_html,
        'clinic_filter': clinic_filter,
        'payment_type_filter': payment_type_filter,
        'start_date': start_date,
        'end_date': end_date,
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

def add_article_view(request):
    if request.method == 'POST':
        form = KnowledgeBaseArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('knowledge_base')
    else:
        form = KnowledgeBaseArticleForm()
    return render(request, 'knowledge_base/add_article.html', {'form': form})
