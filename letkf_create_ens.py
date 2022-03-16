import numpy as np
from netCDF4 import Dataset
import sys
# routine to create pseudo-ensemble for use in LETKF-OI for snow depth
# reads in sfc_data restarts, and sets snowdepth to +/- 
# perturbation, given stdev(ensemble) of B
# Clara Draper, October, 2021.

if (len(sys.argv) != 3): 
    print('argument error, usage: letkf_create file_stub back_error' ) 

fstub=sys.argv[1]
b = float(sys.argv[2]) 

# 2 ens members 
offset=b/np.sqrt(2)

print('adjusting '+fstub+'* by '+str(offset))

sign = [1,-1]
ens_dirs=['mem_pos','mem_neg'] 

for ens in range(2): 
    for tt in range(6):
        # open file 
        out_netcdf = ens_dirs[ens]+'/'+fstub+'.sfc_data.tile'+str(tt+1)+'.nc'
        #print (out_netcdf)
        ncOut = Dataset(out_netcdf, "r+")  
        # add offset to the snow
        var_array = ncOut.variables["snwdph"][:]
        var_array = var_array + sign[ens]*offset
        ncOut.variables["snwdph"][0,:,:] = var_array[:]
        ncOut.renameVariable("sheleg","stype")
        ncOut.variables["stype"][0,:,:] = 30.0
        ncOut.close()
