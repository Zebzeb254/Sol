import cookielib
import urllib2
import re

def Weather(areaCode):
	global sections
	cookieJar = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))

	url = "http://autocomplete.wunderground.com/aq?query=" + areaCode
	request = urllib2.Request(url)
	page = opener.open(request)

	# This is one big string
	rawdata = page.read()
		
	zmw = re.search('"zmw": "(.+?)"', rawdata)
	if zmw:
		zmwAddress = zmw.group(1)
		cookieJar = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))

		url = "http://www.wunderground.com/q/zmw:" + zmwAddress
		request = urllib2.Request(url)
		page = opener.open(request)
		rawdata = page.read()
		# This breaks it up into lines
		lines_of_data = rawdata.split('\n')
		#'<meta name="og:title" content="City, state | 55&deg; | Clear" />
		special_lines = [line for line in lines_of_data if line.find('og:title')>-1]
		# Now we clean up - very crude
		info = special_lines[0].replace('"','').replace('/>','').replace('&deg;','F').split('content=')[1]
		sections = info.split('|')
		return sections
	if not zmw:
		sections = "Oh no! That place doesn't exist!"
		return sections