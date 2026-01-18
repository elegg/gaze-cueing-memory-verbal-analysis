import seaborn as sns
from matplotlib import pyplot as plt


def update_labels(label):

    return label[0].upper() + label[1:].lower() if len(label)==5 else "Gaze"

def generate_graph(df):

    Palette = sns.color_palette("pastel")
    #define your preference
    """
    sns.set(font_scale = 1)
    sns.set_style("whitegrid")
    sns.set_palette(Palette)
    """
    sns.set_theme(
        rc={'figure.figsize':(11.7,8.27)},
        style="whitegrid",
        font_scale=1,
        palette=Palette
        
        )

    fig, axs = plt.subplots(ncols=2, figsize=(14,8.27))

    dprime_graph = sns.boxplot(x="cue_type", y="dprime",
                hue="consistency",
                data=df,
                ax=axs[0])

    

    dprime_graph.set(ylabel = "d'", xlabel="",)
    dprime_graph.set_title('A', y=1, x=0.02, fontsize = 16)
    dprime_graph.set_xticklabels([update_labels(t.get_text().lower()) for t in dprime_graph.get_xticklabels()], fontsize=14)
    dprime_graph.set_ylabel(fontsize = 16, ylabel="d'")

   # dprime_graph.set(ylim=(0, 4))

    rt_graph = sns.boxplot(x="cue_type", y="median_rt",
                hue="consistency",
                data=df,
                ax=axs[1])

    rt_graph.set(ylabel = "Reaction Time (ms)", xlabel="")
    rt_graph.set_ylabel(fontsize = 16, ylabel="Reaction Time (ms)")
    rt_graph.set_xticklabels([update_labels(t.get_text().lower()) for t in rt_graph.get_xticklabels()], fontsize=14)
    rt_graph.set(ylim=(0, 1200))
    rt_graph.set_title('B', y=1, x=0.02, fontsize = 16)

    handles, labels = rt_graph.get_legend_handles_labels()

    l = plt.legend(handles[0:2], ["Cued", "Uncued"], bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    axs[0].get_legend().remove()
    plt.tight_layout()

    fig.figure.savefig('figure4.png',dpi=600)


