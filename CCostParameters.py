### COST PARAMETERS ###

## Fine-root Pi foraging
class RootParameters:
    cmin = 0.012  # Default = 0.012 Minimum C cost for the uptake of p_unit (kg C)
    cmax = 35  # Default = 35 Maximum C cost for the uptake of p_unit (kg C)
    alpha = 0.01  # Default = 0.01 Curve decay rate


## Arbuscular Mycorrhizal symbioses
class MycorrhizalParameters:
    cmin = 0.0000012  # Default = 0.0000012 Minimum C cost for the uptake of p_unit (kg C)
    cmax = 25  # Default = 25 Maximum C cost for the uptake of p_unit (kg C)
    alpha = 0.01  # Default = 0.01 Curve decay rate


## Root phosphatase enzyme exudation
class PhosphatasesParameters:
    cmin = 0.000207  # Default = 0.000207 Minimum C cost for the uptake of p_unit (kg C)
    cmax = 45  # Default = 45 Maximum C cost for the uptake of p_unit (kg C)
    alpha = 0.025  # Default = 0.025 Curve decay rate


## Root organic acids exudation
class OrganicAcidsParameters:
    cmin = 0.071  # Default = 0.071 Minimum C cost for the uptake of p_unit (kg C)
    cmax = 40  # Default = 40 Maximum C cost for the uptake of p_unit (kg C)
    alpha = 0.025  # Default = 0.025 Curve decay rate

# C containing in 1 mol of citrate = 71.08 g C
