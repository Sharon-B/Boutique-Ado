from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from.models import OrderLineItem


# update totals on save
@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order_total on lineitem update/create
    """
    instance.order.update_total()


# update totals on delete
@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order_total on lineitem delete
    """
    instance.order.update_total()
