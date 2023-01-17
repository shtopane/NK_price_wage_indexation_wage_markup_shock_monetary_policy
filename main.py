import econpizza as ep
from grgrlib import *

# model file paths
med_scale_nk_file = './model_definition/med_scale_nk.yaml'
med_scale_nk_price_wage_indexation_file = './model_definition/med_scale_nk_price_wage_indexation.yaml'
small_scale_nk_price_indexation_file = './model_definition/nk_price_indexation.yaml'
# Solve Basic Medium model
# med_scale_nk_mod: ep.PizzaModel = ep.load(med_scale_nk_file)
# _ = med_scale_nk_mod.solve_stst()

med_scale_nk_price_wage_indexation_mod = ep.load(med_scale_nk_price_wage_indexation_file)
small_scale_nk_price_indexation_mod = ep.load(small_scale_nk_price_indexation_file)

# Smallest set of variables
base_variables = small_scale_nk_price_indexation_mod["variables"].copy()
# Order the variables in the bigger model the same way
med_variables = med_scale_nk_price_wage_indexation_mod["variables"].copy()
index_of_small_scale_variables_in_med = [index for index, variable in enumerate(med_variables) if variable in base_variables]

# Solve small model with price indexation
# _  = med_scale_nk_price_wage_indexation_mod.solve_stst()
# Solve model with Price indexation
_ = small_scale_nk_price_indexation_mod.solve_stst()

# Specify shock(beta)
shocks = ('e_w', 0.01)

# Shock the models and extract IRFs
# med_scale_nk_x, _ = med_scale_nk_mod.find_path(shock = shocks)
# med_scale_nk_price_wage_indexation_x, _ = med_scale_nk_price_wage_indexation_mod.find_path(shock = shocks)
small_scale_nk_price_indexation_x, _ = small_scale_nk_price_indexation_mod.find_path(shock = shocks)


med_scale_labels = [med_variables[i] for i in index_of_small_scale_variables_in_med]
# Plot
# pplot(med_scale_nk_x[:30], labels = med_scale_nk_mod["variables"], title = "Basic Medium NK")
pplot(small_scale_nk_price_indexation_x[:30], labels = base_variables, title = "Price Indexation Small NK")
# pplot(med_scale_nk_price_wage_indexation_x[:30, index_of_small_scale_variables_in_med], labels = med_scale_labels, title = "Price Indexation Medium NK")
plt.show()

def get_med_scale_variables(small_nk_variables, med_nk_variables):
    # Smallest set of variables
    base_variables = small_nk_variables.copy()
    # Order the variables in the bigger model the same way
    med_variables = med_nk_variables.copy()
    indexes = [index for index, variable in enumerate(med_variables) if variable in base_variables]
    med_scale_labels = [med_variables[i] for i in indexes]
    
    return (med_scale_labels, indexes)


# eq = R*betaPrime*(c - h*cLag)/(cPrime - h*c)/piPrime -  (1 + (psi_w/2 * (wPrime/wtilde - 1)**2))