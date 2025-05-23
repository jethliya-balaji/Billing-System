# Generated by Django 4.2 on 2025-05-01 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0002_product_barcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='purchase_rate',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='barcode',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
