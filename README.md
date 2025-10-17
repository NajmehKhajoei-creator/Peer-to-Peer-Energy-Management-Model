# Inter-Energy Trading Simulation

This project simulates **inter-energy trading** among multiple groups of households or buildings.
It models **prosumers** (who can produce and consume energy) and **consumers** (who only consume energy),
with possible **shared batteries** within groups. 

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
- The methodology is based on the paper:  
  **"Peer-to-Peer Energy Management Model for Residential Homes"**  
  Najmeh Khajoei, Runar Unnthorsson, and Steinn Gudmundsson,  
  Faculty of Industrial Engineering, Mechanical Engineering and Computer Science,  
  University of Iceland.  
  **Currently in the process of publishing in Nordic EIA 2025, Part I, LNCS 16095.**
