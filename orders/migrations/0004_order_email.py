# Generated by Django 4.2.20 on 2025-07-22 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.EmailField(default='noemail@example.com', max_length=254),
            preserve_default=False,
        ),
    ]
