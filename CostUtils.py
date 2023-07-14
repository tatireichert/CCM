import numpy as np

from CCostParameters import RootParameters, \
    MycorrhizalParameters, \
    PhosphatasesParameters, \
    OrganicAcidsParameters


class CostUtils:

    #### C cost of fine-root Pi foraging ####
    ### Function of soil available Pi pool (sol_pi) ###
    def f_roots(available_p, p_unit):
        return RootParameters.cmin + (RootParameters.cmax - RootParameters.cmin) * np.exp(
            -RootParameters.alpha * (available_p - p_unit))

    #### C cost (kg) of AMF Pi foraging ####
    ### Function of soil available Pi pool (sol_pi) ###
    def f_amf(available_p, p_unit):
        return MycorrhizalParameters.cmin + (MycorrhizalParameters.cmax - MycorrhizalParameters.cmin) * np.exp(
            -MycorrhizalParameters.alpha * (available_p - p_unit))

    #### C cost (kg) of root PME exudation Pi mining ####
    ### Function of soil organic P pool (sol_po) ###
    def f_pase(available_p, p_unit):
        return PhosphatasesParameters.cmin + (PhosphatasesParameters.cmax - PhosphatasesParameters.cmin) * np.exp(
            -PhosphatasesParameters.alpha * (available_p - p_unit))

    #### C cost (kg) of root organic acids exudation Pi mining ####
    ### Depends on soil insoluble Pi pool ###
    def f_oas(available_p, p_unit):
        return OrganicAcidsParameters.cmin + (OrganicAcidsParameters.cmax - OrganicAcidsParameters.cmin) * np.exp(
            -OrganicAcidsParameters.alpha * (available_p - p_unit))
