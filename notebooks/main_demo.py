
import numpy as np
import cvxpy as cp

# Import modular functions
from src.data_generation import generate_synthetic_data
from src.network_structure import build_network_structure
from src.energy_variables import create_energy_variables
from src.constraints import build_constraints
from src.cost_functions import compute_costs, compute_group_costs

# Generate data
(demand_list_house1, demand_list_house2, demand_list_house3,
 demand_list_house4, demand_list_house5,
 solar_production_list_1, solar_production_list_2, solar_production_list_3) = generate_synthetic_data(N_days=122, T=24)

# Define network
G = 2
T = 24
prosumers_per_group = [2, 1]
consumers_per_group = [1, 1]
network = build_network_structure(G, prosumers_per_group, consumers_per_group)
all_houses = [house for group in network.values() for house in group]

# Battery and pricing parameters
b_lower_list = [0.2*5.25, 0.2*5.25]
b_upper_list = [0.8*5.25, 0.8*5.25]
b_max_charge_list = [1.050, 1.050]
b_max_discharge_list = [1.050, 1.050]
charge_eff_list = [0.98, 0.98]
discharge_eff_list = [1/0.96, 1/0.96]
initial_battery_list = [0.2*5.25, 0.2*5.25]

grid_purchase_price = 20.93
neighbour_purchase_price_inter = 0.8 * grid_purchase_price
neighbour_purchase_price_intra = 0.7 * grid_purchase_price
neighbour_selling_price_intra = 0.5 * grid_purchase_price
neighbour_selling_price_inter = 0.3 * grid_purchase_price
grid_selling_price = 0.2 * grid_purchase_price
battery_using_price = 2

initial_battery_levels = {g+1: initial_battery_list[g] for g in range(G)}
b_lower = {g+1: b_lower_list[g] for g in range(G)}
b_upper = {g+1: b_upper_list[g] for g in range(G)}
b_max_charge = {g+1: b_max_charge_list[g] for g in range(G)}
b_max_discharge = {g+1: b_max_discharge_list[g] for g in range(G)}
charge_eff = {g+1: charge_eff_list[g] for g in range(G)}
discharge_eff = {g+1: discharge_eff_list[g] for g in range(G)}

# Multi-day optimization loop
N_days = len(demand_list_house1)
all_optimization_results = []

for day in range(N_days):
    print(f"Optimizing day {day+1}/{N_days}")

    # Prepare demand/solar dicts
    demand_lists = [
        demand_list_house1[day], demand_list_house2[day],
        demand_list_house3[day], demand_list_house4[day],
        demand_list_house5[day]
    ]
    solar_lists = [
        solar_production_list_1[day], solar_production_list_2[day],
        np.zeros_like(demand_list_house3[day]),
        solar_production_list_3[day], np.zeros_like(demand_list_house5[day])
    ]

    demand_dict = {house['id']: d for house, d in zip(all_houses, demand_lists)}
    solar_dict = {house['id']: s for house, s in zip(all_houses, solar_lists)}

    # Create variables
    vars = create_energy_variables(network, T)

    # Build constraints
    constraints = build_constraints(
        network, vars, demand_dict, solar_dict,
        initial_battery_levels, b_lower, b_upper,
        b_max_charge, b_max_discharge, charge_eff, discharge_eff, T
    )

    # Compute costs
    cost_per_house = compute_costs(
        network, vars, demand_dict, solar_dict,
        grid_purchase_price, neighbour_purchase_price_intra,
        neighbour_purchase_price_inter, grid_selling_price,
        neighbour_selling_price_intra, neighbour_selling_price_inter,
        battery_using_price, T
    )
    cost_per_group = compute_group_costs(network, cost_per_house)

    # Solve optimization
    total_cost = cp.sum(list(cost_per_group.values()))
    objective = cp.Minimize(total_cost)
    problem = cp.Problem(objective, constraints)
    problem.solve(solver=cp.GUROBI, verbose=False, NumericFocus=3)

    # Store results
    optimization_results = []
    for group_id in network.keys():
        optimization_results.append({
            "group": group_id,
            "battery": vars["battery"][group_id].value,
            "group_cost": cost_per_group[group_id].value,
            "member_costs": {h['id']: cost_per_house[h['id']].value for h in network[group_id]}
        })
    all_optimization_results.append(optimization_results)

    # Update battery levels for next day
    for g in initial_battery_levels.keys():
        initial_battery_levels[g] = vars["battery"][g].value[T-1]

# Aggregate costs
total_cost_per_house = {}
total_cost_per_group = {}

for day_results in all_optimization_results:
    for group_result in day_results:
        group_id = group_result["group"]
        group_cost = group_result["group_cost"]
        member_costs = group_result["member_costs"]

        total_cost_per_group[group_id] = total_cost_per_group.get(group_id, 0) + group_cost
        for hid, cost in member_costs.items():
            total_cost_per_house[hid] = total_cost_per_house.get(hid, 0) + cost

# Print results
print("\n=== Total Cost per House ===")
for hid, cost in total_cost_per_house.items():
    print(f"{hid}: {cost:.2f}")

print("\n=== Total Cost per Group ===")
for gid, cost in total_cost_per_group.items():
    print(f"Group {gid}: {cost:.2f}")

Overall_cost = sum(total_cost_per_group.values())
print(f"\n=== Overall Total Cost: {Overall_cost:.2f} ===")


