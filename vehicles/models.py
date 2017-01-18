from __future__ import unicode_literals
from decimal import Decimal
import uuid as uuid

from django.db import models


def upload_location(instance, filename):
    """
    set upload location and rename the file
    """
    filebase, extension = filename.split('.')
    return '%s/%s.%s' % (instance.id, instance.name, extension)


class CommonInfo(models.Model):
    """
    Abstract models contains mandatory fields on each models.
    Every class can have these fields by instantiate from this class.
    """
    remarks = models.TextField(
        blank=True, verbose_name='Keterangan Tambahan')

    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Waktu Dibuat')
    modified = models.DateTimeField(
        auto_now=True, verbose_name='Waktu diedit')
    status = models.BooleanField(default=True)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    # flag for update, delete, sync and coming from cloud
    is_delete = models.BooleanField(
        default=False, verbose_name='Soft Delete')

    class Meta:
        abstract = True


class VehicleDetails(CommonInfo):
    """
    Vehicles contain name, image, driver, number , and capacity
    """
    class Meta:
        verbose_name = 'Customers'

    name = models.CharField(max_length=30)
    image = models.ImageField(
        upload_to=upload_location,
        null=True,
        blank=True,
        width_field='width_field',
        height_field='height_field'
    )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    driver = models.CharField(max_length=30)
    number = models.IntegerField()
    capacity = models.IntegerField(default=0)

    def __unicode__(self):
        return '{}'.format(self.name)
