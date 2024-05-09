from django.db import models

from django.db import models

class BotUser(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    # photo = models.ImageField(upload_to='user_photos/', verbose_name="Фото", null=True, blank=True)
    tg_id = models.BigIntegerField(unique=True, verbose_name="ID Telegram")
    is_paid = models.BooleanField(default=False, verbose_name="Оплата")
    subscription_end_date = models.DateTimeField(verbose_name="Дата окончания подписки", null=True, blank=True)
    is_trial = models.BooleanField(default=True, verbose_name="Пробный период")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Пользователь бота"
        verbose_name_plural = "Пользователи бота"


from django.db import models

class BayUsers(models.Model):
    user = models.OneToOneField('BotUser', on_delete=models.CASCADE, verbose_name="Пользователь Telegram", unique=True)
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True, verbose_name="Фото")

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"
    

