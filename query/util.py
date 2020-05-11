import re

from pymatgen.core import periodic_table

def element_of_interest():
    group_dict = {
            'transition_metal': [],
            'chalcogen': ['S', 'Se', 'Te'],
            'others': [],
            }
    for e in periodic_table.Element:
        if e.group >= 3 and e.group <= 12:
            group_dict['transition_metal'].append(e.symbol)
        elif e.symbol not in group_dict['chalcogen']:
            group_dict['others'].append(e.symbol)
    return group_dict

def decomp_formula(formula):
    decomp_list = []
    for comp in re.findall(pattern='[A-Z]{1}[a-z]?\d*', string=formula):
        element_symbol = re.findall(pattern='[A-Z]{1}[a-z]?', string=comp)[0]
        num_element = re.findall(pattern='\d+', string=comp)
        if not num_element: # single element in formula
            num_element = 1
        else: # multiple element
            num_element = int(num_element[0])
        decomp_list.append((element_symbol, num_element))
    return decomp_list
