# Inter-Energy Trading Simulation

This project simulates **inter-energy trading** among multiple groups of households or buildings.
It models **prosumers** (who can produce and consume energy) and **consumers** (who only consume energy),
with possible **shared batteries** within groups.

---

**COPOWER cVPP online demonstration service (Deliverable D3.6.1)**

This repository provides the executable technical demonstration component of the COPOWER online cVPP demonstration service (Deliverable D3.6.1). The complete demonstration service consists of three components: (i) this open-source executable implementation, (ii) a technical and methodological handbook documenting the models and assumptions, and (iii) an online service entry webpage hosted by the project. Together, these components form the COPOWER online cVPP demonstration service.

---
**Repository version:** v1.0 – Deliverable D3.6.1 (COPOWER)


## Features
- Uses **synthetic data** for demand and solar production to maintain privacy.
- Supports any number of **groups** and **users**.
- Models **battery constraints, grid interactions, and peer-to-peer energy trading**.
- Calculates **total cost per house and per group** over multiple days.

  ## Scope and intended use

This repository provides a simulation-based, executable technical demonstration of
peer-to-peer (P2P) energy sharing within a community-based Virtual Power Plant (cVPP).

The code is **not** a live web service or production system. Instead:
- It is intended to be downloaded, installed, and run locally.
- It is designed to be used together with the accompanying handbook (Part 2 of Deliverable D3.6.1), which provides the primary technical and methodological guidance.
- It supports learning, replication, and adaptation of cVPP concepts rather than real-time operation or market participation.


**Handbook as primary guide**  
This repository is intended to be used together with the accompanying handbook:

*AI-Enabled cVPP Demonstration Handbook: Simulating Peer-to-Peer Energy Sharing for Community-Based Virtual Power Plants (cVPP)*

The handbook provides the main technical and methodological guidance, including step-by-step instructions, model explanations, and guidance for adapting or extending the code.  
*(Online link to the handbook will be added once available)*


## Folder Structure

intra-energy-trading/
src/           # Python source files for data generation, network, variables, constraints, costs
notebooks/     # Jupyter notebooks (main_demo.ipynb)
results/       # Simulation outputs and logs
LICENSE        # License file
requirements.txt # Python dependencies



## Installation and running

### Requirements
- Python 3.9 or newer

### Installation
Install dependencies:

```bash
pip install -r requirements.txt
jupyter notebook notebooks/main_demo.ipynb

```
## Notes

- This project uses synthetic data to protect privacy.  
- Supports flexible configurations of groups, prosumers, consumers, and shared batteries.  

## Citation and Acknowledgement

If you use or adapt this code, please acknowledge the COPOWER project and cite:

N. Khajoei, R. Unnþórsson, S. Guðmundsson,  
*A Peer-to-Peer Energy Management Model for Residential Homes*,  
Nordic Energy Informatics Academy Conference, Springer, 2025  
[Link to paper](https://www.springerprofessional.de/en/peer-to-peer-energy-management-model-for-residential-homes/51647472)

This repository supports Deliverable D3.6.1 of the COPOWER project,
funded under the Interreg Northern Periphery and Arctic Programme.

## Quick Start
Open `notebooks/main_demo.ipynb` in Jupyter Notebook.  
Follow the step-by-step cells to explore inter-energy trading scenarios.




