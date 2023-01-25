
import econpizza as ep
from grgrlib import *
import copy

med_scale_nk_price_wage_indexation_file = './model_definition/med_scale_nk_price_wage_indexation.yaml'
mod_dict0 = ep.parse(med_scale_nk_price_wage_indexation_file)

shocks = ('e_w', 0.1)

# phi_y_list = [1.65, 1.45, 1.75, 1.35]
phi_pi_list = [1.45, 1.55]
def loop_over_phi_pi(mod_dict_org, shocks, phi_pi_list):
    # solve original model
    mod_org = ep.load(mod_dict_org)
    phi_pi_org = mod_dict_org['steady_state']['fixed_values']['phi_pi']
    _ = mod_org.solve_stst()
    # shock original model
    x_org, flag_org = mod_org.find_path(shock = shocks)
    
    models_tuple = ()
    
    for phi_pi in phi_pi_list:
        mod_dict = copy.deepcopy(mod_dict_org)
        mod_dict['steady_state']['fixed_values']['phi_pi'] = phi_pi
       
        # solve copied model
        mod = ep.load(mod_dict)
        _ = mod.solve_stst()
        
        x, flag = mod.find_path(shock = shocks)
        # Store IRFs
        models_tuple = (*models_tuple, x[:30])
    
    _, axs, _ = pplot((x_org[:30], *models_tuple), labels = mod_org['variables'])
    
    # Add legend with values of phi_pi
    for ax in axs:
        ax.legend([f'phi_pi = {phi_pi}' for phi_pi in [phi_pi_org, *phi_pi_list]])
    
    plt.show()

loop_over_phi_pi(mod_dict0, shocks, phi_pi_list)