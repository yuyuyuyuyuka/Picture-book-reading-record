from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Family

User = get_user_model()

@receiver(post_save, sender=User)
def create_family(sender, instance, created, **kwargs):
    if created:
        family = Family.objects.create()
        instance.family_id = family
        instance.save()