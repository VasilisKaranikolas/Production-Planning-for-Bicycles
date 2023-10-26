import pyomo.environ as pyo

model = pyo.ConcreteModel(name="CWK_Karanikolas_Concrete")

model.M = pyo.Var([1,2], domain=pyo.NonNegativeIntegers) 
model.T = pyo.Var([1,2], domain=pyo.NonNegativeIntegers)
model.IM = pyo.Var([1,2], domain=pyo.NonNegativeIntegers)
model.IT = pyo.Var([1,2], domain=pyo.NonNegativeIntegers)


model.Obj = pyo.Objective( expr= 60*model.M[1]+60*model.M[2]+
                          45*model.T[1]+45*model.T[2]+
                          60*3/100*model.IM[1]+
                          60*3/100*model.IM[2]+
                          45*3/100*model.IT[1]+
                          45*3/100*model.IT[2] )

model.C1 = pyo.Constraint(expr = 16*model.M[1] + 13*model.T[1] >=3500)

model.C2 = pyo.Constraint(expr = 16*model.M[1] +13*model.T[1] <=4500)

model.C3 = pyo.Constraint(expr = 16*model.M[2] +13*model.T[2] >= 
                          16*model.M[1] + 13*model.T[1] -500)

model.C4 = pyo.Constraint(expr = 16*model.M[2] +13*model.T[2] <=
                          16*model.M[1] + 13*model.T[1] +500)

model.C5 = pyo.Constraint(expr = model.M[1] - model.IM[1] + 15 ==150)
model.C6 = pyo.Constraint(expr = model.M[2] - model.IM[2] + model.IM[1] ==200)
model.C7 = pyo.Constraint(expr = model.T[1] - model.IT[1] + 25 ==125)
model.C8 = pyo.Constraint(expr = model.T[2] - model.IT[2] + model.IT[1] ==150)
model.C9 = pyo.Constraint(expr = model.IM[2] >=25)
model.C10 = pyo.Constraint(expr = model.IT[2] >=25)