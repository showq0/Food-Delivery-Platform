# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from .utils import push_event, sse_connections, connect_sse
from asgiref.sync import async_to_sync


@receiver(post_save, sender=Order)
def order_status_changed(sender, instance, **kwargs):
    try:
        from dirtyfields import DirtyFieldsMixin
        changed = 'status' in instance.get_dirty_fields()
    except ImportError:
        changed = True

    if changed:
        new_status = instance.status
        if instance.id not in sse_connections:
            connect_sse(instance.id)

        # async_to_sync put status in async queue from sync
        async_to_sync(push_event)(instance.id, new_status)

