from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from apps.employees.models import Employee
from .models import Contract
from .forms import ContractForm


def contract_add_modal(request, employee_pk):
    """Возвращает HTML-код модального окна с формой контракта"""
    employee = get_object_or_404(Employee, pk=employee_pk)
    form = ContractForm()
    return render(request, 'contracts/partials/contract_modal.html', {'form': form, 'employee': employee})


def contract_add_submit(request, employee_pk):
    """Обрабатывает отправку формы и возвращает обновленный список контрактов"""
    employee = get_object_or_404(Employee, pk=employee_pk)
    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            contract = form.save(commit=False)
            contract.employee = employee
            contract.save()

            contracts = employee.contracts.all().order_by('-start_date')
            response = render(request, 'contracts/partials/contracts_table.html',
                              {'contracts': contracts, 'employee': employee})
            response['HX-Trigger'] = 'closeModal'
            return response

        return render(request, 'contracts/partials/contract_modal.html', {'form': form, 'employee': employee})

    return HttpResponse(status=405)


def contract_edit_modal(request, contract_pk):
    """Возвращает модальное окно для редактирования контракта"""
    contract = get_object_or_404(Contract, pk=contract_pk)
    form = ContractForm(instance=contract)  # Передаем существующий контракт в форму
    return render(request, 'contracts/partials/contract_edit_modal.html', {'form': form, 'contract': contract})


def contract_edit_submit(request, contract_pk):
    """Обрабатывает редактирование контракта"""
    contract = get_object_or_404(Contract, pk=contract_pk)
    employee = contract.employee

    if request.method == 'POST':
        form = ContractForm(request.POST, instance=contract)
        if form.is_valid():
            form.save()
            # Обновляем таблицу контрактов
            contracts = employee.contracts.all().order_by('-start_date')
            response = render(request, 'contracts/partials/contracts_table.html',
                              {'contracts': contracts, 'employee': employee})
            response['HX-Trigger'] = 'closeModal'
            return response
        return render(request, 'contracts/partials/contract_edit_modal.html', {'form': form, 'contract': contract})
    return HttpResponse(status=405)