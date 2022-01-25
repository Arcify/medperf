# Generated by Django 4.0 on 2021-12-28 04:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('benchmark', '0001_initial'),
        ('dataset', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='BenchmarkDataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approval_status', models.CharField(choices=[('PENDING', 'PENDING'), ('APPROVED', 'APPROVED'), ('REJECTED', 'REJECTED')], default='PENDING', max_length=100)),
                ('approved_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('benchmark', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='benchmark.benchmark')),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dataset.dataset')),
                ('initiated_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auth.user')),
            ],
            options={
                'ordering': ['modified_at'],
            },
        ),
    ]
