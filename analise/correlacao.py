import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.patches as patches
import scipy.interpolate

from matplotlib.path import Path
from scipy import stats
from statsmodels.nonparametric.smoothers_lowess import lowess as  sm_lowess

plt.rc('patch', linewidth=2)
plt.rc('axes', linewidth=2, labelpad=10)
plt.rc('xtick.minor', size=4, width=2)
plt.rc('xtick.major', size=8, width=2, pad=8)
plt.rc('ytick.minor', size=4, width=2)
plt.rc('ytick.major', size=8, width=2, pad=8)
plt.rc('text', usetex=True)
plt.rc('font', family='serif', serif='Computer Modern', size=30)

############## Parâmetros ####################

xlabel = 'POP'
ylabel = 'CRIME'
arquivo_dados = '../dados-exemplo/xy.csv'

############## Parâmetros ####################

df_dados = pd.read_csv(arquivo_dados)

df_dados = df_dados.sort_values(df_dados.columns[0], ascending=True)

x = df_dados.iloc[:, 0].to_numpy()
y = df_dados.iloc[:, 1].to_numpy()

fig, ax = plt.subplots(figsize=(10, 7), dpi=90)
ax.set_xscale('log')
ax.set_yscale('log')

plt.scatter(x, y, s=200, marker='o', c='white', edgecolors='black', linewidth=2)

############## Regressão Não Paramétrica - Nadaraya-Watson ####################

sm_x, sm_y = sm_lowess(x, y,  frac=4./5., 
                           it=5, return_sorted = True).T

def smooth(x, y, xgrid):
    samples = np.random.choice(len(x), 50, replace=True)
    y_s = y[samples]
    x_s = x[samples]
    y_sm = sm_lowess(y_s,x_s, frac=4./5., it=5,
                     return_sorted = False)
    # regularly sample it onto the grid
    y_grid = scipy.interpolate.interp1d(x_s, y_sm, 
                                        fill_value='extrapolate')(xgrid)
    return y_grid

xgrid = np.linspace(x.min(),x.max())
K = 100
smooths = np.stack([smooth(x, y, xgrid) for k in range(K)]).T

# plt.plot(xgrid, smooths, color='tomato', alpha=0.25)

mean = np.nanmean(smooths, axis=1)
stderr = scipy.stats.sem(smooths, axis=1)
stderr = np.nanstd(smooths, axis=1, ddof=0)
# plot it
plt.fill_between(xgrid, mean-1.96*stderr,
                     mean+1.96*stderr, color='#56B4E9',linestyle='--',linewidth=2, alpha=0.25)
plt.plot(xgrid, mean, color='#56B4E9')


############## Regressão Não Paramétrica - Nadaraya-Watson ####################

############## Regressão Linear ####################

slope, intercept, r_value, p_value, std_err = stats.linregress(np.log10(x), np.log10(y))

a = pow(10, intercept)
plt.plot(x, a * pow(x, slope), color='#D55E00', linestyle='-', linewidth=2)

############## Regressão Linear ####################

############## Corner ####################

annotate = r'\begin{center}$\beta={beta}\pm{std_error}$\\($R^2={r2}$)\end{center}'
annotate = annotate.replace('{beta}', str(round(slope, 2)))
annotate = annotate.replace('{std_error}', str(round(std_err, 2)))
annotate = annotate.replace('{r2}', str(round(r_value * r_value, 2)))
plt.annotate(annotate, xy=(0.85, 0.15), xycoords='axes fraction', horizontalalignment='right', verticalalignment='bottom', fontsize=30)

############## Corner ####################

plt.xlabel(xlabel, fontsize=30)
plt.ylabel(ylabel, fontsize=30)

print('slope={}'.format(slope))
print('r2={}'.format(r_value * r_value))
print('intercept={}'.format(intercept))
print('error={}'.format(std_err))
print('p_value={}'.format(p_value))

fig.savefig('/home/carlos/Downloads/fig.pdf', format='pdf', bbox_inches='tight')

plt.show()