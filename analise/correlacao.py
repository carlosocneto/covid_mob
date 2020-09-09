import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.patches as patches

from matplotlib.path import Path
from scipy import stats

plt.rc('patch',linewidth=2)
plt.rc('axes', linewidth=2, labelpad=10)
plt.rc('xtick.minor', size=4, width=2)
plt.rc('xtick.major', size=8, width=2, pad=8)
plt.rc('ytick.minor', size=4, width=2)
plt.rc('ytick.major', size=8, width=2, pad=8)
plt.rc('text', usetex=True)
plt.rc('font', family='serif', serif='Computer Modern', size=30)

##############Parâmetros####################

limites_eixos = [10000, 10000000, 1, 40000]
xlabel='POP'
ylabel='CRIME'
arquivo_dados = '/home/carlos/Downloads/xy.csv'

##############Parâmetros####################


df_dados = pd.read_csv(arquivo_dados)

df_dados = df_dados.sort_values(df_dados.columns[0], ascending=True)

x = df_dados.iloc[:, 0].to_numpy()
y = df_dados.iloc[:, 1].to_numpy()

fig, ax = plt.subplots(figsize=(10,7),dpi=90)
ax.set_xscale('log')
ax.set_yscale('log')

slope, intercept, r_value, p_value, std_err = stats.linregress(np.log10(x),np.log10(y))

plt.scatter(x, y, s=200, marker='o', c='white', edgecolors='black', linewidth='2')

a=pow(10,intercept)
plt.plot(x,a*pow(x,slope), color='#D55E00', linestyle='-', linewidth=2)

# plt.plot(x,intercept + slope*x, color='#D55E00', linestyle='-', linewidth=2)

# Corner
xc=300000
yc=100
delta=0.1 # ]0,1[

logxc=math.log10(xc)
logyc=math.log10(yc)
logdelta=math.log10(delta)

logy0=logyc
logx0=(logy0-logdelta-intercept)/slope
logx1=logxc
logy1=(slope*logx1+intercept+logdelta)

x0=pow(10,logx0)
y0=pow(10,logy0)
x1=pow(10,logx1)
y1=pow(10,logy1)

vertices = [(x0, y0), (xc, yc), (x1, y1)]
codes = [Path.MOVETO, Path.LINETO, Path.LINETO]

path = Path(vertices, codes)
patch = patches.PathPatch(path, facecolor='white', linewidth=2)
ax.add_patch(patch)

annotate=r'\begin{center}$\beta={beta}\pm{std_error}$\\($R^2={r2}$)\end{center}'
annotate = annotate.replace('{beta}',str(round(slope,2)))
annotate = annotate.replace('{std_error}',str(round(std_err,2)))
annotate = annotate.replace('{r2}',str(round(r_value*r_value,2)))
plt.annotate(annotate, xy=(0.85, 0.15), xycoords='axes fraction', horizontalalignment='right', verticalalignment='bottom',fontsize=30)

#Corner

plt.xlabel(xlabel, fontsize=30)
plt.ylabel(ylabel, fontsize=30)

print('slope={}'.format(slope))
print('r2={}'.format(r_value*r_value))
print('intercept={}'.format(intercept))
print('erro={}'.format(std_err))
print('p_value={}'.format(p_value))

plt.axis(limites_eixos)

fig.savefig('/home/carlos/Downloads/fig.pdf', format='pdf',bbox_inches='tight')

plt.show()
