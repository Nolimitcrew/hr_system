from django.shortcuts import render
from django.http import HttpResponse
from .models import Department, Position, Profession
from .forms import DepartmentForm, PositionForm, ProfessionForm

def directories_list(request):
    """Главная страница справочников"""
    context = {
        'departments': Department.objects.all().order_by('name'),
        'positions': Position.objects.all().order_by('name'),
        'professions': Profession.objects.all().order_by('name'),
    }
    return render(request, 'directories/list.html', context)

# --- Подразделения ---
def dept_add_modal(request):
    return render(request, 'directories/partials/dept_modal.html', {'form': DepartmentForm()})

def dept_add_submit(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            response = render(request, 'directories/partials/dept_table.html', {'departments': Department.objects.all().order_by('name')})
            response['HX-Trigger'] = 'closeModal'
            return response
        return render(request, 'directories/partials/dept_modal.html', {'form': form})
    return HttpResponse(status=405)

# --- Должности ---
def pos_add_modal(request):
    return render(request, 'directories/partials/pos_modal.html', {'form': PositionForm()})

def pos_add_submit(request):
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            form.save()
            response = render(request, 'directories/partials/pos_table.html', {'positions': Position.objects.all().order_by('name')})
            response['HX-Trigger'] = 'closeModal'
            return response
        return render(request, 'directories/partials/pos_modal.html', {'form': form})
    return HttpResponse(status=405)

# --- Профессии ---
def prof_add_modal(request):
    return render(request, 'directories/partials/prof_modal.html', {'form': ProfessionForm()})

def prof_add_submit(request):
    if request.method == 'POST':
        form = ProfessionForm(request.POST)
        if form.is_valid():
            form.save()
            response = render(request, 'directories/partials/prof_table.html', {'professions': Profession.objects.all().order_by('name')})
            response['HX-Trigger'] = 'closeModal'
            return response
        return render(request, 'directories/partials/prof_modal.html', {'form': form})
    return HttpResponse(status=405)


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import OrganizationSettings
from .forms import OrganizationSettingsForm


def settings_view(request):
    """Страница настроек организации"""
    # Берем первую запись настроек, если её нет — создаем пустую
    settings_obj, created = OrganizationSettings.objects.get_or_create(pk=1)

    if request.method == 'POST':
        form = OrganizationSettingsForm(request.POST, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Настройки успешно сохранены! Если вы изменили порт, перезапустите программу.")
            return redirect('settings_view')
    else:
        form = OrganizationSettingsForm(instance=settings_obj)

    return render(request, 'directories/settings.html', {'form': form})