# Generated by Django 4.1.5 on 2023-01-13 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0003_alter_certificate_expiry_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='number',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='number'),
        ),
    ]
