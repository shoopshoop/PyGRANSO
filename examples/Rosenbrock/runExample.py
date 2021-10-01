import time
import torch
import sys
## Adding PyGRANSO directories. Should be modified by user
sys.path.append('/home/buyun/Documents/GitHub/PyGRANSO')
from pygranso import pygranso
from pygransoStruct import Options, Data

# Please read the documentation on https://pygranso.readthedocs.io/en/latest/

# device = torch.device('cuda')
device = torch.device('cpu')

# variables and corresponding dimensions.
var_in = {"x1": (1,1), "x2": (1,1)}

# user defined options
opts = Options()
opts.QPsolver = 'osqp'
opts.maxit = 1000
opts.print_level = 1
opts.print_frequency = 1
opts.x0 = torch.ones((2,1), device=device, dtype=torch.double)

#  main algorithm  
start = time.time()
soln = pygranso(var_dim_map = var_in, torch_device=device, user_opts = opts)
end = time.time()
print("Total Wall Time: {}s".format(end - start))

print(soln.final.x)