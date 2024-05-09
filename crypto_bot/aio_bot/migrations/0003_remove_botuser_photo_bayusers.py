# Generated by Django 4.2 on 2024-05-01 23:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aio_bot', '0002_alter_botuser_subscription_end_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='botuser',
            name='photo',
        ),
        migrations.CreateModel(
            name='BayUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='user_photos/', verbose_name='Фото')),
                ('tg_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aio_bot.botuser', verbose_name='Пользователь Telegram')),
            ],
            options={
                'verbose_name': 'Оплата',
                'verbose_name_plural': 'Оплаты',
            },
        ),
    ]
