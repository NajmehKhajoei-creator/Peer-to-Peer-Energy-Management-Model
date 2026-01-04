# Inter-Energy Trading Simulation

This project simulates **inter-energy trading** among multiple groups of households or buildings.
It models **prosumers** (who can produce and consume energy) and **consumers** (who only consume energy),
with possible **shared batteries** within groups.

---

**COPOWER cVPP online demonstration service (Deliverable D3.6.1)**

This repository provides the executable technical demonstration component of the COPOWER online cVPP demonstration service (Deliverable D3.6.1). The complete demonstration service consists of three components: (i) this open-source executable implementation, (ii) a technical and methodological handbook documenting the models and assumptions, and (iii) an online service entry webpage hosted by the project. Together, these components form the COPOWER online cVPP demonstration service.

---

## Features
- Uses **synthetic data** for demand and solar production to maintain privacy.
- Supports any number of **groups** and **users**.
- Models **battery constraints, grid interactions, and peer-to-peer energy trading**.
- Calculates **total cost per house and per group** over multiple days.



## Folder Structure

intra-energy-trading/
src/           # Python source files for data generation, network, variables, constraints, costs
notebooks/     # Jupyter notebooks (main_demo.ipynb)
results/       # Simulation outputs and logs
LICENSE        # License file
requirements.txt # Python dependencies

## Usage

1. Install dependencies:

```bash
pip install -r requirements.txt

notebooks/main_demo.ipynb

## Notes

- This project uses synthetic data to protect privacy.  
- Supports flexible configurations of groups, prosumers, consumers, and shared batteries.  
- The methodology implemented in this repository is based on the following published work:

  **N. Khajoei, R. Unnþórsson, S. Guðmundsson**,  
  *A Peer-to-Peer Energy Management Model for Residential Homes*,  
  Nordic Energy Informatics Academy Conference, Springer, 2025.  
  https://www.springerprofessional.de/en/peer-to-peer-energy-management-model-for-residential-homes/51647472


