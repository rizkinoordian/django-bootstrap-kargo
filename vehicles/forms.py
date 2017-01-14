from django import forms
from django.utils.translation import ugettext_lazy as _
from vehicles.models import VehicleDetails


class VehicleForm(forms.ModelForm):
    """
    Form to manage Order data-entry
    """

    class Meta:
        model = VehicleDetails
        fields = ('name', 'driver', 'number', 'capacity')
