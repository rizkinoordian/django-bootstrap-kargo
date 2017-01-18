from django import forms
from django.utils.translation import ugettext_lazy as _
from vehicles.models import VehicleDetails


class VehicleForm(forms.ModelForm):
    """
    Form to manage Vehicle data-entry
    """

    class Meta:
        model = VehicleDetails
        fields = (
            'name',
            'image',
            'driver',
            'number',
            'capacity'
        )
