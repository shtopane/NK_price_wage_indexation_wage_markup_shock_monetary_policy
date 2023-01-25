import econpizza as ep
from grgrlib import *

# med_scale_nk_price_wage_indexation_file = './model_definition/med_scale_nk_price_wage_indexation1.yaml'
med_scale_nk_price_wage_indexation_file = './model_definition/med_scale_nk_price_wage_indexation.yaml'
# med_scale_nk_price_wage_indexation_file = './model_definition/med_scale_nk.yaml'


med_scale_nk_price_wage_indexation_mod = ep.load(med_scale_nk_price_wage_indexation_file)
_  = med_scale_nk_price_wage_indexation_mod.solve_stst()

shocks = ('e_w', 0.1)
print('pi_w', med_scale_nk_price_wage_indexation_mod['stst']['pi_w'])
print('mc', med_scale_nk_price_wage_indexation_mod['stst']['mc'])
print('w_markup', med_scale_nk_price_wage_indexation_mod['stst']['w_markup'])
print('w', med_scale_nk_price_wage_indexation_mod['stst']['w'])
print('dd', med_scale_nk_price_wage_indexation_mod['stst']['dd'])
print('ds', med_scale_nk_price_wage_indexation_mod['stst']['ds'])
# print('chi', med_scale_nk_price_wage_indexation_mod['parameters']['chi'])
psi_w = med_scale_nk_price_wage_indexation_mod['parameters']['psi_w']
w = med_scale_nk_price_wage_indexation_mod['stst']['w']
wtilde = med_scale_nk_price_wage_indexation_mod['stst']['wtilde']
print('psi_w', psi_w)
print('wtilde', wtilde)
print('wage adjustment costs psi_w/2 * (w/wtilde - 1)**2', (psi_w/2 * (w/wtilde - 1)**2))
print('b(should be around 0?)', med_scale_nk_price_wage_indexation_mod['stst']['b'])
med_scale_nk_price_wage_indexation_x, _ = med_scale_nk_price_wage_indexation_mod.find_path(shock = shocks)
index_of_b = med_scale_nk_price_wage_indexation_mod['variables'].index('b')
index_of_pi = med_scale_nk_price_wage_indexation_mod['variables'].index('pitilde')
# print(med_scale_nk_price_wage_indexation_x[:30][index_of_b])
print(med_scale_nk_price_wage_indexation_x[:30][index_of_pi])

figs, _ , _ = pplot(
    med_scale_nk_price_wage_indexation_x[:30], 
    labels = med_scale_nk_price_wage_indexation_mod["variables"], 
    title = "Price and Wage Indexation Medium NK"
)
plt.show()

# for index, fig in enumerate(figs):
#     fig.savefig(f'plots/version_2/plot_his_version_{index}.png')
