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
    def __init__(self):
        
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

        self.countries = list(set([
            country for sublist in self._race2country.values()
                    for country in (sublist if isinstance(sublist, list) else [sublist])
        ]))

        self.country2short = {
            'United States of America':'USA',
            'United Kingdom':'UK',
            'United Arab Emirates':'UAE',
            'Czech Republic':'Czechia',
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
            .replace('United States','United States of America')  \
            .replace('UK'           ,'United Kingdom')             \
            .replace('Britian'      ,'United Kingdom')              \
            .replace('UAE'          ,'United Arab Emirates')         \
            .replace('Turkiye'      ,'Turkey')                        \
            .replace('Türkiye'      ,'Turkey')                         \
                
        return series
    
    def shorten_country_naming(self,series:pd.Series) -> str:
        return series.apply(
            lambda country: self.country2short[country]
            if country in self.country2short else country
        )

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

    def histogram(self,df:pd.DataFrame,x:str, dataset:str=None,
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
    


class JobHelper:
    def __init__(self):

        #Keep collapsed  
        self._job_title_to_sector = {
            'Restaurant kitchen supervisor': 'Hospitality, Retail and Other Services Managers',
            'Research scientist': 'Science and Engineering Professionals',
            'Administrative Assistant': 'Business and Administration Associate Professionals',
            'Retial Management': 'Administrative and Commercial Managers',
            'Middle Manager in Retail': 'Administrative and Commercial Managers',
            'Retail Worker': 'Sales Workers',
            'Marketing Manager': 'Administrative and Commercial Managers',
            'Taxi Driver': 'Drivers and Mobile Plant Operators',
            'Construction worker': 'Building and Related Trades Workers (excluding Electricians)',
            'Retired Nurse': 'Health Professionals',
            'Environmental Scientist': 'Science and Engineering Professionals',
            'Sales manager': 'Administrative and Commercial Managers',
            'Manufacturing supervisor': 'Production and Specialized Services Managers',
            'Senior developer': 'Information and Communications Technology Professionals',
            'Mental health and stress management': 'Health Professionals', #Assuming this means practicing in the field
            'Freelance translator': 'Legal, Social and Cultural Professionals',
            'Taxi driver': 'Drivers and Mobile Plant Operators',
            'Retired Office Worker': 'General and Keyboard Clerks',
            'Shop Owner': 'Administrative and Commercial Managers',
            'Teacher (unemployed)': 'Teaching Professionals',
            'Farmer': 'Market-oriented Skilled Agricultural Workers',
            'Construction foreman': 'Building and Related Trades Workers (excluding Electricians)',
            'Retired factory worker': 'Stationary Plant and Machine Operators',
            'Daycare center owner': 'Hospitality, Retail and Other Services Managers',
            'Bank Manager': 'Administrative and Commercial Managers',
            'Factory worker': 'Stationary Plant and Machine Operators',
            'Factory Shift Supervisor': 'Production and Specialized Services Managers',
            'IT': 'Information and Communications Technology Professionals',
            'Banker': 'Business and Administration Professionals',
            'Freelance Translator': 'Legal, Social and Cultural Professionals',
            'Housekeeping supervisor': 'Hospitality, Retail and Other Services Managers',
            'Retail Sales Associate': 'Sales Workers',
            'Help desk technician': 'Information and Communications Technicians',
            'Stay-at-Home Mother': 'Unemployed', # Or could be considered 'Personal Service Workers' but unemployed is more appropriate
            'Auto Mechanic': 'Metal, Machinery and Related Trades Workers',
            'Works in hospitality.': 'Personal Service Workers', #Assuming generic worker in hospitality
            'Civil Engineering': 'Science and Engineering Professionals',
            'Retired Gardener': 'Market-oriented Skilled Agricultural Workers',
            'Construction': 'Building and Related Trades Workers (excluding Electricians)',
            'Retail management': 'Administrative and Commercial Managers',
            'Self-employed seamstress': 'Food Processing, Woodworking, Garment and Other Craft and Related Trades Workers',
            'IT Professional': 'Information and Communications Technology Professionals',
            'Accounting clerk, former bank employee in China': 'Numerical and Material Recording Clerks',
            'IT technician': 'Information and Communications Technicians',
            'Food truck owner': 'Hospitality, Retail and Other Services Managers',
            'IT Project Manager': 'Information and Communications Technology Professionals',
            'Corporate Marketing': 'Administrative and Commercial Managers',
            'Caregiver': 'Personal Care Workers',
            'Civil engineer at a construction firm': 'Science and Engineering Professionals',
            'Factory worker, former civil engineer': 'Stationary Plant and Machine Operators',
            'Blue-Collar Worker': 'Labourers in Mining, Construction, Manufacturing and Transport', #Broad definition
            'Farmworker': 'Agricultural, Forestry and Fishery Labourers',
            'Warehouse Worker': 'Labourers in Mining, Construction, Manufacturing and Transport',
            'Part-time bookkeeper': 'Business and Administration Associate Professionals',
            'Senior Software Engineer': 'Information and Communications Technology Professionals',
            'Resturant Manager': 'Hospitality, Retail and Other Services Managers',
            'Marketing Director at FMCG company': 'Administrative and Commercial Managers',
            'Software developer': 'Information and Communications Technology Professionals',
            'Freelance graphic designer': 'Legal, Social and Cultural Professionals',
            'Restaurant worker': 'Personal Service Workers',
            'Part-time accountant': 'Business and Administration Associate Professionals',
            'Self-Employed': 'Administrative and Commercial Managers', #Broad, as a business owner.
            'Researcher': 'Science and Engineering Professionals',
            'Works as a Cashier': 'Customer Services Clerks',
            'Former retail manager, transitioning': 'Administrative and Commercial Managers',
            'Construction project manager': 'Science and Engineering Professionals',
            'Finance': 'Business and Administration Professionals',
            'Marketing Assistant': 'Business and Administration Associate Professionals',
            'Small import business owner': 'Administrative and Commercial Managers',
            'Tech Support': 'Information and Communications Technicians',
            'Social Media Manager': 'Business and Administration Professionals',
            'Works part-time as a care assistant': 'Personal Care Workers',
            'Freelance Writer': 'Legal, Social and Cultural Professionals',
            'Social media manager': 'Business and Administration Professionals',
            'Librarian': 'Legal, Social and Cultural Professionals',
            'Research Scientist': 'Science and Engineering Professionals',
            'Middle Manager at Retail Chain': 'Administrative and Commercial Managers',
            'Graphic Design': 'Legal, Social and Cultural Professionals',
            'Office Manager': 'Business and Administration Professionals',
            'Retired postal worker': 'Other Clerical Support Workers',
            'Environment Consultant': 'Science and Engineering Professionals',
            'Marketing Executive': 'Administrative and Commercial Managers',
            'Landscaping': 'Market-oriented Skilled Agricultural Workers',
            'Project Manager': 'Business and Administration Professionals',
            'Part-time shopkeeper': 'Sales Workers',
            'Self-employed baker': 'Food Processing, Woodworking, Garment and Other Craft and Related Trades Workers',
            'Marketing manager': 'Administrative and Commercial Managers',
            'Software Development': 'Information and Communications Technology Professionals',
            'Language tutor': 'Teaching Professionals',
            'Retired teacher': 'Teaching Professionals',
            'Marketing Director': 'Administrative and Commercial Managers',
            'Self-employed contractor': 'Building and Related Trades Workers (excluding Electricians)',
            'Journalist': 'Legal, Social and Cultural Professionals',
            'Part-time Waitress': 'Personal Service Workers',
            'Retail manager': 'Administrative and Commercial Managers',
            'Social Work': 'Legal, Social and Cultural Professionals',
            'Part-time Cashier': 'Customer Services Clerks',
            'Investment advisor': 'Business and Administration Professionals',
            'Small business owner, former retail manager': 'Administrative and Commercial Managers',
            'Mid-level Marketing Executive': 'Administrative and Commercial Managers',
            'Care Worker': 'Personal Care Workers',
            'Junior Engineer': 'Science and Engineering Associate Professionals',
            'Non-profit organization': 'Administrative and Commercial Managers', #Managerial role within the org?
            'Retired Businessman': 'Administrative and Commercial Managers',
            'Sales': 'Sales Workers',
            'Retired Engineer': 'Science and Engineering Professionals',
            'Retired Factory Worker': 'Stationary Plant and Machine Operators',
            'Senior Marketing Manager': 'Administrative and Commercial Managers',
            'Factory supervisor': 'Production and Specialized Services Managers',
            'Office Administrator': 'Business and Administration Professionals',
            'Works as a software engineer': 'Information and Communications Technology Professionals',
            'Retired Restaurant Owner': 'Hospitality, Retail and Other Services Managers',
            'Unemployed': 'Unemployed',
            'Semi-retired Plumber': 'Building and Related Trades Workers (excluding Electricians)',
            'Registered Nurse': 'Health Professionals',
            'Childcare provider': 'Personal Care Workers',
            'Factory Supervisor': 'Production and Specialized Services Managers',
            'Corporate executive': 'Chief Executives, Senior Officials and Legislators',
            'Shopkeeper': 'Sales Workers',
            'Bookkeeping': 'Business and Administration Associate Professionals',
            'Public Relations': 'Business and Administration Professionals',
            'IT Specialist': 'Information and Communications Technology Professionals',
            'Office administrator': 'Business and Administration Professionals',
            'Accountant': 'Business and Administration Professionals',
            'University professor': 'Teaching Professionals',
            'Self-employed plumber': 'Building and Related Trades Workers (excluding Electricians)',
            'Restaurant Manager': 'Hospitality, Retail and Other Services Managers',
            'Elder care worker': 'Personal Care Workers',
            'Hotel Industry': 'Hospitality, Retail and Other Services Managers',
            'Environmental consultant': 'Science and Engineering Professionals',
            'Retired sales manager': 'Administrative and Commercial Managers',
            'Retired Civil Engineer': 'Science and Engineering Professionals',
            'News Editor': 'Legal, Social and Cultural Professionals',
            'Sales Manager': 'Administrative and Commercial Managers',
            'Truck driver': 'Drivers and Mobile Plant Operators',
            'Part-time freelance designer': 'Legal, Social and Cultural Professionals',
            'Engineer': 'Science and Engineering Professionals',
            'Elementary school teacher': 'Teaching Professionals',
            'Corporate Designer': 'Legal, Social and Cultural Professionals',
            'Restaurant Owner': 'Hospitality, Retail and Other Services Managers',
            'Housekeeper': 'Personal Service Workers',
            'Electronics repair technician': 'Electrical and Electronics Trades Workers',
            'Retail sales associate': 'Sales Workers',
            'Retired': 'Unemployed',
            'Freelance Graphic Designer': 'Legal, Social and Cultural Professionals',
            'Real Estate': 'Business and Administration Professionals', #Agent/Sales Role
            'Full-Time Mother': 'Unemployed', #Or Personal Service Workers, but unemployed is more suitable
            'High School Teacher': 'Teaching Professionals',
            'Stay-at-home mom': 'Unemployed',#Or Personal Service Workers, but unemployed is more suitable
            'Construction Worker': 'Building and Related Trades Workers (excluding Electricians)',
            'High School English Teacher': 'Teaching Professionals',
            'Financial Analyst': 'Business and Administration Professionals',
            'Restaurant Worker': 'Personal Service Workers',
            'Bartender': 'Personal Service Workers',
            'Plumber': 'Building and Related Trades Workers (excluding Electricians)',
            'Part-time retail worker': 'Sales Workers',
            'Works as a Mechanic': 'Metal, Machinery and Related Trades Workers',
            'Substitute teacher': 'Teaching Professionals',
            'Engineering Management': 'Science and Engineering Professionals', #Implies they are MANAGING engineering work
            'Service Industry (Waitress)': 'Personal Service Workers',
            'Healthcare aide, small online business owner': 'Personal Care Workers',
            'Part-time': 'Unemployed', #Broad and ambiguous, need more info.  Assuming unemployed or very occasional work
            'Retired Shop Owner': 'Administrative and Commercial Managers',
            'Freelance Artist': 'Legal, Social and Cultural Professionals',
            'Drafting technician': 'Science and Engineering Associate Professionals',
            'Small business owner': 'Administrative and Commercial Managers',
            'Maintenance supervisor': 'Production and Specialized Services Managers',
            'Freelance Copywriter': 'Legal, Social and Cultural Professionals',
            'IT project manager': 'Information and Communications Technology Professionals',
            'Restaurant Server': 'Personal Service Workers',
            'Auto mechanic': 'Metal, Machinery and Related Trades Workers',
            'Homemaker': 'Unemployed', #Or Personal Service Workers, but unemployed is more suitable
            'Banking': 'Business and Administration Professionals', #General role
            'Marketing Manager in multinational corporation': 'Administrative and Commercial Managers',
            'High School History Teacher': 'Teaching Professionals',
            'HR Manager': 'Business and Administration Professionals',
            'Domestic Worker': 'Personal Service Workers',
            'Stay-at-home mother.': 'Unemployed', #Or Personal Service Workers, but unemployed is more suitable
            'Works as a taxi driver.': 'Drivers and Mobile Plant Operators',
            'Digitial Marketing': 'Business and Administration Professionals',
            'Software Developer': 'Information and Communications Technology Professionals',
            'Retired Construction Worker': 'Building and Related Trades Workers (excluding Electricians)',
            'Digital Marketing': 'Business and Administration Professionals',
            'Retired Accountant': 'Business and Administration Professionals',
            'Office Worker': 'General and Keyboard Clerks',
            'Communications Director': 'Administrative and Commercial Managers',
            'Administrative assistant': 'Business and Administration Associate Professionals',
            'Business Owner': 'Administrative and Commercial Managers',
            'Retail': 'Sales Workers', #General retail work
            'Junior Marketer': 'Business and Administration Associate Professionals',
            'Works as a hairdresser': 'Personal Service Workers',
            'IT Support': 'Information and Communications Technicians',
            'Warehouse worker': 'Labourers in Mining, Construction, Manufacturing and Transport',
            'Real estate agent': 'Business and Administration Professionals', #Agent/Sales Role
            'Security Guard': 'Protective Services Workers',
            'Corporate Finance': 'Business and Administration Professionals',
            'Restaurant Cook': 'Food Preparation Assistants',
            'Hotel management, former restaurant owner': 'Hospitality, Retail and Other Services Managers',
            'Home health aide': 'Personal Care Workers',
            'Environmental compliance': 'Science and Engineering Professionals',
            'Primary School Teacher': 'Teaching Professionals',
            'Office manager': 'Business and Administration Professionals',
            'Mechanic': 'Metal, Machinery and Related Trades Workers',
            'Delivery service driver': 'Drivers and Mobile Plant Operators',
            'Financial Analyst at Big 4 Consulting Firm': 'Business and Administration Professionals',
            'Construction site supervisor': 'Building and Related Trades Workers (excluding Electricians)',
            'Community outreach worker': 'Legal, Social and Cultural Professionals',
            'Nurse': 'Health Professionals',
            'Academic (University Tutor)': 'Teaching Professionals',
            'Human Resources Director': 'Administrative and Commercial Managers',
            'Mid-level marketing manager': 'Administrative and Commercial Managers',
            'Retired Teacher': 'Teaching Professionals',
            'Retired administrative assistant': 'Business and Administration Associate Professionals',
            'Marketing Professional': 'Business and Administration Professionals',
            'Laid off / Unemployed': 'Unemployed',
            'Daycare Provider': 'Personal Care Workers',
            'Truck Driver': 'Drivers and Mobile Plant Operators',
            'Retail store supervisor': 'Hospitality, Retail and Other Services Managers',
            'Freelance writer': 'Legal, Social and Cultural Professionals',
            'Retail Management': 'Administrative and Commercial Managers',
            'Delivery Driver': 'Drivers and Mobile Plant Operators',
            'Manufacturing': 'Production and Specialized Services Managers', #Management
            'Entrepreneur': 'Administrative and Commercial Managers', #General
            'Community Health Roles': 'Health Associate Professionals',
            'University Professor': 'Teaching Professionals',
            'Retired Professor': 'Teaching Professionals',
            'Warehouse Supervisor': 'Production and Specialized Services Managers',
            'Factory Technician': 'Science and Engineering Associate Professionals',
            'Retired Farmer': 'Market-oriented Skilled Agricultural Workers',
            'Former Nurse': 'Health Professionals',
            'Retail worker': 'Sales Workers',
            'Restaurant owner': 'Hospitality, Retail and Other Services Managers',
            'Digital Marketing Manager': 'Administrative and Commercial Managers',
            'IT Consultant': 'Information and Communications Technology Professionals',
            'Auto mechanic, shop owner': 'Metal, Machinery and Related Trades Workers',
            'Construction Management': 'Science and Engineering Professionals',
            'Transitioning from Teaching': 'Teaching Professionals', #Current sector.
            'Sustainability Consultant': 'Science and Engineering Professionals',
            'Electrician': 'Electrical and Electronics Trades Workers',
            'Customer Service': 'Customer Services Clerks',
            'Chef': 'Food Preparation Assistants',
            'Part-time Healthcare Administration': 'Business and Administration Professionals',
            'Retail Manager': 'Administrative and Commercial Managers',
            'Freelance Social Media Manager': 'Business and Administration Professionals',
            'Healthcare Administrator': 'Business and Administration Professionals',
            "Nurse's Assistant": 'Health Associate Professionals',
            'Home Health Aide': 'Personal Care Workers',
            'Construction Site Supervisor': 'Building and Related Trades Workers (excluding Electricians)',
            'Real Estate Agent': 'Business and Administration Professionals',
            'Part-time Retail Worker, Caregiver': 'Sales Workers', #Primarily retail
            'Freelance artist': 'Legal, Social and Cultural Professionals',
            'Works in Childcare': 'Personal Care Workers',
            'Police Officer': 'Protective Services Workers',
            'Underemployed': 'Unemployed',
            'Small Business Owner': 'Administrative and Commercial Managers',
            'Restaurant manager': 'Hospitality, Retail and Other Services Managers',
            'Freelancer': 'Unemployed', # Need more info on the industry, could also be Admin and Commerical Managers
            'Retired electrician': 'Electrical and Electronics Trades Workers',
            'Hospitality Worker': 'Personal Service Workers',
            'Housewife': 'Unemployed', #Or Personal Service Workers, but unemployed is more suitable
            'Middle Manager at Banking Sector': 'Administrative and Commercial Managers',
            'Lawyer': 'Legal, Social and Cultural Professionals',
            'Stay-at-home Mom': 'Unemployed',#Or Personal Service Workers, but unemployed is more suitable
            'Stay-at-home mother': 'Unemployed',#Or Personal Service Workers, but unemployed is more suitable
            'Engineering': 'Science and Engineering Professionals',
            'Secondary School Teacher': 'Teaching Professionals',
            'IT consultant': 'Information and Communications Technology Professionals',
            'Software Engineer': 'Information and Communications Technology Professionals',
            'Mid-Level Manager in Manufacturing': 'Production and Specialized Services Managers',
            'IT project management': 'Information and Communications Technology Professionals',
            'Pharmaceutical Research': 'Science and Engineering Professionals',
            'Healthcare assistant': 'Health Associate Professionals',
            'Retail Assistant': 'Sales Workers',
            'Employed': 'Other', #Need more information
            'Retail Sales': 'Sales Workers',
            'Aerospace engineer (retired)': 'Science and Engineering Professionals',
            'Laboratory technician': 'Science and Engineering Associate Professionals',
            'Licensed Practical Nurse': 'Health Professionals',
            'Professor': 'Teaching Professionals',
            'Technician': 'Science and Engineering Associate Professionals',
            'Graphic Designer': 'Legal, Social and Cultural Professionals',
            'Cashier': 'Customer Services Clerks',
            'Works as a cashier.': 'Customer Services Clerks',
            'Electronics Technician': 'Electrical and Electronics Trades Workers',
            'Elementary School Teacher': 'Teaching Professionals',
            'Construction Foreman': 'Building and Related Trades Workers (excluding Electricians)',
            'Tutor': 'Teaching Professionals',
            'Teacher, private tutor': 'Teaching Professionals',
            'Civil engineer': 'Science and Engineering Professionals',
            'Auto repair shop owner': 'Metal, Machinery and Related Trades Workers',
            'Hospitality': 'Hospitality, Retail and Other Services Managers',
            'Investment Banking': 'Business and Administration Professionals',
            'Social Services Worker': 'Legal, Social and Cultural Professionals',
            'University Researcher': 'Science and Engineering Professionals',
            'Musician': 'Legal, Social and Cultural Professionals',
            'Teacher (on leave)': 'Teaching Professionals',
            'Factory Worker': 'Stationary Plant and Machine Operators',
            'Aerospace engineering': 'Science and Engineering Professionals',
            'Social Worker': 'Legal, Social and Cultural Professionals',
            'Teacher': 'Teaching Professionals',
            'Automotive Manufacturing': 'Production and Specialized Services Managers',
            'Retail Supervisor': 'Hospitality, Retail and Other Services Managers',
            'IT Manager': 'Information and Communications Technology Professionals',
            'Auditing': 'Business and Administration Professionals',
            'Management Consultant': 'Business and Administration Professionals',
            'Data analyst': 'Business and Administration Professionals',
            'Hotel Management': 'Hospitality, Retail and Other Services Managers',
            'Healthcare Assistant': 'Health Associate Professionals',
            'Freelance Graphic Designer and Digital Artist': 'Legal, Social and Cultural Professionals',
            'Freelance designer': 'Legal, Social and Cultural Professionals',
            'Lab technician': 'Science and Engineering Associate Professionals',
            'Senior Software Engineer at Financial Services Firm': 'Information and Communications Technology Professionals',
            'Public relations': 'Business and Administration Professionals',
            'Self-Employed Electrician': 'Electrical and Electronics Trades Workers',
            'Advertising': 'Business and Administration Professionals',
            'Housekeeping': 'Personal Service Workers',
            'Home-based daycare provider': 'Personal Care Workers',
            'Construction supervisor': 'Building and Related Trades Workers (excluding Electricians)',
            'Translator': 'Legal, Social and Cultural Professionals',
            'Works as a construction worker.': 'Building and Related Trades Workers (excluding Electricians)',
            'Research Scientist in Pharmaceutical Company': 'Science and Engineering Professionals',
            'Retired mechanic': 'Metal, Machinery and Related Trades Workers',
            'Stay-at-home Mother': 'Unemployed',#Or Personal Service Workers, but unemployed is more suitable
            'Restaurant server, former small business owner in Mexico': 'Personal Service Workers',
            'Cleaner': 'Cleaners and Helpers',
            'IT Technician': 'Information and Communications Technicians',
            'Retired (Seamstress)': 'Food Processing, Woodworking, Garment and Other Craft and Related Trades Workers',
            'Research': 'Science and Engineering Professionals',
            'Preschool Teacher': 'Teaching Professionals',
            'Junior engineer': 'Science and Engineering Associate Professionals',
            'Project engineer': 'Science and Engineering Professionals'
        }

        self.certifications = [
            "Associate Degree","Technical Education",
            "Bachelor's Degree","Master's Degree",
            "Ph.D","Diploma","Non-tertiary Education"
        ]
        
        self.sectors = list(set(self._job_title_to_sector.values()))

    def employment2sector(self,job_title:str):
        if job_title in self._job_title_to_sector:
            return self._job_title_to_sector[job_title]
        else:
            return 'Other'
    
    def education2certification(self, education:str):
        education = education.lower()
        
        if "associate degree" in education:
            return "Associate Degree"
        
        if any(term in education for term in ["vocational", "technical", "trade"]):
            return "Technical Education"
        
        if any(term in education for term in ["bachelor","college degree", "university degree"]) or \
           "college" in education and "diploma" not in education: #We consider cases like "Some College" as meaning a bachelors degree. 
            return "Bachelor's Degree"
        
        if any(term in education for term in ["master's","MBA"]):
            return "Master's Degree"
        
        if any(term in education for term in ["phd","ph.d"]):
            return "Ph.D"
        
        if "diploma" in education and "high school" not in education:
            return "Diploma"
        
        return "Non-tertiary Education"