from django.db.models import signals, Sum
from django.dispatch import receiver
from supplier.models import Supplier

@receiver(signals.pre_save, sender=Supplier)
def supplier_pre_save(sender, instance, **kwargs):
    if not instance.fantasy_name:
        instance.fantasy_name = instance.corporate_name
    return instance