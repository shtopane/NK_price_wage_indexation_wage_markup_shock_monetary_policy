import econpizza as ep
from grgrlib import *
from variables_names_to_labels_map import variables_names_map_sorted

# med_scale_nk_price_wage_indexation_file = './model_definition/med_scale_nk_price_wage_indexation1.yaml'
med_scale_nk_price_wage_indexation_file = './model_definition/med_scale_nk_price_wage_indexation.yaml'
# med_scale_nk_price_wage_indexation_file = './model_definition/med_scale_nk.yaml'


med_scale_nk_price_wage_indexation_mod = ep.load(med_scale_nk_price_wage_indexation_file)
_  = med_scale_nk_price_wage_indexation_mod.solve_stst()

shocks = ('e_w', 0.1)
mod_org_stst = np.fromiter(med_scale_nk_price_wage_indexation_mod['stst'].values(), dtype = float)
print(mod_org_stst)
print(med_scale_nk_price_wage_indexation_mod['variables'])

med_scale_nk_price_wage_indexation_x, _ = med_scale_nk_price_wage_indexation_mod.find_path(shock = shocks)

figs, axs , _ = pplot(
    med_scale_nk_price_wage_indexation_x[:30], 
    labels = list(variables_names_map_sorted.values()), 
    title = "Price and Wage Indexation Medium NK"
)

plt.show()

# for index, fig in enumerate(figs):
#     fig.savefig(f'plots/version_2/plot_his_version_{index}.png')
