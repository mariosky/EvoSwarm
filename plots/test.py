import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from   scipy import stats
from statistics import median, mean

files = [r'..\5m.csv', r'..\10m.csv', r'..\20m.csv' ]


def get_data_frame(file):
    data = pd.read_csv(file, header=None, names=[ 'instance', 'dim', 'worker', 'ratio'] )
    return data




dim = [10,20]
tests = [('1w','2w'),('2w','4w'),('4w','8w'),('8w','16w')]
workers  = ['1w','2w','4w','8w', '16w']


for f in files:
    results = []
    df = get_data_frame(f)

    print(f)
    for d in dim:
        for test in tests:
            X = df[df.dim.eq(d) & df.worker.eq(test[0])].ratio
            Y = df[df.dim.eq(d) & df.worker.eq(test[1])].ratio

            Xmedian = median(X)
            Ymedian = median(Y)


            speedup = Ymedian/Xmedian

            #print(stats.normaltest(X), stats.normaltest(Y))

            kstat, k_pvalue = stats.ks_2samp(X, Y)
            wstat, w_pvalue = stats.mannwhitneyu(X, Y, alternative='less')
            print( ",".join( map(str, [d, test[0],test[1],speedup,kstat, k_pvalue ,wstat, w_pvalue])))
    #       results.append( (d, test[0], test[1],speedup, kstat, k_pvalue, wstat, w_pvalue))
    #print(results)


# for f in files:
#     results = []
#     df = get_data_frame(f)
#     for d in dim:
#             medians = [median(df[df.dim.eq(d) & df.worker.eq(w)].ratio)  for w in workers]
#             base = medians[0]
#             speedup = [str(m/base) for m in medians]
#             print (d,',',','.join(speedup))
