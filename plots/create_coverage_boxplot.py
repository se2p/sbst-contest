"""
Generate a boxplot for the distributions of line coverage, branch coverage and mutants killed.

This script requires one csv-Files to load the results from the SBST-tool competition for every budget.

You can generate such a csv-file from the provided zip-File by:

# unzip evosuite_results_30.zip
# cd evosuite_results_30
# head -1 <ANY_BENCHMARK_FOLDER>/metrics/transcript.csv > metrics.csv
# find -wholename "*/metrics/transcript.csv" -exec sed -n 2p {} \; >> metrics.csv

This will generate a metrics.csv in the results-folder as needed by this script.
Generate the csv-File for every budget.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style("whitegrid")

"""
List of tuples to specify the location and search budgets to be used.
Every tuple must contain of 3 elements: (int, str, file_path)

The first element is used to order the boxes.
The second element is used in the legend of the box plot for the given dataset.
The thrid element is the file_path to the data set
"""
data_sets = [
    (30, "30s", "results_evosuite_30/metrics.csv"),
    (120, "120s", "results_evosuite_120/metrics.csv"),
    (300, "300s", "results_evosuite_300/metrics.csv")
]

output_file_name = "CoverageBoxV.pdf"


def load_data_set(data_set):
    data = pd.read_csv(data_set[2])
    data["budget"] = data_set[0]
    return data


metrics = [x for x in map(load_data_set, data_sets)]
means = [x for x in map(lambda x: x.groupby("benchmark").mean().reset_index(), metrics)]

metrics_all = pd.concat(metrics)
means_all = pd.concat(means)


def plot_whole_coverage_v(df, cols=None,
                          save_as="",
                          palette=None,
                          labels=None,
                          xticklabels=None):
    if cols is None:
        cols = ["linesCoverageRatio", "conditionsCoverageRatio", "mutantsCoverageRatio"]
    if xticklabels is None:
        xticklabels = ["Lines Covered", "Branches Covered", "Mutants Killed"]
    if not palette:
        palette = sns.color_palette()
    fig = plt.figure(figsize=(7, 5))
    data = pd.melt(df.set_index(["benchmark", "run", "budget"])[cols], ignore_index=False).reset_index()
    ax = sns.boxplot(data=data,
                     x="variable", y="value", hue="budget", palette=palette)
    ax.set_xticklabels(xticklabels)
    ax.set_xlabel("")
    ax.set_ylabel("Ratio")
    ax.legend(title="Search Budget", labels=labels, handles=ax.legend().legendHandles, bbox_to_anchor=(0.5, -.1), loc=9,
              borderaxespad=0., ncol=3)
    ax.set_yticklabels([str(int(x)) + "%" for x in ax.get_yticks()])
    if save_as:
        fig.savefig(save_as, bbox_inches="tight")
    plt.show()


coverage_cols = ["linesCoverageRatio", "conditionsCoverageRatio", "mutantsCoverageRatio"]
viridis = sns.color_palette("viridis")
pal = [viridis[1], viridis[3], viridis[5]] if len(data_sets) == 3 else viridis
plot_whole_coverage_v(means_all, coverage_cols, save_as=output_file_name, palette=pal, labels=[x[1] for x in data_sets])
