# -*- coding: UTF-8 -*-
#
# Converter - MSNWeatherAstro
# Developer - Sirius
# Version 1.3
# Homepage - http://www.gisclub.tv
#
# Jean Meeus - Astronomical algorithms
# Victor Abalakin - Astronomical calendar
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import absolute_import
import os
import math
import gettext
import datetime, time
from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.config import config, configfile
from Components.Console import Console as iConsole
from Components.Language import language
from time import localtime, strftime
from datetime import date
from os import environ
from Components.Converter.Poll import Poll
import six


weather_city = config.plugins.weathermsn.city.value # 'Moscow,Russia'
degreetype = config.plugins.weathermsn.degreetype.value # 'C'
windtype = config.plugins.weathermsn.windtype.value # 'ms'
weather_location = config.osd.language.value.replace('_', '-') # 'ru-RU'

if weather_location == 'en-EN':
	weather_location = 'en-US'

time_update = 30
time_update_ms = 30000

class GlamMSNWeather(Poll, Converter, object):

	VFD = 1
	DATE = 2
	SHORTDATE = 3
	DAY = 4
	JDAY = 5
	SHORTDAY = 6
	LOCATION = 7
	TIMEZONE = 8
	LATITUDE = 9
	LONGITUDE = 10
	SUNRISE = 11
	SUNSET = 12
	SUNCULMINATION = 13
	MERCURYRISE = 14
	MERCURYSET = 15
	MERCURYCULMINATION = 16
	MERCURYAZIMUTH = 17
	VENUSRISE = 18
	VENUSSET = 19
	VENUSCULMINATION = 20
	VENUSAZIMUTH = 21
	MARSRISE = 22
	MARSSET = 23
	MARSCULMINATION = 24
	MARSAZIMUTH = 25
	JUPITERRISE = 26
	JUPITERSET = 27
	JUPITERCULMINATION = 28
	JUPITERAZIMUTH = 29
	SATURNRISE = 30
	SATURNSET = 31
	SATURNCULMINATION = 32
	SATURNAZIMUTH = 33
	URANUSRISE = 34
	URANUSSET = 35
	URANUSCULMINATION = 36
	URANUSAZIMUTH = 37
	NEPTUNERISE = 38
	NEPTUNESET = 39
	NEPTUNECULMINATION = 40
	NEPTUNEAZIMUTH = 41
	MOONRISE = 42
	MOONSET = 43
	MOONCULMINATION = 44
	MOONDIST = 45
	MOONAZIMUTH = 46
	MOONPHASE = 47
	MOONLIGHT = 48
	MOONPICON = 49
	TEMP = 50
	PICON = 51
	SKYTEXT = 52
	FEELSLIKE = 53
	HUMIDITY = 54
	WIND = 55
	WINDSPEED = 56
	DATE0 = 60
	SHORTDATE0 = 61
	DAY0 = 62
	SHORTDAY0 = 63
	TEMP0 = 64
	LOWTEMP0 = 65
	HIGHTEMP0 = 66
	PICON0 = 67
	SKYTEXT0 = 68
	PRECIP0 = 69
	DATE1 = 70
	SHORTDATE1 = 71
	DAY1 = 72
	SHORTDAY1 = 73
	TEMP1 = 74
	LOWTEMP1 = 75
	HIGHTEMP1 = 76
	PICON1 = 77
	SKYTEXT1 = 78
	PRECIP1 = 79
	DATE2 = 80
	SHORTDATE2 = 81
	DAY2 = 82
	SHORTDAY2 = 83
	TEMP2 = 84
	LOWTEMP2 = 85
	HIGHTEMP2 = 86
	PICON2 = 87
	SKYTEXT2 = 88
	PRECIP2 = 89
	DATE3 = 90
	SHORTDATE3 = 91
	DAY3 = 92
	SHORTDAY3 = 93
	TEMP3 = 94
	LOWTEMP3 = 95
	HIGHTEMP3 = 96
	PICON3 = 97
	SKYTEXT3 = 98
	PRECIP3 = 99
	DATE4 = 100
	SHORTDATE4 = 101
	DAY4 = 102
	SHORTDAY4 = 103
	TEMP4 = 104
	LOWTEMP4 = 105
	HIGHTEMP4 = 106
	PICON4 = 107
	SKYTEXT4 = 108
	PRECIP4 = 109

	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		if type == "Vfd":
			self.type = self.VFD
		elif type == "Date":
			self.type = self.DATE
		elif type == "Shortdate":
			self.type = self.SHORTDATE
		elif type == "Day":
			self.type = self.DAY
		elif type == "Julianday":
			self.type = self.JDAY
		elif type == "Shortday":
			self.type = self.SHORTDAY
		elif type == "Location":
			self.type = self.LOCATION
		elif type == "Timezone":
			self.type = self.TIMEZONE
		elif type == "Latitude":
			self.type = self.LATITUDE
		elif type == "Longitude":
			self.type = self.LONGITUDE
# Astro
		elif type == "Sunrise":
			self.type = self.SUNRISE
		elif type == "Sunset":
			self.type = self.SUNSET
		elif type == "Solstice":
			self.type = self.SUNCULMINATION
		elif type == "Mercuryrise":
			self.type = self.MERCURYRISE
		elif type == "Mercuryset":
			self.type = self.MERCURYSET
		elif type == "Mercuryculmination":
			self.type = self.MERCURYCULMINATION
		elif type == "Mercuryazimuth":
			self.type = self.MERCURYAZIMUTH
		elif type == "Venusrise":
			self.type = self.VENUSRISE
		elif type == "Venusset":
			self.type = self.VENUSSET
		elif type == "Venusculmination":
			self.type = self.VENUSCULMINATION
		elif type == "Venusazimuth":
			self.type = self.VENUSAZIMUTH
		elif type == "Marsrise":
			self.type = self.MARSRISE
		elif type == "Marsset":
			self.type = self.MARSSET
		elif type == "Marsculmination":
			self.type = self.MARSCULMINATION
		elif type == "Marsazimuth":
			self.type = self.MARSAZIMUTH
		elif type == "Jupiterrise":
			self.type = self.JUPITERRISE
		elif type == "Jupiterset":
			self.type = self.JUPITERSET
		elif type == "Jupiterculmination":
			self.type = self.JUPITERCULMINATION
		elif type == "Jupiterazimuth":
			self.type = self.JUPITERAZIMUTH
		elif type == "Saturnrise":
			self.type = self.SATURNRISE
		elif type == "Saturnset":
			self.type = self.SATURNSET
		elif type == "Saturnculmination":
			self.type = self.SATURNCULMINATION
		elif type == "Saturnazimuth":
			self.type = self.SATURNAZIMUTH
		elif type == "Uranusrise":
			self.type = self.URANUSRISE
		elif type == "Uranusset":
			self.type = self.URANUSSET
		elif type == "Uranusculmination":
			self.type = self.URANUSCULMINATION
		elif type == "Uranusazimuth":
			self.type = self.URANUSAZIMUTH
		elif type == "Neptunerise":
			self.type = self.NEPTUNERISE
		elif type == "Neptuneset":
			self.type = self.NEPTUNESET
		elif type == "Neptuneculmination":
			self.type = self.NEPTUNECULMINATION
		elif type == "Neptuneazimuth":
			self.type = self.NEPTUNEAZIMUTH
		elif type == "Moonrise":
			self.type = self.MOONRISE
		elif type == "Moonset":
			self.type = self.MOONSET
		elif type == "Moonculmination":
			self.type = self.MOONCULMINATION
		elif type == "Moondist":
			self.type = self.MOONDIST
		elif type == "Moonazimuth":
			self.type = self.MOONAZIMUTH
		elif type == "Moonphase":
			self.type = self.MOONPHASE
		elif type == "Moonlight":
			self.type = self.MOONLIGHT
		elif type == "PiconMoon":
			self.type = self.MOONPICON
# Now
		elif type == "Temp":
			self.type = self.TEMP
		elif type == "Picon":
			self.type = self.PICON
		elif type == "Skytext":
			self.type = self.SKYTEXT
		elif type == "Feelslike":
			self.type = self.FEELSLIKE
		elif type == "Humidity":
			self.type = self.HUMIDITY
		elif type == "Wind":
			self.type = self.WIND
		elif type == "Windspeed":
			self.type = self.WINDSPEED
# Day 0
		elif type == "Date0":
			self.type = self.DATE0
		elif type == "Shortdate0":
			self.type = self.SHORTDATE0
		elif type == "Day0":
			self.type = self.DAY0
		elif type == "Shortday0":
			self.type = self.SHORTDAY0
		elif type == "Temp0":
			self.type = self.TEMP0
		elif type == "Lowtemp0":
			self.type = self.LOWTEMP0
		elif type == "Hightemp0":
			self.type = self.HIGHTEMP0
		elif type == "Picon0":
			self.type = self.PICON0
		elif type == "Skytext0":
			self.type = self.SKYTEXT0
		elif type == "Precip0":
			self.type = self.PRECIP0
# Day 1
		elif type == "Date1":
			self.type = self.DATE1
		elif type == "Shortdate1":
			self.type = self.SHORTDATE1
		elif type == "Day1":
			self.type = self.DAY1
		elif type == "Shortday1":
			self.type = self.SHORTDAY1
		elif type == "Temp1":
			self.type = self.TEMP1
		elif type == "Lowtemp1":
			self.type = self.LOWTEMP1
		elif type == "Hightemp1":
			self.type = self.HIGHTEMP1
		elif type == "Picon1":
			self.type = self.PICON1
		elif type == "Skytext1":
			self.type = self.SKYTEXT1
		elif type == "Precip1":
			self.type = self.PRECIP1
# Day 2
		elif type == "Date2":
			self.type = self.DATE2
		elif type == "Shortdate2":
			self.type = self.SHORTDATE2
		elif type == "Day2":
			self.type = self.DAY2
		elif type == "Shortday2":
			self.type = self.SHORTDAY2
		elif type == "Temp2":
			self.type = self.TEMP2
		elif type == "Lowtemp2":
			self.type = self.LOWTEMP2
		elif type == "Hightemp2":
			self.type = self.HIGHTEMP2
		elif type == "Picon2":
			self.type = self.PICON2
		elif type == "Skytext2":
			self.type = self.SKYTEXT2
		elif type == "Precip2":
			self.type = self.PRECIP2
# Day 3
		elif type == "Date3":
			self.type = self.DATE3
		elif type == "Shortdate3":
			self.type = self.SHORTDATE3
		elif type == "Day3":
			self.type = self.DAY3
		elif type == "Shortday3":
			self.type = self.SHORTDAY3
		elif type == "Temp3":
			self.type = self.TEMP3
		elif type == "Lowtemp3":
			self.type = self.LOWTEMP3
		elif type == "Hightemp3":
			self.type = self.HIGHTEMP3
		elif type == "Picon3":
			self.type = self.PICON3
		elif type == "Skytext3":
			self.type = self.SKYTEXT3
		elif type == "Precip3":
			self.type = self.PRECIP3
# Day 4
		elif type == "Date4":
			self.type = self.DATE4
		elif type == "Shortdate4":
			self.type = self.SHORTDATE4
		elif type == "Day4":
			self.type = self.DAY4
		elif type == "Shortday4":
			self.type = self.SHORTDAY4
		elif type == "Temp4":
			self.type = self.TEMP4
		elif type == "Lowtemp4":
			self.type = self.LOWTEMP4
		elif type == "Hightemp4":
			self.type = self.HIGHTEMP4
		elif type == "Picon4":
			self.type = self.PICON4
		elif type == "Skytext4":
			self.type = self.SKYTEXT4
		elif type == "Precip4":
			self.type = self.PRECIP4

		self.iConsole = iConsole()
		self.poll_interval = time_update_ms
		self.poll_enabled = True

	def control_xml(self, result, retval, extra_args):
		if retval != 0:
			self.write_none()

	def write_none(self):
		with open("/tmp/weathermsn2.xml", "wb") as noneweather:
			noneweather.write("None").encode("utf8", "ignore")
		noneweather.close()

	def get_xmlfile(self):
		self.iConsole.ePopen("wget -P /tmp -T2 'http://weather.service.msn.com/data.aspx?weadegreetype=%s&culture=%s&weasearchstr=%s&src=outlook' -O /tmp/weathermsn2.xml" % (degreetype, weather_location, weather_city), self.control_xml)

	@cached
	def getText(self):
		year = float(strftime('%Y'))
		month = float(strftime('%m'))
		day = float(strftime('%d'))
		hour = float(strftime('%H'))
		min = float(strftime('%M'))
		sec = float(strftime('%S'))
		info, weze = 'n/a', ''
		msnweather = {'Vfd': '',\
			'Date': '',\
			'Shortdate': '',\
			'Day': '',\
			'Shortday': '',\
			'Location': '',\
			'Timezone': '',\
			'Latitude': '',\
			'Longitude': '',\
			'Julianday': '',\
			'Sunrise': '',\
			'Sunset': '',\
			'Solstice': '',\
			'Mercuryrise': '',\
			'Mercuryset': '',\
			'Mercuryculmination': '',\
			'Mercuryazimuth': '',\
			'Venusrise': '',\
			'Venusset': '',\
			'Venusculmination': '',\
			'Venusazimuth': '',\
			'Marsrise': '',\
			'Marsset': '',\
			'Marsculmination': '',\
			'Marsazimuth': '',\
			'Jupiterrise': '',\
			'Jupiterset': '',\
			'Jupiterculmination': '',\
			'Jupiterazimuth': '',\
			'Saturnrise': '',\
			'Saturnset': '',\
			'Saturnculmination': '',\
			'Saturnazimuth': '',\
			'Uranusrise': '',\
			'Uranusset': '',\
			'Uranusculmination': '',\
			'Uranusazimuth': '',\
			'Neptunerise': '',\
			'Neptuneset': '',\
			'Neptuneculmination': '',\
			'Neptuneazimuth': '',\
			'Moonrise': '',\
			'Moonset': '',\
			'Moonculmination': '',\
			'Moondist': '',\
			'Moonazimuth': '',\
			'Moonphase': '',\
			'Moonlight': '',\
			'PiconMoon': '1',\
			'Temp': '',\
			'Picon': '',\
			'Skytext': '',\
			'Feelslike': '',\
			'Humidity': '',\
			'Wind': '',\
			'Windspeed': '',\
			'Date0': '',\
			'Shortdate0': '',\
			'Day0': '',\
			'Shortday0': '',\
			'Temp0': '',\
			'Lowtemp0': '',\
			'Hightemp0': '',\
			'Picon0': '',\
			'Skytext0': '',\
			'Precip0': '',\
			'Date1': '',\
			'Shortdate1': '',\
			'Day1': '',\
			'Shortday1': '',\
			'Temp1': '',\
			'Lowtemp1': '',\
			'Hightemp1': '',\
			'Picon1': '',\
			'Skytext1': '',\
			'Precip1': '',\
			'Date2': '',\
			'Shortdate2': '',\
			'Day2': '',\
			'Shortday2': '',\
			'Temp2': '',\
			'Lowtemp2': '',\
			'Hightemp2': '',\
			'Picon2': '',\
			'Skytext2': '',\
			'Precip2': '',\
			'Date3': '',\
			'Shortdate3': '',\
			'Day3': '',\
			'Shortday3': '',\
			'Temp3': '',\
			'Lowtemp3': '',\
			'Hightemp3': '',\
			'Picon3': '',\
			'Skytext3': '',\
			'Precip3': '',\
			'Date4': '',\
			'Shortdate4': '',\
			'Day4': '',\
			'Shortday4': '',\
			'Temp4': '',\
			'Lowtemp4': '',\
			'Hightemp4': '',\
			'Picon4': '',\
			'Skytext4': '',\
			'Precip4': '',\
			}
#
		if six.PY2:
			wdata = open("/tmp/weathermsn2.xml")
		else:
			wdata = open("/tmp/weathermsn2.xml", encoding="utf-8")
		if os.path.exists("/tmp/weathermsn2.xml"):
			if int((time.time() - os.stat("/tmp/weathermsn2.xml").st_mtime)/60) >= time_update:
				self.get_xmlfile()
		else:
			self.get_xmlfile()
		if not os.path.exists("/tmp/weathermsn2.xml"):
			self.write_none()
			return info
		if os.path.exists("/tmp/weathermsn2.xml") and wdata == 'None':
			return info
		for line in wdata:
			try:
				if "<weather" in line:
					msnweather['Location'] = line.split('weatherlocationname')[1].split('"')[1].split(',')[0]
					if not line.split('timezone')[1].split('"')[1][0] == '0':
						msnweather['Timezone'] = _('+%s h') % line.split('timezone')[1].split('"')[1]
					else:
						msnweather['Timezone'] = _('%s h') % line.split('timezone')[1].split('"')[1]
					timezone = '%s' % float(line.split('timezone')[1].split('"')[1])
					msnweather['Latitude'] = line.split(' lat')[1].split('"')[1]
					msnweather['Longitude'] = line.split(' long')[1].split('"')[1]
					latitude = '%s' %  line.split(' lat')[1].split('"')[1].replace(',', '.')
					longitude = '%s' %  line.split(' long')[1].split('"')[1].replace(',', '.')
				if "<current" in line:
					if not line.split('temperature')[1].split('"')[1][0] == '-' and not line.split('temperature')[1].split('"')[1][0] == '0':
						msnweather['Temp'] = '+' + line.split('temperature')[1].split('"')[1] + '%s%s' % (six.ensure_str(six.unichr(176)), degreetype)
					else:
						msnweather['Temp'] = line.split('temperature')[1].split('"')[1] + '%s%s' % (six.ensure_str(six.unichr(176)), degreetype)
					if not line.split('feelslike')[1].split('"')[1][0] == '-' and not line.split('feelslike')[1].split('"')[1][0] == '0':
						msnweather['Feelslike'] = '+' + line.split('feelslike')[1].split('"')[1] + '%s%s' % (six.ensure_str(six.unichr(176)), degreetype)
					else:
						msnweather['Feelslike'] = line.split('feelslike')[1].split('"')[1] + '%s%s' % (six.ensure_str(six.unichr(176)), degreetype)
					msnweather['Picon'] = line.split('skycode')[1].split('"')[1]
					msnweather['Skytext'] = line.split('skytext')[1].split('"')[1]
					msnweather['Humidity'] = line.split('humidity')[1].split('"')[1] + ' %s' % six.ensure_str(six.unichr(37))
					try:
						msnweather['Wind'] = line.split('winddisplay')[1].split('"')[1].split(' ')[2]
					except:
						pass
# m/s
					if windtype == 'ms' and line.split('windspeed')[1].split('"')[1].split(' ')[1] == 'm/s':
						msnweather['Windspeed'] = _('%s m/s') % line.split('windspeed')[1].split('"')[1].split(' ')[0]
					elif windtype == 'ms' and line.split('windspeed')[1].split('"')[1].split(' ')[1] == 'km/h':
						msnweather['Windspeed'] = _('%.01f m/s') % (float(line.split('windspeed')[1].split('"')[1].split(' ')[0]) * 0.28)
					elif windtype == 'ms' and line.split('windspeed')[1].split('"')[1].split(' ')[1] == 'mph':
						msnweather['Windspeed'] = _('%.01f m/s') % (float(line.split('windspeed')[1].split('"')[1].split(' ')[0]) * 0.45)
# ft/s
					elif windtype == 'fts' and line.split('windspeed')[1].split('"')[1].split(' ')[1] == 'm/s':
						msnweather['Windspeed']= _('%.01f ft/s') % (float(line.split('windspeed')[1].split('"')[1].split(' ')[0]) * 3.28)
					elif windtype == 'fts' and line.split('windspeed')[1].split('"')[1].split(' ')[1] == 'km/h':
						msnweather['Windspeed']= _('%.01f ft/s') % (float(line.split('windspeed')[1].split('"')[1].split(' ')[0]) * 0.91)
					elif windtype == 'ms' and line.split('windspeed')[1].split('"')[1].split(' ')[1] == 'mph':
						msnweather['Windspeed'] = _('%.01f ft/s') % (float(line.split('windspeed')[1].split('"')[1].split(' ')[0]) * 1.47)
# mp/h
					elif windtype == 'mph' and line.split('windspeed')[1].split('"')[1].split(' ')[1] == 'm/s':
						msnweather['Windspeed'] = _('%.01f mp/h') % (float(line.split('windspeed')[1].split('"')[1].split(' ')[0]) * 2.24)
					elif windtype == 'mph' and line.split('windspeed')[1].split('"')[1].split(' ')[1] == 'km/h':
						msnweather['Windspeed'] = _('%.01f mp/h') % (float(line.split('windspeed')[1].split('"')[1].split(' ')[0]) * 0.62)
					elif windtype == 'ms' and line.split('windspeed')[1].split('"')[1].split(' ')[1] == 'mph':
						msnweather['Windspeed'] = _('%s mp/h') % line.split('windspeed')[1].split('"')[1].split(' ')[0]
# knots
					elif windtype == 'knots' and line.split('windspeed')[1].split('"')[1].split(' ')[1] == 'm/s':
						msnweather['Windspeed'] = _('%.01f knots') % (float(line.split('windspeed')[1].split('"')[1].split(' ')[0]) * 1.94)
					elif windtype == 'knots' and line.split('windspeed')[1].split('"')[1].split(' ')[1] == 'km/h':
						msnweather['Windspeed'] = _('%.01f knots') % (float(line.split('windspeed')[1].split('"')[1].split(' ')[0]) * 0.54)
					elif windtype == 'ms' and line.split('windspeed')[1].split('"')[1].split(' ')[1] == 'mph':
						msnweather['Windspeed'] = _('%.01f knots') % (float(line.split('windspeed')[1].split('"')[1].split(' ')[0]) * 0.87)
# km/h
					elif windtype == 'kmh' and line.split('windspeed')[1].split('"')[1].split(' ')[1] == 'm/s':
						msnweather['Windspeed'] = _('%.01f km/h') % (float(line.split('windspeed')[1].split('"')[1].split(' ')[0]) * 3.6)
					elif windtype == 'kmh' and line.split('windspeed')[1].split('"')[1].split(' ')[1] == 'km/h':
						msnweather['Windspeed'] = _('%s km/h') % line.split('windspeed')[1].split('"')[1].split(' ')[0]
					elif windtype == 'ms' and line.split('windspeed')[1].split('"')[1].split(' ')[1] == 'mph':
						msnweather['Windspeed'] = _('%.01f km/h') % (float(line.split('windspeed')[1].split('"')[1].split(' ')[0]) * 1.61)
					msnweather['Date'] = line.split('date')[1].split('"')[1].split('-')[2].strip() + '.' + line.split('date')[1].split('"')[1].split('-')[1].strip() + '.' + line.split('date')[1].split('"')[1].split('-')[0].strip()
					msnweather['Shortdate'] = line.split('shortday')[1].split('"')[1] + ' ' + line.split('date')[1].split('"')[1].split('-')[2].strip()
					msnweather['Day'] = line.split(' day')[1].split('"')[1]
					msnweather['Shortday'] = line.split('shortday')[1].split('"')[1]
# Day 0
				if "<forecast" in line:
					if not line.split('low')[1].split('"')[1][0] == '-' and not line.split('low')[1].split('"')[1][0] == '0':
						low0weather = '+' + line.split('low')[1].split('"')[1] + '%s' % six.ensure_str(six.unichr(176))
						msnweather['Lowtemp0'] = '%s%s' % (low0weather, degreetype)
					else:
						low0weather = line.split('low')[1].split('"')[1] + '%s' % six.ensure_str(six.unichr(176))
						msnweather['Lowtemp0'] = '%s%s' % (low0weather, degreetype)
					if not line.split('high')[1].split('"')[1][0] == '-' and not line.split('high')[1].split('"')[1][0] == '0':
						hi0weather = '+' + line.split('high')[1].split('"')[1] + '%s' % six.ensure_str(six.unichr(176))
						msnweather['Hightemp0'] = '%s%s' % (hi0weather, degreetype)
					else:
						hi0weather = line.split('high')[1].split('"')[1] + '%s' % six.ensure_str(six.unichr(176))
						msnweather['Hightemp0'] = '%s%s' % (hi0weather, degreetype)
					msnweather['Temp0'] = '%s / %s' % (hi0weather, low0weather)
					msnweather['Picon0'] = line.split('skycodeday')[1].split('"')[1]
					msnweather['Date0'] = line.split('date')[2].split('"')[1].split('-')[2].strip() + '.' + line.split('date')[2].split('"')[1].split('-')[1].strip() + '.' + line.split('date')[2].split('"')[1].split('-')[0].strip()
					msnweather['Shortdate0'] = line.split('shortday')[2].split('"')[1] + ' ' + line.split('date')[2].split('"')[1].split('-')[2].strip()
					msnweather['Day0'] = line.split(' day')[2].split('"')[1]
					msnweather['Shortday0'] = line.split('shortday')[2].split('"')[1]
					msnweather['Skytext0'] = line.split('skytextday')[1].split('"')[1]
					msnweather['Precip0'] = line.split('precip')[1].split('"')[1] + ' %s' % six.ensure_str(six.unichr(37))
# Day 1
				if "<forecast" in line:
					if not line.split('low')[2].split('"')[1][0] == '-' and not line.split('low')[2].split('"')[1][0] == '0':
						low1weather = '+' + line.split('low')[2].split('"')[1] + '%s' % six.ensure_str(six.unichr(176))
						msnweather['Lowtemp1'] = '%s%s' % (low1weather, degreetype)
					else:
						low1weather = line.split('low')[2].split('"')[1] + '%s' % six.ensure_str(six.unichr(176))
						msnweather['Lowtemp1'] = '%s%s' % (low1weather, degreetype)
					if not line.split('high')[2].split('"')[1][0] == '-' and not line.split('high')[2].split('"')[1][0] == '0':
						hi1weather = '+' + line.split('high')[2].split('"')[1] + '%s' % six.ensure_str(six.unichr(176))
						msnweather['Hightemp1'] = '%s%s' % (hi1weather, degreetype)
					else:
						hi1weather = line.split('high')[2].split('"')[1] + '%s' % six.ensure_str(six.unichr(176))
						msnweather['Hightemp1'] = '%s%s' % (hi1weather, degreetype)
					msnweather['Temp1'] = '%s / %s' % (hi1weather, low1weather)
					msnweather['Picon1'] = line.split('skycodeday')[2].split('"')[1]
					msnweather['Date1'] = line.split('date')[3].split('"')[1].split('-')[2].strip() + '.' + line.split('date')[3].split('"')[1].split('-')[1].strip() + '.' + line.split('date')[3].split('"')[1].split('-')[0].strip()
					msnweather['Shortdate1'] = line.split('shortday')[3].split('"')[1] + ' ' + line.split('date')[3].split('"')[1].split('-')[2].strip()
					msnweather['Day1'] = line.split(' day')[3].split('"')[1]
					msnweather['Shortday1'] = line.split('shortday')[3].split('"')[1]
					msnweather['Skytext1'] = line.split('skytextday')[2].split('"')[1]
					msnweather['Precip1'] = line.split('precip')[2].split('"')[1] + ' %s' % six.ensure_str(six.unichr(37))
# Day 2
				if "<forecast" in line:
					if not line.split('low')[3].split('"')[1][0] == '-' and not line.split('low')[3].split('"')[1][0] == '0':
						low2weather = '+' + line.split('low')[3].split('"')[1] + '%s' % six.ensure_str(six.unichr(176))
						msnweather['Lowtemp2'] = '%s%s' % (low2weather, degreetype)
					else:
						low2weather = line.split('low')[3].split('"')[1] + '%s' % six.ensure_str(six.unichr(176))
						msnweather['Lowtemp2'] = '%s%s' % (low2weather, degreetype)
					if not line.split('high')[3].split('"')[1][0] == '-' and not line.split('high')[3].split('"')[1][0] == '0':
						hi2weather = '+' + line.split('high')[3].split('"')[1] + '%s' % six.ensure_str(six.unichr(176))
						msnweather['Hightemp2'] = '%s%s' % (hi2weather, degreetype)
					else:
						hi2weather = line.split('high')[3].split('"')[1] + '%s' % six.ensure_str(six.unichr(176))
						msnweather['Hightemp2'] = '%s%s' % (hi2weather, degreetype)
					msnweather['Temp2'] = '%s / %s' % (hi2weather, low2weather)
					msnweather['Picon2'] = line.split('skycodeday')[3].split('"')[1]
					msnweather['Date2'] = line.split('date')[4].split('"')[1].split('-')[2].strip() + '.' + line.split('date')[4].split('"')[1].split('-')[1].strip() + '.' + line.split('date')[4].split('"')[1].split('-')[0].strip()
					msnweather['Shortdate2'] = line.split('shortday')[4].split('"')[1] + ' ' + line.split('date')[4].split('"')[1].split('-')[2].strip()
					msnweather['Day2'] = line.split(' day')[4].split('"')[1]
					msnweather['Shortday2'] = line.split('shortday')[4].split('"')[1]
					msnweather['Skytext2'] = line.split('skytextday')[3].split('"')[1]
					msnweather['Precip2'] = line.split('precip')[3].split('"')[1] + ' %s' % six.ensure_str(six.unichr(37))
# Day 3
				if "<forecast" in line:
					if not line.split('low')[4].split('"')[1][0] == '-' and not line.split('low')[4].split('"')[1][0] == '0':
						low3weather = '+' + line.split('low')[4].split('"')[1] + '%s' % six.ensure_str(six.unichr(176))
						msnweather['Lowtemp3'] = '%s%s' % (low3weather, degreetype)
					else:
						low3weather = line.split('low')[4].split('"')[1] + '%s' % six.ensure_str(six.unichr(176))
						msnweather['Lowtemp3'] = '%s%s' % (low3weather, degreetype)
					if not line.split('high')[4].split('"')[1][0] == '-' and not line.split('high')[4].split('"')[1][0] == '0':
						hi3weather = '+' + line.split('high')[4].split('"')[1] + '%s' % six.ensure_str(six.unichr(176))
						msnweather['Hightemp3'] = '%s%s' % (hi3weather, degreetype)
					else:
						hi3weather = line.split('high')[4].split('"')[1] + '%s' % six.ensure_str(six.unichr(176))
						msnweather['Hightemp3'] = '%s%s' % (hi3weather, degreetype)
					msnweather['Temp3'] = '%s / %s' % (hi3weather, low3weather)
					msnweather['Picon3'] = line.split('skycodeday')[4].split('"')[1]
					msnweather['Date3'] = line.split('date')[5].split('"')[1].split('-')[2].strip() + '.' + line.split('date')[5].split('"')[1].split('-')[1].strip() + '.' + line.split('date')[5].split('"')[1].split('-')[0].strip()
					msnweather['Shortdate3'] = line.split('shortday')[5].split('"')[1] + ' ' + line.split('date')[5].split('"')[1].split('-')[2].strip()
					msnweather['Day3'] = line.split(' day')[5].split('"')[1]
					msnweather['Shortday3'] = line.split('shortday')[5].split('"')[1]
					msnweather['Skytext3'] = line.split('skytextday')[4].split('"')[1]
					msnweather['Precip3'] = line.split('precip')[4].split('"')[1] + ' %s' % six.ensure_str(six.unichr(37))
# Day 4
				if "<forecast" in line:
					if not line.split('low')[5].split('"')[1][0] == '-' and not line.split('low')[5].split('"')[1][0] == '0':
						low4weather = '+' + line.split('low')[5].split('"')[1] + '%s' % six.ensure_str(six.unichr(176))
						msnweather['Lowtemp4'] = '%s%s' % (low4weather, degreetype)
					else:
						low4weather = line.split('low')[5].split('"')[1] + '%s' % six.ensure_str(six.unichr(176))
						msnweather['Lowtemp4'] = '%s%s' % (low4weather, degreetype)
					if not line.split('high')[5].split('"')[1][0] == '-' and not line.split('high')[5].split('"')[1][0] == '0':
						hi4weather = '+' + line.split('high')[5].split('"')[1] + '%s' % six.ensure_str(six.unichr(176))
						msnweather['Hightemp4'] = '%s%s' % (hi4weather, degreetype)
					else:
						hi4weather = line.split('high')[5].split('"')[1] + '%s' % six.ensure_str(six.unichr(176))
						msnweather['Hightemp4'] = '%s%s' % (hi4weather, degreetype)
					msnweather['Temp4'] = '%s / %s' % (hi4weather, low4weather)
					msnweather['Picon4'] = line.split('skycodeday')[5].split('"')[1]
					msnweather['Date4'] = line.split('date')[6].split('"')[1].split('-')[2].strip() + '.' + line.split('date')[6].split('"')[1].split('-')[1].strip() + '.' + line.split('date')[6].split('"')[1].split('-')[0].strip()
					msnweather['Shortdate4'] = line.split('shortday')[6].split('"')[1] + ' ' + line.split('date')[6].split('"')[1].split('-')[2].strip()
					msnweather['Day4'] = line.split(' day')[6].split('"')[1]
					msnweather['Shortday4'] = line.split('shortday')[6].split('"')[1]
					msnweather['Skytext4'] = line.split('skytextday')[5].split('"')[1]
					msnweather['Precip4'] = line.split('precip')[5].split('"')[1] + ' %s' % six.ensure_str(six.unichr(37))
			except:
				pass

		if self.type == self.VFD:
			try:
				weze = msnweather['Skytext'].split(' ')[1]
			except:
				weze = msnweather['Skytext']
			info = msnweather['Temp'] + ' ' + weze
		if self.type == self.DATE:
			info = msnweather['Date']
		if self.type == self.SHORTDATE:
			info = msnweather['Shortdate']
		if self.type == self.DAY:
			info = msnweather['Day']
		if self.type == self.JDAY:
			info = msnweather['Julianday']
		if self.type == self.SHORTDAY:
			info = msnweather['Shortday']
		if self.type == self.LOCATION:
			info = msnweather['Location']
		if self.type == self.TIMEZONE:
			info = msnweather['Timezone']
		if self.type == self.LATITUDE:
			info = msnweather['Latitude']
		if self.type == self.LONGITUDE:
			info = msnweather['Longitude']
# Astro
		if self.type == self.SUNRISE:
			info = msnweather['Sunrise']
		if self.type == self.SUNSET:
			info = msnweather['Sunset']
		if self.type == self.SUNCULMINATION:
			info = msnweather['Solstice']
		if self.type == self.MERCURYRISE:
			info = msnweather['Mercuryrise']
		if self.type == self.MERCURYSET:
			info = msnweather['Mercuryset']
		if self.type == self.MERCURYCULMINATION:
			info = msnweather['Mercuryculmination']
		if self.type == self.MERCURYAZIMUTH:
			info = msnweather['Mercuryazimuth']
		if self.type == self.VENUSRISE:
			info = msnweather['Venusrise']
		if self.type == self.VENUSSET:
			info = msnweather['Venusset']
		if self.type == self.VENUSCULMINATION:
			info = msnweather['Venusculmination']
		if self.type == self.VENUSAZIMUTH:
			info = msnweather['Venusazimuth']
		if self.type == self.MARSRISE:
			info = msnweather['Marsrise']
		if self.type == self.MARSSET:
			info = msnweather['Marsset']
		if self.type == self.MARSCULMINATION:
			info = msnweather['Marsculmination']
		if self.type == self.MARSAZIMUTH:
			info = msnweather['Marsazimuth']
		if self.type == self.JUPITERRISE:
			info = msnweather['Jupiterrise']
		if self.type == self.JUPITERSET:
			info = msnweather['Jupiterset']
		if self.type == self.JUPITERCULMINATION:
			info = msnweather['Jupiterculmination']
		if self.type == self.JUPITERAZIMUTH:
			info = msnweather['Jupiterazimuth']
		if self.type == self.SATURNRISE:
			info = msnweather['Saturnrise']
		if self.type == self.SATURNSET:
			info = msnweather['Saturnset']
		if self.type == self.SATURNCULMINATION:
			info = msnweather['Saturnculmination']
		if self.type == self.SATURNAZIMUTH:
			info = msnweather['Saturnazimuth']
		if self.type == self.URANUSRISE:
			info = msnweather['Uranusrise']
		if self.type == self.URANUSSET:
			info = msnweather['Uranusset']
		if self.type == self.URANUSCULMINATION:
			info = msnweather['Uranusculmination']
		if self.type == self.URANUSAZIMUTH:
			info = msnweather['Uranusazimuth']
		if self.type == self.NEPTUNERISE:
			info = msnweather['Neptunerise']
		if self.type == self.NEPTUNESET:
			info = msnweather['Neptuneset']
		if self.type == self.NEPTUNECULMINATION:
			info = msnweather['Neptuneculmination']
		if self.type == self.NEPTUNEAZIMUTH:
			info = msnweather['Neptuneazimuth']
		if self.type == self.MOONRISE:
			info = msnweather['Moonrise']
		if self.type == self.MOONSET:
			info = msnweather['Moonset']
		if self.type == self.MOONCULMINATION:
			info = msnweather['Moonculmination']
		if self.type == self.MOONDIST:
			info = msnweather['Moondist']
		if self.type == self.MOONAZIMUTH:
			info = msnweather['Moonazimuth']
		if self.type == self.MOONPHASE:
			info = msnweather['Moonphase']
		if self.type == self.MOONLIGHT:
			info = msnweather['Moonlight']
		if self.type == self.MOONPICON:
			info = msnweather['PiconMoon']
# Today
		if self.type == self.TEMP:
			info = msnweather['Temp']
		if self.type == self.PICON:
			info = msnweather['Picon']
		if self.type == self.SKYTEXT:
			info = msnweather['Skytext']
		if self.type == self.FEELSLIKE:
			info = msnweather['Feelslike']
		if self.type == self.HUMIDITY:
			info = msnweather['Humidity']
		if self.type == self.WIND:
			info = msnweather['Wind']
		if self.type == self.WINDSPEED:
			info = msnweather['Windspeed']
# Day 0
		if self.type == self.DATE0:
			info = msnweather['Date0']
		if self.type == self.SHORTDATE0:
			info = msnweather['Shortdate0']
		if self.type == self.DAY0:
			info = msnweather['Day0']
		if self.type == self.SHORTDAY0:
			info = msnweather['Shortday0']
		if self.type == self.TEMP0:
			info = msnweather['Temp0']
		if self.type == self.LOWTEMP0:
			info = msnweather['Lowtemp0']
		if self.type == self.HIGHTEMP0:
			info = msnweather['Hightemp0']
		if self.type == self.PICON0:
			info = msnweather['Picon0']
		if self.type == self.SKYTEXT0:
			info = msnweather['Skytext0']
		if self.type == self.PRECIP0:
			info = msnweather['Precip0']
# Day 1
		if self.type == self.DATE1:
			info = msnweather['Date1']
		if self.type == self.SHORTDATE1:
			info = msnweather['Shortdate1']
		if self.type == self.DAY1:
			info = msnweather['Day1']
		if self.type == self.SHORTDAY1:
			info = msnweather['Shortday1']
		if self.type == self.TEMP1:
			info = msnweather['Temp1']
		if self.type == self.LOWTEMP1:
			info = msnweather['Lowtemp1']
		if self.type == self.HIGHTEMP1:
			info = msnweather['Hightemp1']
		if self.type == self.PICON1:
			info = msnweather['Picon1']
		if self.type == self.SKYTEXT1:
			info = msnweather['Skytext1']
		if self.type == self.PRECIP1:
			info = msnweather['Precip1']
# Day 2
		if self.type == self.DATE2:
			info = msnweather['Date2']
		if self.type == self.SHORTDATE2:
			info = msnweather['Shortdate2']
		if self.type == self.DAY2:
			info = msnweather['Day2']
		if self.type == self.SHORTDAY2:
			info = msnweather['Shortday2']
		if self.type == self.TEMP2:
			info = msnweather['Temp2']
		if self.type == self.LOWTEMP2:
			info = msnweather['Lowtemp2']
		if self.type == self.HIGHTEMP2:
			info = msnweather['Hightemp2']
		if self.type == self.PICON2:
			info = msnweather['Picon2']
		if self.type == self.SKYTEXT2:
			info = msnweather['Skytext2']
		if self.type == self.PRECIP2:
			info = msnweather['Precip2']
# Day 3
		if self.type == self.DATE3:
			info = msnweather['Date3']
		if self.type == self.SHORTDATE3:
			info = msnweather['Shortdate3']
		if self.type == self.DAY3:
			info = msnweather['Day3']
		if self.type == self.SHORTDAY3:
			info = msnweather['Shortday3']
		if self.type == self.TEMP3:
			info = msnweather['Temp3']
		if self.type == self.LOWTEMP3:
			info = msnweather['Lowtemp3']
		if self.type == self.HIGHTEMP3:
			info = msnweather['Hightemp3']
		if self.type == self.PICON3:
			info = msnweather['Picon3']
		if self.type == self.SKYTEXT3:
			info = msnweather['Skytext3']
		if self.type == self.PRECIP3:
			info = msnweather['Precip3']
# Day 4
		if self.type == self.DATE4:
			info = msnweather['Date4']
		if self.type == self.SHORTDATE4:
			info = msnweather['Shortdate4']
		if self.type == self.DAY4:
			info = msnweather['Day4']
		if self.type == self.SHORTDAY4:
			info = msnweather['Shortday4']
		if self.type == self.TEMP4:
			info = msnweather['Temp4']
		if self.type == self.LOWTEMP4:
			info = msnweather['Lowtemp4']
		if self.type == self.HIGHTEMP4:
			info = msnweather['Hightemp4']
		if self.type == self.PICON4:
			info = msnweather['Picon4']
		if self.type == self.SKYTEXT4:
			info = msnweather['Skytext4']
		if self.type == self.PRECIP4:
			info = msnweather['Precip4']
		return info
	text = property(getText)

	def changed(self, what):
		Converter.changed(self, (self.CHANGED_POLL,))
