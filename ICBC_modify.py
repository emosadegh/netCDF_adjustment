#!/usr/bin/env python3

########################################
# Created on Sat Dec  8 20:17:37 2018
#
# author: ehsan (ehsanm@dri.edu)
# purpose: to set IC and BC values to zero.
########################################

from netCDF4 import Dataset
import numpy as np

########################################

work_dir = '/Users/ehsan/Documents/PYTHON_CODES/netCDF_modify'
repository_name = 'netCDF_adjustment'
script_dir = work_dir+'/github/'+repository_name
input_dir = work_dir+'/inputs'
output_dir = work_dir+'/outputs'

########################################

my_value = 1e-10

file_name = 'ICON_v521_test_for_v53_profile'

file_path = '/Users/ehsan/Documents/Python_projects/netCDF_modify/inputs/'

file_name_path = file_path+file_name

print( '-> file name is "%s" ' %file_name )
print( '-> file path is "%s" ' %file_path )
print( '-> file name and path is "%s" ' %file_name_path )
print( '-> nc values will be set to min of = %s' %my_value)

nc_file = Dataset(file_name_path , 'r+')

#nc_file_modified = nc_file.copy()

var_keys = []

for ivar in nc_file.variables.keys():

	var_keys.append(ivar)

var_keys_array = np.array(var_keys)

print('-> size of var_keys list is : %s ' %var_keys_array.size)

#nc_var_array = np.array([])

for var_key in var_keys_array :

	print('-> 0-ing the values for %s ...'  %var_key)

	nc_var = nc_file.variables[var_key]

	if nc_var.name == 'TFLAG' :

		print('-> VAR is TFLAG, we do not need it, so we pass!')

		continue

		#print('-> for %s variable, shape is %s and dtype is %s'  %( nc_var.name , nc_var.shape , nc_var.dtype))

	print('-> max value inside "%s" array is = %s'  %( var_key , np.amax( nc_var[:] ) ) )

	datatype = nc_var.dtype

	if datatype == 'float32' :

		nc_var[:] = my_value

	else:

		print('-> dtype is NOT "float32", check the dtype for %s '  %nc_var.name  )

nc_file.close()
print('-> closing netcdf file now!')

print('--------------------------------------------------------------')
print('-> doing QA check on arrays ...')

nc_file = Dataset(file_name_path , 'r')

var_keys = []

for ivar in nc_file.variables.keys():

	var_keys.append(ivar)

var_keys_array = np.array(var_keys)

for var_key in var_keys_array :

	var_max = np.amax( nc_file.variables[ var_key ] )

	var_min = np.amin( nc_file.variables[ var_key ] )

	print('-> for VAR = %s min is : %s and max is %s '  %( var_key , var_min , var_max) )

	if var_max - my_value <= 1e-10 :

		print( '-> QA checked, all elements inside (%s) array are now set to : %s ' %( var_key , my_value))

	else:

		print( '-> NOTE: for VAR: %s max value is = %s, but our favorite value is = %s, go back and check.' %( var_key , var_max , my_value ))

nc_file.close()
print('-> closing netcdf file now.')
