import pandas as pd

from pymatgen.ext import matproj
from pymatgen.core import periodic_table

if __name__ == '__main__':
    # path
    output_filepath = './query_result.csv'

    # elements groups
    transition_metal = []
    chalcogen = []
    others = []
    for e in periodic_table.Element:
        if e.group == 16:
            chalcogen.append(e.symbol)
        elif e.group >= 3 and e.group <= 12:
            transition_metal.append(e.symbol)
        else:
            others.append(e.symbol)

    # only consider a few chalcogens
    chalcogen = ['S', 'Se', 'Te']

    # open restful interface
    with matproj.MPRester(api_key='9bASScRXuQNDSebS') as m:
        # build criteria
        criteria = {
                'elements':{
                    '$in': transition_metal,
                    '$in': chalcogen,
                    '$nin': others,
                    },
                'nelements':{'$in': [2, 3]},
                }
        properties = ['material_id', 'pretty_formula']
        result = m.query(criteria=criteria, properties=properties)

    result_df = pd.DataFrame.from_records(result)
    result_df.to_csv(output_filepath, index=False)
