# Generated by Django 5.0.3 on 2024-09-28 04:57

import library.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0014_alter_issuedbook_expirydate_transactionmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='accession_number',
            field=models.CharField(blank=True, max_length=8, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='book',
            name='published_year',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='quantity',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='issuedbook',
            name='expirydate',
            field=models.DateField(default=library.models.get_expiry),
        ),
    ]
