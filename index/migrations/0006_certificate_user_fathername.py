# Generated by Django 4.1.5 on 2023-01-14 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0005_certificate_seria_alter_certificate_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='user_fathername',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='fathername'),
        ),
    ]
