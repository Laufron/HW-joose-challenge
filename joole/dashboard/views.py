from django.shortcuts import render, redirect
from django.views.generic import View

from .forms import ClientForm
from .models import Conso_eur, Conso_watt


def client_log(request):
    form = ClientForm(request.POST or None)
    if form.is_valid():
        client_id = form.cleaned_data['client']
        return redirect('dashboard:results', client_id=client_id)

    return render(request, 'dashboard/accueil.html', locals())


def results(request, client_id):
    # indice 0 : 2016; indice 1 : 2017
    conso_euro = [
        Conso_eur.objects.get(client_id=client_id, year__exact=2016),
        Conso_eur.objects.get(client_id=client_id, year__exact=2017)
    ]
    conso_watt = [
        Conso_watt.objects.get(client_id=client_id, year__exact=2016),
        Conso_watt.objects.get(client_id=client_id, year__exact=2017)
    ]

    annual_costs = compute_costs(conso_euro)
    cost_increase = annual_costs[0] <= annual_costs[1]

    elec_heating = is_elec_heating(conso_watt)
    dysfunction_detected = is_dysfunctionning(conso_watt)

    ###################################
    # ----> YOUR CODE GOES HERE <---- #
    ###################################

    context = {
        "conso_euro": conso_euro,
        "conso_watt": conso_watt,
        "annual_costs": annual_costs,
        "is_elec_heating": elec_heating,
        "dysfunction_detected": is_dysfunctionning(conso_watt)
    }
    return render(request, 'dashboard/results.html', context)


def is_elec_heating(conso_watt):
    conso_winter_2016 = conso_watt[0].decembre + conso_watt[0].janvier + conso_watt[0].fevrier + conso_watt[0].mars
    conso_winter_2017 = conso_watt[1].decembre + conso_watt[1].janvier + conso_watt[1].fevrier + conso_watt[1].mars
    conso_winter = [conso_winter_2016, conso_winter_2017]

    conso_summer_2016 = conso_watt[0].juin + conso_watt[0].juillet + conso_watt[0].aout + conso_watt[0].septembre
    conso_summer_2017 = conso_watt[1].juin + conso_watt[1].juillet + conso_watt[1].aout + conso_watt[1].septembre
    conso_summer = [conso_summer_2016, conso_summer_2017]

    winter_percent = [conso_winter[0]/(conso_summer[0]+conso_winter[0]),
                      conso_winter[1]/(conso_summer[1]+conso_winter[1])]

    # Calcul à savoir expliquer; cf photo tel
    return [winter_percent[0] >= 0.62, winter_percent[1] >= 0.62]


def is_dysfunctionning(conso_watt):
    # augmentation de plus de 10% = dysfonctionnement (+3% en France en moyenne) / peut certainement etre diminué
    annual_conso = compute_costs(conso_watt)
    conso_increase = (annual_conso[1]-annual_conso[0])/annual_conso[0]

    return conso_increase >= 0.1


def compute_costs(conso_euro):
    conso_2016 = conso_euro[0]
    cost_2016 = conso_2016.janvier + conso_2016.fevrier + conso_2016.janvier \
                + conso_2016.fevrier + conso_2016.janvier + conso_2016.fevrier \
                + conso_2016.janvier + conso_2016.fevrier + conso_2016.janvier \
                + conso_2016.fevrier + conso_2016.janvier + conso_2016.fevrier

    conso_2017 = conso_euro[1]
    cost_2017 = conso_2017.janvier + conso_2017.fevrier + conso_2017.janvier \
                + conso_2017.fevrier + conso_2017.janvier + conso_2017.fevrier \
                + conso_2017.janvier + conso_2017.fevrier + conso_2017.janvier \
                + conso_2017.fevrier + conso_2017.janvier + conso_2017.fevrier

    return [cost_2016, cost_2017]
