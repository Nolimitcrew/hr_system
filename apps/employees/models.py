from django.db import models

# Create your models here.
from django.db import models


class Employee(models.Model):
    """Сотрудник организации"""
    # --- Личные данные ---
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    middle_name = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    birth_date = models.DateField(verbose_name="Дата рождения")

    # Идентификационный номер (в РБ это 12 символов)
    inn = models.CharField(max_length=12, unique=True, verbose_name="Идентификационный номер (ИН)")
    passport_series = models.CharField(max_length=10, blank=True, verbose_name="Серия паспорта")
    passport_number = models.CharField(max_length=20, blank=True, verbose_name="Номер паспорта")

    # --- Контакты ---
    address = models.TextField(blank=True, verbose_name="Адрес проживания")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    email = models.EmailField(blank=True, verbose_name="Email")

    # --- Кадровые данные ---
    hire_date = models.DateField(verbose_name="Дата приема")
    dismissal_date = models.DateField(null=True, blank=True, verbose_name="Дата увольнения")

    # Флаг для архива: True = работает, False = уволен (в архиве)
    is_active = models.BooleanField(default=True, verbose_name="Работает в настоящее время")

    # --- Связи со справочниками ---
    department = models.ForeignKey(
        'directories.Department',
        on_delete=models.PROTECT,
        verbose_name="Подразделение",
        related_name='employees'
    )
    position = models.ForeignKey(
        'directories.Position',
        on_delete=models.PROTECT,
        verbose_name="Должность",
        related_name='employees'
    )
    profession = models.ForeignKey(
        'directories.Profession',
        on_delete=models.PROTECT,
        verbose_name="Профессия",
        null=True,
        blank=True,
        related_name='employees'
    )

    # ... (ваши существующие поля hire_date, dismissal_date, is_active) ...

    default_vacation_days = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=24.00,
        verbose_name="Дней отпуска за год (по умолчанию)",
        help_text="Сколько дней отпуска начислять сотруднику за рабочий год (обычно 24)"
    )


    # --- Служебные поля ---
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания записи")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        # Сортировка по фамилии, имени, отчеству
        ordering = ['last_name', 'first_name', 'middle_name']

    def __str__(self):
        # Возвращает ФИО для отображения в админке и выпадающих списках
        return f"{self.last_name} {self.first_name} {self.middle_name}".strip()


class Child(models.Model):
    """Ребенок сотрудника"""
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,  # Если удалить сотрудника, удалятся и его дети
        related_name='children',
        verbose_name="Сотрудник"
    )
    full_name = models.CharField(max_length=200, verbose_name="ФИО ребенка")
    birth_date = models.DateField(verbose_name="Дата рождения")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Ребенок"
        verbose_name_plural = "Дети"
        ordering = ['birth_date']

    def __str__(self):
        return f"{self.full_name} (род. {self.birth_date.strftime('%d.%m.%Y')})"