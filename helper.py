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

# https://unstats.un.org/unsd/methodology/m49/  + with the inclusion of Kosovo, Taiwan
class CountryHelper:
    def __init__(self):
        
        hispanic = ['Argentina','Bolivia','Bouvet Island','Brazil','Chile','Colombia','Ecuador','Falkland Islands','French Guiana','Guyana','Paraguay','Peru','South Georgia and the South Sandwich Islands','Suriname','Uruguay','Venezuela','Belize','Costa Rica','El Salvador','Guatemala','Honduras','Mexico','Nicaragua','Panama']
        
        middle_east = ['Saudi Arabia','Iran','Iraq','Syria','Jordan','Lebanon','Israel','Palestine','Kuwait','Oman','Yemen','United Arab Emirates','Qatar','Bahrain']
        west_africa = ['Benin', 'Burkina Faso', 'Cabo Verde', "Côte d'Ivoire", 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Liberia', 'Mali', 'Mauritania', 'Niger', 'Nigeria', 'Saint Helena', 'Senegal', 'Sierra Leone', 'Togo']
        north_africa =['Algeria','Egypt','Libya','Morocco','Sudan','Tunisia','W. Sahara']
        east_africa = ['Burundi','Comoros','Djibouti','Eritrea','Ethiopia','Kenya','Madagascar','Malawi','Mauritius','Mayotte','Mozambique','Réunion','Rwanda','Seychelles','Somalia','S. Sudan','Uganda','Tanzania','Zambia','Zimbabwe']
        africa = west_africa + north_africa + east_africa + ['British Indian Ocean Territory','Burundi','Comoros','Djibouti','Eritrea','Ethiopia','French Southern Territories','Kenya','Madagascar','Malawi','Mauritius','Mayotte','Mozambique','Réunion','Rwanda','Seychelles','Somalia','S. Sudan','Uganda','Tanzania','Zambia','Zimbabwe','Angola','Cameroon','Central African Rep.','Chad','Congo','Dem. Rep. Congo','Eq. Guinea','Gabon','Sao Tome and Principe','Botswana','Eswatini','Lesotho','Namibia','South Africa']
        africa = list(set(africa))
        south_asian = ['Afghanistan','Bangladesh','Bhutan','India','Iran','Maldives','Nepal','Pakistan','Sri Lanka']
        east_asian = ['China','Japan','Mongolia','North Korea','South Korea','Taiwan']
        asia = ['Turkey','Kazakhstan','Kyrgyzstan','Tajikistan','Turkmenistan','Uzbekistan','China','North Korea','Japan','Mongolia','South Korea','Brunei','Cambodia','Indonesia','Laos','Malaysia','Myanmar','Philippines','Singapore','Thailand','Timor-Leste','Vietnam']
        asia += ['Armenia','Azerbaijan','Georgia']
        east_europe = ['Kosovo','Poland','Belarus','Czechia','Slovakia','Hungary','Romania','Bulgaria','Moldova','Ukraine','Russia']
        balkan = ['Greece','Serbia','Croatia','Bosnia and Herz.','Albania','North Macedonia','Kosovo','Montenegro','Bulgaria','Romania','Slovenia','Moldova']
        europe = east_europe + ['Denmark','Estonia','Finland','Iceland','Ireland','Latvia','Lithuania','Norway','Sweden','United Kingdom','Albania','Andorra','Bosnia and Herz.','Croatia','Greece','Italy','Malta','Montenegro','North Macedonia','Portugal','San Marino','Serbia','Slovenia','Spain','Austria','Belgium','France','Germany','Liechtenstein','Luxembourg','Monaco','Netherlands','Switzerland']
        
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

        self. _country2region = {
            # Africa - Northern Africa
            "Algeria": {"region": "Africa", "subregion": "Northern Africa"},
            "Egypt": {"region": "Africa", "subregion": "Northern Africa"},
            "Libya": {"region": "Africa", "subregion": "Northern Africa"},
            "Morocco": {"region": "Africa", "subregion": "Northern Africa"},
            "Sudan": {"region": "Africa", "subregion": "Northern Africa"},
            "Tunisia": {"region": "Africa", "subregion": "Northern Africa"},
            "W. Sahara": {"region": "Africa", "subregion": "Northern Africa"},

            # Africa - Eastern Africa
            "British Indian Ocean Territory": {"region": "Africa", "subregion": "Eastern Africa"},
            "Burundi": {"region": "Africa", "subregion": "Eastern Africa"},
            "Comoros": {"region": "Africa", "subregion": "Eastern Africa"},
            "Djibouti": {"region": "Africa", "subregion": "Eastern Africa"},
            "Eritrea": {"region": "Africa", "subregion": "Eastern Africa"},
            "Ethiopia": {"region": "Africa", "subregion": "Eastern Africa"},
            "French Southern Territories": {"region": "Africa", "subregion": "Eastern Africa"},
            "Kenya": {"region": "Africa", "subregion": "Eastern Africa"},
            "Madagascar": {"region": "Africa", "subregion": "Eastern Africa"},
            "Malawi": {"region": "Africa", "subregion": "Eastern Africa"},
            "Mauritius": {"region": "Africa", "subregion": "Eastern Africa"},
            "Mayotte": {"region": "Africa", "subregion": "Eastern Africa"},
            "Mozambique": {"region": "Africa", "subregion": "Eastern Africa"},
            "Réunion": {"region": "Africa", "subregion": "Eastern Africa"},
            "Rwanda": {"region": "Africa", "subregion": "Eastern Africa"},
            "Seychelles": {"region": "Africa", "subregion": "Eastern Africa"},
            "Somalia": {"region": "Africa", "subregion": "Eastern Africa"},
            "S. Sudan": {"region": "Africa", "subregion": "Eastern Africa"},
            "Uganda": {"region": "Africa", "subregion": "Eastern Africa"},
            "Tanzania": {"region": "Africa", "subregion": "Eastern Africa"},
            "Zambia": {"region": "Africa", "subregion": "Eastern Africa"},
            "Zimbabwe": {"region": "Africa", "subregion": "Eastern Africa"},

            # Africa - Middle Africa
            "Angola": {"region": "Africa", "subregion": "Middle Africa"},
            "Cameroon": {"region": "Africa", "subregion": "Middle Africa"},
            "Central African Rep.": {"region": "Africa", "subregion": "Middle Africa"},
            "Chad": {"region": "Africa", "subregion": "Middle Africa"},
            "Congo": {"region": "Africa", "subregion": "Middle Africa"},
            "Dem. Rep. Congo": {"region": "Africa", "subregion": "Middle Africa"},
            "Eq. Guinea": {"region": "Africa", "subregion": "Middle Africa"},
            "Gabon": {"region": "Africa", "subregion": "Middle Africa"},
            "Sao Tome and Principe": {"region": "Africa", "subregion": "Middle Africa"},
            
            # Africa - Southern Africa
            "Botswana": {"region": "Africa", "subregion": "Southern Africa"},
            "Eswatini": {"region": "Africa", "subregion": "Southern Africa"},
            "Lesotho": {"region": "Africa", "subregion": "Southern Africa"},
            "Namibia": {"region": "Africa", "subregion": "Southern Africa"},
            "South Africa": {"region": "Africa", "subregion": "Southern Africa"},
            
            # Africa - Western Africa
            "Benin": {"region": "Africa", "subregion": "Western Africa"},
            "Burkina Faso": {"region": "Africa", "subregion": "Western Africa"},
            "Cabo Verde": {"region": "Africa", "subregion": "Western Africa"},
            "Côte d'Ivoire": {"region": "Africa", "subregion": "Western Africa"},
            "Gambia": {"region": "Africa", "subregion": "Western Africa"},
            "Ghana": {"region": "Africa", "subregion": "Western Africa"},
            "Guinea": {"region": "Africa", "subregion": "Western Africa"},
            "Guinea-Bissau": {"region": "Africa", "subregion": "Western Africa"},
            "Liberia": {"region": "Africa", "subregion": "Western Africa"},
            "Mali": {"region": "Africa", "subregion": "Western Africa"},
            "Mauritania": {"region": "Africa", "subregion": "Western Africa"},
            "Niger": {"region": "Africa", "subregion": "Western Africa"},
            "Nigeria": {"region": "Africa", "subregion": "Western Africa"},
            "Saint Helena": {"region": "Africa", "subregion": "Western Africa"},
            "Senegal": {"region": "Africa", "subregion": "Western Africa"},
            "Sierra Leone": {"region": "Africa", "subregion": "Western Africa"},
            "Togo": {"region": "Africa", "subregion": "Western Africa"},
            
             # Americas - Caribbean
            "Anguilla": {"region": "Americas", "subregion": "Caribbean"},
            "Antigua and Barbuda": {"region": "Americas", "subregion": "Caribbean"},
            "Aruba": {"region": "Americas", "subregion": "Caribbean"},
            "Bahamas": {"region": "Americas", "subregion": "Caribbean"},
            "Barbados": {"region": "Americas", "subregion": "Caribbean"},
            "Cayman Islands": {"region": "Americas", "subregion": "Caribbean"},
            "Cuba": {"region": "Americas", "subregion": "Caribbean"},
            "Curaçao": {"region": "Americas", "subregion": "Caribbean"},
            "Dominican Rep.": {"region": "Americas", "subregion": "Caribbean"},
            "Grenada": {"region": "Americas", "subregion": "Caribbean"},
            "Haiti": {"region": "Americas", "subregion": "Caribbean"},
            "Jamaica": {"region": "Americas", "subregion": "Caribbean"},
            "Puerto Rico": {"region": "Americas", "subregion": "Caribbean"},
            "Saint Kitts and Nevis": {"region": "Americas", "subregion": "Caribbean"},
            "Saint Lucia": {"region": "Americas", "subregion": "Caribbean"},
            "Trinidad and Tobago": {"region": "Americas", "subregion": "Caribbean"},

            # Americas - Central America
            "Belize": {"region": "Americas", "subregion": "Central America"},
            "Costa Rica": {"region": "Americas", "subregion": "Central America"},
            "El Salvador": {"region": "Americas", "subregion": "Central America"},
            "Guatemala": {"region": "Americas", "subregion": "Central America"},
            "Honduras": {"region": "Americas", "subregion": "Central America"},
            "Mexico": {"region": "Americas", "subregion": "Central America"},
            "Nicaragua": {"region": "Americas", "subregion": "Central America"},
            "Panama": {"region": "Americas", "subregion": "Central America"},

            # Americas - South America
            "Argentina": {"region": "Americas", "subregion": "South America"},
            "Bolivia": {"region": "Americas", "subregion": "South America"},
            "Bouvet Island": {"region": "Americas", "subregion": "South America"},
            "Brazil": {"region": "Americas", "subregion": "South America"},
            "Chile": {"region": "Americas", "subregion": "South America"},
            "Colombia": {"region": "Americas", "subregion": "South America"},
            "Ecuador": {"region": "Americas", "subregion": "South America"},
            "Falkland Islands": {"region": "Americas", "subregion": "South America"},
            "French Guiana": {"region": "Americas", "subregion": "South America"},
            "Guyana": {"region": "Americas", "subregion": "South America"},
            "Paraguay": {"region": "Americas", "subregion": "South America"},
            "Peru": {"region": "Americas", "subregion": "South America"},
            "South Georgia and the South Sandwich Islands": {"region": "Americas", "subregion": "South America"},
            "Suriname": {"region": "Americas", "subregion": "South America"},
            "Uruguay": {"region": "Americas", "subregion": "South America"},
            "Venezuela": {"region": "Americas", "subregion": "South America"},

            # Americas - Northern America
            "Bermuda": {"region": "Americas", "subregion": "Northern America"},
            "Canada": {"region": "Americas", "subregion": "Northern America"},
            "Greenland": {"region": "Americas", "subregion": "Northern America"},

            "United States": {"region": "Americas", "subregion": "Northern America"},
            "United States of America": {"region": "Americas", "subregion": "Northern America"},
            "US": {"region": "Americas", "subregion": "Northern America"},
            "USA": {"region": "Americas", "subregion": "Northern America"},
            
            # Asia - Central Asia
            "Kazakhstan": {"region": "Asia", "subregion": "Central Asia"},
            "Kyrgyzstan": {"region": "Asia", "subregion": "Central Asia"},
            "Tajikistan": {"region": "Asia", "subregion": "Central Asia"},
            "Turkmenistan": {"region": "Asia", "subregion": "Central Asia"},
            "Uzbekistan": {"region": "Asia", "subregion": "Central Asia"},
            
            # Asia - Eastern Asia
            "China": {"region": "Asia", "subregion": "Eastern Asia"},
            "Taiwan": {"region": "Asia", "subregion": "Eastern Asia"},
            "North Korea": {"region": "Asia", "subregion": "Eastern Asia"},
            "Japan": {"region": "Asia", "subregion": "Eastern Asia"},
            "Mongolia": {"region": "Asia", "subregion": "Eastern Asia"},
            "South Korea": {"region": "Asia", "subregion": "Eastern Asia"},
            
            # Asia - South-eastern Asia
            "Brunei": {"region": "Asia", "subregion": "South-eastern Asia"},
            "Cambodia": {"region": "Asia", "subregion": "South-eastern Asia"},
            "Indonesia": {"region": "Asia", "subregion": "South-eastern Asia"},
            "Laos": {"region": "Asia", "subregion": "South-eastern Asia"},
            "Malaysia": {"region": "Asia", "subregion": "South-eastern Asia"},
            "Myanmar": {"region": "Asia", "subregion": "South-eastern Asia"},
            "Philippines": {"region": "Asia", "subregion": "South-eastern Asia"},
            "Singapore": {"region": "Asia", "subregion": "South-eastern Asia"},
            "Thailand": {"region": "Asia", "subregion": "South-eastern Asia"},
            "Timor-Leste": {"region": "Asia", "subregion": "South-eastern Asia"},
            "Vietnam": {"region": "Asia", "subregion": "South-eastern Asia"},
            
            # Asia - Southern Asia
            "Afghanistan": {"region": "Asia", "subregion": "Southern Asia"},
            "Bangladesh": {"region": "Asia", "subregion": "Southern Asia"},
            "Bhutan": {"region": "Asia", "subregion": "Southern Asia"},
            "India": {"region": "Asia", "subregion": "Southern Asia"},
            "Iran": {"region": "Asia", "subregion": "Southern Asia"},
            "Maldives": {"region": "Asia", "subregion": "Southern Asia"},
            "Nepal": {"region": "Asia", "subregion": "Southern Asia"},
            "Pakistan": {"region": "Asia", "subregion": "Southern Asia"},
            "Sri Lanka": {"region": "Asia", "subregion": "Southern Asia"},
            
            # Asia - Western Asia
            "Armenia": {"region": "Asia", "subregion": "Western Asia"},
            "Azerbaijan": {"region": "Asia", "subregion": "Western Asia"},
            "Bahrain": {"region": "Asia", "subregion": "Western Asia"},
            "Cyprus": {"region": "Asia", "subregion": "Western Asia"},
            "Georgia": {"region": "Asia", "subregion": "Western Asia"},
            "Iraq": {"region": "Asia", "subregion": "Western Asia"},
            "Israel": {"region": "Asia", "subregion": "Western Asia"},
            "Jordan": {"region": "Asia", "subregion": "Western Asia"},
            "Kuwait": {"region": "Asia", "subregion": "Western Asia"},
            "Lebanon": {"region": "Asia", "subregion": "Western Asia"},
            "Oman": {"region": "Asia", "subregion": "Western Asia"},
            "Qatar": {"region": "Asia", "subregion": "Western Asia"},
            "Saudi Arabia": {"region": "Asia", "subregion": "Western Asia"},
            "Palestine": {"region": "Asia", "subregion": "Western Asia"},
            "Syria": {"region": "Asia", "subregion": "Western Asia"},
            "Türkiye": {"region": "Asia", "subregion": "Western Asia"},
            "Turkey": {"region": "Asia", "subregion": "Western Asia"},
            "UAE": {"region": "Asia", "subregion": "Western Asia"},
            "United Arab Emirates": {"region": "Asia", "subregion": "Western Asia"},
            "Yemen": {"region": "Asia", "subregion": "Western Asia"},
            
            # Europe - Eastern Europe
            "Belarus": {"region": "Europe", "subregion": "Eastern Europe"},
            "Bulgaria": {"region": "Europe", "subregion": "Eastern Europe"},
            "Czechia": {"region": "Europe", "subregion": "Eastern Europe"},
            "Hungary": {"region": "Europe", "subregion": "Eastern Europe"},
            "Poland": {"region": "Europe", "subregion": "Eastern Europe"},
            "Moldova": {"region": "Europe", "subregion": "Eastern Europe"},
            "Romania": {"region": "Europe", "subregion": "Eastern Europe"},
            "Russia": {"region": "Europe", "subregion": "Eastern Europe"},
            "Slovakia": {"region": "Europe", "subregion": "Eastern Europe"},
            "Ukraine": {"region": "Europe", "subregion": "Eastern Europe"},
            
            # Europe - Northern Europe
            "Denmark": {"region": "Europe", "subregion": "Northern Europe"},
            "Estonia": {"region": "Europe", "subregion": "Northern Europe"},
            "Finland": {"region": "Europe", "subregion": "Northern Europe"},
            "Iceland": {"region": "Europe", "subregion": "Northern Europe"},
            "Ireland": {"region": "Europe", "subregion": "Northern Europe"},
            "Latvia": {"region": "Europe", "subregion": "Northern Europe"},
            "Lithuania": {"region": "Europe", "subregion": "Northern Europe"},
            "Norway": {"region": "Europe", "subregion": "Northern Europe"},
            "Sweden": {"region": "Europe", "subregion": "Northern Europe"},
            "United Kingdom": {"region": "Europe", "subregion": "Northern Europe"},
            
            # Europe - Southern Europe
            "Albania": {"region": "Europe", "subregion": "Southern Europe"},
            "Andorra": {"region": "Europe", "subregion": "Southern Europe"},
            "Bosnia and Herz.": {"region": "Europe", "subregion": "Southern Europe"},
            "Croatia": {"region": "Europe", "subregion": "Southern Europe"},
            "Gibraltar": {"region": "Europe", "subregion": "Southern Europe"},
            "Greece": {"region": "Europe", "subregion": "Southern Europe"},
            "Italy": {"region": "Europe", "subregion": "Southern Europe"},
            "Malta": {"region": "Europe", "subregion": "Southern Europe"},
            "Montenegro": {"region": "Europe", "subregion": "Southern Europe"},
            "North Macedonia": {"region": "Europe", "subregion": "Southern Europe"},
            "Portugal": {"region": "Europe", "subregion": "Southern Europe"},
            "San Marino": {"region": "Europe", "subregion": "Southern Europe"},
            "Serbia": {"region": "Europe", "subregion": "Southern Europe"},
            "Kosovo": {"region": "Europe", "subregion": "Southern Europe"},
            "Slovenia": {"region": "Europe", "subregion": "Southern Europe"},
            "Spain": {"region": "Europe", "subregion": "Southern Europe"},
            
            # Europe - Western Europe
            "Austria": {"region": "Europe", "subregion": "Western Europe"},
            "Belgium": {"region": "Europe", "subregion": "Western Europe"},
            "France": {"region": "Europe", "subregion": "Western Europe"},
            "Germany": {"region": "Europe", "subregion": "Western Europe"},
            "Liechtenstein": {"region": "Europe", "subregion": "Western Europe"},
            "Luxembourg": {"region": "Europe", "subregion": "Western Europe"},
            "Monaco": {"region": "Europe", "subregion": "Western Europe"},
            "Netherlands": {"region": "Europe", "subregion": "Western Europe"},
            "Switzerland": {"region": "Europe", "subregion": "Western Europe"},
            
            # Oceania - Australia and New Zealand
            "Australia": {"region": "Oceania", "subregion": "Australia and New Zealand"},
            "New Zealand": {"region": "Oceania", "subregion": "Australia and New Zealand"},
            
            # Oceania - Melanesia
            "Fiji": {"region": "Oceania", "subregion": "Melanesia"},
            "New Caledonia": {"region": "Oceania", "subregion": "Melanesia"},
            "Papua New Guinea": {"region": "Oceania", "subregion": "Melanesia"},
            "Solomon Islands": {"region": "Oceania", "subregion": "Melanesia"},
            "Vanuatu": {"region": "Oceania", "subregion": "Melanesia"},
            
            # Oceania - Micronesia
            "Guam": {"region": "Oceania", "subregion": "Micronesia"},
            "Kiribati": {"region": "Oceania", "subregion": "Micronesia"},
            "Marshall Islands": {"region": "Oceania", "subregion": "Micronesia"},
            "Micronesia": {"region": "Oceania", "subregion": "Micronesia"},
            "Nauru": {"region": "Oceania", "subregion": "Micronesia"},
            "Palau": {"region": "Oceania", "subregion": "Micronesia"},
            
            # Oceania - Polynesia
            "Cook Islands": {"region": "Oceania", "subregion": "Polynesia"},
            "Niue": {"region": "Oceania", "subregion": "Polynesia"},
            "Samoa": {"region": "Oceania", "subregion": "Polynesia"},
            "Tonga": {"region": "Oceania", "subregion": "Polynesia"},
            "Tuvalu": {"region": "Oceania", "subregion": "Polynesia"},
        }
       
        self.countries = list(set([
            country for sublist in self._race2country.values()
                    for country in (sublist if isinstance(sublist, list) else [sublist])
        ]))

        self._country2short = {
            'United States of America':'USA',
            'United Kingdom':'UK',
            'United Arab Emirates':'UAE',
            'Czech Republic':'Czechia',
        }

    def country2region(self,country_name):
        try:
            return self._country2region[country_name]
        except KeyError:
            raise KeyError(f"Country '{country_name}' not found in the UNSD taxonomy")

    def region2continent(self, region):
        pass


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
    
    def country2short(self,country_name:str) -> str:
        return self._country2short[country_name] if country_name in self._country2short else country_name
        
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

class ColorHelper:
    def __init__(self):
        jobH = JobHelper()
        countryH = CountryHelper()
        labels = jobH.sectors + jobH.subsectors + jobH.certifications + \
                 countryH.countries + list(countryH._country2short.values())
        self._label2color = dict(zip(labels,sns.color_palette("tab20", len(labels))))

        continents = list(set([
            continent['region'] for continent in countryH._country2region.values()
        ]))
        self._continent2color = dict(zip(continents, sns.color_palette("pastel", len(continents))))
    
    def label2color(self, label: str) -> str:
        return self._label2color[label.replace('\n',' ')]
    
    def continent2color(self, region: str) -> str:
        return self._continent2color[region]
        
  
class JobHelper:
    def __init__(self):

        #Keep collapsed  
        # https://unstats.un.org/unsd/classifications/Family/Detail/1067 ISCO-08 classification is used
        self._job_title_to_sector = {'Restaurant kitchen supervisor': {'sector': 'Managers', 'subsector': 'Hospitality, Retail and Other Services Managers'}, 'Research scientist': {'sector': 'Professionals', 'subsector': 'Science and Engineering Professionals'}, 'Administrative Assistant': {'sector': 'Technicians and Associate Professionals', 'subsector': 'Business and Administration Associate Professionals'}, 'Retial Management': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'Middle Manager in Retail': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'Retail Worker': {'sector': 'Service and Sales Workers', 'subsector': 'Sales Workers'}, 'Marketing Manager': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'Taxi Driver': {'sector': 'Plant and Machine Operators, and Assemblers', 'subsector': 'Drivers and Mobile Plant Operators'}, 'Construction worker': {'sector': 'Craft and Related Trades Workers', 'subsector': 'Building and Related Trades Workers (excluding Electricians)'}, 'Retired Nurse': {'sector': 'Professionals', 'subsector': 'Health Professionals'}, 'Environmental Scientist': {'sector': 'Professionals', 'subsector': 'Science and Engineering Professionals'}, 'Sales manager': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'Manufacturing supervisor': {'sector': 'Managers', 'subsector': 'Production and Specialized Services Managers'}, 'Senior developer': {'sector': 'Professionals', 'subsector': 'Information and Communications Technology Professionals'}, 'Mental health and stress management': {'sector': 'Professionals', 'subsector': 'Health Professionals'}, 'Freelance translator': {'sector': 'Professionals', 'subsector': 'Legal, Social and Cultural Professionals'}, 'Taxi driver': {'sector': 'Plant and Machine Operators, and Assemblers', 'subsector': 'Drivers and Mobile Plant Operators'}, 'Retired Office Worker': {'sector': 'Clerical Support Workers', 'subsector': 'General and Keyboard Clerks'}, 'Shop Owner': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'Teacher (unemployed)': {'sector': 'Professionals', 'subsector': 'Teaching Professionals'}, 'Farmer': {'sector': 'Skilled Agricultural, Forestry and Fishery Workers', 'subsector': 'Market-oriented Skilled Agricultural Workers'}, 'Construction foreman': {'sector': 'Craft and Related Trades Workers', 'subsector': 'Building and Related Trades Workers (excluding Electricians)'}, 'Retired factory worker': {'sector': 'Plant and Machine Operators, and Assemblers', 'subsector': 'Stationary Plant and Machine Operators'}, 'Daycare center owner': {'sector': 'Managers', 'subsector': 'Hospitality, Retail and Other Services Managers'}, 'Bank Manager': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'Factory worker': {'sector': 'Plant and Machine Operators, and Assemblers', 'subsector': 'Stationary Plant and Machine Operators'}, 'Factory Shift Supervisor': {'sector': 'Managers', 'subsector': 'Production and Specialized Services Managers'}, 'IT': {'sector': 'Professionals', 'subsector': 'Information and Communications Technology Professionals'}, 'Banker': {'sector': 'Professionals', 'subsector': 'Business and Administration Professionals'}, 'Freelance Translator': {'sector': 'Professionals', 'subsector': 'Legal, Social and Cultural Professionals'}, 'Housekeeping supervisor': {'sector': 'Managers', 'subsector': 'Hospitality, Retail and Other Services Managers'}, 'Retail Sales Associate': {'sector': 'Service and Sales Workers', 'subsector': 'Sales Workers'}, 'Help desk technician': {'sector': 'Technicians and Associate Professionals', 'subsector': 'Information and Communications Technicians'}, 'Stay-at-Home Mother': {'sector': 'Unemployed', 'subsector': 'Unemployed'}, 'Auto Mechanic': {'sector': 'Craft and Related Trades Workers', 'subsector': 'Metal, Machinery and Related Trades Workers'}, 'Works in hospitality.': {'sector': 'Service and Sales Workers', 'subsector': 'Personal Service Workers'}, 'Civil Engineering': {'sector': 'Professionals', 'subsector': 'Science and Engineering Professionals'}, 'Retired Gardener': {'sector': 'Skilled Agricultural, Forestry and Fishery Workers', 'subsector': 'Market-oriented Skilled Agricultural Workers'}, 'Construction': {'sector': 'Craft and Related Trades Workers', 'subsector': 'Building and Related Trades Workers (excluding Electricians)'}, 'Retail management': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'Self-employed seamstress': {'sector': 'Craft and Related Trades Workers', 'subsector': 'Food Processing, Woodworking, Garment and Other Craft and Related Trades Workers'}, 'IT Professional': {'sector': 'Professionals', 'subsector': 'Information and Communications Technology Professionals'}, 'Accounting clerk, former bank employee in China': {'sector': 'Clerical Support Workers', 'subsector': 'Numerical and Material Recording Clerks'}, 'IT technician': {'sector': 'Technicians and Associate Professionals', 'subsector': 'Information and Communications Technicians'}, 'Food truck owner': {'sector': 'Managers', 'subsector': 'Hospitality, Retail and Other Services Managers'}, 'IT Project Manager': {'sector': 'Professionals', 'subsector': 'Information and Communications Technology Professionals'}, 'Corporate Marketing': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'Caregiver': {'sector': 'Service and Sales Workers', 'subsector': 'Personal Care Workers'}, 'Civil engineer at a construction firm': {'sector': 'Professionals', 'subsector': 'Science and Engineering Professionals'}, 'Factory worker, former civil engineer': {'sector': 'Plant and Machine Operators, and Assemblers', 'subsector': 'Stationary Plant and Machine Operators'}, 'Blue-Collar Worker': {'sector': 'Elementary Occupations', 'subsector': 'Labourers in Mining, Construction, Manufacturing and Transport'}, 'Farmworker': {'sector': 'Elementary Occupations', 'subsector': 'Agricultural, Forestry and Fishery Labourers'}, 'Warehouse Worker': {'sector': 'Elementary Occupations', 'subsector': 'Labourers in Mining, Construction, Manufacturing and Transport'}, 'Part-time bookkeeper': {'sector': 'Technicians and Associate Professionals', 'subsector': 'Business and Administration Associate Professionals'}, 'Senior Software Engineer': {'sector': 'Professionals', 'subsector': 'Information and Communications Technology Professionals'}, 'Resturant Manager': {'sector': 'Managers', 'subsector': 'Hospitality, Retail and Other Services Managers'}, 'Marketing Director at FMCG company': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'Software developer': {'sector': 'Professionals', 'subsector': 'Information and Communications Technology Professionals'}, 'Freelance graphic designer': {'sector': 'Professionals', 'subsector': 'Legal, Social and Cultural Professionals'}, 'Restaurant worker': {'sector': 'Service and Sales Workers', 'subsector': 'Personal Service Workers'}, 'Part-time accountant': {'sector': 'Technicians and Associate Professionals', 'subsector': 'Business and Administration Associate Professionals'}, 'Self-Employed': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'Researcher': {'sector': 'Professionals', 'subsector': 'Science and Engineering Professionals'}, 'Works as a Cashier': {'sector': 'Clerical Support Workers', 'subsector': 'Customer Services Clerks'}, 'Former retail manager, transitioning': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'Construction project manager': {'sector': 'Professionals', 'subsector': 'Science and Engineering Professionals'}, 'Finance': {'sector': 'Professionals', 'subsector': 'Business and Administration Professionals'}, 'Marketing Assistant': {'sector': 'Technicians and Associate Professionals', 'subsector': 'Business and Administration Associate Professionals'}, 'Small import business owner': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'Tech Support': {'sector': 'Technicians and Associate Professionals', 'subsector': 'Information and Communications Technicians'}, 'Social Media Manager': {'sector': 'Professionals', 'subsector': 'Business and Administration Professionals'}, 'Works part-time as a care assistant': {'sector': 'Service and Sales Workers', 'subsector': 'Personal Care Workers'}, 'Freelance Writer': {'sector': 'Professionals', 'subsector': 'Legal, Social and Cultural Professionals'}, 'Social media manager': {'sector': 'Professionals', 'subsector': 'Business and Administration Professionals'}, 'Librarian': {'sector': 'Professionals', 'subsector': 'Legal, Social and Cultural Professionals'}, 'Research Scientist': {'sector': 'Professionals', 'subsector': 'Science and Engineering Professionals'}, 'Middle Manager at Retail Chain': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'Graphic Design': {'sector': 'Professionals', 'subsector': 'Legal, Social and Cultural Professionals'}, 'Office Manager': {'sector': 'Professionals', 'subsector': 'Business and Administration Professionals'}, 'Retired postal worker': {'sector': 'Clerical Support Workers', 'subsector': 'Other Clerical Support Workers'}, 'Environment Consultant': {'sector': 'Professionals', 'subsector': 'Science and Engineering Professionals'}, 'Marketing Executive': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'Landscaping': {'sector': 'Skilled Agricultural, Forestry and Fishery Workers', 'subsector': 'Market-oriented Skilled Agricultural Workers'}, 'Project Manager': {'sector': 'Professionals', 'subsector': 'Business and Administration Professionals'}, 'Part-time shopkeeper': {'sector': 'Service and Sales Workers', 'subsector': 'Sales Workers'}, 'Self-employed baker': {'sector': 'Craft and Related Trades Workers', 'subsector': 'Food Processing, Woodworking, Garment and Other Craft and Related Trades Workers'}, 'Marketing manager': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'Software Development': {'sector': 'Professionals', 'subsector': 'Information and Communications Technology Professionals'}, 'Language tutor': {'sector': 'Professionals', 'subsector': 'Teaching Professionals'}, 'Retired teacher': {'sector': 'Professionals', 'subsector': 'Teaching Professionals'}, 'Marketing Director': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'Self-employed contractor': {'sector': 'Craft and Related Trades Workers', 'subsector': 'Building and Related Trades Workers (excluding Electricians)'}, 'Journalist': {'sector': 'Professionals', 'subsector': 'Legal, Social and Cultural Professionals'}, 'Part-time Waitress': {'sector': 'Service and Sales Workers', 'subsector': 'Personal Service Workers'}, 'Retail manager': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'Social Work': {'sector': 'Professionals', 'subsector': 'Legal, Social and Cultural Professionals'}, 'Part-time Cashier': {'sector': 'Clerical Support Workers', 'subsector': 'Customer Services Clerks'}, 'Investment advisor': {'sector': 'Professionals', 'subsector': 'Business and Administration Professionals'}, 'Small business owner, former retail manager': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'Mid-level Marketing Executive': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'Care Worker': {'sector': 'Service and Sales Workers', 'subsector': 'Personal Care Workers'}, 'Junior Engineer': {'sector': 'Technicians and Associate Professionals', 'subsector': 'Science and Engineering Associate Professionals'}, 'Non-profit organization': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'Retired Businessman': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'Sales': {'sector': 'Service and Sales Workers', 'subsector': 'Sales Workers'}, 'Retired Engineer': {'sector': 'Professionals', 'subsector': 'Science and Engineering Professionals'}, 'Retired Factory Worker': {'sector': 'Plant and Machine Operators, and Assemblers', 'subsector': 'Stationary Plant and Machine Operators'}, 'Senior Marketing Manager': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'Factory supervisor': {'sector': 'Managers', 'subsector': 'Production and Specialized Services Managers'}, 'Office Administrator': {'sector': 'Professionals', 'subsector': 'Business and Administration Professionals'}, 'Works as a software engineer': {'sector': 'Professionals', 'subsector': 'Information and Communications Technology Professionals'}, 'Retired Restaurant Owner': {'sector': 'Managers', 'subsector': 'Hospitality, Retail and Other Services Managers'}, 'Unemployed': {'sector': 'Unemployed', 'subsector': 'Unemployed'}, 'Semi-retired Plumber': {'sector': 'Craft and Related Trades Workers', 'subsector': 'Building and Related Trades Workers (excluding Electricians)'}, 'Registered Nurse': {'sector': 'Professionals', 'subsector': 'Health Professionals'}, 'Childcare provider': {'sector': 'Service and Sales Workers', 'subsector': 'Personal Care Workers'}, 'Factory Supervisor': {'sector': 'Managers', 'subsector': 'Production and Specialized Services Managers'}, 'Corporate executive': {'sector': 'Managers', 'subsector': 'Chief Executives, Senior Officials and Legislators'}, 'Shopkeeper': {'sector': 'Service and Sales Workers', 'subsector': 'Sales Workers'}, 'Bookkeeping': {'sector': 'Technicians and Associate Professionals', 'subsector': 'Business and Administration Associate Professionals'}, 'Public Relations': {'sector': 'Professionals', 'subsector': 'Business and Administration Professionals'}, 'IT Specialist': {'sector': 'Professionals', 'subsector': 'Information and Communications Technology Professionals'}, 'Office administrator': {'sector': 'Professionals', 'subsector': 'Business and Administration Professionals'}, 'Accountant': {'sector': 'Professionals', 'subsector': 'Business and Administration Professionals'}, 'University professor': {'sector': 'Professionals', 'subsector': 'Teaching Professionals'}, 'Self-employed plumber': {'sector': 'Craft and Related Trades Workers', 'subsector': 'Building and Related Trades Workers (excluding Electricians)'}, 'Restaurant Manager': {'sector': 'Managers', 'subsector': 'Hospitality, Retail and Other Services Managers'}, 'Elder care worker': {'sector': 'Service and Sales Workers', 'subsector': 'Personal Care Workers'}, 'Hotel Industry': {'sector': 'Managers', 'subsector': 'Hospitality, Retail and Other Services Managers'}, 'Environmental consultant': {'sector': 'Professionals', 'subsector': 'Science and Engineering Professionals'}, 'Retired sales manager': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'Retired Civil Engineer': {'sector': 'Professionals', 'subsector': 'Science and Engineering Professionals'}, 'News Editor': {'sector': 'Professionals', 'subsector': 'Legal, Social and Cultural Professionals'}, 'Sales Manager': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'Truck driver': {'sector': 'Plant and Machine Operators, and Assemblers', 'subsector': 'Drivers and Mobile Plant Operators'}, 'Part-time freelance designer': {'sector': 'Professionals', 'subsector': 'Legal, Social and Cultural Professionals'}, 'Engineer': {'sector': 'Professionals', 'subsector': 'Science and Engineering Professionals'}, 'Elementary school teacher': {'sector': 'Professionals', 'subsector': 'Teaching Professionals'}, 'Corporate Designer': {'sector': 'Professionals', 'subsector': 'Legal, Social and Cultural Professionals'}, 'Restaurant Owner': {'sector': 'Managers', 'subsector': 'Hospitality, Retail and Other Services Managers'}, 'Housekeeper': {'sector': 'Service and Sales Workers', 'subsector': 'Personal Service Workers'}, 'Electronics repair technician': {'sector': 'Craft and Related Trades Workers', 'subsector': 'Electrical and Electronics Trades Workers'}, 'Retail sales associate': {'sector': 'Service and Sales Workers', 'subsector': 'Sales Workers'}, 'Retired': {'sector': 'Unemployed', 'subsector': 'Unemployed'}, 'Freelance Graphic Designer': {'sector': 'Professionals', 'subsector': 'Legal, Social and Cultural Professionals'}, 'Real Estate': {'sector': 'Professionals', 'subsector': 'Business and Administration Professionals'}, 'Full-Time Mother': {'sector': 'Unemployed', 'subsector': 'Unemployed'}, 'High School Teacher': {'sector': 'Professionals', 'subsector': 'Teaching Professionals'}, 'Stay-at-home mom': {'sector': 'Unemployed', 'subsector': 'Unemployed'}, 'Construction Worker': {'sector': 'Craft and Related Trades Workers', 'subsector': 'Building and Related Trades Workers (excluding Electricians)'}, 'High School English Teacher': {'sector': 'Professionals', 'subsector': 'Teaching Professionals'}, 'Financial Analyst': {'sector': 'Professionals', 'subsector': 'Business and Administration Professionals'}, 'Restaurant Worker': {'sector': 'Service and Sales Workers', 'subsector': 'Personal Service Workers'}, 'Bartender': {'sector': 'Service and Sales Workers', 'subsector': 'Personal Service Workers'}, 'Plumber': {'sector': 'Craft and Related Trades Workers', 'subsector': 'Building and Related Trades Workers (excluding Electricians)'}, 'Part-time retail worker': {'sector': 'Service and Sales Workers', 'subsector': 'Sales Workers'}, 'Works as a Mechanic': {'sector': 'Craft and Related Trades Workers', 'subsector': 'Metal, Machinery and Related Trades Workers'}, 'Substitute teacher': {'sector': 'Professionals', 'subsector': 'Teaching Professionals'}, 'Engineering Management': {'sector': 'Professionals', 'subsector': 'Science and Engineering Professionals'}, 'Service Industry (Waitress)': {'sector': 'Service and Sales Workers', 'subsector': 'Personal Service Workers'}, 'Healthcare aide, small online business owner': {'sector': 'Service and Sales Workers', 'subsector': 'Personal Care Workers'}, 'Part-time': {'sector': 'Unemployed', 'subsector': 'Unemployed'}, 'Retired Shop Owner': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'Freelance Artist': {'sector': 'Professionals', 'subsector': 'Legal, Social and Cultural Professionals'}, 'Drafting technician': {'sector': 'Technicians and Associate Professionals', 'subsector': 'Science and Engineering Associate Professionals'}, 'Small business owner': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'Maintenance supervisor': {'sector': 'Managers', 'subsector': 'Production and Specialized Services Managers'}, 'Freelance Copywriter': {'sector': 'Professionals', 'subsector': 'Legal, Social and Cultural Professionals'}, 'IT project manager': {'sector': 'Professionals', 'subsector': 'Information and Communications Technology Professionals'}, 'Restaurant Server': {'sector': 'Service and Sales Workers', 'subsector': 'Personal Service Workers'}, 'Auto mechanic': {'sector': 'Craft and Related Trades Workers', 'subsector': 'Metal, Machinery and Related Trades Workers'}, 'Homemaker': {'sector': 'Unemployed', 'subsector': 'Unemployed'}, 'Banking': {'sector': 'Professionals', 'subsector': 'Business and Administration Professionals'}, 'Marketing Manager in multinational corporation': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'High School History Teacher': {'sector': 'Professionals', 'subsector': 'Teaching Professionals'}, 'HR Manager': {'sector': 'Professionals', 'subsector': 'Business and Administration Professionals'}, 'Domestic Worker': {'sector': 'Service and Sales Workers', 'subsector': 'Personal Service Workers'}, 'Stay-at-home mother.': {'sector': 'Unemployed', 'subsector': 'Unemployed'}, 'Works as a taxi driver.': {'sector': 'Plant and Machine Operators, and Assemblers', 'subsector': 'Drivers and Mobile Plant Operators'}, 'Digitial Marketing': {'sector': 'Professionals', 'subsector': 'Business and Administration Professionals'}, 'Software Developer': {'sector': 'Professionals', 'subsector': 'Information and Communications Technology Professionals'}, 'Retired Construction Worker': {'sector': 'Craft and Related Trades Workers', 'subsector': 'Building and Related Trades Workers (excluding Electricians)'}, 'Digital Marketing': {'sector': 'Professionals', 'subsector': 'Business and Administration Professionals'}, 'Retired Accountant': {'sector': 'Professionals', 'subsector': 'Business and Administration Professionals'}, 'Office Worker': {'sector': 'Clerical Support Workers', 'subsector': 'General and Keyboard Clerks'}, 'Communications Director': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'Administrative assistant': {'sector': 'Technicians and Associate Professionals', 'subsector': 'Business and Administration Associate Professionals'}, 'Business Owner': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'Retail': {'sector': 'Service and Sales Workers', 'subsector': 'Sales Workers'}, 'Junior Marketer': {'sector': 'Technicians and Associate Professionals', 'subsector': 'Business and Administration Associate Professionals'}, 'Works as a hairdresser': {'sector': 'Service and Sales Workers', 'subsector': 'Personal Service Workers'}, 'IT Support': {'sector': 'Technicians and Associate Professionals', 'subsector': 'Information and Communications Technicians'}, 'Warehouse worker': {'sector': 'Elementary Occupations', 'subsector': 'Labourers in Mining, Construction, Manufacturing and Transport'}, 'Real estate agent': {'sector': 'Professionals', 'subsector': 'Business and Administration Professionals'}, 'Security Guard': {'sector': 'Service and Sales Workers', 'subsector': 'Protective Services Workers'}, 'Corporate Finance': {'sector': 'Professionals', 'subsector': 'Business and Administration Professionals'}, 'Restaurant Cook': {'sector': 'Elementary Occupations', 'subsector': 'Food Preparation Assistants'}, 'Hotel management, former restaurant owner': {'sector': 'Managers', 'subsector': 'Hospitality, Retail and Other Services Managers'}, 'Home health aide': {'sector': 'Service and Sales Workers', 'subsector': 'Personal Care Workers'}, 'Environmental compliance': {'sector': 'Professionals', 'subsector': 'Science and Engineering Professionals'}, 'Primary School Teacher': {'sector': 'Professionals', 'subsector': 'Teaching Professionals'}, 'Office manager': {'sector': 'Professionals', 'subsector': 'Business and Administration Professionals'}, 'Mechanic': {'sector': 'Craft and Related Trades Workers', 'subsector': 'Metal, Machinery and Related Trades Workers'}, 'Delivery service driver': {'sector': 'Plant and Machine Operators, and Assemblers', 'subsector': 'Drivers and Mobile Plant Operators'}, 'Financial Analyst at Big 4 Consulting Firm': {'sector': 'Professionals', 'subsector': 'Business and Administration Professionals'}, 'Construction site supervisor': {'sector': 'Craft and Related Trades Workers', 'subsector': 'Building and Related Trades Workers (excluding Electricians)'}, 'Community outreach worker': {'sector': 'Professionals', 'subsector': 'Legal, Social and Cultural Professionals'}, 'Nurse': {'sector': 'Professionals', 'subsector': 'Health Professionals'}, 'Academic (University Tutor)': {'sector': 'Professionals', 'subsector': 'Teaching Professionals'}, 'Human Resources Director': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'Mid-level marketing manager': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'Retired Teacher': {'sector': 'Professionals', 'subsector': 'Teaching Professionals'}, 'Retired administrative assistant': {'sector': 'Technicians and Associate Professionals', 'subsector': 'Business and Administration Associate Professionals'}, 'Marketing Professional': {'sector': 'Professionals', 'subsector': 'Business and Administration Professionals'}, 'Laid off / Unemployed': {'sector': 'Unemployed', 'subsector': 'Unemployed'}, 'Daycare Provider': {'sector': 'Service and Sales Workers', 'subsector': 'Personal Care Workers'}, 'Truck Driver': {'sector': 'Plant and Machine Operators, and Assemblers', 'subsector': 'Drivers and Mobile Plant Operators'}, 'Retail store supervisor': {'sector': 'Managers', 'subsector': 'Hospitality, Retail and Other Services Managers'}, 'Freelance writer': {'sector': 'Professionals', 'subsector': 'Legal, Social and Cultural Professionals'}, 'Retail Management': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'Delivery Driver': {'sector': 'Plant and Machine Operators, and Assemblers', 'subsector': 'Drivers and Mobile Plant Operators'}, 'Manufacturing': {'sector': 'Managers', 'subsector': 'Production and Specialized Services Managers'}, 'Entrepreneur': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'Community Health Roles': {'sector': 'Technicians and Associate Professionals', 'subsector': 'Health Associate Professionals'}, 'University Professor': {'sector': 'Professionals', 'subsector': 'Teaching Professionals'}, 'Retired Professor': {'sector': 'Professionals', 'subsector': 'Teaching Professionals'}, 'Warehouse Supervisor': {'sector': 'Managers', 'subsector': 'Production and Specialized Services Managers'}, 'Factory Technician': {'sector': 'Technicians and Associate Professionals', 'subsector': 'Science and Engineering Associate Professionals'}, 'Retired Farmer': {'sector': 'Skilled Agricultural, Forestry and Fishery Workers', 'subsector': 'Market-oriented Skilled Agricultural Workers'}, 'Former Nurse': {'sector': 'Professionals', 'subsector': 'Health Professionals'}, 'Retail worker': {'sector': 'Service and Sales Workers', 'subsector': 'Sales Workers'}, 'Restaurant owner': {'sector': 'Managers', 'subsector': 'Hospitality, Retail and Other Services Managers'}, 'Digital Marketing Manager': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'IT Consultant': {'sector': 'Professionals', 'subsector': 'Information and Communications Technology Professionals'}, 'Auto mechanic, shop owner': {'sector': 'Craft and Related Trades Workers', 'subsector': 'Metal, Machinery and Related Trades Workers'}, 'Construction Management': {'sector': 'Professionals', 'subsector': 'Science and Engineering Professionals'}, 'Transitioning from Teaching': {'sector': 'Professionals', 'subsector': 'Teaching Professionals'}, 'Sustainability Consultant': {'sector': 'Professionals', 'subsector': 'Science and Engineering Professionals'}, 'Electrician': {'sector': 'Craft and Related Trades Workers', 'subsector': 'Electrical and Electronics Trades Workers'}, 'Customer Service': {'sector': 'Clerical Support Workers', 'subsector': 'Customer Services Clerks'}, 'Chef': {'sector': 'Elementary Occupations', 'subsector': 'Food Preparation Assistants'}, 'Part-time Healthcare Administration': {'sector': 'Professionals', 'subsector': 'Business and Administration Professionals'}, 'Retail Manager': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'Freelance Social Media Manager': {'sector': 'Professionals', 'subsector': 'Business and Administration Professionals'}, 'Healthcare Administrator': {'sector': 'Professionals', 'subsector': 'Business and Administration Professionals'}, "Nurse's Assistant": {'sector': 'Technicians and Associate Professionals', 'subsector': 'Health Associate Professionals'}, 'Home Health Aide': {'sector': 'Service and Sales Workers', 'subsector': 'Personal Care Workers'}, 'Construction Site Supervisor': {'sector': 'Craft and Related Trades Workers', 'subsector': 'Building and Related Trades Workers (excluding Electricians)'}, 'Real Estate Agent': {'sector': 'Professionals', 'subsector': 'Business and Administration Professionals'}, 'Part-time Retail Worker, Caregiver': {'sector': 'Service and Sales Workers', 'subsector': 'Sales Workers'}, 'Freelance artist': {'sector': 'Professionals', 'subsector': 'Legal, Social and Cultural Professionals'}, 'Works in Childcare': {'sector': 'Service and Sales Workers', 'subsector': 'Personal Care Workers'}, 'Police Officer': {'sector': 'Service and Sales Workers', 'subsector': 'Protective Services Workers'}, 'Underemployed': {'sector': 'Unemployed', 'subsector': 'Unemployed'}, 'Small Business Owner': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'Restaurant manager': {'sector': 'Managers', 'subsector': 'Hospitality, Retail and Other Services Managers'}, 'Freelancer': {'sector': 'Unemployed', 'subsector': 'Unemployed'}, 'Retired electrician': {'sector': 'Craft and Related Trades Workers', 'subsector': 'Electrical and Electronics Trades Workers'}, 'Hospitality Worker': {'sector': 'Service and Sales Workers', 'subsector': 'Personal Service Workers'}, 'Housewife': {'sector': 'Unemployed', 'subsector': 'Unemployed'}, 'Middle Manager at Banking Sector': {'sector': 'Managers', 'subsector': 'Administrative and Commercial Managers'}, 'Lawyer': {'sector': 'Professionals', 'subsector': 'Legal, Social and Cultural Professionals'}, 'Stay-at-home Mom': {'sector': 'Unemployed', 'subsector': 'Unemployed'}, 'Stay-at-home mother': {'sector': 'Unemployed', 'subsector': 'Unemployed'}, 'Engineering': {'sector': 'Professionals', 'subsector': 'Science and Engineering Professionals'}, 'Secondary School Teacher': {'sector': 'Professionals', 'subsector': 'Teaching Professionals'}, 'IT consultant': {'sector': 'Professionals', 'subsector': 'Information and Communications Technology Professionals'}, 'Software Engineer': {'sector': 'Professionals', 'subsector': 'Information and Communications Technology Professionals'}, 'Mid-Level Manager in Manufacturing': {'sector': 'Managers', 'subsector': 'Production and Specialized Services Managers'}, 'IT project management': {'sector': 'Professionals', 'subsector': 'Information and Communications Technology Professionals'}, 'Pharmaceutical Research': {'sector': 'Professionals', 'subsector': 'Science and Engineering Professionals'}, 'Healthcare assistant': {'sector': 'Technicians and Associate Professionals', 'subsector': 'Health Associate Professionals'}, 'Retail Assistant': {'sector': 'Service and Sales Workers', 'subsector': 'Sales Workers'}, 'Employed': {'sector': 'Other', 'subsector': 'Other'}, 'Retail Sales': {'sector': 'Service and Sales Workers', 'subsector': 'Sales Workers'}, 'Aerospace engineer (retired)': {'sector': 'Professionals', 'subsector': 'Science and Engineering Professionals'}, 'Laboratory technician': {'sector': 'Technicians and Associate Professionals', 'subsector': 'Science and Engineering Associate Professionals'}, 'Licensed Practical Nurse': {'sector': 'Professionals', 'subsector': 'Health Professionals'}, 'Professor': {'sector': 'Professionals', 'subsector': 'Teaching Professionals'}, 'Technician': {'sector': 'Technicians and Associate Professionals', 'subsector': 'Science and Engineering Associate Professionals'}, 'Graphic Designer': {'sector': 'Professionals', 'subsector': 'Legal, Social and Cultural Professionals'}, 'Cashier': {'sector': 'Clerical Support Workers', 'subsector': 'Customer Services Clerks'}, 'Works as a cashier.': {'sector': 'Clerical Support Workers', 'subsector': 'Customer Services Clerks'}, 'Electronics Technician': {'sector': 'Craft and Related Trades Workers', 'subsector': 'Electrical and Electronics Trades Workers'}, 'Elementary School Teacher': {'sector': 'Professionals', 'subsector': 'Teaching Professionals'}, 'Construction Foreman': {'sector': 'Craft and Related Trades Workers', 'subsector': 'Building and Related Trades Workers (excluding Electricians)'}, 'Tutor': {'sector': 'Professionals', 'subsector': 'Teaching Professionals'}, 'Teacher, private tutor': {'sector': 'Professionals', 'subsector': 'Teaching Professionals'}, 'Civil engineer': {'sector': 'Professionals', 'subsector': 'Science and Engineering Professionals'}, 'Auto repair shop owner': {'sector': 'Craft and Related Trades Workers', 'subsector': 'Metal, Machinery and Related Trades Workers'}, 'Hospitality': {'sector': 'Managers', 'subsector': 'Hospitality, Retail and Other Services Managers'}, 'Investment Banking': {'sector': 'Professionals', 'subsector': 'Business and Administration Professionals'}, 'Social Services Worker': {'sector': 'Professionals', 'subsector': 'Legal, Social and Cultural Professionals'}, 'University Researcher': {'sector': 'Professionals', 'subsector': 'Science and Engineering Professionals'}, 'Musician': {'sector': 'Professionals', 'subsector': 'Legal, Social and Cultural Professionals'}, 'Teacher (on leave)': {'sector': 'Professionals', 'subsector': 'Teaching Professionals'}, 'Factory Worker': {'sector': 'Plant and Machine Operators, and Assemblers', 'subsector': 'Stationary Plant and Machine Operators'}, 'Aerospace engineering': {'sector': 'Professionals', 'subsector': 'Science and Engineering Professionals'}, 'Social Worker': {'sector': 'Professionals', 'subsector': 'Legal, Social and Cultural Professionals'}, 'Teacher': {'sector': 'Professionals', 'subsector': 'Teaching Professionals'}, 'Automotive Manufacturing': {'sector': 'Managers', 'subsector': 'Production and Specialized Services Managers'}, 'Retail Supervisor': {'sector': 'Managers', 'subsector': 'Hospitality, Retail and Other Services Managers'}, 'IT Manager': {'sector': 'Professionals', 'subsector': 'Information and Communications Technology Professionals'}, 'Auditing': {'sector': 'Professionals', 'subsector': 'Business and Administration Professionals'}, 'Management Consultant': {'sector': 'Professionals', 'subsector': 'Business and Administration Professionals'}, 'Data analyst': {'sector': 'Professionals', 'subsector': 'Business and Administration Professionals'}, 'Hotel Management': {'sector': 'Managers', 'subsector': 'Hospitality, Retail and Other Services Managers'}, 'Healthcare Assistant': {'sector': 'Technicians and Associate Professionals', 'subsector': 'Health Associate Professionals'}, 'Freelance Graphic Designer and Digital Artist': {'sector': 'Professionals', 'subsector': 'Legal, Social and Cultural Professionals'}, 'Freelance designer': {'sector': 'Professionals', 'subsector': 'Legal, Social and Cultural Professionals'}, 'Lab technician': {'sector': 'Technicians and Associate Professionals', 'subsector': 'Science and Engineering Associate Professionals'}, 'Senior Software Engineer at Financial Services Firm': {'sector': 'Professionals', 'subsector': 'Information and Communications Technology Professionals'}, 'Public relations': {'sector': 'Professionals', 'subsector': 'Business and Administration Professionals'}, 'Self-Employed Electrician': {'sector': 'Craft and Related Trades Workers', 'subsector': 'Electrical and Electronics Trades Workers'}, 'Advertising': {'sector': 'Professionals', 'subsector': 'Business and Administration Professionals'}, 'Housekeeping': {'sector': 'Service and Sales Workers', 'subsector': 'Personal Service Workers'}, 'Home-based daycare provider': {'sector': 'Service and Sales Workers', 'subsector': 'Personal Care Workers'}, 'Construction supervisor': {'sector': 'Craft and Related Trades Workers', 'subsector': 'Building and Related Trades Workers (excluding Electricians)'}, 'Translator': {'sector': 'Professionals', 'subsector': 'Legal, Social and Cultural Professionals'}, 'Works as a construction worker.': {'sector': 'Craft and Related Trades Workers', 'subsector': 'Building and Related Trades Workers (excluding Electricians)'}, 'Research Scientist in Pharmaceutical Company': {'sector': 'Professionals', 'subsector': 'Science and Engineering Professionals'}, 'Retired mechanic': {'sector': 'Craft and Related Trades Workers', 'subsector': 'Metal, Machinery and Related Trades Workers'}, 'Stay-at-home Mother': {'sector': 'Unemployed', 'subsector': 'Unemployed'}, 'Restaurant server, former small business owner in Mexico': {'sector': 'Service and Sales Workers', 'subsector': 'Personal Service Workers'}, 'Cleaner': {'sector': 'Elementary Occupations', 'subsector': 'Cleaners and Helpers'}, 'IT Technician': {'sector': 'Technicians and Associate Professionals', 'subsector': 'Information and Communications Technicians'}, 'Retired (Seamstress)': {'sector': 'Craft and Related Trades Workers', 'subsector': 'Food Processing, Woodworking, Garment and Other Craft and Related Trades Workers'}, 'Research': {'sector': 'Professionals', 'subsector': 'Science and Engineering Professionals'}, 'Preschool Teacher': {'sector': 'Professionals', 'subsector': 'Teaching Professionals'}, 'Junior engineer': {'sector': 'Technicians and Associate Professionals', 'subsector': 'Science and Engineering Associate Professionals'}, 'Project engineer': {'sector': 'Professionals', 'subsector': 'Science and Engineering Professionals'}}

        self.certifications = [
            "Associate Degree","Technical Education",
            "Bachelor's Degree","Master's Degree",
            "Ph.D","Diploma","Non-tertiary Education"
        ]
        
        self.sectors = list(set([
            info['sector'] for info in self._job_title_to_sector.values()
        ]))
        
        self.subsectors = list(set([
            info['subsector'] for info in self._job_title_to_sector.values()
        ]))

    def employment2sector(self,job_title:str):
        if job_title in self._job_title_to_sector:
            return self._job_title_to_sector[job_title]['sector']
        else:
            return 'Other'
        
    def employment2subsector(self,job_title:str):
        if job_title in self._job_title_to_sector:
            return self._job_title_to_sector[job_title]['subsector']
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
    

def squeeze_text(txt:str, width:int=25)->str:
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