import seaborn as sns
import matplotlib.pyplot as plt


def boxplot(data, x, y, hue, title=None, figsize=None):
    if title is None:
        title = hue

    n_colors = data[hue].nunique()

    def style_axes():
        # Enlarge the range of the y-axis. Otherwise, whiskers at 0% or 100% are
        # not visible.
        ax.set_ylim(-5, 105)
        all_axes = {'top': True, 'right': True, 'left': True, 'bottom': True}
        sns.despine(fig, ax, **all_axes)

    def set_legend():
        # Remove the label from the x-axis. We create a separate "legend box"
        # instead.
        ax.set_xlabel('')
        center_legend_below_plot = {
            'loc': 'lower center',
            'bbox_to_anchor': (0.5, -0.6)
        }
        ax.legend(title=title,
                  ncol=min(3, n_colors),
                  **center_legend_below_plot)

    # Create a grouped boxplot using the supplied data. "x" is the column name
    # of the data to plot on the x-axis, and "y" is the column name of the data
    # to plot on the y-axis. The "hue" determines the subgroups.
    fig = plt.figure(figsize=figsize)
    palette = sns.color_palette(palette='pastel', n_colors=n_colors)
    flierprops = {'marker': 'o', 'markersize': 1.0}
    ax = sns.boxplot(data=data, x=x, y=y, hue=hue, palette=palette,
                     linewidth=0.5, flierprops=flierprops)

    style_axes()

    # Display a legend below the plot, also giving the x-axis a label
    # (or "title"). The main purpose of the legend is to distinguish the boxes
    # within a grouped boxplot via their color.
    set_legend()

    return fig


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
