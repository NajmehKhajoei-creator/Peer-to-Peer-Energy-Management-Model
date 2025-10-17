import cvxpy as cp
import numpy as np

def create_energy_variables(network, T=24):
    all_houses = [h for group in network.values() for h in group]
    all_prosumers = [h for h in all_houses if h['type'] == 'prosumer']
    all_consumers = [h for h in all_houses if h['type'] == 'consumer']
    
    battery = {}
    charge = {}
    discharge = {}
    grid_buy = {}
    grid_sell = {}
    sell_to = {}
    buy_from = {}
    
    for g, houses in network.items():
        battery[g] = cp.Variable(T, nonneg=True)
        group_prosumers = [h for h in houses if h['type'] == 'prosumer']
        group_consumers = [h for h in houses if h['type'] == 'consumer']

        for h in houses:
            hid = h['id']
            discharge[hid] = cp.Variable(T, nonneg=True)
            grid_buy[hid] = cp.Variable(T, nonneg=True)
            if h['type'] == 'prosumer':
                charge[hid] = cp.Variable(T, nonneg=True)
                grid_sell[hid] = cp.Variable(T, nonneg=True)
                for peer in group_prosumers:
                    if peer['id'] != hid:
                        var = cp.Variable(T, nonneg=True)
                        sell_to[(hid, peer['id'])] = var
                        buy_from[(peer['id'], hid)] = var
                for consumer in group_consumers:
                    var = cp.Variable(T, nonneg=True)
                    sell_to[(hid, consumer['id'])] = var
                    buy_from[(consumer['id'], hid)] = var
    return {
        "battery": battery,
        "charge": charge,
        "discharge": discharge,
        "grid_buy": grid_buy,
        "grid_sell": grid_sell,
        "sell_to": sell_to,
        "buy_from": buy_from
    }



