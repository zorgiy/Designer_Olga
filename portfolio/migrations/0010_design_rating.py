# Generated by Django 4.1 on 2022-09-13 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0009_alter_userdesignrelation_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='design',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=3, null=True),
        ),
    ]
