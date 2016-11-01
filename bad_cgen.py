import casadi as C
import numpy as np
import os

nrotors = 4

# objective function
def make_qp_fun():
    x = C.MX.sym('x', 1 + nrotors)
    p = C.MX.sym('p', 2)
    
    flaps = x[0]
    rotors = x[1:]
    
    flapMoments = flaps
    rotorMoments = sum([rotors[k] for k in range(nrotors)])
    totalMoment = rotorMoments + flapMoments
    
    momentError = totalMoment * totalMoment
    
    meanThrustCommand = p[0]
    rotorRegStrat = p[1]
    
    rotor0 = C.conditional(rotorRegStrat, [meanThrustCommand], sum([rotors[k] for k in range(nrotors)]))
    rotorReg = sum([(rotors[k] - rotor0)**2 for k in range(nrotors)])
    
    f = momentError + rotorReg
    
    qpfun = C.Function("qp_fun_hrm", [x,p], [f,0])
    #qpfun.printDimensions()
    return qpfun

qpfun = make_qp_fun()
# hessian of objective functoin
hess = qpfun.hessian(0, 0)
#hess.printDimensions()


# call with constant inputs, but get the sparsity right
x = C.MX.sym('x', 1 + nrotors)
p = C.MX.sym('p', 2)
x = 0*x + np.zeros(1 + nrotors)
p = 0*p + np.array([-0.12500, 0])

# final function has one dummy input
dummyIn = C.MX.sym('dummy', 1)
# we only need the jacobian, thought the hessian is also bugged
_, jac, _, _ = hess(x, p)
masterFun = C.Function('casadi_bug_fun', [dummyIn], [jac])

# generate this bad function
masterFun.generate('casadi_bug_fun')
# and compile
os.system("gcc -fPIC -shared casadi_bug_fun.c -o casadi_bug_fun.so")

# load external function
emasterFun = C.external('casadi_bug_fun', {})

# call external function twice with the same input, getting the same answer
r0 = emasterFun(0)
r1 = emasterFun(0)
r2 = emasterFun(0)
print('python outputs equal: '+str(np.all(r0 == r1) and np.all(r0 == r2)))
print('first python call:    '+str(r0))
print('second python call:   '+str(r1))
print('third python call:    '+str(r2))
