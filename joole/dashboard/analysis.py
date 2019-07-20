
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
    return [winter_percent[0] >= 0.68, winter_percent[1] >= 0.68]


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
