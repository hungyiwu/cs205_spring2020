import os
import pandas as pd
import seaborn as sns

from matplotlib import pyplot as plt

if __name__ == '__main__':
    folderpath = './speed_test_result'
    df_list = []
    for name in os.listdir(folderpath):
        n_core = name[:-len('.txt')].split('_')[1]
        run_id = name[:-len('.txt')].split('_')[3]
        p = os.path.join(folderpath, name)
        df = pd.read_csv(p)
        df['n_core'] = n_core
        df['run_id'] = run_id
        df_list.append(df)

    df = pd.concat(df_list, axis=0)\
            .reset_index(drop=True)

    sns.catplot(data=df, x='log10(num_file)', y='real(sec)', hue='n_core')
    plt.savefig('speed_test_result.png')
