import econpizza as ep
from grgrlib import *
import copy

yaml = './model_definition/nk_price_indexation.yaml'

mod_dict0 = ep.parse(yaml)
# this is now a dictionary!
type(mod_dict0) # dict

shocks = ('e_w', .01)

# load and find stst of first model
# mod0 = ep.load(mod_dict0)
# _ = mod0.solve_stst()
# x0, flag0 = mod0.find_path(shock=shocks)

# # create a copy for different parameters
# mod_dict1 = copy.deepcopy(mod_dict0)

# # set different alpha
# mod_dict1['steady_state']['fixed_values']['phi_y'] = 2



# # load and find stst of other model
# mod1 = ep.load(mod_dict1)
# _ = mod1.solve_stst()


# # use the stacking method. As above, you could also feed in the initial state instead
# x1, flag1 = mod1.find_path(shock=shocks)

# pplot((x0[:30], x1[:30]), labels=mod0['variables'], legend = ['label1', 'label2'])
# plt.show()


# Try doing it in a function, in a loop
# 1.25: strange output
# [1.65, 1.45, 1.75, 1.35] <- try this although its hard to read
phi_y_list = [1.65, 1.45, 1.75, 1.35]
def loop_over_phi_y(mod_dict_org, shocks, phi_y_list):
    # solve original model
    mod_org = ep.load(mod_dict_org)
    phi_y_org = mod_dict_org['steady_state']['fixed_values']['phi_y']
    _ = mod_org.solve_stst()
    # shock original model
    x_org, flag_org = mod_org.find_path(shock = ('e_w', 0.01))
    
    models_tuple = ()
    
    for phi_y in phi_y_list:
        mod_dict = copy.deepcopy(mod_dict_org)
        mod_dict['steady_state']['fixed_values']['phi_y'] = phi_y
       
        # solve copied model
        mod = ep.load(mod_dict)
        _ = mod.solve_stst()
        
        x, flag = mod.find_path(shock = shocks)
        # Store IRFs
        models_tuple = (*models_tuple, x[:30])
    
    _, axs, _ = pplot((x_org[:30], *models_tuple), labels = mod_org['variables'])
    
    # Add legend with values of phi_y
    for ax in axs:
        ax.legend([f'phi_y = {phi_y}' for phi_y in [phi_y_org, *phi_y_list]])
    
    plt.show()

loop_over_phi_y(mod_dict0, shocks, phi_y_list)
