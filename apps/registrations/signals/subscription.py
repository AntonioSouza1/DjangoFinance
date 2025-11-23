from django.db.models import signals
from django.dispatch import receiver
from apps.registrations.models.subscription import Subscription, SubscriptionLog


@receiver(signals.post_save, sender=Subscription)
def create_subscription_log(sender, instance, **kwargs):
    SubscriptionLog.objects.create(subscription=instance)
