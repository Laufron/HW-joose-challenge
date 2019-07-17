from django.shortcuts import render, redirect
from django.views.generic import View

from .forms import ClientForm
from .models import Conso_eur, Conso_watt


def client_log(request):

    form = ClientForm(request.POST or None)
    if form.is_valid():
        client_id = form.cleaned_data['client']
        print(type(client_id))
        return redirect('dashboard:results', client_id=client_id)

    return render(request, 'dashboard/accueil.html', locals())


def results(request, client_id):
    conso_euro = [
        Conso_eur.objects.get(client_id=client_id, year__exact=2016),
        Conso_eur.objects.get(client_id=client_id, year__exact=2017)
    ]
    conso_watt = [
        Conso_watt.objects.get(client_id=client_id, year__exact=2016),
        Conso_watt.objects.get(client_id=client_id, year__exact=2017)
    ]
    annual_costs = [0, 0]
    is_elec_heating = True
    dysfunction_detected = False

    ###################################
    # ----> YOUR CODE GOES HERE <---- #
    ###################################

    context = {
         "conso_euro": conso_euro,
         "conso_watt": conso_watt,
         "annual_costs": annual_costs,
         "is_elec_heating": is_elec_heating,
         "dysfunction_detected": dysfunction_detected
    }
    return render(request, 'dashboard/results.html', context)
