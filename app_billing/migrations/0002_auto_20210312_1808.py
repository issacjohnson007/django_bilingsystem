# Generated by Django 3.1.7 on 2021-03-12 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_billing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('billnumber', models.CharField(max_length=12, unique=True)),
                ('bill_date', models.DateField(auto_now=True)),
                ('customer_name', models.CharField(max_length=60)),
                ('phone_number', models.CharField(max_length=12)),
                ('bill_total', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='purchase',
            name='purchase_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.CreateModel(
            name='OrderLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_qty', models.FloatField()),
                ('amount', models.FloatField()),
                ('bill_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_billing.order')),
                ('product_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_billing.items')),
            ],
        ),
    ]
