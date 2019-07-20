from django.shortcuts import render, redirect

from .forms import ClientForm
from .models import Conso_eur, Conso_watt
from .analysis import *


def client_log(request):
    mismatch_message = ''
    form = ClientForm(request.POST or None)
    if form.is_valid():
        client_id = form.cleaned_data['client']
        match_client_query = Conso_watt.objects.filter(client_id=client_id)
        if match_client_query.exists():
            return redirect('dashboard:results', client_id=client_id)
        else:
            mismatch_message = "Désolé ce numéro ne correspond à aucun client..."

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
    annual_costs_dict = {'2016': annual_costs[0], '2017': annual_costs[1]}
    cost_increase = annual_costs[0] <= annual_costs[1]

    elec_heating = is_elec_heating(conso_watt)
    dysfunction_detected = is_dysfunctionning(conso_watt)
    print(dysfunction_detected)

    ###################################
    # ----> YOUR CODE GOES HERE <---- #
    ###################################

    context = {
        "conso_euro_2017": conso_euro[1],
        "conso_watt_2017": conso_watt[1],
        "annual_costs": annual_costs_dict,
        "cost_increase": cost_increase,
        "is_elec_heating": elec_heating,
        "dysfunction_detected": dysfunction_detected
    }
    return render(request, 'dashboard/results.html', context)

