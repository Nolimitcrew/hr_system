from django.shortcuts import render
from django.db.models import Q
from .models import HREvent

def event_global_list(request):
    """Глобальная страница со всеми кадровыми событиями"""
    query = request.GET.get('q', '')
    event_type = request.GET.get('type', '')

    # Берем все события, подтягиваем сотрудников, сортируем по дате (сначала новые)
    events = HREvent.objects.select_related('employee').order_by('-event_date', '-created_at')

    # Фильтр по ФИО или номеру документа
    if query:
        events = events.filter(
            Q(employee__last_name__icontains=query) |
            Q(employee__first_name__icontains=query) |
            Q(document_number__icontains=query)
        )

    # Фильтр по типу события
    if event_type:
        events = events.filter(event_type=event_type)

    context = {
        'events': events,
        'query': query,
        'current_type': event_type,
        'event_types': HREvent.EVENT_TYPES,
    }
    return render(request, 'events/global_list.html', context)