# Generated by Django 5.0.3 on 2024-09-25 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0011_alter_book_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.CharField(choices=[('Education', 'Education'), ('Entertainment', 'Entertainment'), ('Comics', 'Comics'), ('Biography', 'Biographie'), ('History', 'History'), ('Romantic', 'Romantic'), ('Manipulation', 'Manipulation'), ('Fantacy', 'Fantacy')], default='Education', max_length=30),
        ),
    ]
