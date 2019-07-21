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

    # boolean indiquant une augmentation ou une diminution de la facture
    cost_increase = annual_costs[0] <= annual_costs[1]

    # detection du chauffage électrique
    elec_heating = is_elec_heating(conso_watt)

    # la variable dysfunction_detected contient un boolean et la valeur de la variation
    dysfunction_detected = is_dysfunctionning(conso_watt)[1]
    conso_increase = is_dysfunctionning(conso_watt)[0]

    # conso annuelle en kWh
    annual_conso = compute_costs(conso_watt)

    context = {
        "conso_euro_2017": conso_euro[1],
        "conso_watt_2017": conso_watt[1],
        "conso_ete": (conso_watt[1].juin + conso_watt[1].juillet + conso_watt[1].aout)/annual_conso[1]*100,
        "conso_automne": (conso_watt[1].septembre + conso_watt[1].octobre + conso_watt[1].novembre)/annual_conso[1]*100,
        "conso_hiver": (conso_watt[1].decembre + conso_watt[1].janvier + conso_watt[1].fevrier)/annual_conso[1]*100,
        "conso_printemps": (conso_watt[1].mars + conso_watt[1].avril + conso_watt[1].mai)/annual_conso[1]*100,
        "annual_costs": annual_costs_dict,
        "cost_increase": cost_increase,
        'conso_increase': conso_increase*100,
        "is_elec_heating": elec_heating[1],
        "dysfunction_detected": dysfunction_detected
    }
    return render(request, 'dashboard/results.html', context)

