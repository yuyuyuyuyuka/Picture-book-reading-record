# Generated by Django 5.1.7 on 2025-03-31 12:07

import accounts.models
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invite_token', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('expiry_date', models.DateTimeField(default=accounts.models.Invitation.get_expiry_data)),
                ('used', models.IntegerField(choices=[(0, '未使用'), (1, '使用済み'), (2, '期限切れ')], default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('family_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='family_invitations', to='accounts.family')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_invitations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
