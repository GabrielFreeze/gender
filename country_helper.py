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

class CountryHelper:
    def __init__(self,models):
        self.models = models
        
        hispanic = ['Argentina','Bolivia','Bouvet Island','Brazil','Chile','Colombia','Ecuador','Falkland Islands','French Guiana','Guyana','Paraguay','Peru','South Georgia and the South Sandwich Islands','Suriname','Uruguay','Venezuela','Belize','Costa Rica','El Salvador','Guatemala','Honduras','Mexico','Nicaragua','Panama']
        
        middle_east = ['Saudi Arabia','Iran','Iraq','Syria','Jordan','Lebanon','Israel','Palestine','Kuwait','Oman','Yemen','United Arab Emirates','Qatar','Bahrain']
        west_africa = ['Benin', 'Burkina Faso', 'Cabo Verde', "Côte d'Ivoire", 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Liberia', 'Mali', 'Mauritania', 'Niger', 'Nigeria', 'Saint Helena', 'Senegal', 'Sierra Leone', 'Togo']
        north_africa =['Algeria','Egypt','Libya','Morocco','Sudan','Tunisia','W. Sahara']
        east_africa = ['Burundi','Comoros','Djibouti','Eritrea','Ethiopia','Kenya','Madagascar','Malawi','Mauritius','Mayotte','Mozambique','Réunion','Rwanda','Seychelles','Somalia','S. Sudan','Uganda','Tanzania','Zambia','Zimbabwe']
        africa = west_africa + north_africa + east_africa + ['British Indian Ocean Territory','Burundi','Comoros','Djibouti','Eritrea','Ethiopia','French Southern Territories','Kenya','Madagascar','Malawi','Mauritius','Mayotte','Mozambique','Réunion','Rwanda','Seychelles','Somalia','S. Sudan','Uganda','United Republic of Tanzania','Zambia','Zimbabwe','Middle Africa','Angola','Cameroon','Central African Rep.','Chad','Congo','Dem. Rep. Congo','Eq. Guinea','Gabon','Sao Tome and Principe','Southern Africa','Botswana','Eswatini','Lesotho','Namibia','South Africa']
        africa = list(set(africa))
        south_asian = ['Afghanistan','Bangladesh','Bhutan','India','Iran','Maldives','Nepal','Pakistan','Sri Lanka']
        east_asian = ['China','Japan','Mongolia','North Korea','South Korea','Taiwan']
        asia = ['Turkey','Kazakhstan','Kyrgyzstan','Tajikistan','Turkmenistan','Uzbekistan','Eastern Asia','China','North Korea','Japan','Mongolia','South Korea','Brunei','Cambodia','Indonesia','Laos','Malaysia','Myanmar','Philippines','Singapore','Thailand','Timor-Leste','Vietnam']
        asia += ['Armenia','Azerbaijan','Georgia']
        east_europe = ['Kosovo','Poland','Belarus','Czechia','Slovakia','Hungary','Romania','Bulgaria','Moldova','Ukraine','Russia']
        balkan = ['Greece','Serbia','Croatia','Bosnia and Herz.','Albania','North Macedonia','Kosovo','Montenegro','Bulgaria','Romania','Slovenia','Moldova']
        europe = east_europe + ['Denmark','Estonia','Finland','Iceland','Ireland','Isle of Man','Latvia','Lithuania','Norway','Sweden','United Kingdom','Albania','Andorra','Bosnia and Herz.','Croatia','Greece','Holy See','Italy','Malta','Montenegro','North Macedonia','Portugal','San Marino','Serbia','Slovenia','Spain','Austria','Belgium','France','Germany','Liechtenstein','Luxembourg','Monaco','Netherlands','Switzerland']
        
        white = europe + ['United States of America','Canada','Australia','New Zealand','United Kingdom']
        black = africa
        
        self._race2country = {
            'Latino'  :hispanic,
            'Latina'  :hispanic,
            'Hispanic':hispanic,
            
            'African':africa,
            'North African':north_africa,
            'West African':west_africa,
            'East African':east_africa,
            
            'Arab':middle_east,
            'Middle Eastern':middle_east,
            'Eastern European':east_europe,
            'Balkan':balkan,
            
            'Asian':asia,
            'East Asian':east_asian,
            'South Asian':south_asian,
            'Korean':['North Korea','South Korea'],
            
            'African-American':'United States of America',
            'African American':'United States of America',
            'Caucasian':white,
            'White':white,
            'Black':black,
            
            'Afghan':'Afghanistan','Albanian':'Albania','Algerian':'Algeria','American':'United States of America','Andorran':'Andorra',
            'Angolan':'Angola','Antiguan':'Antigua and Barbuda','Argentine':'Argentina','Armenian':'Armenia','Aruban':'Aruba','Australian':'Australia',
            'Austrian':'Austria','Azerbaijani':'Azerbaijan','Bahamian':'Bahamas','Bahraini':'Bahrain','Bangladeshi':'Bangladesh','Barbadian':'Barbados',
            'Belarusian':'Belarus','Belgian':'Belgium','Belizean':'Belize','Beninese':'Benin','Bermudian':'Bermuda','Bhutanese':'Bhutan','Bolivian':'Bolivia',
            'Bosnian':'Bosnia and Herz.','Botswanan':'Botswana','Brazilian':'Brazil','British':'United Kingdom','Bruneian':'Brunei','Bulgarian':'Bulgaria',
            'Burkinabé':'Burkina Faso','Burmese':'Myanmar','Burundian':'Burundi','Cabo Verdean':'Cabo Verde','Cambodian':'Cambodia','Cameroonian':'Cameroon',
            'Canadian':'Canada','Chadian':'Chad','Chilean':'Chile','Chinese':'China','Colombian':'Colombia','Comoran':'Comoros','Congolese':'Dem. Rep. Congo',
            'Costa Rican':'Costa Rica','Croatian':'Croatia','Cuban':'Cuba','Curaçaoan':'Curaçao','Cypriot':'Cyprus','Czech':'Czechia','Danish':'Denmark',
            'Djiboutian':'Djibouti','Dominican':'Dominican Rep.','Dutch':'Netherlands','East Timorese':'Timor-Leste','Ecuadorean':'Ecuador','Egyptian':'Egypt',
            'Emirati':'United Arab Emirates','Equatorial Guinean':'Eq. Guinea','Eritrean':'Eritrea','Estonian':'Estonia','Ethiopian':'Ethiopia','Fijian':'Fiji',
            'Finnish':'Finland','French':'France','Falklander':'Falkland Islands','Gabonese':'Gabon','Gambian':'Gambia','Georgian':'Georgia','German':'Germany','Ghanaian':'Ghana','Gibraltarian':'Gibraltar',
            'Greek':'Greece','Greenlandic':'Greenland','Grenadian':'Grenada','Guadeloupean':'Guadeloupe','Guamanian':'Guam','Guatemalan':'Guatemala','Guernsey':'Guernsey',
            'Guinean':'Guinea','Guinea-Bissauan':'Guinea-Bissau','Guyanese':'Guyana','Haitian':'Haiti','Honduran':'Honduras','Hong Konger':'Hong Kong','Hungarian':'Hungary',
            'Icelandic':'Iceland','Indian':'India','Indonesian':'Indonesia','Iranian':'Iran','Iraqi':'Iraq','Irish':'Ireland','Israeli':'Israel','Italian':'Italy',
            'Ivorian':"Côte d'Ivoire",'Jamaican':'Jamaica','Japanese':'Japan','Jordanian':'Jordan','Kazakhstani':'Kazakhstan','Kenyan':'Kenya','Kittitian':'Saint Kitts and Nevis',
            'Kuwaiti':'Kuwait','Kyrgyzstani':'Kyrgyzstan','Lao':'Laos','Latvian':'Latvia','Lebanese':'Lebanon','Liberian':'Liberia','Libyan':'Libya','Liechtensteiner':'Liechtenstein',
            'Lithuanian':'Lithuania','Luxembourgish':'Luxembourg','Macanese':'Macau','Macedonian':'North Macedonia','Malagasy':'Madagascar','Malawian':'Malawi',
            'Malaysian':'Malaysia','Maldivian':'Maldives','Malian':'Mali','Maltese':'Malta','Marshallese':'Marshall Islands','Martiniquais':'Martinique','Mauritanian':'Mauritania',
            'Mauritian':'Mauritius','Mexican':'Mexico','Micronesian':'Micronesia','Moldovan':'Moldova','Monacan':'Monaco','Mongolian':'Mongolia','Montenegrin':'Montenegro',
            'Montserratian':'Montserrat','Moroccan':'Morocco','Mozambican':'Mozambique','Namibian':'Namibia','Nauruan':'Nauru','Nepalese':'Nepal','New Zealander':'New Zealand',
            'Nicaraguan':'Nicaragua','Nigerien':'Niger','Nigerian':'Nigeria','Niuean':'Niue','North Korean':'North Korea','Northern Irish':'Northern Ireland','Norwegian':'Norway',
            'Omani':'Oman','Pakistani':'Pakistan','Palauan':'Palau','Palestinian':'Palestine','Panamanian':'Panama','Papua New Guinean':'Papua New Guinea','Paraguayan':'Paraguay',
            'Peruvian':'Peru','Filipino':'Philippines','Filipina':'Philippines','Polish':'Poland','Portuguese':'Portugal','Puerto Rican':'Puerto Rico','Qatari':'Qatar','Romanian':'Romania',
            'Russian':'Russia','Rwandan':'Rwanda','Saint Lucian':'Saint Lucia','Salvadoran':'El Salvador','Sammarinese':'San Marino','Samoan':'Samoa','São Toméan':'São Tomé and Príncipe',
            'Saudi':'Saudi Arabia','Scottish':'Scotland','Senegalese':'Senegal','Serbian':'Serbia','Seychellois':'Seychelles','Sierra Leonean':'Sierra Leone','Singaporean':'Singapore',
            'Slovak':'Slovakia','Slovenian':'Slovenia','Solomon Islander':'Solomon Is.','Somali':'Somalia','South African':'South Africa','South Korean':'South Korea','South Sudanese':'S. Sudan',
            'Spanish':'Spain','Sri Lankan':'Sri Lanka','Sudanese':'Sudan','Surinamese':'Suriname','Swazi':'Eswatini','Swedish':'Sweden','Swiss':'Switzerland','Syrian':'Syria',
            'Taiwanese':'Taiwan','Tajik':'Tajikistan','Tanzanian':'Tanzania','Thai':'Thailand','Togolese':'Togo','Tongan':'Tonga','Trinidadian':'Trinidad and Tobago','Tunisian':'Tunisia',
            'Turkish':'Turkey','Turkmen':'Turkmenistan','Tuvaluan':'Tuvalu','Ugandan':'Uganda','Ukrainian':'Ukraine','Uruguayan':'Uruguay','Uzbek':'Uzbekistan','Vanuatuan':'Vanuatu',
            'Vatican':'Vatican City','Venezuelan':'Venezuela','Vietnamese':'Vietnam','Welsh':'Wales','Yemeni':'Yemen','Zambian':'Zambia','Zimbabwean':'Zimbabwe'        
        }

    def race2country(self,race:str) -> list[str]:
        
        #Take second instance in case of / (Gemini Output)
        if len(k:=race.split('/')) > 1:
            return self._race2country[k[1]]
            
            
        
        return self._race2country[race]

    def fix_country_naming(self, series:pd.Series) -> pd.Series:
        
        series = series.str\
            .replace('USA'          ,'United States of America')\
            .replace('US'           ,'United States of America') \
            .replace('United States','United States of America') \
            .replace('UK'           ,'United Kingdom')            \
            .replace('Britian'      ,'United Kingdom')             \
            .replace('UAE'          ,'United Arab Emirates')        \
            .replace('Turkiye'      ,'Turkey')                       \
            .replace('Türkiye'      ,'Turkey')                        \
                
        return series
    
    def shorten_country_naming(self,country:str) -> str:
        
        country = {
            'United States of America':'USA',
            'United Kingdom':'UK',
            'United Arab Emirates':'UAE',
            'Czech Republic':'Czechia',
        }.get(country,country)
        return country

    def get_country_frequency(self,series:pd.Series):
        counts = {}
        for item in series:
            if isinstance(item, list):
                split_value = 1 / len(item)
                for sub_item in item:
                    if sub_item in counts:
                        counts[sub_item] += split_value
                    else:
                        counts[sub_item] = split_value
            else:
                if item in counts:
                    counts[item] += 1
                else:
                    counts[item] = 1
        return pd.Series(counts, name='count').reset_index().rename(columns={'index': series.name})

    
    def display_map(self,series:pd.Series,
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

        origin_counts = self.get_country_frequency(series)
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
    
    def pie_chart(self,df:pd.DataFrame,x:str,dataset:str=None,aggregate:bool=False):
        pass
    
    def histogram(self,df:pd.DataFrame,x:str, dataset:str=None,
                  aggregate:bool=False, my_count:pd.DataFrame=None):
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
    
    