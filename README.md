# TSP Solver: Mathematical Optimization vs Genetic Algorithm

This project compares two approaches to solving the **Traveling Salesman Problem (TSP)**:
- An **exact mathematical model** using Gurobi and Python (GurobiPy)
- A **Genetic Algorithm (GA)** developed from scratch

## Problem Description

The Traveling Salesman Problem (TSP) aims to find the shortest route that visits all cities exactly once and returns to the starting city. It is a well-known NP-hard combinatorial optimization problem.

---

## Mathematical Model (GurobiPy)

The model is implemented using Python with Gurobi's optimization library. It:
- Defines binary decision variables for each edge
- Minimizes total distance
- Enforces constraints to prevent subtours (MTZ or Lazy Constraints)

📁 File: `modelo_matematico_tsp.py`

---

## 🧬 Genetic Algorithm (Metaheuristic)

A population-based approach that:
- Encodes solutions as permutations of cities
- Applies selection, crossover, mutation, and elitism
- Evolves over generations to approximate an optimal route

📁 File: `algoritmo_genetico_tsp.py`

---

## Features

- Compare solution quality and runtime between both methods
- Visualize convergence of the GA
- Modular and easy to extend

---

## 💻 Technologies

- Python
- GurobiPy
- Matplotlib 
- NumPy / Random (for GA)

---

## How to Run

> Prerequisite: You must have a valid Gurobi license for the exact model (for exact model).

