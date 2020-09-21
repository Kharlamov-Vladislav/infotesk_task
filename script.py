from flask import Flask, request, jsonify
from datetime import datetime
import pandas as pd
import pytz

# init db
names_columns = ['geoid', 'asciiname', 'alternatenames', 'latitude',
                 'longitude', 'feature class', 'feature code', 'country code',
                 'cc2', 'admin1 code', 'admin2 code', 'admin3 code', 'admin4 code',
                 'population', 'elevation', 'dem', 'timezone', 'modification date']

table = pd.read_csv('RU.txt', sep='\t', names=names_columns, index_col=1)
# the most important columns
table = table[['geoid', 'asciiname', 'latitude', 'longitude', 'population', 'timezone']]

# for a more reliable search for an object / city
table.index = table['asciiname'].apply(lambda x: x.lower() if isinstance(x, str) else x)

# error no more than 10 meters
table[['latitude', 'longitude']] = table[['latitude', 'longitude']].applymap(lambda x: round(x, 4))

# calculate timezones
timezones = {}
for tz_1 in table['timezone'].unique():
    for tz_2 in table['timezone'].unique():
        try:
            time_1, time_2 = datetime.now(pytz.timezone(tz_1)), datetime.now(pytz.timezone(tz_2))
            dif_time = abs(time_1.hour - time_2.hour) % 12 + abs(time_2.minute - time_2.minute)
            timezones[(tz_1, tz_2)], timezones[(tz_2, tz_1)] = dif_time, dif_time
        except:
            continue

# sort cities by population
table = table.sort_values('population', ascending=False)


app = Flask(__name__)

app.config['SECRET_KEY'] = '494889f786a2253ebddafb0142ec20f4'


@app.route('/api/getcity/<int:geoid>', methods=['GET'])
def getcity(geoid):
    try:
        rows = table[table['geoid'] == geoid]
        return jsonify(rows.to_dict('records'))
    except:
        return 'Not found geoid', 400


@app.route('/api/cites', methods=['GET'])
def cites():
    page, n_cites = int(request.args['page']), int(request.args['n_cites'])
    try:
        if page > 0 and n_cites > 0:
            rows = table.iloc[n_cites * (page - 1): n_cites * page]
            return jsonify(rows.to_dict('records'))
        else:
            return 'Either the number of pages is less than zero, or the page number itself.', 400
    except:
        return 'Error in database', 400


@app.route('/api/compare_cites', methods=['GET'])
def compare_cites():

    city_1, city_2 = request.args['city_1'], request.args['city_2']
    city_1, city_2 = table[table['asciiname'] == city_1].iloc[:1], table[table['asciiname'] == city_2].iloc[:1]
    tz_city_1, tz_city_2 = city_1['timezone'].iloc[0], city_2['timezone'].iloc[0]
    diff_timezones = timezones[(tz_city_1, tz_city_2)] if (tz_city_1, tz_city_2) in timezones else None

    ans_json = [city_1.to_dict('records')[0], city_2.to_dict('records')[0],
                {'equal timezones': str(tz_city_1 == tz_city_2)},
                {'first city to the north': str(city_1['latitude'].iloc[0] > city_2['latitude'].iloc[0])},
                {"diff_timezones": diff_timezones}]

    return jsonify(ans_json)


if __name__ == '__main__':
    app.run(host="localhost", port=8000)


