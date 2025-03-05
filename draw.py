import os
import matplotlib
import pandas as pd
import seaborn as sns
import geopandas as gpd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.gridspec as gridspec
from typing import List, Dict, Union, Tuple
from matplotlib.colors import LogNorm, Normalize
from helper import JobHelper,CountryHelper

class Histogram():
    def __init__(self, models):
        self.models = models
        pass

    def draw(self,df:pd.DataFrame,x:str, dataset:str=None,
                  aggregate:bool=False):
        
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
        
        if aggregate:
            fig, ax = plt.subplots(figsize=(10, 8))
            
            ax = sns.countplot(data=df, x=x,
                hue='model',palette='Set1',
                order=df[x].value_counts().index,
                saturation=0.9,edgecolor='black',
                linewidth=0.8
            )

            plt.title(f"Frequency of {x} by Model", fontsize=18, fontweight='bold', pad=20, color='#333333')
            plt.xlabel(x, fontsize=14, fontweight='medium', labelpad=15)
            plt.ylabel("Count", fontsize=14, fontweight='medium', labelpad=15)
            plt.xticks(rotation=45, ha='center', fontsize=12)
            plt.yticks(range(16), fontsize=12)

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

        fig = plt.figure(figsize=(16, 12))
        gs = gridspec.GridSpec(2, 2, figure=fig, wspace=0.2, hspace=0.3)
        colors = sns.color_palette("Set1", len(self.models))

        for i, model_name in enumerate(self.models):
            ax = fig.add_subplot(gs[i//2, i%2])
            
            sns.countplot(
                data=df[df['model'] == model_name],
                x=x,
                order=df[x].value_counts().index,
                color=colors[i],
                edgecolor='black',
                linewidth=0.7,
                ax=ax,
                saturation=1.0
            )
            
            ax.set_title(f"{model_name}", fontsize=16, fontweight='bold', pad=0)
            ax.set_xlabel("")
            ax.set_ylabel("Count", fontsize=14, fontweight='medium', labelpad=10)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha='center', fontsize=11, fontweight='medium')
            ax.set_yticks(range(16))
            ax.yaxis.grid(True, linestyle='--', alpha=0.7)
            
            for spine in ax.spines.values():
                spine.set_linewidth(0.8)
                spine.set_color('#444444')
            
            ax.set_ylim(bottom=0)

        fig.text(0.5, 0.02, x, ha='center', fontsize=16, fontweight='bold')
        fig.suptitle(f'Frequency of {x} by Model', 
                    fontsize=20, y=0.98, fontweight='bold', color='#333333')
        fig.text(0.5, 1, dataset, 
                ha='center', fontsize=14, color='#666666', style='italic')

        plt.tight_layout(rect=[0, 0.04, 1, 0.94])
        
        return plt
    
class Map():
    def __init__(self,models):
        self.models = models
        self.countryH = CountryHelper()

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
        
        jobH = JobHelper()
        countryH = CountryHelper()
        labels = jobH.sectors + jobH.certifications + \
                 countryH.countries + countryH.country2short.values()

        self._label2color = dict(zip(labels,sns.color_palette("tab20", len(labels))))

    def squeeze_text(self,txt:str, width:int=25)->str:
        def get_idx(txt:str, width:int=15)->int:
            idx = 0
            prev_idx = 0
            distance = None
            best_distance = float('inf')

            #Get index of best space to convert to newline
            while True:
                idx += txt[idx:].find(' ') + 1
                distance = abs(width-idx)            

                if distance >= best_distance:
                    return prev_idx-1

                best_distance = distance
                prev_idx = idx        
        
        if len(txt) <= width:
            return txt
        
        #Perform first replacement
        prev_txt = txt
        idx = get_idx(txt,width)
        
        if idx == -1:
            return txt
        
        txt = txt[:idx]+'\n'+txt[idx+1:]
        prev_idx = idx

        #Perform while the text keeps changing
        while (prev_txt != txt) and (len(txt[idx:]) >= width):
            prev_txt = txt
            prev_idx = idx
            
            idx = get_idx(txt[idx:],width)
            idx += prev_idx
            txt = txt[:idx]+'\n'+txt[idx+1:]
            
        return txt

    def label2color(self, label:str):
        return self._label2color[label.replace('\n',' ')]

    def draw(self,df:pd.DataFrame,x:str,
                 dataset:str=None,aggregate:bool=False,
                 text_width:int=None, other:float=None,
                 rotation:int=140):
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
            df[x] = df[x].apply(lambda x: self.squeeze_text(x,text_width))

        if aggregate:
            fig, ax = plt.subplots(figsize=(9, 7))
            
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
                colors=list(map(self.label2color, data.index)),
                startangle=rotation,textprops={'fontsize': 10}
            )   

            title = f"Distribution of {x} - Aggregate"

        else:

            fig = plt.figure(figsize=(16, 12))
            gs = gridspec.GridSpec(2, 2, figure=fig, wspace=-0.1)

            for i, model_name in enumerate(self.models):
                ax = fig.add_subplot(gs[i//2, i%2])
                
                data = df[df['model'] == model_name][x].value_counts()
                if other is not None: #Group classes with less than [other]% representation in an Other class
                    total = data.sum()
                    data = data[data >= other * total]
                    other_count = total - data.sum()
                    if other_count > 0:
                        data['Other'] = other_count

                colors = list(map(self.label2color,data.index))

                ax.pie(
                    data,
                    labels=[l if pct >= other*100 else '' for l,pct in zip(data.index, 100.*data/data.sum())],
                    autopct=lambda pct: f'{round(pct)}%',
                    startangle=rotation, colors=colors,
                    explode=[max((10-pct)/35,0) for pct in 100.*data/data.sum()]
                )   

                #Set font size of labels differently from pct
                for text in ax.texts:
                    if '%' in text.get_text():
                        text.set_fontsize(11) #pct
                    else:
                        text.set_fontsize(8) #labels

                title = f'Distribution of {x} by Model'
                ax.set_title(f"{model_name}", fontsize=16, fontweight='bold', pad=0)
                ax.yaxis.grid(True, linestyle='--', alpha=0.7)
                
                for spine in ax.spines.values():
                    spine.set_linewidth(0.8)
                    spine.set_color('#444444')

        fig.text(0.5, 0.02, x, ha='center', fontsize=16, fontweight='bold')
        fig.suptitle(title,fontsize=20, y=0.93, fontweight='bold', color='#333333')
        fig.text(0.5, 0.95, dataset, ha='center', fontsize=14, color='#666666', style='italic')
        plt.tight_layout(rect=[0, 0.04, 1, 0.94])

        return plt

