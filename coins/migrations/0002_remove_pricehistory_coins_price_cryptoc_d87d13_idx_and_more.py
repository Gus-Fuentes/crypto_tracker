# Generated by Django 4.2.9 on 2025-01-18 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0001_initial'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='pricehistory',
            name='coins_price_cryptoc_d87d13_idx',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='pricehistory',
            name='cryptocurrency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price_history', to='coins.cryptocurrency'),
        ),
        migrations.AddIndex(
            model_name='pricehistory',
            index=models.Index(fields=['cryptocurrency', '-timestamp'], name='coins_price_cryptoc_70ffab_idx'),
        ),
        migrations.AddIndex(
            model_name='pricehistory',
            index=models.Index(fields=['interval', '-timestamp'], name='coins_price_interva_eabc06_idx'),
        ),
    ]
