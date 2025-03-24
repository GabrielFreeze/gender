import os
import matplotlib
import pandas as pd
import seaborn as sns
import geopandas as gpd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.gridspec as gridspec
import matplotlib.patheffects as path_effects 
from typing import List, Dict, Union, Tuple
from matplotlib.colors import LogNorm, Normalize
from helper import JobHelper,CountryHelper,ColorHelper, squeeze_text

class Histogram():
    def __init__(self, models):
        self.models = models
        self.jobH = JobHelper()
        self.countryH = CountryHelper()
        
        self.colorH = ColorHelper()
          
    def draw(self,df:pd.DataFrame,x:str, dataset:str=None,
             aggregate:bool=False, hue:str=None,
             long_layout:bool=False,ylim:int=15,
             xtick_label_max_len:int=0, rotation:int=90,
             text_width:int=None,figsize:Tuple[int,int]=(16,12),
             hspace:int=0.3,title_size:int=12):
        
        plt.rcParams.update({
            'font.family': 'sans-serif',
            'font.sans-serif': ['Bahnschrift', 'Verdana'],
            'font.size': 11,
            'axes.titlesize': 16,
            'axes.labelsize': 14,
            'xtick.labelsize': 10,
            'ytick.labelsize': 10,
            'legend.fontsize': 12,
            'figure.titlesize': 18
        })
        sns.set_style("ticks", {'grid.linestyle': '--', 'grid.alpha': 0.6})
        
        #Delimit text with new lines for better drawing
        if text_width is not None:
            df = df.copy()
            df[x] = df[x].apply(lambda x: squeeze_text(x, text_width))
        
        if aggregate:
            fig, ax = plt.subplots(figsize=figsize if not long_layout else (24,6))
            
            ax = sns.countplot(
                data=df, x=x,
                hue=hue,
                order=df[x].value_counts().index,
                palette={**self.colorH._label2color, **self.colorH._continent2color},
                saturation=0.9,edgecolor='black',
                linewidth=0.8,
            )

            plt.title(f"Frequency of {x} by Model", fontsize=18, fontweight='bold', pad=20, color='#333333')
            plt.xlabel(x, fontsize=14, fontweight='medium', labelpad=15)
            plt.ylabel("Count", fontsize=14, fontweight='medium', labelpad=15)
            plt.xticks(rotation=45, ha='center', fontsize=12)
            plt.yticks(range(ylim+1), fontsize=12)

            legend = plt.legend(title='Model',frameon=True, 
                framealpha=0.95, fontsize=14,title_fontsize=15,
                edgecolor='#444444',loc='upper right',bbox_to_anchor=(1.01, 1.01)
            )
            legend.get_title().set_fontweight('bold')

            ax.yaxis.grid(True, linestyle='--', alpha=0.7, color='#888888')
            
            for spine in ax.spines.values():
                spine.set_linewidth(0.8)
                spine.set_color('#444444')
            
            ax.set_frame_on(True)
            ax.patch.set_edgecolor('#888888')
            ax.patch.set_linewidth(0.8)

            plt.tight_layout()
            return plt

        if long_layout:
            fig = plt.figure(figsize=figsize)
            gs = gridspec.GridSpec(4, 1, figure=fig, wspace=0.2, hspace=hspace)
        else:
            fig = plt.figure(figsize=figsize)
            gs = gridspec.GridSpec(2, 2, figure=fig, wspace=0.2, hspace=hspace)
        colors = sns.color_palette("Set1", len(self.models))

        for i, model_name in enumerate(self.models):
            
            ax = fig.add_subplot(
                gs[i//2, i%2] if not long_layout else gs[i,0]
            )
            sns.countplot(
                data=df[df['model'] == model_name],
                x=x, hue=hue,
                palette={**self.colorH._label2color, **self.colorH._continent2color},
                edgecolor='black',
                linewidth=0.7,
                ax=ax,
                saturation=1.0,
                order=df[df['model']==model_name][x].value_counts().index,
                legend=(i==0)
            )
            if hue and i==0:
                ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title=hue)
            
            ax.set_title(f"{model_name}", fontsize=title_size, fontweight='bold', pad=0)
            ax.set_xlabel("")
            ax.set_ylabel("Count", fontsize=14, fontweight='medium', labelpad=10)
            ax.tick_params(axis='x', rotation=rotation, labelsize=11)
            ax.set_ylim(bottom=0)
            ax.set_yticks(range(ylim+1) if not long_layout else range(0,ylim+1,5))

            #Shorten xtick_label
            if xtick_label_max_len > 0:
                ax.set_xticklabels([
                    f'{label.get_text()[:xtick_label_max_len]}..'
                    if len(label.get_text()) > xtick_label_max_len else label.get_text()
                    for label in ax.get_xticklabels()
                ])

                #If shortening xtick_labels and long_layout==True, move xtick_labels on bars
                if long_layout:
                    
                    # Get the tick positions and labels
                    positions = ax.get_xticks()
                    labels = [item.get_text() for item in ax.get_xticklabels()]

                    # Add annotations at the exact tick positions
                    for i, (pos, label) in enumerate(zip(positions, labels)):
                        ax.annotate(
                            text=label,
                            xy=(pos, 0),  # Use the exact tick position
                            ha='center', va='bottom',
                            xytext=(0, 9),
                            textcoords='offset points',
                            fontsize=max(6.5, 
                                min(12,#The less unique countires = the wider the bars = the larger the text
                                0.06 * (196 - len(df[df['model']==model_name][x].unique()))
                            )),
                            fontweight='light', color='black',
                            rotation=rotation
                        )

                    # Remove xticklabels
                    ax.set_xticklabels([])
            
            #No Grids and spines if we are offsetting the xticklabels
            else:
                ax.yaxis.grid(True, linestyle='--', alpha=0.7)
                for spine in ax.spines.values():
                    spine.set_linewidth(0.8)
                    spine.set_color('#444444')

        fig.text(0.5, 0.02, x, ha='center', fontsize=16, fontweight='bold')
        fig.suptitle(f'Frequency of {x} by Model', 
                    fontsize=20, y=0.98, fontweight='bold', color='#333333')
        fig.text(0.5, 1, dataset, ha='center', fontsize=title_size-2, color='#666666', style='italic')

        plt.tight_layout(rect=[0, 0.04, 1, 0.94])
        
        return plt
    
class Map():
    def __init__(self,models):
        self.models = models
        self.countryH = CountryHelper()
        self.jobH = JobHelper()

        labels = self.jobH.sectors + self.jobH.certifications + \
                 self.countryH.countries + list(self.countryH._country2short.values())

        self._label2color = dict(zip(labels,sns.color_palette("tab20", len(labels))))

    def draw(self,series:pd.Series,
                    title:str,cmap:str,
                    ax:Union[Tuple[Tuple[matplotlib.axes._axes.Axes]],None]=None,
                    show:bool=False,log:bool=False,
                    low_poly:bool=False,legend:bool=True,
                    max_count:int=15,legend_loc=[0,0,0,0]) -> matplotlib.axes._axes.Axes:
    
        legend_loc = [[0.15, 0.06, 0.71, 0.02][i]+j for i,j in enumerate(legend_loc)]

        if ax is None:
            fig = plt.figure(figsize=(14, 7))
            ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())
            
        world = gpd.read_file(os.path.join("world_data",f"ne_{11 if low_poly else 1}0m_admin_0_countries.shp"))
        world.boundary.plot(ax=ax, transform=ccrs.PlateCarree(), linewidth=0)

        origin_counts = self.countryH.get_country_frequency(series)
        world = world.merge(
            origin_counts,
            how='left', left_on='NAME', right_on=series.name
        )
        world['count'] = world['count'].fillna(0)
        world['log_count'] = world['count'].replace(0, 0.1)

        #Calculate min and max for better tick control
        vmin = 0.1 if log else 0
        vmax = max_count
        custom_ticks = [0,0.1,1,5,10,15] if log else [0,1,2,3,4, 5,6,7,8,9,10,11,12,13,14,15]
        custom_ticks = [t for t in custom_ticks if vmin <= t <= vmax]

        world.plot(
            column='log_count',
            cmap=cmap,
            transform=ccrs.PlateCarree(),
            linewidth=0.05,
            edgecolor='black',
            legend=True,
            ax=ax,
            norm=LogNorm(vmin=vmin, vmax=vmax) if log else Normalize(vmin=vmin, vmax=vmax),
            legend_kwds={
                'label': "Count",
                'orientation': "horizontal",
                'format': ticker.FuncFormatter(lambda x, _: f'{int(x)}' if x >= 1 else f'{x:.1f}'),
                'ticks': custom_ticks,
                'extend': 'max',
                'cax': ax.figure.add_axes(legend_loc)
            } if legend else {
                'label': "",
                'shrink':0.0000001,
                'ticks': [],
                'extend': 'neither',
                'cax': ax.figure.add_axes([0.5,0.5,0.001,0.001])
                
            }
        )
        ax.set_facecolor('#A6CAE0')
        ax.set_title(title, fontsize=12)
        ax.set_global()  # Set global extent
        ax.gridlines(draw_labels=False, alpha=0.1)

        if show:
            plt.tight_layout()
            plt.show()
        return ax

class Piechart():
    def __init__(self,models):
        self.models = models
        self.colorH = ColorHelper()

    def draw(self,df:pd.DataFrame,x:str, hue:str='model',
                 dataset:str=None,aggregate:bool=False,
                 text_width:int=None, other:float=None,
                 rotation:int=140, space:float=-0.1,
                 figsize:Tuple[int,int]=(16,12)):
        plt.rcParams.update({
            'font.family': 'sans-serif',
            'font.sans-serif': ['Bahnschrift', 'Verdana'],
            'font.size': 11,
            'axes.titlesize': 16,
            'axes.labelsize': 14,
            'xtick.labelsize': 10,
            'ytick.labelsize': 10,
            'legend.fontsize': 12,
            'figure.titlesize': 18
        })
        
        sns.set_style("whitegrid", {'grid.linestyle': '--', 'grid.alpha': 0.6})
        
        if text_width is not None:
            #Delimit text with new lines for better drawing
            df = df.copy()
            df[x] = df[x].apply(lambda x: squeeze_text(x, text_width))

        if aggregate:
            fig, ax = plt.subplots(figsize=figsize)
            
            data = df[x].value_counts()
            
            #Group classes with less than [other]% representation in an Other class
            if other is not None:
                total = data.sum()
                data = data[data >= other * total]
                other_count = total - data.sum()
                if other_count > 0:
                    data['Other'] = other_count
            
            ax.pie(
                data,
                labels=[l if pct >= other*100 else '' for l,pct in zip(data.index, 100.*data/data.sum())],
                autopct=lambda pct: f'{round(pct)}%' if pct >= other*100 else '',
                colors=list(map(self.colorH.label2color, data.index)),
                startangle=rotation,textprops={'fontsize': 10}
            )   

            title = f"Distribution of {x} - Aggregate"
            
            for text in ax.texts:
                if '%' in text.get_text():
                    text.set_fontsize(11)  # pct
                else:
                    text.set_fontsize(8)  # labels
                
                #Add white border around each character to ensure legibility
                text.set_path_effects([
                    matplotlib.patheffects.Stroke(linewidth=2, foreground='white'),
                    matplotlib.patheffects.Normal()
                ])
 
        else:

            fig = plt.figure(figsize=figsize)
            
            hues = df[hue].unique()
            n_hues = len(hues) 
            
            match n_hues:
                case 2:
                    gs = gridspec.GridSpec(1, 2, figure=fig, wspace=space,hspace=space)
                case 3:
                    gs = gridspec.GridSpec(2, 2, figure=fig, wspace=space)
                    gs.update(left=0.05, right=0.95, top=0.95, bottom=0.05, hspace=space)
                    gs[1, 0].set_position(gs[1, 0].get_position(fig).translated(0.25, 0))
                case 4:
                    gs = gridspec.GridSpec(2, 2, figure=fig, wspace=space,hspace=space)
                case _:
                    gs = gridspec.GridSpec(1, n_hues, figure=fig, wspace=space,hspace=space)      

            for i, hue_i in enumerate(df[hue].unique()):
                data = df[df['model'] == hue_i][x].value_counts()
                
                ax = fig.add_subplot(gs[i//2, i%2])
                
                if other is not None: #Group classes with less than [other]% representation in an Other class
                    total = data.sum()
                    data = data[data >= other * total]
                    other_count = total - data.sum()
                    if other_count > 0:
                        data['Other'] = other_count

                colors = list(map(self.colorH.label2color,data.index))

                ax.pie(
                    data,
                    labels=[l if pct >= other*100 else '' for l,pct in zip(data.index, 100.*data/data.sum())],
                    autopct=lambda pct: f'{round(pct)}%',
                    startangle=rotation, colors=colors,
                    explode=[max((10-pct)/35,0) for pct in 100.*data/data.sum()]
                )   

                # Set font size of labels differently from pct
                for text in ax.texts:
                    if '%' in text.get_text():
                        text.set_fontsize(11)  # pct
                    else:
                        text.set_fontsize(8)  # labels
                    
                    #Add white border around each character to ensure legibility
                    text.set_path_effects([
                        matplotlib.patheffects.Stroke(linewidth=2, foreground='white'),
                        matplotlib.patheffects.Normal()
                    ])

                title = f'Distribution of {x} by Model'
                ax.set_title(f"{hue_i}", fontsize=16, fontweight='bold', pad=0)
                ax.yaxis.grid(True, linestyle='--', alpha=0.7)
                
                for spine in ax.spines.values():
                    spine.set_linewidth(0.8)
                    spine.set_color('#444444')

        fig.text(0.5, 0.02, x, ha='center', fontsize=16, fontweight='bold')
        fig.suptitle(title,fontsize=20, y=0.93, fontweight='bold', color='#333333')
        fig.text(0.5, 0.95, dataset, ha='center', fontsize=14, color='#666666', style='italic')
        plt.tight_layout(rect=[0, 0.04, 1, 0.94])

        return plt
    
class StackedBar():
    def __init__(self,models):
        self.models=models
        self.colorH = ColorHelper()

    def draw(self, df:pd.DataFrame, x:str, stacked_hue:str,
         dataset:str=None, hue:str='model', ylim:int=5, ystep:int=1,
         figsize:Tuple[int, int]=(16,12), space:float=0, bar_labels:bool=False):

        fig = plt.figure(figsize=figsize)
        gs = gridspec.GridSpec(4, 1, figure=fig, wspace=space, hspace=space)

        #To ensure x-axis and stacked_hue ordering is consistent across different hues
        x_ordering = {v: j for j, v in enumerate(df[x].unique())}
        y_ordering = {v: j for j, v in enumerate(df[stacked_hue].unique())}

        for i, hue_i in enumerate(df[hue].unique()):

            #Prepare the data for stacking
            data = df[df['model'] == hue_i] \
                        .groupby([x, stacked_hue]) \
                        .size() \
                        .reset_index(name='Frequency')

            #Pivot data to have each stacked_hue category as a separate column
            pivot_df = data.pivot_table(index=x, columns=stacked_hue, values='Frequency', aggfunc='sum', fill_value=0)
            pivot_df = pivot_df.reindex(sorted(x_ordering.keys(), key=lambda k: x_ordering[k]), fill_value=0)
            bottoms = [0] * len(pivot_df) 

            #Ensure consistent ordering of stacked_hue categories across different hue_i
            ordered_columns = sorted(
                pivot_df.columns,
                key=lambda col: y_ordering[col]
            )

            ax = fig.add_subplot(gs[i, 0])

            for stacked_label in ordered_columns:
                bars = ax.bar(pivot_df.index, pivot_df[stacked_label], bottom=bottoms,
                              color=self.colorH.label2color(stacked_label), label=stacked_label)
                bottoms = [bottoms[j] + pivot_df[stacked_label].iloc[j] for j in range(len(bottoms))]

                #Display values on bar
                if bar_labels:
                    for bar in bars:
                        h = bar.get_height()
                        if h > 1:
                            ax.text(
                                x=bar.get_x()+bar.get_width()/2,
                                y=bar.get_y()+h/2,
                                s=f'{int(h)}',
                                ha='center', va='center', fontsize=10, color='white'
                            )

            if i == 0:
                ax.legend(loc='upper right', bbox_to_anchor=(1.03, 1), title=stacked_hue)

            #Title and labels
            ax.set_title(f"{hue_i}", fontsize=16, fontweight='bold', pad=0)
            ax.yaxis.grid(True, linestyle='--', alpha=0.7)
            ax.set_xlabel(x if i == len(df[hue].unique()) - 1 else "")
            ax.set_xticks(range(len(pivot_df)))

            # Set y-axis limits and labels
            ax.set_yticks(range(0, ylim+1, ystep))
            ax.set_ylabel('Frequency')

            # Style the spines
            for spine in ax.spines.values():
                spine.set_linewidth(0.8)
                spine.set_color('#444444')

        # Set the overall title and other texts
        title = f'Frequency of {stacked_hue} by {x}' if x != '№' else f'Frequency of {stacked_hue} by order of responses'
        # fig.text(0.5, 0.02, x, ha='center', fontsize=16, fontweight='bold')
        fig.suptitle(title, fontsize=20, y=0.93, fontweight='bold', color='#333333')
        fig.text(0.5, 0.95, dataset, ha='center', fontsize=14, color='#666666', style='italic')

        # Adjust layout to prevent overlap
        plt.tight_layout(rect=[0, 0.04, 1, 0.94])

        return plt