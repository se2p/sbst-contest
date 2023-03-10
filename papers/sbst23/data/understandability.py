import pandas as pd
import matplotlib.pyplot as plt
import utils

utils.preload_latex_style("IEEE")

data = pd.read_csv('./human-study.csv')

columns = [q + '_EV' for q in ['Q2', 'Q6', 'Q9']]
tool_names = ['Collections', 'Threeten', 'Spatial4j']

data_EV = data[columns].rename(columns={key: utils.textsc(value) for key, value in zip(columns, tool_names)})

fig = plt.figure(figsize=(3.5, 2.15))
ax = utils.violinplot(data_EV)
ax.set_yticks(range(1, 6))
utils.style_axes(fig, ax)
ax.set_ylabel('Understandability Rank')

utils.save_fig(fig, './understandability.pdf')
