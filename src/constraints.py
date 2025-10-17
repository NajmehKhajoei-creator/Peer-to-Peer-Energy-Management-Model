def enforce_trade_symmetry(constraints, vars, t):
    for (s, b), sell_var in vars["sell_to"].items():
        if (b, s) in vars["buy_from"]:
            constraints += [sell_var[t] == vars["buy_from"][(b, s)][t]]


def build_constraints(network, vars, demand_dict, solar_dict,
                             initial_battery_levels, b_lower, b_upper,
                             b_max_charge, b_max_discharge,
                             charge_eff, discharge_eff,
                             T=24):
    constraints = []
    all_houses = [h for group in network.values() for h in group]
    all_prosumers = [h for h in all_houses if h['type'] == 'prosumer']
    all_consumers = [h for h in all_houses if h['type'] == 'consumer']
    for t in range(T):
        enforce_trade_symmetry(constraints, vars, t)
        surplus = {}
        for group_id, houses in network.items():
            group_prosumers = [h for h in houses if h['type'] == 'prosumer']
            group_consumers = [h for h in houses if h['type'] == 'consumer']
            b = vars["battery"][group_id]
            if t == 0:
                constraints += [
                    b[0] == initial_battery_levels[group_id]
                    + charge_eff[group_id] * cp.sum([
                        vars["charge"][h["id"]][0] for h in houses if h["type"] == "prosumer"
                    ])
                    - discharge_eff[group_id] * cp.sum([
                        vars["discharge"][h["id"]][0] for h in houses
                    ])
                ]
            else:
                constraints += [
                    b[t] == b[t - 1]
                    + charge_eff[group_id] * cp.sum([
                        vars["charge"][h["id"]][t] for h in houses if h["type"] == "prosumer"
                    ])
                    - discharge_eff[group_id] * cp.sum([
                        vars["discharge"][h["id"]][t] for h in houses
                    ])
                ]
            constraints += [b_lower[group_id] <= b[t], b[t] <= b_upper[group_id]]
            constraints += [
                cp.sum([
                    vars["charge"][h["id"]][t] for h in houses if h["type"] == "prosumer"
                ]) <= b_max_charge[group_id]
            ]
            constraints += [
                cp.sum([
                    vars["discharge"][h["id"]][t] for h in houses
                ]) <= b_max_discharge[group_id]
            ]
            for h in houses:
                hid = h['id']
                htype = h['type']
                demand = demand_dict[hid][t]
                solar = solar_dict[hid][t]
                inflow = [vars["grid_buy"][hid][t], vars["discharge"][hid][t]]
                outflow = []
                if htype == 'prosumer':
                    inflow += [vars["buy_from"][(hid, peer['id'])][t]
                               for peer in group_prosumers if peer['id'] != hid]
                    inflow += [vars["buy_from"][(hid, other['id'])][t]
                               for other in all_prosumers if other['group'] != group_id]
                    outflow += [vars["grid_sell"][hid][t], vars["charge"][hid][t]]
                    outflow += [vars["sell_to"][(hid, peer['id'])][t]
                                for peer in group_prosumers if peer['id'] != hid]
                    outflow += [vars["sell_to"][(hid, consumer['id'])][t]
                                for consumer in group_consumers]
                    outflow += [vars["sell_to"][(hid, other['id'])][t]
                                for other in all_prosumers if other['group'] != group_id]
                    outflow += [vars["sell_to"][(hid, consumer['id'])][t]
                                for consumer in all_consumers if consumer['group'] != group_id]
                    constraints.append(solar + cp.sum(inflow) - cp.sum(outflow) == demand)

                    # Boundry
                    constraints += [vars["grid_sell"][hid][t] <= solar]
                    constraints += [vars["sell_to"][(hid, peer['id'])][t] <= solar
                                    for peer in group_prosumers if peer['id'] != hid]
                    constraints += [vars["sell_to"][(hid, consumer['id'])][t] <= solar
                                    for consumer in group_consumers]
                    constraints += [vars["sell_to"][(hid, other['id'])][t] <= solar
                                    for other in all_prosumers if other['group'] != group_id]
                    constraints += [vars["sell_to"][(hid, consumer['id'])][t] <= solar
                                    for consumer in all_consumers if consumer['group'] != group_id]

                    # Boundry
                    constraints += [vars["grid_buy"][hid][t] <= demand]
                    constraints += [vars["buy_from"][(hid, peer['id'])][t] <= demand
                                    for peer in group_prosumers if peer['id'] != hid]
                    constraints += [vars["buy_from"][(hid, other['id'])][t] <= demand
                                    for other in all_prosumers if other['group'] != group_id]
                    surplus[hid] = np.maximum(0, solar - demand)
                elif htype == 'consumer':
                    inflow += [vars["buy_from"][(hid, prosumer['id'])][t]
                               for prosumer in group_prosumers]
                    inflow += [vars["buy_from"][(hid, prosumer['id'])][t]
                               for prosumer in all_prosumers if prosumer['group'] != group_id]
                    constraints.append(solar+cp.sum(inflow) == demand)
        for s in all_prosumers:
            for r in all_prosumers:
                if s['id'] != r['id']:
                    s_surplus = surplus.get(s['id'], 0)
                    r_surplus = surplus.get(r['id'], 0)
                    if s_surplus > 0 and r_surplus > 0:
                        constraints += [vars["sell_to"][(s['id'], r['id'])][t] == 0]
                        constraints += [vars["sell_to"][(r['id'], s['id'])][t] == 0]
                        
    return constraints



