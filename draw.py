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
             aggregate:bool=False, hue:str=None, y:str=None, bar_labels:bool=False,
             long_layout:bool=False,ylim:int=15, grid:bool=False,jaja:int=0,
             xtick_label_max_len:int=0, rotation:int=90, ystep:int=1,
             text_width:int=None,figsize:Tuple[int,int]=(16,12), legend:Union[None,Tuple[float,float]]=None,
             hspace:int=0.3,title_size:int=12, violin:bool=False, swarm:bool=False):
        
        assert not(violin and swarm)
        
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
        
        if not y:
            y='count'
            df[y] = df.groupby([x,'model'] + ([hue] if hue else []))[x].transform('count')

        #Delimit text with new lines for better drawing
        if text_width is not None:
            df = df.copy()
            df[x] = df[x].apply(lambda x: squeeze_text(x, text_width))
        
        if 'Education' in x:
            order = list(map(lambda cert: squeeze_text(cert, text_width), self.jobH.certifications))
        elif 'Sector' in x:
            order = {squeeze_text(v, text_width): j for j, v in enumerate(self.jobH.sectors)}
        else:
            order = df.groupby(x)[y].sum().sort_values(ascending=False).index.tolist() if aggregate else None
        
        palette = {**self.colorH._label2color, **self.colorH._continent2color, **self.colorH._region2color}
        if aggregate:
            fig, ax = plt.subplots(figsize=figsize if not long_layout else (24,6))
            
            ax = [sns.barplot,sns.swarmplot, sns.violinplot][2 if violin else swarm](
                data=df, x=x, y=y,hue=hue,
                order=order,
                palette=palette,
                
                #Parameters for violin plot only
                **({} if not violin else {
                    'split': True, 'inner': None,
                }),

                #Parameters for swarm plot only
                **({} if not swarm else {
                    'dodge': True,
                    'size': 5,
                })
            )

            fig.suptitle(f'Distribution of {x} by Model (Aggregate)' if y=='count' else f'Mean {y} Distribution in {x} by Model', 
                         fontsize=title_size, y=0.965, fontweight='bold', color='#333333')
            plt.xlabel(x, fontsize=14, fontweight='medium', labelpad=15)
            plt.ylabel(y.capitalize(), fontsize=14, fontweight='medium', labelpad=15)
            plt.xticks(rotation=rotation, ha='center', fontsize=12)
            plt.yticks(range(0,ylim+ystep,ystep), fontsize=12)
            fig.text(0.5, 0.93, dataset, ha='center', fontsize=title_size-2, color='#666666', style='italic')


            if hue and legend is not None:
                _legend = ax.legend(
                    title=f'{hue}',frameon=True, framealpha=0.95,
                    fontsize=title_size-4,
                    title_fontsize=title_size-3,
                    edgecolor='#444444',loc='upper right',bbox_to_anchor=legend,
                                     
                    handles = [
                        matplotlib.patches.Patch(
                            color=[self.colorH.label2color,self.colorH.region2color]['Region' in hue](h),
                            label=h
                        )
                        for h in (df[hue].unique()\
                                  if 'Region' not in hue else \
                                  sorted(df[hue].unique(),key=lambda h: self.colorH._region2order[h])
                        )
                    ]
                )
                _legend.get_title().set_fontweight('bold')

            ax.yaxis.grid(True, linestyle='--', alpha=0.7, color='#888888')
            
            for spine in ax.spines.values():
                spine.set_linewidth(0.8)
                spine.set_color('#444444')
            
            ax.set_frame_on(True)
            ax.patch.set_edgecolor('#888888')
            ax.patch.set_linewidth(0.8)

            #Shorten xtick_label
            if xtick_label_max_len > 0:
                ax.set_xticklabels([
                    f'{label.get_text()[:xtick_label_max_len]}..'
                    if len(label.get_text()) > xtick_label_max_len else label.get_text()
                    for label in ax.get_xticklabels()
                ])

                #If shortening xtick_labels and long_layout==True, move xtick_labels on bars
                if long_layout:
                    positions = ax.get_xticks()
                    labels = [item.get_text() for item in ax.get_xticklabels()]
                    for i, (pos, label) in enumerate(zip(positions, labels)):
                        ax.annotate(
                            text=label,
                            xy=(pos, 0),
                            ha='center', va='bottom',
                            xytext=(0, 4),
                            textcoords='offset points',
                            fontsize=max(6.5, 
                                min(12,#The less unique countires = the wider the bars = the larger the text
                                0.06 * (196 - len(df[x].unique()))
                            )),
                            fontweight='light', color='black',
                            rotation=rotation
                        )

                    # Remove xticklabels
                    ax.set_xticklabels([])

            
            if bar_labels and not swarm and not violin:
                for bar in ax.patches:
                    height = bar.get_height()
                    if height > 0:
                        ax.text(
                            bar.get_x() + bar.get_width() / 2,
                            bar.get_y() + height / 2,
                            f'{int(height)}',
                            ha='center', va='center', fontsize=10,
                            color='black', alpha=0.8,
                            path_effects=[
                                path_effects.Stroke(linewidth=1, foreground='white'),
                                path_effects.Normal()
                            ]
                        )

            plt.tight_layout()
            return plt

        if long_layout:
            fig = plt.figure(figsize=figsize)
            gs = gridspec.GridSpec(4, 1, figure=fig, wspace=0.2, hspace=hspace)
        else:
            fig = plt.figure(figsize=figsize)
            gs = gridspec.GridSpec(2, 2, figure=fig, wspace=0.2, hspace=hspace)
            
        for i, model_name in enumerate(self.models):
            
            ax = fig.add_subplot(
                gs[i//2, i%2] if not long_layout else gs[i,0]
            )
            data = df[df['model'] == model_name]

            [sns.barplot, sns.swarmplot, sns.violinplot][2 if violin else swarm](
                data=data,
                x=x, y=y, hue=hue,
                palette=palette,
                linewidth=0.7,
                order=order if order else data.groupby(x)[y].sum().sort_values(ascending=False).index.tolist(),
                ax=ax, legend=(i==0),
                
                # Parameters for violin plot only
                **({} if not violin else {
                    'split': True, 'inner': None,
                }),
                
                # Parameters for swarm plot only
                **({} if not swarm else {
                    'dodge': True,
                    'size': 4,
                })
            )
            
            #Move positions underneat xlabels
            if violin:
                # Add the number of items on each violin plot
                counts = data.groupby(x).size()
                for idx, count in enumerate(counts):
                    ax.text(
                        x=idx, y=ylim - 1, s=f'{count}',
                        ha='center', va='top', fontsize=10, color='black'
                    )
            if hue and legend is not None and i==0:
                _legend = ax.legend(
                    title=f'{hue}',frameon=True, framealpha=0.95,
                    fontsize=title_size-4,
                    title_fontsize=title_size-3,
                    edgecolor='#444444',loc='upper right',bbox_to_anchor=legend,

                    handles = [
                        [matplotlib.patches.Patch,matplotlib.lines.Line2D][swarm](
                            label=h,
                            **({
                                'color':[self.colorH.label2color,self.colorH.region2color]['Region' in hue](h)
                            } if not swarm else {
                                #Display handles using dots instead of a bar
                                'xdata':[0],'ydata':[0],'color':'w',
                                'marker':'o','markersize':8,
                                'markerfacecolor':[self.colorH.label2color,self.colorH.region2color]['Region' in hue](h)
                            }),

                        )
                        for h in (df[hue].unique()\
                                  if 'Region' not in hue else \
                                  sorted(df[hue].unique(),key=lambda h: self.colorH._region2order[h])
                        )
                    ]
                )
                _legend.get_title().set_fontweight('bold')

            if bar_labels and not swarm and not violin:
                for bar in ax.patches:
                    height = bar.get_height()
                    if height > 0:
                        ax.text(
                            bar.get_x() + bar.get_width() / 2,
                            bar.get_y() + height / 2,
                            f'{int(height)}',
                            ha='center', va='center', fontsize=10,
                            color='black', alpha=0.8,
                            path_effects=[
                                path_effects.Stroke(linewidth=1, foreground='white'),
                                path_effects.Normal()
                            ]
                        )

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
                            xytext=(0, 4),
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
            
            if grid:
                for spine in ax.spines.values():
                    spine.set_linewidth(0.8)
                    spine.set_color('#444444')
                ax.yaxis.grid(True, linestyle='--', alpha=0.7, color='#888888')
                ax.xaxis.grid(not swarm, linestyle='--', alpha=0.7 if not swarm else 0, color='#888888')

            ax.set_title(f"{model_name}", fontsize=title_size, fontweight='bold', pad=0)
            ax.set_xlabel("")
            ax.set_ylabel(y.capitalize(), fontsize=14, fontweight='medium', labelpad=10)
            ax.tick_params(axis='x', rotation=rotation, labelsize=11)
            ax.set_ylim(bottom=0)
            ax.set_yticks(range(0,ylim+ystep,ystep) if not long_layout and not violin else range(0,ylim+ystep,ystep))


        fig.text(0.5, 0.035, x, ha='center', fontsize=16, fontweight='bold')
        fig.suptitle(f'Distribution of {x} by Model' if y=='count' else f'Mean {y} Distribution in {x} by Model', 
                    fontsize=title_size, y=0.965, fontweight='bold', color='#333333')
        fig.text(0.5, 0.93, dataset, ha='center', fontsize=title_size-2, color='#666666', style='italic')

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

    def draw(self,df:pd.DataFrame,x:str,
                  title:str,cmap:str,y:str=None,
                  ax:Union[Tuple[Tuple[matplotlib.axes._axes.Axes]],None]=None,
                  show:bool=False,log:bool=False, show_labels:bool=False,
                  low_poly:bool=False,legend:bool=True,step:int=1,
                  max_count:int=15,legend_loc=[0,0,0,0]) -> matplotlib.axes._axes.Axes:
    
        legend_loc = [[0.15, 0.06, 0.71, 0.02][i]+j for i,j in enumerate(legend_loc)]

        if ax is None:
            fig = plt.figure(figsize=(14, 7))
            ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())
            
        world = gpd.read_file(os.path.join("world_data",f"ne_{11 if low_poly else 1}0m_admin_0_countries.shp"))
        world.boundary.plot(ax=ax, transform=ccrs.PlateCarree(), linewidth=0)

        if not y:
            y='count'
            x_counts = self.countryH.get_country_frequency(df[x])
        else:
            x_counts = self.countryH.get_country_average_y(df,x,y)
            
        negligible_value = 0.1
        world = world.merge(x_counts, how='left', left_on='NAME', right_on=x)
        world[y] = world[y].fillna(negligible_value)

        #Calculate min and max for better tick control
        vmin = int(world[y][world[y]>negligible_value].min() // 10 * 10) \
               if 'Age' in y else [0, 0.1][log]
        vmax = int(world[y].max() // 10 * 10 + 10) if 'Age' in y else max_count
        custom_ticks = \
            ([0,negligible_value,1] if log else []) + \
            list(range(int(vmin),int(vmax)+step,step))

        world.plot(
            column=y,cmap=cmap,
            transform=ccrs.PlateCarree(),
            linewidth=0.05,edgecolor='black',
            legend=True, ax=ax,
            norm=[Normalize,LogNorm][log](vmin=vmin, vmax=vmax),
            legend_kwds={
                'label': y.capitalize(),
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
        
        #Apply hatching + greying color for countries with neglibile values
        for _, row in world.iterrows():
            if row[y] <= negligible_value:
                ax.add_geometries(
                    [row.geometry],
                    crs=ccrs.PlateCarree(),
                    facecolor='lightgrey',
                    edgecolor='black',
                    linewidth=0.1,
                    alpha=0.8,
                    hatch='///'
                )

        if show_labels:
            for _, row in world.iterrows():
                if row[y] > vmin: 
                    ax.text(
                        row['LABEL_X'],row['LABEL_Y'],
                        f"{int(row[y])}" if row[y]>=1 else '',
                        fontsize=6, ha='center', va='center',
                        transform=ccrs.PlateCarree(),
                        color='black', alpha=0.8,
                        path_effects=[
                            path_effects.Stroke(linewidth=1, foreground='white'),
                            path_effects.Normal()
                        ]
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
                        text.set_fontsize(14)  # pct
                    else:
                        text.set_fontsize(10)  # labels
                    
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
 
class PopulationPyramid():
    def __init__(self, models):
        self.models=models
        self.colorH = ColorHelper()
        self.model_hatches = {
            'ChatGPT' : 4*'o',
            'Claude'  : 4*'/', 
            'Gemini'  : 4*'.', 
            'DeepSeek': 4*'x',
        }

    def draw(self, df:pd.DataFrame,x:str,stacked_hue:str,xlabels:List[str],dataset:str,
             aggregate:bool=False,xlim:int=10, xstep:int=1,hue:str='model',
             dodge:int=1.5,bar_width:float=0.2,fontsize:int=10, figsize:Tuple[int,int]=None):
        
        y='pct'
        hatches = {"/\\|-+xo*."[i]*4:hue_i for i,hue_i in enumerate(df[hue].unique())} \
                  if hue!='model' else self.model_hatches
        
        #Prepare data for population pyramid
        df = df.groupby([stacked_hue, x,hue]).size().reset_index(name='count')
        df[y] = (df['count'] / df['count'].sum()) * 100

        if aggregate:
            plt.figure(figsize=figsize if figsize else (10,6))

            #Separate males and females
            males   = df[df[stacked_hue] == 'Male'  ].groupby(x)[y].sum().reindex(xlabels, fill_value=0)
            females = df[df[stacked_hue] == 'Female'].groupby(x)[y].sum().reindex(xlabels, fill_value=0)
            female_surplus = (females-males).apply(lambda j: max(j,0))
            male_surplus   = (females-males).apply(lambda j: min(j,0))

            plt.barh(females.index, females-female_surplus,
                    color='#D81B60' , alpha=0.7, label='Females')
            plt.barh(
                females.index, female_surplus, left=males,
                color='#AD1457',alpha=0.7, label='Female Surplus',
            )

            plt.barh(males.index, -males-male_surplus, color='#1E88E5', alpha=0.7, label='Males')
            plt.barh(
                males.index, male_surplus,
                left=-females,
                color='#1565C0',alpha=0.7, label='Male Surplus',
            )

            for i, (m,f) in enumerate(zip(males,females)):
                plt.text(f+0.5, i, f'{f:.1f}%' if f else "", va='center', ha='left', color='black')
                plt.text(-m-3 , i, f'{m:.1f}%' if m else "", va='center', ha='left', color='black')

        else:
            plt.figure(figsize=figsize if figsize else (16, 9), dpi=300)  # Larger figure, higher DPI
            plt.style.use('seaborn-v0_8-whitegrid')  # More professional background
            for i,hue_i in enumerate(df[hue].unique()):

                #Get model-specific data
                model_df = df[df[hue] == hue_i]
                males   = model_df[model_df[stacked_hue] == 'Male'  ] \
                            .groupby(x)[y].sum().reindex(xlabels, fill_value=0)
                females = model_df[model_df[stacked_hue] == 'Female'] \
                            .groupby(x)[y].sum().reindex(xlabels, fill_value=0)
                
                female_surplus = (females-males).apply(lambda j: max(j,0))
                male_surplus   = (females-males).apply(lambda j: min(j,0))
                
                bar_adjust = bar_width*(i-dodge)
                female_x = [idx + bar_adjust for idx in range(len(xlabels))]
                male_x   = [idx + bar_adjust for idx in range(len(xlabels))]

                #Plot bars
                plt.barh(
                    y=female_x,
                    width=females-female_surplus, height=bar_width,
                    color='#D81B60', alpha=0.7, label='Females',
                    hatch=hatches[hue_i], edgecolor='snow', linewidth=0
                )
                plt.barh(
                    y=male_x,
                    width=-males-male_surplus, height=bar_width,
                    color='#1E88E5', alpha=0.7, label='Males',
                    hatch=hatches[hue_i],edgecolor='snow',linewidth=0
                )
                plt.barh(
                    y=female_x,
                    width=female_surplus, height=bar_width, left=males, 
                    color='#AD1457',alpha=0.7, label='Female Surplus',
                    hatch=hatches[hue_i],edgecolor='#F5F5F5',linewidth=0
                )
                plt.barh(
                    y=male_x,
                    width=male_surplus, height=bar_width, left=-females, 
                    color='#1565C0', alpha=0.7, label='Male Surplus',
                    hatch=hatches[hue_i],edgecolor='#F5F5F5',linewidth=0
                )
                
                #Add labels on each bar
                for fx,f in zip(female_x,females):
                    plt.text(x=f+0.1,y=fx,s=f'{f:.1f}%' if f else "",
                        va='center', ha='left', color='black', fontsize=10
                    )

                for mx,m in zip(male_x,males):
                    plt.text(x=-m-0.7,y=mx,s=f'{m:.1f}%' if m else "",
                        va='center', ha='left', color='black', fontsize=10
                    )

        #Customize the plot
        plt.xlabel('Population (%)', fontsize=fontsize)
        plt.ylabel(x,fontsize=fontsize)
        plt.xticks(range(-xlim,xlim+xstep,xstep))
        plt.yticks(range(len(xlabels)),xlabels)
        plt.suptitle(f'Population Pyramid', fontsize=fontsize+5, y=0.95, x=0.52, ha='center', fontweight='bold', color='#333333')
        plt.text(0, len(df[x].unique())-0.07, dataset, ha='center', fontsize=fontsize+2, color='#666666', style='italic')

        from matplotlib.patches import Patch
        plt.legend(
            handles=([
                Patch(facecolor='white',label=hue_i,hatch=hatches[hue_i],edgecolor='black',linewidth=0)
                for hue_i in reversed(df[hue].unique())
                ] if not aggregate else []) + [
                    Patch(facecolor='#1E88E5', label='Males',          edgecolor='black'),
                    Patch(facecolor='#D81B60', label='Females',        edgecolor='black'),
                    Patch(facecolor='#1565C0', label='Male Surplus',   edgecolor='black'),
                    Patch(facecolor='#AD1457', label='Female Surplus', edgecolor='black')
                ],
            title="Legend",title_fontsize=fontsize+2,loc='best',
            frameon=True,framealpha=0.7,edgecolor='lightgrey'
        )

        plt.axvline(x=0, color='black', linewidth=1, linestyle='--')
        plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{abs(x):g}'))
        plt.tight_layout()

        return plt
    
class StackedBar():
    def __init__(self,models):
        self.models=models
        self.colorH = ColorHelper()
        self.jobH = JobHelper()

    def draw(self, df:pd.DataFrame, x:str, stacked_hue:str,
         dataset:str=None, hue:str='model', ylim:int=5, ystep:int=1,grid:bool=True,
         figsize:Tuple[int, int]=(16,12), space:float=0, bar_labels:bool=False,
         txt_width:int=None, aggregate:bool=False, legend:bool=True):

        fig = plt.figure(figsize=figsize)
        gs = gridspec.GridSpec(4, 1, figure=fig, wspace=space, hspace=space)

        df = df.copy()
        df[x] = df[x].apply(lambda s: squeeze_text(s, txt_width))
        
        #To ensure x-axis and stacked_hue ordering is consistent across different hues
        x_ordering = {v: i for i, v in enumerate(
            df[x].unique() if x!='Sector' else list(map(lambda s: squeeze_text(s,txt_width),self.jobH.sectors)))
        }
        y_ordering = {v: i for i, v in enumerate(df[stacked_hue].unique())}\
                     if 'Region' not in stacked_hue else self.colorH._region2order

        coloring_scheme = [self.colorH.label2color, self.colorH.continent2color, self.colorH.region2color][
            2 if 'Region' in stacked_hue else 'Continent' in stacked_hue
        ]

        if aggregate:
            # Prepare the data for stacking
            data = df.groupby([x, stacked_hue]).size().reset_index(name='Frequency')

            # Pivot data to have each stacked_hue category as a separate column
            pivot_df = data.pivot_table(index=x, columns=stacked_hue, values='Frequency', aggfunc='sum', fill_value=0)
            pivot_df = pivot_df.reindex(sorted(x_ordering.keys(), key=lambda k: x_ordering[k]), fill_value=0)
            bottoms = [0] * len(pivot_df)

            # Ensure consistent ordering of stacked_hue categories
            ordered_columns = sorted(
                pivot_df.columns,
                key=lambda col: y_ordering[col]
            )

            ax = fig.add_subplot(gs[0, 0])

            for stacked_label in ordered_columns:
                bars = ax.bar(pivot_df.index, pivot_df[stacked_label], bottom=bottoms,
                              color=coloring_scheme(stacked_label), label=stacked_label)
                bottoms = [bottoms[j] + pivot_df[stacked_label].iloc[j] for j in range(len(bottoms))]

                # Display values on bar
                if bar_labels:
                    for bar in bars:
                        h = bar.get_height()
                        if h > 0:
                            ax.text(
                                x=bar.get_x() + bar.get_width() / 2,
                                y=bar.get_y() + h / 2,
                                s=f'{int(h)}',
                                ha='center', va='center', fontsize=10,
                                color='white', alpha=0.8,
                                path_effects=[
                                    path_effects.Stroke(linewidth=1, foreground='black'),
                                    path_effects.Normal()
                                ]
                            )

            if legend:
                ax.legend(
                    loc='best',title=stacked_hue, bbox_to_anchor=(1.03, 1.1),
                    handles = sorted(
                        ax.get_legend_handles_labels()[0],
                        key=lambda h: y_ordering[h.get_label()]
                    )
                )

            # Title and labels
            ax.set_title("Aggregate", fontsize=16, fontweight='bold', pad=0)
            ax.yaxis.grid(grid, linestyle='--', alpha=0.7 if grid else 0)
            ax.set_xlabel(x)
            ax.set_xticks(range(len(pivot_df)))

            # Set y-axis limits and labels
            ax.set_yticks(range(0, ylim + 1, ystep))
            ax.set_ylabel('Frequency')

            # Style the spines
            for spine in ax.spines.values():
                spine.set_linewidth(0.8)
                spine.set_color('#444444')
        else:        
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
                                color=coloring_scheme(stacked_label), label=stacked_label)
                    bottoms = [bottoms[j] + pivot_df[stacked_label].iloc[j] for j in range(len(bottoms))]

                    #Display values on bar
                    if bar_labels:
                        for bar in bars:
                            h = bar.get_height()
                            if h > 0:
                                ax.text(
                                    x=bar.get_x()+bar.get_width()/2,
                                    y=bar.get_y()+h/2,
                                    s=f'{int(h)}',
                                    ha='center', va='center', fontsize=10,
                                    color='white', alpha=0.8,
                                    path_effects=[
                                        path_effects.Stroke(linewidth=1, foreground='black'),
                                        path_effects.Normal()
                                    ]
                                )

                if legend and i==0:
                    ax.legend(
                        loc='best', title=stacked_hue, bbox_to_anchor=(1.03, 1.1),
                        handles=sorted(
                            [
                                matplotlib.patches.Patch(
                                    color=coloring_scheme(label),
                                    label=label
                                )
                                for label in y_ordering.keys()
                            ],
                            key=lambda h: y_ordering[h.get_label()]
                        )
                    )
                            

                #Title and labels
                ax.set_title(f"{hue_i}", fontsize=16, fontweight='bold', pad=0.2)
                ax.yaxis.grid(grid, linestyle='--', alpha=0.7 if grid else 0)
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