#!/usr/bin/env python

import pandas as pd
import utils

all_data = pd.read_csv('./results.csv')

coverage_columns = ['linesCoverageRatio',
                    'conditionsCoverageRatio',
                    'mutantsCoverageRatio']

translation = ['Lines Covered', 'Branches Covered', 'Mutants Killed']

columns = {
    'timeBudget': 'Time Budget',
    **dict(zip(coverage_columns, translation))
}

"""
(1) Remove all data not related to EvoSuite and only keep the relevant columns
(2) Rename the columns to give them more descriptive names
(3) Reshape the data such that the "Time Budget" is used as identifier, and the
    remaining columns are "un-pivoted":

          Time Budget          Metric     Percent
    0              30   Lines Covered    0.000000
    1              30   Lines Covered   20.833332
    ...           ...             ...         ...
    3898          120  Mutants Killed   55.882350
    3899          120  Mutants Killed    0.000000
"""
plot_data = (all_data[columns.keys()]  # (1)
             .rename(columns=columns)  # (2)
             .melt(id_vars='Time Budget',
                   var_name='Metric',
                   value_name='Percent'))  # (3)

"""
Create a boxplot of the EvoSuite data per "Metric" on the x-axis, plotting the 
corresponding values in the "Percent" column on the y-axis. Using "Time Budget"
as hue key creates grouped a boxplot: for each metric, it actually plots two 
boxes for the two budgets.
"""
utils.preload_latex_style("ACM")

fig = utils.boxplot(data=plot_data,
                    x='Metric',
                    y='Percent',
                    hue='Time Budget',
                    title='Time Budget [s]',
                    figsize=(3.5, 2.15))
utils.save_fig(fig, './CoverageBoxV.pdf')


def budget(seconds):
    return all_data['timeBudget'] == seconds


data30 = all_data[budget(30)]
data120 = all_data[budget(120)]


def benchmark_basename(benchmark_name):
    return textsc(benchmark_name.split('-')[0].capitalize())


def textsc(text):
    return r'\textsc{' + text + '}'


columns = {
    'benchmark': 'Benchmark',
    **dict(zip(coverage_columns, translation))
}

data_by_benchmark30 = (data30[['benchmark', *coverage_columns]]
                       .rename(columns=columns)
                       .melt(id_vars='Benchmark',
                             var_name='Metric',
                             value_name='Percent'))
benchmarks = data_by_benchmark30['Benchmark'].copy()
data_by_benchmark30['Benchmark'] = benchmarks.map(benchmark_basename)

fig = utils.boxplot(data=data_by_benchmark30,
                    x='Metric',
                    y='Percent',
                    hue='Benchmark',
                    figsize=(3.5, 2.15))
utils.save_fig(fig, './CoverageByBenchmark30.pdf')

data_by_benchmark120 = (data120[['benchmark', *coverage_columns]]
                        .rename(columns=columns)
                        .melt(id_vars='Benchmark',
                              var_name='Metric',
                              value_name='Percent'))
benchmarks = data_by_benchmark120['Benchmark'].copy()
data_by_benchmark120['Benchmark'] = benchmarks.map(benchmark_basename)

fig = utils.boxplot(data=data_by_benchmark120,
                    x='Metric',
                    y='Percent',
                    hue='Benchmark',
                    figsize=(3.5, 2.15))
utils.save_fig(fig, './CoverageByBenchmark120.pdf')

stats = {
    'score': 380.57,
    'cuts': all_data['class'].nunique(),
    'budgetShort': r'\SI{30}{\second}',
    'budgetLong': r'\SI{120}{\second}',
}


def my_capitalize(s):
    return s[0].upper() + s[1:]


# Mean line coverage, branch coverage, mutation score per budget
for criterion in coverage_columns:
    criterion_name = my_capitalize(criterion)

    # Short time budget
    avg = data30[criterion].mean()
    med = data30[criterion].median()
    stats['avg' + criterion_name + 'Short'] = float(avg)
    stats['med' + criterion_name + 'Short'] = float(med)

    # Long time budget
    avg = data120[criterion].mean()
    med = data120[criterion].median()
    stats['avg' + criterion_name + 'Long'] = float(avg)
    stats['med' + criterion_name + 'Long'] = float(med)


def test_gen_failed(data):
    return data[data['testcaseNumber'] == 0]


stats['numTestGenFailedShort'] = test_gen_failed(data30).shape[0]
stats['numTestGenFailedLong'] = test_gen_failed(data120).shape[0]

utils.write_tex_macros('./macros.tex', utils.create_tex_macros(stats))


def test_gen_failed_histogram(data):
    return (test_gen_failed(data)[['benchmark', 'class', 'testcaseNumber']]
            .groupby(['benchmark', 'class'])
            .count()
            .sort_values(by='testcaseNumber', ascending=False))


print('Classes for which no tests were generated (30 secs):',
      test_gen_failed_histogram(data30))

print('Classes for which no tests were generated (120 secs):',
      test_gen_failed_histogram(data120))
