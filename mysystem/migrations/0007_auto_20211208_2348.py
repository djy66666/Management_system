# Generated by Django 2.2.2 on 2021-12-09 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysystem', '0006_auto_20211208_2346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveyresult',
            name='ans2',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='surveyresult',
            name='ans3',
            field=models.IntegerField(default=0),
        ),
    ]
