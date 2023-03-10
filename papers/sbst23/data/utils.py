import seaborn as sns
import matplotlib.pyplot as plt


def boxplot(data, *, x=None, y=None, hue=None, ax=None):
    n_colors = 1 if hue is None else data[hue].nunique()

    # Create a grouped boxplot using the supplied data. "x" is the column name
    # of the data to plot on the x-axis, and "y" is the column name of the data
    # to plot on the y-axis. The "hue" determines the subgroups.
    palette = sns.color_palette(palette='pastel', n_colors=n_colors)
    flierprops = {'marker': 'o', 'markersize': 1.0}

    if ax is None:
        ax = sns.boxplot(data=data, x=x, y=y, hue=hue, palette=palette,
                         linewidth=0.5, flierprops=flierprops)
    else:
        sns.boxplot(data=data, x=x, y=y, hue=hue, palette=palette,
                    linewidth=0.5, flierprops=flierprops, ax=ax)

    return ax


def violinplot(data, *, x=None, y=None, hue=None, ax=None):
    n_colors = 1 if hue is None else data[hue].nunique()

    # Create a grouped boxplot using the supplied data. "x" is the column name
    # of the data to plot on the x-axis, and "y" is the column name of the data
    # to plot on the y-axis. The "hue" determines the subgroups.
    palette = sns.color_palette(palette='pastel', n_colors=n_colors)
    flierprops = {'marker': 'o', 'markersize': 1.0}

    if ax is None:
        ax = sns.violinplot(data=data, x=x, y=y, hue=hue, palette=palette,
                            linewidth=0.5, flierprops=flierprops)
    else:
        sns.violinplot(data=data, x=x, y=y, hue=hue, palette=palette,
                       linewidth=0.5, flierprops=flierprops, ax=ax)

    return ax


def style_axes(fig, ax, ylim=None):
    # Enlarge the range of the y-axis. Otherwise, whiskers at 0% or 100% are
    # not visible.
    if ylim is not None:
        ylim_x, ylim_y = ylim
        ax.set_ylim(ylim_x, ylim_y)

    all_axes = {'top': True, 'right': True, 'left': True, 'bottom': True}
    sns.despine(fig, ax, **all_axes)


def set_legend(ax, title, ncol=1):
    # Remove the label from the x-axis. We create a separate "legend box"
    # instead.
    ax.set_xlabel('')
    center_legend_below_plot = {
        'loc': 'lower center',
        'bbox_to_anchor': (0.5, -0.5)
    }
    ax.legend(title=title,
              ncol=ncol,
              **center_legend_below_plot)


def save_fig(fig, filename):
    # Save the plot as a PDF. Without bbox_inches='tight', the legend is missing
    # in the PDF...
    fig.savefig(filename, bbox_inches='tight', backend='pgf')


def preload_latex_style(document_class="ACM"):
    plt.style.use('seaborn')
    sns.set_style('whitegrid', {'grid.linewidth': 52})
    sns.set_context('paper')

    # Load custom fonts. ACM uses Linux Libertine, IEEE uses Times.
    if document_class == "ACM":
        load_custom_font = '\n'.join([
            r'\usepackage{libertine,libertinust1math}',
            r'\usepackage[T1]{fontenc}',
        ])
    elif document_class == "IEEE":
        load_custom_font = '\n'.join([
            r'\usepackage{}',
            r'\usepackage[T1]{fontenc}',
        ])
    elif document_class == "beamer":
        load_custom_font = '\n'.join([
            r'\usepackage{sansmathfonts}',
            r'\usepackage[scaled=0.95]{helvet}',
            r'\renewcommand{\rmdefault}{\sfdefault}',
            r'\usepackage[T1]{fontenc}',
        ])
    else:
        load_custom_font = ''

    plt.rcParams.update({
        'text.usetex': True,
        'pgf.texsystem': 'pdflatex',
        'pgf.preamble': load_custom_font,
        'font.family': 'serif',
        'font.size': 11
    })


def create_tex_macros(kwargs):
    def create_tex_macro(kwarg):
        name, value = kwarg
        new_command = r'\newcommand{{\{}}}'

        if type(value) is str:
            new_command += r'{{{}\xspace}}'
        elif type(value) is float and 0 <= value <= 100:
            new_command += r'{{\SI[round-mode=figures,round-precision=3]{{{}}}{{\percent}}\xspace}}'
        elif type(value) is float or type(value) is int:
            new_command += r'{{\num{{{}}}\xspace}}'
        else:
            new_command += r'{{{}\xspace}}'

        return new_command.format(name, value)

    return (create_tex_macro(kwarg) for kwarg in kwargs.items())


def write_tex_macros(filename, macros):
    with open(filename, 'w') as f:
        lines = '\n'.join(macros)
        f.write(lines)

def textsc(text):
    return r'\textsc{' + text + '}'