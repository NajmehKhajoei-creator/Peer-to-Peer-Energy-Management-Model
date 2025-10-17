def compute_costs(network, vars, demand_dict, solar_dict,
                  grid_purchase_price,
                  neighbour_purchase_price_intra,
                  neighbour_purchase_price_inter,
                  grid_selling_price,
                  neighbour_selling_price_intra,
                  neighbour_selling_price_inter,
                  battery_using_price,
                  T=24):
    cost_per_house = {}
    all_houses = [h for group in network.values() for h in group]
    all_prosumers = [h for h in all_houses if h['type'] == 'prosumer']
    all_consumers = [h for h in all_houses if h['type'] == 'consumer']
    for group_id, houses in network.items():
        group_prosumers = [h for h in houses if h["type"] == "prosumer"]
        group_consumers = [h for h in houses if h["type"] == "consumer"]
        for h in houses:
            hid = h['id']
            htype = h['type']
            total_cost = 0
            if htype == "prosumer":
                total_cost += battery_using_price * cp.sum([vars["charge"][hid] + vars["discharge"][hid]])
            else:
                total_cost += battery_using_price * cp.sum([vars["discharge"][hid]])
            total_cost += grid_purchase_price * cp.sum([vars["grid_buy"][hid]])
            if htype == "prosumer":
                total_cost += neighbour_purchase_price_intra * cp.sum(
                    [vars["buy_from"][(hid, peer['id'])] for peer in group_prosumers if peer['id'] != hid]
                )
                total_cost += neighbour_purchase_price_inter * cp.sum(
                    [vars["buy_from"][(hid, other['id'])] for other in all_prosumers if other["group"] != group_id]
                )
                total_cost -= grid_selling_price * cp.sum([vars["grid_sell"][hid]])
                total_cost -= neighbour_selling_price_intra * cp.sum(
                    [vars["sell_to"][(hid, peer['id'])] for peer in group_prosumers if peer['id'] != hid]
                )
                total_cost -= neighbour_selling_price_intra * cp.sum(
                    [vars["sell_to"][(hid, consumer['id'])] for consumer in group_consumers]
                )
                total_cost -= neighbour_selling_price_inter * cp.sum(
                    [vars["sell_to"][(hid, other['id'])] for other in all_prosumers if other["group"] != group_id]
                )
                total_cost -= neighbour_selling_price_inter * cp.sum(
                    [vars["sell_to"][(hid, consumer['id'])] for consumer in all_consumers if consumer["group"] != group_id]
                )
            else:
                total_cost += neighbour_purchase_price_intra * cp.sum(
                    [vars["buy_from"][(hid, pros["id"])] for pros in group_prosumers]
                )
                total_cost += neighbour_purchase_price_inter * cp.sum(
                    [vars["buy_from"][(hid, pros["id"])] for pros in all_prosumers if pros["group"] != group_id]
                )
            cost_per_house[hid] = cp.sum(total_cost)
    return cost_per_house

#  Step 6: Compute group costs
def compute_group_costs(network, cost_per_house):
    cost_per_group = {}
    for group_id, houses in network.items():
        group_cost = cp.sum([cost_per_house[h['id']] for h in houses])
        cost_per_group[group_id] = group_cost
    return cost_per_group



