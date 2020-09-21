*Тестовое задание В.Д. Харламова*

# Database API

# Table of contents

1. [Methods](#sec1) <a name="sec1"></a>
    1.1. [Method 1](#sec1.1)</br>
    1.2. [Method 2](#sec1.2)</br>
    1.3. [Method 3](#sec1.3)</br>
    

## Method 1
<a name="sec1.1"></a>
It accepts the following type of URL for input: 

"http://127.0.0.1:8000/api/getcity/<ind:geoid>",

where geoid is the object identifier number from the database `geonames` or `RU.txt` database.

Return JSON response in the form of information about the object, namely name, latitude, longitude, population, time zone.

### Example:

Input: "http://127.0.0.1:8000/api/getcity/563708"   
Output: [{   
"asciiname" : Dzerzhinsk,   
"geoid" : 563708,    
"latitude" : 56.2414,    
"longitude" : 43.4554,    
"population" : 233126,    
"timezone" : Europe/Moscow    
}]

## Method 2
<a name="sec1.2"></a>
It accepts the following type of URL for input: 

"http://127.0.0.1:8000/api/cites?page=<int: page>&n_cites=<int: n_cites>",

where `page` is the page number in the pagination, and `n_cites` is the number of cities displayed on this page.

Returns in response JSON an object containing information about all cities on the page, namely name, latitude, longitude, population, time zone.

### Example:

Input: "http://127.0.0.1:8000/api/cites?page=1&n_cites=3"   
Output: [    
    {    
        "asciiname": "Russian Federation",    
        "geoid": 2017370,    
        "latitude": 60.0,    
        "longitude": 100.0,    
        "population": 144478050,    
        "timezone": NaN    
    },    
    {     
        "asciiname": "European Russia",    
        "geoid": 11961320,     
        "latitude": 55.0,    
        "longitude": 40.0,     
        "population": 110000000,     
        "timezone": "Europe/Moscow"     
    },     
    {     
        "asciiname": "Central",     
        "geoid": 11961322,    
        "latitude": 55.7538,    
        "longitude": 37.6224,     
        "population": 38438600,     
        "timezone": "Europe/Moscow"     
    }     
]

## Method 3
<a name="sec1.3"></a>
It accepts the following type of URL for input: 

"http://127.0.0.1:8000/api/compare_cites?city_1=<str: name_city>&city_2=<str: name_city>",

where city names are taken from the database `RU.txt` from asciiname column.

returns JSON object with information about cities found by name, namely name, latitude, longitude, population, time zone. And also whether the first city is more northerly than the second, whether they have the same time zones and how much they differ. Attention, time zones may differ, but in fact they may have the same time.

### Example:

Input: "http://127.0.0.1:8000/api/compare_cites?city_1=Moscow&city_2=Vladivostok"   
Output: [    
-{    
"asciiname" : Moscow,    
"geoid" : 524901,    
"latitude" : 55.7522,    
"longitude" : 37.6156,    
"population" : 10381222,    
"timezone" : Europe/Moscow    
},    
-{    
"asciiname" : Vladivostok,    
"geoid" : 2013348,    
"latitude" : 43.1056,    
"longitude" : 131.8735,    
"population" : 587022,    
"timezone" : Asia/Vladivostok    
},    
-{    
"equal timezones" : False    
},    
-{    
"first city to the north" : True    
},    
-{    
"diff_timezones" : 7    
}    
]    

