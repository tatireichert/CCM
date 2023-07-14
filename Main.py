import os
import pathlib

import numpy as np
import pandas as pd

from CCostModel import CCostModel
from CCostParameters import RootParameters, \
    MycorrhizalParameters, \
    PhosphatasesParameters, \
    OrganicAcidsParameters
from DataPrep import MaxPAccessCalculator, PDemandCalculator
from Figures import Figures

os.chdir(pathlib.Path().resolve())

### BEGIN INPUT VARIABLES ###

data = pd.read_csv("input dataset.csv", encoding="ISO-8859-1")

# Unit of phosphorus
p_unit = 0.03097  # unit of phosphorus uptake (kg) -> 1 mol P = 0.03097 kg

# Change the fertilization value to add it to the soluble Pi pool (Pi in kg)
pi_sol_fertilization = 0

def fertilizatize_pi_sol(kg_p_added):
    data['pi_sol'] = data['pi_sol'] + kg_p_added

def prepare_output(data, results, p_unit):
    data['cost_root'], data['cost_amf'], data['cost_pase'], data['cost_oas'], data['uptake_root'], data['uptake_amf'], \
    data['uptake_pase'], data['uptake_oas'] = zip(*results)

    # Overall total P uptake (kg P ha-1 yr-1)
    data['uptake_total'] = data["uptake_root"] + data["uptake_amf"] + data["uptake_pase"] + data["uptake_oas"]

    # Final Size of the P pools (kg P ha-1 yr-1)
    data['pi_sol_final'] = data['pi_sol'] - (data['uptake_root'] + data['uptake_amf'])
    data['po_sol_final'] = data['po_sol'] - data['uptake_pase']
    data['pi_insol_final'] = data['pi_insol'] - data['uptake_oas']

    # P taken up from each P pool (kg P ha-1 yr-1)
    data['pi_sol_used'] = data['pi_sol'] - data['pi_sol_final']
    data['po_sol_used'] = data['po_sol'] - data['po_sol_final']
    data['pi_insol_used'] = data['pi_insol'] - data['pi_insol_final']

    # Total C cost of P acquisition (kg C ha-1 yr-1)
    data['total_cost'] = data['cost_root'] + data['cost_amf'] + data['cost_pase'] + data['cost_oas']

    # Investment in P acquisition as a % of total NPP (biomass + VOCs)
    data['total_npp'] = data['npp_total'] * 1000  # kg C ha-1 yr-1

    data['total_%npp'] = data['total_cost'] * 100 / data['total_npp']
    data['root_%npp'] = data['cost_root'] * 100 / data['total_npp']
    data['amf_%npp'] = data['cost_amf'] * 100 / data['total_npp']
    data['pase_%npp'] = data['cost_pase'] * 100 / data['total_npp']
    data['oas_%npp'] = data['cost_oas'] * 100 / data['total_npp']

    # Percent of the total C cost per strategy (normalized to 100%)
    data['root_cost%'] = data['cost_root'] * 100 / data['total_cost']
    data['amf_cost%'] = data['cost_amf'] * 100 / data['total_cost']
    data['pase_cost%'] = data['cost_pase'] * 100 / data['total_cost']
    data['oas_cost%'] = data['cost_oas'] * 100 / data['total_cost']

    # C cost (kg C) per unit P acquired
    data['cost_per_p'] = (data['total_cost'] / data['uptake_total']) / (p_unit * 1000)  # p-unit in grams

    # Normalize Unit (kg C ha-1 yr-1)
    data['npp_fr'] = data['npp_fr'] * 1000


def export_csvs(output_file, data):
    data.to_csv(output_file + 'output_full.csv')
    data.to_csv(output_file + 'output_selected.csv',
                columns=['soil_site', 'p_demand', 'total_cost', 'cost_root', 'cost_amf', 'cost_pase',
                         'cost_oas', 'uptake_root', 'uptake_amf', 'uptake_pase', 'uptake_oas', 'uptake_total',
                         'root_%npp', 'amf_%npp', 'pase_%npp', 'oas_%npp', 'total_%npp',
                         'cost_per_p'])


## Run model ##

def main(data, p_unit, pi_sol_fertilization):
    fertilizatize_pi_sol(pi_sol_fertilization)

    PDemandCalculator.calculatePDemand(data)
    MaxPAccessCalculator.calculateMaxPAccess(data)

    results = \
        [CCostModel.calculate_final_cost(p_unit, p_demand, pi_sol, po_sol, pi_insol, access_limit, access_fr,
                                         access_amf)
         for
         p_demand, pi_sol, po_sol, pi_insol, access_limit, access_fr, access_amf in
         zip(data['p_demand'], data['pi_sol'], data['po_sol'], data['pi_insol'], data['access_limit'],
             data['access_fr'], data['access_amf'])]

### Print results ###

    output_file = 'output/'
    if pi_sol_fertilization != 0:
        output_file = 'output_fertilization_' + str(pi_sol_fertilization) + '/'

    output_file = 'output/'
    if not os.path.exists(output_file):
        os.mkdir(output_file)

    prepare_output(data, results, p_unit)

    data = np.round(data, decimals=2)

    export_csvs(output_file, data)

    Figures.plot_figures(data, output_file)

    ### print parameter values used
    PAR = {'CMIN': [RootParameters.cmin, MycorrhizalParameters.cmin, PhosphatasesParameters.cmin,
                    OrganicAcidsParameters.cmin],
           'CMAX': [RootParameters.cmax, MycorrhizalParameters.cmax, PhosphatasesParameters.cmax,
                    OrganicAcidsParameters.cmax],
           'ALPHA': [RootParameters.alpha, MycorrhizalParameters.alpha, PhosphatasesParameters.alpha,
                     OrganicAcidsParameters.alpha]}

    parameters = pd.DataFrame(PAR, columns=['CMIN', 'CMAX', 'ALPHA'], index=['roots', 'amf', 'pase', 'oas'])
    parameters.to_csv(output_file + 'parameters.csv')


main(data, p_unit, pi_sol_fertilization)
