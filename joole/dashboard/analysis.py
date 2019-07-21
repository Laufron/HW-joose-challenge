
def is_elec_heating(conso_watt):
    conso_winter_2016 = conso_watt[0].novembre + conso_watt[0].decembre + conso_watt[0].janvier + conso_watt[0].fevrier
    conso_winter_2017 = conso_watt[1].novembre + conso_watt[1].decembre + conso_watt[1].janvier + conso_watt[1].fevrier
    conso_winter = [conso_winter_2016, conso_winter_2017]

    conso_summer_2016 = conso_watt[0].mai + conso_watt[0].juin + conso_watt[0].juillet + conso_watt[0].aout
    conso_summer_2017 = conso_watt[1].mai + conso_watt[1].juin + conso_watt[1].juillet + conso_watt[1].aout
    conso_summer = [conso_summer_2016, conso_summer_2017]

    winter_percent = [conso_winter[0]/(conso_summer[0]+conso_winter[0]),
                      conso_winter[1]/(conso_summer[1]+conso_winter[1])]

    # Calcul basé sur le fait que le chauffage electrique représente
    # en moyenne 67% de la facture électrique hivernale
    # en considérant qu'en hiver on consomme autant qu'en été sans chauffage électrique

    # Calcul de conso_hiver/conso_totale(ete+hiver)
    # ==> valeur limite calculée : 75% (marge prise pour accepter un rapport de 50% sur la facture --> vl=0.67)
    return [winter_percent[0] >= 0.67, winter_percent[1] >= 0.67]


def is_dysfunctionning(conso_watt):
    # augmentation de plus de 10% = dysfonctionnement (+3% en France en moyenne) / peut certainement etre diminué
    annual_conso = compute_costs(conso_watt)
    conso_increase = (annual_conso[1]-annual_conso[0])/annual_conso[0]

    return [conso_increase, conso_increase >= 0.1]


def compute_costs(tab_conso):
    conso_2016 = tab_conso[0]
    cost_2016 = conso_2016.janvier + conso_2016.fevrier + conso_2016.mars \
                + conso_2016.avril + conso_2016.mai + conso_2016.juin \
                + conso_2016.juillet + conso_2016.aout + conso_2016.septembre \
                + conso_2016.octobre + conso_2016.novembre + conso_2016.decembre

    conso_2017 = tab_conso[1]
    cost_2017 = conso_2017.janvier + conso_2017.fevrier + conso_2017.mars \
                + conso_2017.avril + conso_2017.mai + conso_2017.juin \
                + conso_2017.juillet + conso_2017.aout + conso_2017.septembre \
                + conso_2017.octobre + conso_2017.novembre + conso_2017.decembre

    return [cost_2016, cost_2017]
