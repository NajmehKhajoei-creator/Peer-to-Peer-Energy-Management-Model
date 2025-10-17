import numpy as np

def generate_synthetic_data(N_days=122, T=24):
    np.random.seed(42)
    demand_list_house1 = []
    demand_list_house2 = []
    demand_list_house3 = []
    demand_list_house4 = []
    demand_list_house5 = []

    for day in range(N_days):
        hours = np.arange(T)
        base_demand = 0.5 + 0.3 * np.sin(2 * np.pi * hours / T + np.pi / 4)
        daily_factor = np.random.uniform(0.8, 1.2)
        noise = np.random.normal(0, 0.05, T)

        demand_list_house1.append((base_demand * 0.8 * daily_factor + noise).clip(min=0.1, max=1.0).tolist())
        demand_list_house2.append((base_demand * 1.0 * daily_factor + noise).clip(min=0.1, max=1.2).tolist())
        demand_list_house3.append((base_demand * 1.5 * daily_factor + noise).clip(min=0.2, max=2.0).tolist())
        demand_list_house4.append((base_demand * 0.8 * daily_factor + noise).clip(min=0.1, max=1.0).tolist())
        demand_list_house5.append((base_demand * 1.2 * daily_factor + noise).clip(min=0.2, max=1.8).tolist())

    solar_production_list_1 = []
    solar_production_list_2 = []
    solar_production_list_3 = []

    for day in range(N_days):
        hours = np.arange(T)
        base_solar = 1.5 * np.sin(np.pi * hours / T).clip(min=0)
        daily_factor = np.random.uniform(0.7, 1.3)
        noise = np.random.normal(0, 0.03, T)

        solar_production_list_1.append((base_solar * daily_factor + noise).clip(min=0, max=1.5).tolist())
        solar_production_list_2.append((base_solar * 0.8 * daily_factor + noise).clip(min=0, max=1.2).tolist())
        solar_production_list_3.append((base_solar * daily_factor + noise).clip(min=0, max=1.5).tolist())

    return (demand_list_house1, demand_list_house2, demand_list_house3,
            demand_list_house4, demand_list_house5,
            solar_production_list_1, solar_production_list_2, solar_production_list_3)

# ==== CALL THE FUNCTION ====
(demand_list_house1, demand_list_house2, demand_list_house3,
 demand_list_house4, demand_list_house5,
 solar_production_list_1, solar_production_list_2, solar_production_list_3) = generate_synthetic_data()

# ==== PRINT SHAPES ====
print("Demand shapes:")
print(f"demand_list_house1: {np.array(demand_list_house1).shape}")
print(f"demand_list_house2: {np.array(demand_list_house2).shape}")
print(f"demand_list_house3: {np.array(demand_list_house3).shape}")
print(f"demand_list_house4: {np.array(demand_list_house4).shape}")
print(f"demand_list_house5: {np.array(demand_list_house5).shape}")

print("Solar shapes:")
print(f"solar_production_list_1: {np.array(solar_production_list_1).shape}")
print(f"solar_production_list_2: {np.array(solar_production_list_2).shape}")
print(f"solar_production_list_3: {np.array(solar_production_list_3).shape}")


