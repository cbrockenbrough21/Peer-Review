from django.contrib.auth.models import Group
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import UserProfile


@receiver(user_signed_up)
def assign_group(sender, request, user, **kwargs):
    common_user_group, created = Group.objects.get_or_create(name='Common Users')
    user.groups.add(common_user_group)

    # Check if UserProfile already exists
    UserProfile.objects.get_or_create(user=user)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
