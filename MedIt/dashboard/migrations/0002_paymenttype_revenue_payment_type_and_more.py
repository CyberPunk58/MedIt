# Generated by Django 4.1 on 2024-08-26 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='revenue',
            name='payment_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='dashboard.paymenttype'),
        ),
        migrations.AlterUniqueTogether(
            name='revenue',
            unique_together={('clinic', 'date', 'payment_type')},
        ),
    ]
