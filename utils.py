from urllib2 import urlopen
import math
import ast
from helper import get_redis_connection, set_redis_key, get_redis_key
from constants import CACHE_EXPIRE_TIME

def get_weather_data(station_code,nocache):
	if nocache == "1" or get_redis_key(station_code) == None:
		return fetch_weather_data(station_code) 
	else:
	    #ast.literal_eval is used to convert unicode to dictionary
	    #fetching data from cache
		return ast.literal_eval(get_redis_key(station_code)) 

def fetch_weather_data(station_code):
	url = "http://tgftp.nws.noaa.gov/data/observations/metar/stations/" + station_code + ".TXT"

	textpage = urlopen(url)

	first_row = textpage.readline()
	first_row_list = first_row.split(' ')

	second_row = textpage.readline()
	second_row_list = second_row.split(' ')

	report = {}
	#stores station code in report
	report["station"] = station_code

	#stores date and time in report
	date_and_time = first_row_list[0] + " at " + first_row_list[1].strip("\n") + " GMT";

	report["last_observation"] = date_and_time
	
	is_temp_exist = 0
	is_wind_exist = 0

	prev_value = ""
	for value in second_row_list:
		if len(prev_value) >=3 and (prev_value[:3]=="SKC" or prev_value[:3]=="FEW" or prev_value[:3]=="SCT" or prev_value[:3]=="BKN" or prev_value[:3]=="OVC"):
			if if_temperature_exist(value):
				#stores temperature in report
				report["temperature"] = set_temperature(value)
				is_temp_exist = 1

		#checking for wind		
		if "KT" in value:
			KT_index = value.index("KT")
			size = len(value[:KT_index])
			if (size == 5 and value[ :KT_index].isdigit()) or (size == 8 and value[ :KT_index].isdigit() and value[5] == "G" and value[6:8].isdigit()):
				#stores wind in report
				report["wind"] = set_wind(value)			
				is_wind_exist = 1

		if is_temp_exist == 1 and is_wind_exist == 1:
			break

		prev_value = value			
		

	final_report = {}
	final_report["data"] = report
	set_redis_key(station_code,final_report,CACHE_EXPIRE_TIME)
	return final_report		

#check if temperature is present in METAR
def if_temperature_exist(value):
	str1 = value
	value.strip("\n")
	str1.strip("\n")
	if len(str1) == 7 and str1[0] == "M":
		str1.strip("M")

	if len(str1) == 6 and str1[0] == "M":
		str1.strip("M")

	if len(str1) == 6 and str1[3] == "M":
		str1 = str1[:3] + str1[4:]

	if len(str1) == 5 and str1[2] == "/" and str1[:2].isdigit() and str1[3:].isdigit():
		return 1
	else:
		return 0	


# set temperature in correct format
def set_temperature(value):
	if value[0]=="M":
		if value[1]=="0":
			temperature = "-" + value[2] 
		else: 
			temperature = "-" + value[1:3] 
	else:
		if value[0]=="0":
			temperature = value[1]
		else: 
			temperature = value[:2]

	temp_in_fahrenheit = int(temperature) + 32
	temperature = temperature + " C (" + str(temp_in_fahrenheit) + " F)"
	return temperature
			
# set wind in correct format
def set_wind(value):
	direction = value[0:3] + " degree"
	if direction[:2] == "00":
		direction = direction.strip("00")

	elif direction[0] == "0":
		direction = direction.strip("0")

	velocity_in_knot = value[3:5]
	if velocity_in_knot[0] == "0":
		velocity_in_knot = value[4]

	velocity_in_mph = 1.15078 * float(velocity_in_knot)
	wind = direction + " at " + str(int(math.ceil(velocity_in_mph))) + " mph (" + velocity_in_knot + " knot)"
	return wind




	



    	



