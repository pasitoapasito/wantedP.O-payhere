# Generated by Django 4.0.6 on 2022-07-13 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_books', '0002_alter_accountbook_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountbookcategory',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='accountbooklog',
            name='title',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
