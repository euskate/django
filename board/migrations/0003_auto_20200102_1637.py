# Generated by Django 3.0.1 on 2020-01-02 07:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_table1_img'),
    ]

    operations = [
        migrations.RenameField(
            model_name='table1',
            old_name='img',
            new_name='model_img',
        ),
    ]
