from django.db.models.signals import post_save, post_delete
from products.models import Product
from django.dispatch import receiver
from .models import Inventory
from datetime import date

@receiver(post_save, sender=Product)
def create_inventory(sender, instance, created, **kwargs):
    if created:
        print('product created')
        new_inventory = Inventory(sfmId=instance.sfmId, style=instance.style, size=instance.size, color=instance.color, inStock=0,
                                  arrivalDate=date.today(), minimum=0, maximum=100)
        new_inventory.save()
        # Profile.objects.create(user=instance)

@receiver(post_delete, sender=Product)
def delete_inventory(sender, instance, using, **kwargs):
    print('product deleted')
    inv = Inventory.objects.get(sfmId=instance.sfmId)
    inv.delete()
