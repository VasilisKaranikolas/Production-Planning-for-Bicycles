import pyomo.environ as pyo

model = pyo.AbstractModel(name = "CWK_Karanikolas")

model.p = pyo.Param() 
model.P = pyo.RangeSet(model.p) 

model.T = pyo.Set()   

model.C = pyo.Param(model.T) 
model.MH = pyo.Param(model.T) 
model.AH = pyo.Param(model.T) 
model.SI = pyo.Param(model.T) 
model.FI = pyo.Param(model.T) 

model.LU = pyo.Param() 
model.LV = pyo.Param() 
model.HC = pyo.Param() 

model.D = pyo.Param(model.T,model.P) 

model.B = pyo.Var(model.T, model.P, within=pyo.NonNegativeIntegers)

#θεωρω το αποθεμα της προηγούμενης περιοδου μηνα 0
def bnd_rule_start_final_inventory(model,i,j):
    if j == 0:
        return(model.SI[i],model.SI[i]) 
    elif j == model.p:
        return(model.FI[i],None) 
    else:
        return(0.0, None)
model.I = pyo.Var(model.T, pyo.RangeSet(0, model.p), within=pyo.NonNegativeIntegers, 
                  bounds=bnd_rule_start_final_inventory)


def obj_rule(model):
    return(sum( model.C[i] * model.B[i,j] + model.HC * model.C[i] * model.I[i,j] 
               for i in model.T for j in model.P))
model.obj = pyo.Objective(rule=obj_rule)


def con_month_prod_hours_rule(model,j):
     if j==1:
        return(model.LU - model.LV, sum(model.B[i,j]*(model.MH[i]+model.AH[i]) for i in model.T),
               model.LU + model.LV)
     else:
        return(-model.LV, sum(model.B[i,j] * (model.MH[i]+model.AH[i]) for i in model.T) -
               sum(model.B[i,j-1] * (model.MH[i]+model.AH[i]) for i in model.T), model.LV)
model.con_month_prod_hours = pyo.Constraint(model.P, rule=con_month_prod_hours_rule)

def con_demand_rule(model, i, j):
    return (model.B[i,j] - model.I[i,j] + model.I[i,j-1] == model.D[i,j])
model.con_demand = pyo.Constraint(model.T,model.P, rule=con_demand_rule)


model = model.create_instance('CWK_Karanikolas_2.dat')
solver = pyo.SolverFactory('glpk')
opt = solver.solve(model)
model.display()
