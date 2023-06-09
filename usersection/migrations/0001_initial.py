# Generated by Django 3.1.5 on 2021-06-28 13:16

from django.db import migrations, models
import encrypted_fields.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('_fullname_data', encrypted_fields.fields.EncryptedCharField(blank=True, default='', max_length=255, null=True)),
                ('fullname', encrypted_fields.fields.SearchField(blank=True, db_index=True, encrypted_field_name='_fullname_data', hash_key='1e3e1246ee77d9eb260ca706e5f30425124a5f1b9084539821e6858842a10ec3', max_length=66, null=True)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('_username_data', encrypted_fields.fields.EncryptedCharField(default=encrypted_fields.fields.SearchField(blank=True, db_index=True, encrypted_field_name='_fullname_data', hash_key='1e3e1246ee77d9eb260ca706e5f30425124a5f1b9084539821e6858842a10ec3', max_length=66, null=True), max_length=100)),
                ('username', encrypted_fields.fields.SearchField(blank=True, db_index=True, encrypted_field_name='_username_data', hash_key='6eb7eea7ee801850ce5e4a79f6856b720d41126a8dd492a4c92788667b551e12', max_length=66, null=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
