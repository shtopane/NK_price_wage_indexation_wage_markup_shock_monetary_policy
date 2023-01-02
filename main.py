import econpizza as ep
from grgrlib import *

# model file paths
med_scale_nk_file = './model_definition/med_scale_nk.yaml'
med_scale_nk_price_indexation_file = './model_definition/med_scale_nk_price_indexation.yaml'

# Solve Basic Medium model
med_scale_nk_mod: ep.PizzaModel = ep.load(med_scale_nk_file)
_ = med_scale_nk_mod.solve_stst()

# Solve model with Price indexation
med_scale_nk_price_indexation_mod = ep.load(med_scale_nk_price_indexation_file)
_  = med_scale_nk_price_indexation_mod.solve_stst()

# Specify shock(beta)
shocks = ('e_beta', 0.01)

# Shock the models and extract IRFs
med_scale_nk_x, _ = med_scale_nk_mod.find_path(shock = shocks)
med_scale_nk_price_indexation_x, _ = med_scale_nk_price_indexation_mod.find_path(shock = shocks)

# Plot
pplot(med_scale_nk_x[:30], labels = med_scale_nk_mod["variables"], title = "Basic Medium NK")
pplot(med_scale_nk_price_indexation_x[:30], labels = med_scale_nk_price_indexation_mod["variables"], title = "Price Indexation Medium NK")
plt.show()