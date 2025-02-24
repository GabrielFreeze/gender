class CountryHelper:
    def __init__(self):
        self.country_list = ['India', 'USA', 'UK', 'Canada', 'Australia']
        hispanic = ['Argentina','Bolivia','Bouvet Island','Brazil','Chile','Colombia','Ecuador','Falkland Islands (Malvinas)','French Guiana','Guyana','Paraguay','Peru','South Georgia and the South Sandwich Islands','Suriname','Uruguay','Venezuela','Belize','Costa Rica','El Salvador','Guatemala','Honduras','Mexico','Nicaragua','Panama']
        
        middle_east = ['Saudi Arabia','Iran','Iraq','Syria','Jordan','Lebanon','Israel','Palestine','Kuwait','Oman','Yemen','United Arab Emirates','Qatar','Bahrain']
        west_africa = ['Benin', 'Burkina Faso', 'Cabo Verde', 'Côte d’Ivoire', 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Liberia', 'Mali', 'Mauritania', 'Niger', 'Nigeria', 'Saint Helena', 'Senegal', 'Sierra Leone', 'Togo']
        north_africa =['Algeria','Egypt','Libya','Morocco','Sudan','Tunisia','Western Sahara']
        east_africa = ['Burundi','Comoros','Djibouti','Eritrea','Ethiopia','Kenya','Madagascar','Malawi','Mauritius','Mayotte','Mozambique','Réunion','Rwanda','Seychelles','Somalia','South Sudan','Uganda','Tanzania','Zambia','Zimbabwe']
        africa = west_africa + north_africa + ['British Indian Ocean Territory','Burundi','Comoros','Djibouti','Eritrea','Ethiopia','French Southern Territories','Kenya','Madagascar','Malawi','Mauritius','Mayotte','Mozambique','Réunion','Rwanda','Seychelles','Somalia','South Sudan','Uganda','United Republic of Tanzania','Zambia','Zimbabwe','Middle Africa','Angola','Cameroon','Central African Republic','Chad','Congo','Democratic Republic of the Congo','Equatorial Guinea','Gabon','Sao Tome and Principe','Southern Africa','Botswana','Eswatini','Lesotho','Namibia','South Africa']
        south_asian = ['Afghanistan','Bangladesh','Bhutan','India','Iran','Maldives','Nepal','Pakistan','Sri Lanka']
        east_asian = ['China','Japan','Mongolia','North Korea','South Korea','Taiwan']
        asia = ['Kazakhstan','Kyrgyzstan','Tajikistan','Turkmenistan','Uzbekistan','Eastern Asia','China','North Korea','Japan','Mongolia','South Korea','Brunei','Cambodia','Indonesia','Laos','Malaysia','Myanmar','Philippines','Singapore','Thailand','Timor-Leste','Vietnam']
        
        east_europe = ['Poland','Belarus','Czechia','Slovakia','Hungary','Romania','Bulgaria','Moldova','Ukraine','Russia']
        balkan = ['Greece','Serbia','Croatia','Bosnia and Herzegovina','Albania','North Macedonia','Kosovo','Montenegro','Bulgaria','Romania','Slovenia','Moldova']
        europe = east_europe + ['Denmark','Estonia','Finland','Iceland','Ireland','Isle of Man','Latvia','Lithuania','Norway','Sweden','United Kingdom','Albania','Andorra','Bosnia and Herzegovina','Croatia','Greece','Holy See','Italy','Malta','Montenegro','North Macedonia','Portugal','San Marino','Serbia','Slovenia','Spain','Austria','Belgium','France','Germany','Liechtenstein','Luxembourg','Monaco','Netherlands','Switzerland']
        
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
            'Bosnian':'Bosnia and Herzegovina','Botswanan':'Botswana','Brazilian':'Brazil','British':'United Kingdom','Bruneian':'Brunei','Bulgarian':'Bulgaria',
            'Burkinabé':'Burkina Faso','Burmese':'Myanmar','Burundian':'Burundi','Cabo Verdean':'Cabo Verde','Cambodian':'Cambodia','Cameroonian':'Cameroon',
            'Canadian':'Canada','Chadian':'Chad','Chilean':'Chile','Chinese':'China','Colombian':'Colombia','Comoran':'Comoros','Congolese':'Democratic Republic of the Congo',
            'Costa Rican':'Costa Rica','Croatian':'Croatia','Cuban':'Cuba','Curaçaoan':'Curaçao','Cypriot':'Cyprus','Czech':'Czech Republic','Danish':'Denmark',
            'Djiboutian':'Djibouti','Dominican':'Dominican Republic','Dutch':'Netherlands','East Timorese':'Timor-Leste','Ecuadorean':'Ecuador','Egyptian':'Egypt',
            'Emirati':'United Arab Emirates','Equatorial Guinean':'Equatorial Guinea','Eritrean':'Eritrea','Estonian':'Estonia','Ethiopian':'Ethiopia','Fijian':'Fiji',
            'Finnish':'Finland','French':'France','Gabonese':'Gabon','Gambian':'Gambia','Georgian':'Georgia','German':'Germany','Ghanaian':'Ghana','Gibraltarian':'Gibraltar',
            'Greek':'Greece','Greenlandic':'Greenland','Grenadian':'Grenada','Guadeloupean':'Guadeloupe','Guamanian':'Guam','Guatemalan':'Guatemala','Guernsey':'Guernsey',
            'Guinean':'Guinea','Guinea-Bissauan':'Guinea-Bissau','Guyanese':'Guyana','Haitian':'Haiti','Honduran':'Honduras','Hong Konger':'Hong Kong','Hungarian':'Hungary',
            'Icelandic':'Iceland','Indian':'India','Indonesian':'Indonesia','Iranian':'Iran','Iraqi':'Iraq','Irish':'Ireland','Israeli':'Israel','Italian':'Italy',
            'Ivorian':'Côte d`Ivoire','Jamaican':'Jamaica','Japanese':'Japan','Jordanian':'Jordan','Kazakhstani':'Kazakhstan','Kenyan':'Kenya','Kittitian':'Saint Kitts and Nevis',
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
            'Slovak':'Slovakia','Slovenian':'Slovenia','Solomon Islander':'Solomon Islands','Somali':'Somalia','South African':'South Africa','South Korean':'South Korea','South Sudanese':'South Sudan',
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
