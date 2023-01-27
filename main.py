
import econpizza as ep
import numpy as np
from grgrlib import *
import jax
import copy

from variables_names_to_labels_map import variables_names_map_sorted

med_scale_nk_price_wage_indexation_file = './model_definition/med_scale_nk_price_wage_indexation.yaml'
mod_dict0 = ep.parse(med_scale_nk_price_wage_indexation_file)

shocks = ('e_w', 0.1)

phi_y_list = [0.5, 1.0]
phi_pi_list = [1., 2.0]
psi_w_list = [120.60, 2000.0, 5250.0]
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
        
        # Store IRFs
        models_tuple = (*models_tuple, get_deviations_from_steady_state(mod_org_stst, x1[:30]))
    
    figs, axs, _ = pplot((get_deviations_from_steady_state(mod_org_stst, x_org1[:30]), *models_tuple), labels = list(variables_names_map_sorted.values()))
    
    # Add legend with values of the parameter(phi_y or phi_pi)
    for ax in axs:
        ax.legend([f'{param_name} = {param_value}' for param_value in [param_value_org, *parameter_values_list]])
        ax.axhline(y=0.0, color='0.8', linestyle='--')
    
    # for index, fig in enumerate(figs):
    #     fig.savefig(f'plots/over_parameters/{param_name}/ten_periods/figure{index+1}.png')
    
    plt.show()

# solve_model_for_different_parameter_values(mod_dict0, shocks, phi_y_list, 'phi_y')
solve_model_for_different_parameter_values(mod_dict0, shocks, phi_pi_list, 'phi_pi')