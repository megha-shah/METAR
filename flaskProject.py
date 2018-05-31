from flask import Flask
from flask import jsonify 
from flask import request 
from utils import get_weather_data


app = Flask(__name__)


@app.route('/metar/ping')
def ping():
    dic = {}
    dic["data"] = "pong"
    return jsonify(dic)


@app.route('/metar/info')
def metar_info():
    dic = {}
    scode_value = request.args.get('scode') 
    nocache_value = request.args.get('nocache')
    result = get_weather_data(scode_value,nocache_value)
    return jsonify(result)


if __name__ == '__main__': 
    app.run(debug=True)