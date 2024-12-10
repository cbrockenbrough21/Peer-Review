from django import template
from users.models import ProjectInvitation

register = template.Library()

@register.filter
def dict_key(value, key):
    return value.get(key)

@register.filter
def is_transcribable(file_type):
    transcribable_types = ["audio/mpeg", "audio/mp4", "audio/wav", "audio/flac", "video/mp4"]
    return file_type in transcribable_types

@register.filter
def pending_invites_count(user):
    if user.is_authenticated:
        return ProjectInvitation.objects.filter(invited_user=user, status='PENDING').count()
    return 0

@register.filter
def is_admin(user):
    return user.groups.filter(name='PMA Administrators').exists()