import numpy as np
# import gurobipy as gp
from gurobipy import GRB, Model, quicksum
import random as rd

#Semilla
rd.seed(2025)

# Generar Matriz
def genera_matriz(n):
    dist = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            if i>j:
                a = rd.randint(100, 500)
                dist[i,j] = a
                dist[j,i] = a
            else:
                dist[i,j] = 0
    return dist

# Modelo
n=100
modelo = Model("Agente Viajero(TSP)")
costos = genera_matriz(n)
#v.a
x={}
u={}
for i in range(n):
    for j in range(n):
        if i != j:
            x[i,j] = modelo.addVar(vtype=GRB.BINARY,name="x%d%d"%(i,j))
       
for i in range(n):
    u[i]=modelo.addVar(vtype=GRB.CONTINUOUS, name="u%d"%i)
    
# Funcion Objetivo
modelo.setObjective(quicksum(costos[i,j]*x[i,j] for i in range(n) for j in range(n) if i!=j) ,GRB.MINIMIZE)    

# Restricciones

for j in range(n):
    modelo.addConstr(quicksum(x[i,j] for i in range(n) if i!=j)==1)

for i in range(n):
    modelo.addConstr(quicksum(x[i,j] for j in range(n) if i!=j)==1)
    

for i in range(n):
    for j in range(n):
        if i != j and i!=0 and j!=0:
            modelo.addConstr(u[i]-u[j]+(n-1)*x[i,j]<=n-2)
            
            
            
modelo.update()
modelo.write("modelo extendido 50 puntos.lp")
modelo.optimize()
modelo.setParam("Timelimit", 432000)

if modelo.Status ==GRB.OPTIMAL:
    print(f"\ndistancia total: {modelo.Objval}")
    for i in range(n):
        for j in range(n):
            if i!=j and x[i,j].x>0:
                print(f"inicio: {i} - fin: {j}")
    