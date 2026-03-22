import cadquery as cq

import numpy as np
from scipy.optimize import fsolve
from scipy.integrate import solve_ivp
from scipy.optimize import root_scalar
import matplotlib.pyplot as plt


def TM(theta,y):
    u,v,r = y
    A = (u+v/np.tan(theta))/(v*v-1)
    du = v + (gamma-1)/2*u*v*(A)
    dv = -u+(1+(gamma-1)/2*v*v)*(A)
    dr = r*u/v
    return [du,dv,dr]
    
    
def Busemann(M,delta,theta0):
    beta = solve_beta(M,delta)

    Mn1 = M*np.sin(beta)
    Mn2 = normal_M2(Mn1)

    v0 = Mn2
    u0 = Mn2/np.tan(beta-delta)

    sol = solve_ivp(TM,
                    (theta0,np.pi),
                    [u0,v0,1],
                    max_step=1e-3)

    return sol.t,sol.y
    
    
def nu(M):
    return np.sqrt((gamma+1)/(gamma-1))*\
           np.arctan(np.sqrt((gamma-1)/(gamma+1)*(M**2-1)))\
           -np.arctan(np.sqrt(M**2-1))

def M_from_nu(nu_target):
    f=lambda M:nu(M)-nu_target
    sol=root_scalar(f,bracket=[1.01,50])
    return sol.root

gamma=1.4
def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)
def intakeMach(M2,th23):
    k2=M2**2*(np.sin(th23))**2
    g=1.4   #gamma
    M3=np.sqrt(((g+12)**2*M2**2*k2-4*(k2-1)*(g*k2+1))/((2*g*k2-(g-1))*((g-1)*k2+1))) #
    return M3
    
    
def theta_beta_m(M, beta):
    return np.arctan(2/np.tan(beta)*
           ((M**2*np.sin(beta)**2-1)/
           (2*M*M*(gamma+1-(2*np.sin(beta)**2)))))

def solve_beta(M, delta):
    def f(b): return theta_beta_m(M,b)-delta
    return fsolve(f, delta)

def normal_M2(Mn1):
    return np.sqrt(((gamma-1)*Mn1**2 + 2)/(2*gamma*Mn1**2-(gamma-1)))
                   
                   
theta23= np.deg2rad(69)
M2 = 2.5

#inlet height
offset_y = 1.0  
#thickness
offset_z = 0.1  

M3 = intakeMach(M2,theta23)
u2 = M2*np.cos(theta23)
v2 = -M2*np.sin(theta23)

delta23= theta_beta_m(M2, theta23)

theta2=theta23-delta23;

sol = solve_ivp(TM, (theta2,np.pi),
                    [u2,v2,1],
                    max_step=0.01)

M = np.sqrt(sol.y[0]**2+sol.y[1]**2)
idx = np.argmax(M)
x,y=pol2cart(sol.y[2][:idx],sol.t[:idx])


#normalize X to start at 0
x_offset = x[0]

#generate points in 3D
points_left = []
points_right = []

for xi, yi in zip(x, y):
    px = float(xi - x_offset)
    py = float(yi + offset_y)
    points_left.append((px, py, offset_z))
    points_right.append((px, py, -offset_z))

#create wires, not objs
left_wire = cq.Workplane("XY").spline(points_left)
right_wire = cq.Workplane("XY").spline(points_right)

show_object(left_wire, name="left_spline")
show_object(right_wire, name="right_spline")

#export

with open("left_spline.csv", "w") as f:
    for p in points_left:
        f.write(f"{p[0]},{p[1]},{p[2]}\n")

with open("right_spline.csv", "w") as f:
    for p in points_right:
        f.write(f"{p[0]},{p[1]},{p[2]}\n")

inlet_y = points_left[0][1]
outlet_y = points_left[-1][1]
freestream_mach = M[idx]

with open("dimensions.txt", "w") as f:
    f.write(f"{inlet_y}\n")
    f.write(f"{outlet_y}\n")
    f.write(f"{freestream_mach}\n")