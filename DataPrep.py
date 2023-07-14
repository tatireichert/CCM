import numpy as np


class PDemandCalculator:

    def __calculate_wood_p_concentration(data):  # Heinemann et al., 2016
        log_a = 0.0000440582
        log_b = 2.1
        data['wood_p'] = log_a * ((data['leaf_p'] * 1000) ** log_b) / 1000  # P concentration in wood (g/kg)

    def __calculate_wood_cp(data):
        data['wood_cp'] = 500 / data['wood_p']  # 500 g C/kg = 50% --> C conversion factor Malhi et al., 2009

    # Calculation: Leaf P resorption
    def __calculate_leaf_p_resorption(data):
        resorption = 0.65  # 65% resorption efficiency
        data['p_resorption'] = (data['litterfall'] / data['leaf_cp'] * 1000) * resorption

    # Calculation: Canopy P demand (kg P/ha/yr)
    def __calculate_leaf_demand(data):
        data['leaf_demand'] = (data['npp_leaf'] / data['leaf_cp']) * 1000

    # Calculation: Wood P demand (kg P/ha/yr)
    def __calculate_wood_demand(data):
        data['wood_demand'] = (data['npp_wood'] / data['wood_cp'] * 1000)

    # Calculation: Below-ground (roots) P demand (kg P/ha/yr)
    def __calculate_bg_demand(data):
        root_cp = 1701  # mean root C:P ratio in sandy and clayey soils from Tapajós (Silver et al., 2000)
        data['bg_demand'] = (data['npp_bg'] / root_cp) * 1000

    # Total P demand (kg P/ha/yr)
    # p_demand = (leaf_demand + wood_demand + bg_demand)
    def __calculate_total_p_demand(data):
        data['p_demand'] = (data['leaf_demand'] + data['wood_demand'] + data['bg_demand']) - data['p_resorption']

    def calculatePDemand(data):
        PDemandCalculator.__calculate_wood_p_concentration(data)
        PDemandCalculator.__calculate_wood_cp(data)
        PDemandCalculator.__calculate_leaf_p_resorption(data)
        PDemandCalculator.__calculate_leaf_demand(data)
        PDemandCalculator.__calculate_wood_demand(data)
        PDemandCalculator.__calculate_bg_demand(data)
        PDemandCalculator.__calculate_total_p_demand(data)


class MaxPAccessCalculator:

    def __calculate_access_limit(data):
        sum_pools = data['pi_sol'] + data['pi_insol'] + data['po_sol']

        # P uptake limit from each P pool
        data['access_limit'] = (data['p_demand'] / sum_pools)

    # Modeling P uptake via fine roots vs. via AMF
    # Access to Pi_sol via roots increases with root length

    def __calculate_access_fr(data):
        beta_access = 0.3
        data['access_fr'] = 1 - np.exp(-beta_access * data['frld'])

    def __calculate_access_amf(data):
        data['access_amf'] = 1 - data['access_fr']

    def calculateMaxPAccess(data):
        MaxPAccessCalculator.__calculate_access_limit(data)
        MaxPAccessCalculator.__calculate_access_fr(data)
        MaxPAccessCalculator.__calculate_access_amf(data)
