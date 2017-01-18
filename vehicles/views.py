from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import render, redirect

from vehicles.forms import VehicleForm
from vehicles.models import VehicleDetails


def management(request):
    """
    Showing list of vehicle in management home page
    """

    # query on all vehicle records
    vehicles = VehicleDetails.objects.all()

    # structured vehicle into simple dict,
    # later on, in template, we can render it easily, ex: {{ vehicles }}
    data = {'vehicles': vehicles}

    return render(request, 'vehicle/management.html', data)


def create_vehicle(request):
    """
    Handle new vehicle creation
    """

    # Initial form and data
    data = {
        'form': VehicleForm(),
    }

    # if user submit data from this page, we capture the POST data and save it
    if request.method == 'POST':

        # wrap POST data with the form
        form = VehicleForm(request.POST, request.FILES)

        # Transaction savepoint (good to provide rollback data)
        sid = transaction.savepoint()

        print request.POST

        if form.is_valid():

            # wrap form result into dict VehicleDetails model fields structure
            vehicle_data = {
                'name': form.cleaned_data.get('name'),
                'image': form.cleaned_data.get('image'),
                'driver': form.cleaned_data.get('driver'),
                'number': form.cleaned_data.get('number'),
                'capacity': form.cleaned_data.get('capacity'),
            }

            try:
                VehicleDetails.objects.create(**vehicle_data)
            except:
                transaction.savepoint_rollback(sid)
                messages.error(request, "Oops! Something wrong happened!")

            messages.info(request, "A new record has been created!")

    return render(request, 'vehicle/create_vehicle.html', data)


def edit_vehicle(request, uuid=None):
    """
    How to remove vehicle
    """
    if not uuid:
        return redirect(reverse('vehicle:management'))

    # validate given UUID match with record in database
    try:
        vehicle = VehicleDetails.objects.get(uuid=uuid)
    except VehicleDetails.DoesNotExist:
        messages.error(request, "Record not found!")
        return redirect(reverse('vehicle:management'))

    data = {
        'form': VehicleForm(instance=vehicle),
    }

    # if user submit data from this page, we capture the POST data and save it
    if request.method == 'POST':

        # wrap POST data with the form
        form = VehicleForm(request.POST, request.FILES, instance=vehicle)

        # Transaction savepoint (good to provide rollback data)
        sid = transaction.savepoint()

        if form.is_valid():

            try:
                form.save()
            except:
                transaction.savepoint_rollback(sid)
                messages.error(request, "Oops! Something wrong happened!")

            messages.info(request, "Record has been updated!")

    return render(request, 'vehicle/edit_vehicle.html', data)


def delete_vehicle(request, uuid=None):
    """
    How to remove vehicle
    """
    if uuid:

        # finding given UUID to match vehicle in database
        try:
            vehicle = VehicleDetails.objects.get(uuid=uuid)
        except VehicleDetails.DoesNotExist:
            messages.error(request, "vehicle not found")
        else:
            # delete vehicle from database
            vehicle.delete()
            messages.success(
                request, 'vehicle "{}" has been deleted'.format(vehicle.name))

    return redirect(reverse('vehicle:management'))
