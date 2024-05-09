from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *  # Импортируйте модель BotUser из models.py вашего приложения
#1 способ регистрации в админке
class BotUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'tg_id', 'is_paid', 'subscription_end_date', 'is_trial')  # поля, которые будут отображаться в списке
    list_filter = ('is_paid', 'is_trial')  # фильтры по этим полям в панели
    search_fields = ('name', 'tg_id')  # поля, по которым можно проводить поиск

admin.site.register(BotUser, BotUserAdmin)  # Регистрация модели с настройками

#2 способ регистрации в админке
@admin.register(BayUsers)
class BayUsersAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo')
    search_fields = ('tg_id__tg_id',)  # Позволяет искать по ID пользователя в Telegram