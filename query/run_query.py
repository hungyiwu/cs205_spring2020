import pandas as pd

from pymatgen.ext import matproj
from pymatgen.core import periodic_table

import util

if __name__ == '__main__':
    # path
    output_filepath = './query_result.csv'

    elementgroup_dict = util.element_of_interest()

    # open restful interface
    with matproj.MPRester(api_key='9bASScRXuQNDSebS') as m:
        # build criteria
        criteria = {
                'elements':{
                    '$in': elementgroup_dict['transition_metal'],
                    '$in': elementgroup_dict['chalcogen'],
                    '$nin': elementgroup_dict['others'],
                    },
                'nelements':{'$in': [2, 3]},
                }
        properties = ['material_id', 'pretty_formula', 'spacegroup']
        result = m.query(criteria=criteria, properties=properties)

    record = [{'material_id': row['material_id'],
        'pretty_formula': row['pretty_formula'],
        'space_group': row['spacegroup']['symbol'],
        } for row in result]
    result_df = pd.DataFrame.from_records(record)
    result_df.to_csv(output_filepath, index=False)
