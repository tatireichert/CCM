import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats


# # # This all about creating the figures # # #

class Figures:

    @staticmethod
    def plot_figures(data, output_file):
        #######################################

        def annotate(ax, data, x, y):
            slope, intercept, r_value, p_value, std_err = stats.linregress(data[x], data[y])
            text = "y=({0:.3f}x + {1:.2f}); r={2:.2f}; p={3:.3f}".format(slope, intercept,
                                                                         r_value,
                                                                         p_value)
            ax.annotate(text, xy=(0.05, 0.1), xycoords='axes fraction')


        ########################################

        mpl.rcParams['font.size'] = 11

        model_color = ['coral', 'peachpuff', 'cadetblue', 'powderblue']
        strategies = ('Absorptive roots', 'Arbuscular mycorrhizas', 'Phosphatases', 'Organic acids')
        x_class = data["soil_site"]


        ############################## FIGURE 1 ##############################

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        data1 = data[["root_%npp", "amf_%npp", "pase_%npp", "oas_%npp"]]

        fig1 = data1.plot(ax=ax2, kind="bar", stacked=True, color=model_color,
                          title='b',
                          ylabel='Percent (%) of total NPP', legend=False)
        fig1.set_xticklabels(x_class)

        # total C costs of P uptake per strategy, without labels
        data2 = data[["cost_root", "cost_amf", "cost_pase", "cost_oas"]]

        fig2 = data2.plot(ax=ax1, kind="bar", stacked=True, color=model_color,
                          title='a', legend=False,
                          ylabel='Total C cost of P acquisition (kg C $ha^{-1}$ $yr^{-1}$)')
        fig2.set_xticklabels(x_class)

        plt.xticks(rotation="vertical", horizontalalignment="center")
        plt.legend(title='P acquisition strategies', labels=strategies, bbox_to_anchor=(1.04, 0.5),
                   loc="center left")
        plt.savefig(output_file + 'Figure 1.png', bbox_inches='tight')
        plt.tight_layout()
        plt.clf()

        ############################## FIGURE 2 ##############################

        data1 = data[["root_%npp", "amf_%npp", "pase_%npp", "oas_%npp"]]
        fig1 = data1.plot(kind="bar", stacked=True, color=model_color,
                          title='', ylabel='Percent (%) of total NPP', legend=False)
        for i in fig1.containers:
            fig1.bar_label(i, label_type='center')
        fig1.set_xticklabels(x_class)

        plt.xticks(rotation="vertical", horizontalalignment="center")
        plt.legend(title='', labels=strategies, bbox_to_anchor=(1.04, 0.5),
                   loc="center left")
        plt.savefig(output_file + 'Figure 2.png', bbox_inches='tight')
        plt.tight_layout()
        plt.clf()

        ############################## FIGURE 3 ##############################

        uptake_p = data[["uptake_root", "uptake_amf", "uptake_pase", "uptake_oas"]].plot(kind="bar",
                                                                                         stacked=True,
                                                                                         color=model_color)
        for i in uptake_p.containers:
            uptake_p.bar_label(i, label_type='center')
        uptake_p.set_xticklabels(x_class)
        plt.title('')
        plt.ylabel('Total P uptake (kg P $ha^{-1}$ $yr^{-1}$)')
        plt.legend(title='Strategies', labels=strategies, bbox_to_anchor=(1.04, 0.5), loc="center left")
        plt.xticks(rotation="vertical", horizontalalignment="center")
        uptake_p.set_xticklabels(['{:,.0f}'.format(x) for x in uptake_p.get_xticks()])
        plt.savefig(output_file + 'Figure 3.png', bbox_inches='tight')
        plt.clf()

        ############################## FIGURE 4 ##############################

        fig = data[["root_cost%", "amf_cost%", "pase_cost%", "oas_cost%"]].plot(kind="bar",
                                                                                 stacked=True,
                                                                                 color=model_color)
        for i in fig.containers:
            fig.bar_label(i, label_type='center')
        fig.set_xticklabels(x_class)
        plt.title('')
        plt.ylabel('Costs of P acquisition per strategy (%)')
        plt.xticks(rotation="vertical", horizontalalignment="center")
        plt.legend(title='P acquisition strategies', labels=strategies, bbox_to_anchor=(1.04, 0.5),
                   loc="center left")
        plt.savefig(output_file + 'Figure 4.png', bbox_inches='tight')
        plt.clf()

        ############################## FIGURE 5 ##############################

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # total C costs of P uptake per strategy, without labels
        data1 = data[["cost_root", "cost_amf", "cost_pase", "cost_oas"]]

        fig1 = data1.plot(ax=ax1, kind="bar", stacked=True, color=model_color, legend=False,
                          ylabel='Total C cost of P acquisition (kg C $ha^{-1}$ $yr^{-1}$)')
        fig1.set_title('(a)', loc='left')
        fig1.set_xticklabels(x_class)

        plt.xticks(rotation="vertical", horizontalalignment="center")
        fig1.legend(title='', labels=strategies, bbox_to_anchor=(1, 1),
                    loc="upper right")

        fig2 = sns.regplot(ax=ax2, x=data['p_total'], y=data['cost_per_p'], color='black',
                           line_kws={'linestyle': '--', 'color': 'lightgrey'})
        fig2.set(xlabel='Total soil P  (kg $ha^{-1}$)',
                 ylabel='Average C cost per mol P (kg C)')
        fig2.set_title('(b)', loc='left')
        plt.xticks(rotation="horizontal", horizontalalignment="center")
        plt.ylim(0, 30)
        annotate(fig2, data=data, x='p_total', y='cost_per_p')

        plt.tight_layout()
        fig.savefig(output_file + "Figure 5.png")
        plt.clf()

        ############################## FIGURE 6 ##############################

        data['cost_foraging'] = data['cost_root'] + data['cost_amf']
        data['cost_mining'] = data['cost_pase'] + data['cost_oas']

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        fig1 = sns.regplot(ax=ax1, x=data['p_total'], y=data['cost_foraging'], color='black',
                           line_kws={'linestyle': '--', 'color': 'lightgrey'})
        fig1.set(xlabel='Total soil P (kg $ha^{-1}$)',
                 ylabel='Total C costs of P foraging (kg C $ha^{-1}$ $yr^{-1}$)')
        fig1.set_title('(a)', loc='left')
        annotate(ax1, data=data, x='p_total', y='cost_foraging')

        fig2 = sns.regplot(ax=ax2, x=data['p_total'], y=data['cost_mining'], color='black',
                           line_kws={'linestyle': '--', 'color': 'lightgrey'})
        fig2.set(xlabel='Total soil P  (kg $ha^{-1}$)',
                 ylabel='Total C costs of P mining (kg C $ha^{-1}$ $yr^{-1}$)')
        fig2.set_title('(b)', loc='left')
        annotate(ax2, data=data, x='p_total', y='cost_mining')

        plt.tight_layout()
        fig.savefig(output_file + "Figure 6.png")
        plt.clf()

        ############################## FIGURE 7 ##############################

        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 5))

        sns.regplot(ax=ax1, x=data['pi_sol'], y=data['cost_root'], color='black', ci=None,
                    line_kws={'linestyle': '--'}, label='Absorptive roots')
        sns.regplot(ax=ax1, x=data['pi_sol'], y=data['cost_amf'], color='grey', ci=None,
                    line_kws={'linestyle': '--'}, label='Arbuscular mycorrhizas')
        ax1.set(xlabel='Soluble Pi (kg $ha^{-1}$)',
                ylabel='Total C cost of foraging strategies (kg C $ha^{-1}$ $yr^{-1}$)')
        ax1.set_ylim(0, 1400)
        ax1.set_title('(a)', loc='left')
        ax1.legend(loc='upper left')

        sns.regplot(ax=ax2, x=data['po_sol'], y=data['cost_pase'], color='black', ci=None,
                    line_kws={'linestyle': '--', 'color': 'lightgrey'})
        ax2.set(xlabel='Soluble Po (kg $ha^{-1}$)',
                ylabel='Total C cost of phosphatases (kg C $ha^{-1}$ $yr^{-1}$)')
        ax2.set_ylim(0, 1400)
        ax2.set_title('(b)', loc='left')

        sns.regplot(ax=ax3, x=data['pi_insol'], y=data['cost_oas'], color='black', ci=None,
                    line_kws={'linestyle': '--', 'color': 'lightgrey'})
        ax3.set(xlabel='Insoluble Pi pool  (kg $ha^{-1}$)',
                ylabel='Total C cost of OAs (kg C $ha^{-1}$ $yr^{-1}$)')
        ax3.set_ylim(0, 1400)
        ax3.set_title('(c)', loc='left')

        # save the figure
        plt.tight_layout()
        fig.savefig(output_file + "Figure 7.png")

        plt.clf()

