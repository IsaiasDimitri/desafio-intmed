# Generated by Django 3.2.7 on 2021-10-03 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_medico_especialidade'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='agenda',
            unique_together={('medico', 'dia')},
        ),
    ]