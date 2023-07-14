from enum import Enum, auto

from CostUtils import CostUtils


class Pool(Enum):
    PI_SOL = 'pi_sol'
    PO_SOL = 'po_sol'
    PI_INSOL = 'pi_insol'


def get_lower_cost_strategy(strategy_cost):
    positive_costs = dict(filter(lambda item: item[1] > 0, strategy_cost.items()))
    if len(positive_costs) == 0:
        raise Exception('All pools are emtpy', strategy_cost)

    return min(positive_costs.items(), key=lambda item: item[1])


class Strategy(Enum):
    ROOT = (auto(), Pool.PI_SOL, lambda p_available, p_unit: CostUtils.f_roots(p_available, p_unit))
    AMF = (auto(), Pool.PI_SOL, lambda p_available, p_unit: CostUtils.f_amf(p_available, p_unit))
    PASE = (auto(), Pool.PO_SOL, lambda p_available, p_unit: CostUtils.f_pase(p_available, p_unit))
    OAS = (auto(), Pool.PI_INSOL, lambda p_available, p_unit: CostUtils.f_oas(p_available, p_unit))

    def __new__(cls, value, pool, get_cost_per_strategy):
        entry = object.__new__(cls)
        entry._value_ = value
        entry.pool = pool
        entry.get_cost_per_strategy = get_cost_per_strategy
        return entry


class CCostModel:

    def calculate_final_cost(p_unit, p_demand, pi_sol, po_sol, pi_insol, access_limit, access_fr, access_amf):
        final_cost = {
            Strategy.ROOT: 0,
            Strategy.AMF: 0,
            Strategy.PASE: 0,
            Strategy.OAS: 0,
        }
        p_per_strategy = {
            Strategy.ROOT: 0,
            Strategy.AMF: 0,
            Strategy.PASE: 0,
            Strategy.OAS: 0,
        }
        p_pool_initial_value = {
            Pool.PI_SOL: pi_sol,
            Pool.PO_SOL: po_sol,
            Pool.PI_INSOL: pi_insol,
        }
        p_pool_final_value = p_pool_initial_value.copy()
        c_cost_value = {
            Strategy.ROOT: Strategy.ROOT.get_cost_per_strategy(p_pool_initial_value[Pool.PI_SOL], p_unit),
            Strategy.AMF: Strategy.AMF.get_cost_per_strategy(p_pool_initial_value[Pool.PI_SOL], p_unit),
            Strategy.PASE: Strategy.PASE.get_cost_per_strategy(p_pool_initial_value[Pool.PO_SOL], p_unit),
            Strategy.OAS: Strategy.OAS.get_cost_per_strategy(p_pool_initial_value[Pool.PI_INSOL], p_unit),
        }

        remaining_p_demand = p_demand

        try:
            while remaining_p_demand > 0:

                # ignore pools that are lower than the p_unit or the quota was already consumed
                for strategy, p_uptake in p_per_strategy.items():
                    strategy_pool = strategy.pool
                    access_limit_per_strategy = None
                    match strategy:
                        case Strategy.ROOT:
                            access_limit_per_strategy = access_limit * access_fr
                        case Strategy.AMF:
                            access_limit_per_strategy = access_limit * access_amf
                        case Strategy.PASE | Strategy.OAS:
                            access_limit_per_strategy = access_limit

                    if p_uptake >= p_pool_initial_value[strategy_pool] * access_limit_per_strategy \
                            or p_pool_final_value[strategy_pool] < p_unit:
                        c_cost_value[strategy] = -1

                # Find cheapest strategy and their cost
                selected_strategy, total_cost = get_lower_cost_strategy(c_cost_value)

                final_cost[selected_strategy] += total_cost
                p_per_strategy[selected_strategy] += p_unit
                selected_strategy_pool = selected_strategy.pool
                p_pool_final_value[selected_strategy_pool] -= p_unit
                c_cost_value[selected_strategy] = \
                    selected_strategy.get_cost_per_strategy(p_pool_final_value[selected_strategy_pool], p_unit)

                remaining_p_demand = remaining_p_demand - p_unit
        except Exception as e:
            print('##############################\n',
                  'Process finalized abruptly\n\t-', e,
                  '\n##############################')

        cost_root = final_cost[Strategy.ROOT]
        cost_amf = final_cost[Strategy.AMF]
        cost_pase = final_cost[Strategy.PASE]
        cost_oas = final_cost[Strategy.OAS]

        uptake_root = p_per_strategy[Strategy.ROOT]
        uptake_amf = p_per_strategy[Strategy.AMF]
        uptake_pase = p_per_strategy[Strategy.PASE]
        uptake_oas = p_per_strategy[Strategy.OAS]

        return cost_root, cost_amf, cost_pase, cost_oas, uptake_root, uptake_amf, uptake_pase, uptake_oas
