# Generated by Django 4.1.5 on 2023-01-15 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0008_certificate_permission_alter_worker_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='worker',
            name='branch',
        ),
        migrations.RemoveField(
            model_name='worker',
            name='department',
        ),
        migrations.RemoveField(
            model_name='worker',
            name='position',
        ),
        migrations.AlterField(
            model_name='worker',
            name='status',
            field=models.CharField(choices=[('null', "Noma'lum"), ('0', 'Admin'), ('1', 'Leader'), ('2', 'HeadLeader')], default='null', max_length=10, verbose_name='Nomalum'),
        ),
        migrations.DeleteModel(
            name='Branch',
        ),
        migrations.DeleteModel(
            name='Department',
        ),
    ]
