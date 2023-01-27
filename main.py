
import econpizza as ep
import numpy as np
from grgrlib import *
import jax
import copy

from variables_names_to_labels_map import variables_names_map_sorted

med_scale_nk_price_wage_indexation_file = './model_definition/med_scale_nk_price_wage_indexation.yaml'
mod_dict0 = ep.parse(med_scale_nk_price_wage_indexation_file)

shocks = ('e_w', 0.1)

phi_pi_list = [1., 2.0]
psi_w_list = [2000.0, 5250.0]

def get_subset_of_variable_indexes(mod_org):
    want_to_show_vars_list = ['c', 'w', 'n', 'pi_w', 'pi', 'y', 'mc', 'R']
    want_to_show_vars_indexes_list = []

    for l in want_to_show_vars_list:
        want_to_show_vars_indexes_list.append(mod_org['variables'].index(l))
    
    return want_to_show_vars_indexes_list

def calculate_real_interest_rate(variables, x):
    result = None
    index_of_pi = variables.index('pi')
    index_of_interest_rate = variables.index('R')
    
    # check if array is jax array(immutable)
    if(isinstance(x, jax.numpy.ndarray)):
        result = x.at[:, index_of_interest_rate].set(x[:, index_of_interest_rate] - x[:, index_of_pi])
    else:
        result = x
        result[index_of_interest_rate] = x[index_of_interest_rate] - x[index_of_pi]
    
    return result
    
def get_deviations_from_steady_state(org_stst, shocked_stst):
    return (shocked_stst - org_stst)/org_stst * 100

def solve_model_for_different_parameter_values(mod_dict_org, shocks, parameter_values_list, param_name):
    # solve original model
    mod_org = ep.load(mod_dict_org)
    param_value_org = mod_dict_org['steady_state']['fixed_values'][param_name]
    _ = mod_org.solve_stst()
    
    mod_org_stst = np.fromiter(mod_org['stst'].values(), dtype = float)
    
    # have real interest rate in steady state
    mod_org_stst = calculate_real_interest_rate(mod_org['variables'], mod_org_stst)
    
    # shock original model
    x_org, flag_org = mod_org.find_path(shock = shocks)
    
    # transform to real interest rate
    x_org1 = calculate_real_interest_rate(mod_org['variables'], x_org)
    
    # Select a subset of variables to plot
    # Uncomment to show a subset of variables
    # subset_variable_indexes = get_subset_of_variable_indexes(mod_org)
    # subset_mod_org_stst = mod_org_stst[subset_variable_indexes]
    
    models_tuple = ()
    
    for param_value in parameter_values_list:
        mod_dict = copy.deepcopy(mod_dict_org)
        mod_dict['steady_state']['fixed_values'][param_name] = param_value
       
        # solve copied model
        mod = ep.load(mod_dict)
        _ = mod.solve_stst()
        
        x, flag = mod.find_path(shock = shocks)
        # transform to real interest rate
        x1 = calculate_real_interest_rate(mod_org['variables'], x)
        
        # Uncomment line 83 and 86 to show just a subset of variables
        # Select a subset of variables to show
        # subset_x1 = x1[0:10, subset_variable_indexes]
        
        
        # models_tuple = (*models_tuple, get_deviations_from_steady_state(subset_mod_org_stst, subset_x1))
        # Store IRFs
        models_tuple = (*models_tuple, get_deviations_from_steady_state(mod_org_stst, x1[:10]))
        
    
    # Plotting just a subset of variables. Uncomment lines 92. 93 and 95
    # subset_x_org1 = x_org1[0:10, subset_variable_indexes]
    # subset_labels = [list(variables_names_map_sorted.values())[i] for i in subset_variable_indexes]
    
    # figs, axs, _ = pplot((get_deviations_from_steady_state(subset_mod_org_stst, subset_x_org1), *models_tuple), labels = subset_labels)
    figs, axs, _ = pplot((get_deviations_from_steady_state(mod_org_stst, x_org1[:10]), *models_tuple), labels = list(variables_names_map_sorted.values()))

    
    # Add legend with values of the parameter
    # Add horizontal line at 0
    for ax in axs:
        ax.legend([f'{param_name} = {param_value}' for param_value in [param_value_org, *parameter_values_list]])
        ax.axhline(y=0.0, color='0.8', linestyle='--')
    
    
    plt.show()

# Solve for either different values of phi_pi or psi_w
solve_model_for_different_parameter_values(mod_dict0, shocks, phi_pi_list, 'phi_pi')
# solve_model_for_different_parameter_values(mod_dict0, shocks, psi_w_list, 'psi_w')