# Generated by Django 5.0 on 2024-02-05 10:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0006_productimages'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProductImages',
            new_name='ProductImage',
        ),
        migrations.RenameField(
            model_name='productimage',
            old_name='images',
            new_name='image',
        ),
    ]