from django.db import models


class Department(models.Model):
    """Подразделение (отдел, цех, управление)"""
    name = models.CharField(max_length=150, verbose_name="Название подразделения")
    is_active = models.BooleanField(default=True, verbose_name="Действующее")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделения"
        ordering = ['name']

    def __str__(self):
        return self.name


class Position(models.Model):
    """Должность"""
    name = models.CharField(max_length=150, verbose_name="Название должности")
    is_active = models.BooleanField(default=True, verbose_name="Действующая")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"
        ordering = ['name']

    def __str__(self):
        return self.name


class Profession(models.Model):
    """Профессия (рабочая специальность)"""
    name = models.CharField(max_length=150, verbose_name="Название профессии")
    is_active = models.BooleanField(default=True, verbose_name="Действующая")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Профессия"
        verbose_name_plural = "Профессии"
        ordering = ['name']

    def __str__(self):
        return self.name

class OrganizationSettings(models.Model):
    """Глобальные настройки организации (должна быть только одна запись)"""
    name = models.CharField(max_length=200, verbose_name="Название организации")
    address = models.TextField(blank=True, verbose_name="Юридический адрес")
    telegram_bot_token = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Токен Telegram-бота"
    )
    telegram_chat_id = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="ID чата/канала для уведомлений"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Настройки организации"
        verbose_name_plural = "Настройки организации"

    def __str__(self):
        return self.name