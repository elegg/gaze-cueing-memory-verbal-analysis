import seaborn as sns
from matplotlib import pyplot as plt



def generate_graph(df):

    Palette = sns.color_palette("pastel")
    #define your preference
    sns.set(font_scale = 1)
    sns.set_style("whitegrid")
    sns.set_palette(Palette)

    fig, axs = plt.subplots(ncols=2)

    dprime_graph = sns.boxplot(
        df[["dprime-gazed-at", "dprime-gazed-away"]], 
        ax=axs[0]
        )
    

    dprime_graph.set(ylabel = "d'", xlabel="")
    dprime_graph.set_title('A', y=1, x=0.02, fontsize = 12)
    dprime_graph.set_xticklabels(["-".join(t.get_text().split("-")[1:]).title() for t in dprime_graph.get_xticklabels()])
    dprime_graph.set(ylim=(0, 4))



    rt_graph = sns.boxplot(
        df[["rt-gazed-at", "rt-gazed-away"]],
        ax=axs[1]
                )

    rt_graph.set(ylabel = "Reaction Time (ms)", xlabel="")
    rt_graph.set_xticklabels(["-".join(t.get_text().split("-")[1:]).title() for t in rt_graph.get_xticklabels()])
    rt_graph.set(ylim=(0, 1200))
    rt_graph.set_title('B', y=1, x=0.02, fontsize = 12)

    plt.show()


