from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import Review


@receiver(post_save, sender=Review)
def comment_handler(sender, **kwargs):
    """Відображаємо, що в консолі що коментар добавленно"""

    # потім тут буде інша логіка
    if settings.DEBUG:
        print(f'{kwargs["instance"]} saved!')
