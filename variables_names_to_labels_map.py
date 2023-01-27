variables_names_map = {
    'y': 'Real output',
    'c': 'Consumption',
    'pi': 'Inflation',
    'R': 'Real interest rate',
    'Rn': 'CB interest rate',
    'Rk': 'Gross rental cost of capital',
    'beta': 'Discount factor',
    'w': 'Real wage',
    'w_markup': 'Wage mark up',
    'q': 'q',
    'mc': 'Real marginal costs',
    'k': 'Capital',
    'i': 'Investment',
    'n': 'Employment',
    'hhdf': 'Household discount factor',
    'g': 'Government spending',
    'b': 'Quantity of government bonds',
    'qb': 'Price of a government bond',
    't': 'Lump-sum taxes/transfers',
    'ds': 'Deposit supply',
    'bprof': 'Bank profits',
    'dd': 'Deposit demand',
    'MPK': 'Marginal productivity of capital',
    'cap_util': 'Capital utilization',
    'cap_util_costs': 'Capital utilization costs',
    'y_prod': 'Production',
    'pitilde': 'Price indexation',
    'wtilde': 'Wage indexation',
    'pi_w': 'Wage inflation'
}

# sorted_dict = sorted(variables_names_map, key=str.lower)
variables_names_map_sorted = dict(sorted(variables_names_map.items(), key=lambda x: x[0].lower()))
# variables_list = ['b', 'beta', 'bprof', 'c', 'cap_util', 'cap_util_costs', 'dd', 'ds', 'g', 'hhdf', 'i', 'k', 'mc', 'MPK', 'n', 'pi', 'pi_w', 'pitilde', 'q', 'qb', 'R', 'Rk', 'Rn', 't', 'w', 'w_markup', 'wtilde', 'y', 'y_prod']