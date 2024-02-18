# Generated by Django 4.2.10 on 2024-02-18 18:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social_network_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=100)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='social_network_app.customuser')),
            ],
        ),
    ]