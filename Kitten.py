# Most of the code comes from  Twisted Matrix Laboratories. Their imports and what not.
#All the kitten actions belong to me I'm pretty sure. I could be wrong.
# To run the script: $ python ircLogBot.py <file>

# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, ssl
from twisted.python import log

# system imports
import cookielib
import random
import re
import time, sys, unicodedata
import urllib2

##### Global Variables #####

command = '&'
CAT_INTERACT = ['flops onto floor while purring and nuzzling into %s', 'lays on the floor with her belly up for %s',
	'loves being scratched by %s', 'meows at %s', 'shoves face into %s\'s hand', 'rolls on floor in front of %s',
	'licks %s\'s hand', 'meows at %s', 'swishes tail at %s', 'kneads %s\'s leg while purring', 'cuddles up in %s\'s lap',
	'grabs %s\'s hand with its paws when they stop petting', 'meows at %s for more', 'loves %s',
	'thinks %s is the best human in the world', 'doesnt want the love from %s to stop', 'raises her butt as %s scratches it',
	'follows %s afterwards', 'meows at %s for food after', 'gets into a meowing contest with %s', 'doesnt leave %s\'s side',
	'wants to be friends with %s forever', 'holds hiddent contempt for %s but doesnt mind as long as theres food',
	'wants to take %s out for a real fancy feast', '\'s eyes turn black as she stares into the soul and melts the mind of %s while murmurring unintelligble R\'lyehian',
	'knows they lord over %s in every way']
CAT_EAT = ['hungrily chews the food', 'sniffs the food and meows', 'licks the food', 'chews the food some before spitting it out',
			'eats like a king', 'loves food', 'doesnt even know this food is bad and loves it', 'wishes there was more fancy feast','stares at the food and meows at it',
			'flips the bowl of food over and meows for more', 'slowly eats the meal a little at a time', 'hungrily chomps the meal down']
EIGHT_BALL =["Very doubtful", "You may rely on it", "Outlook not so good", "Without a doubt", "Outlook good", "It is decidedly so",
		"Yes", "Cannot predict now", "Better not tell you now", "Signs point to yes", "Yes, definitely", "Ask again later",
		"My sources say no", "Don\'t count on it", "As I see it, yes", "Most likely", "Reply hazy, try again", "My reply is no",
		"Concentrate and ask again"]
movieInfo = []
bitcoinInfo = []
coinInfo = []

##### Applications #####

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
	if not zmw:
		sections = "Oh no! That place doesn't exist!"

def Movie(movieName):
	cookieJar = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))

	url = "http://www.imdbapi.com/?t=" + movieName
	request = urllib2.Request(url)
	page = opener.open(request)

	# This is one big string
	rawdata = page.read()

	title = re.search('"Title":"(.+?)"', rawdata)
	if title:
		titleOut = title.group(1)
		movieInfo.insert(0, "Title: " + titleOut)
	year = re.search('"Year":"(.+?)"', rawdata)
	if year:
		yearOut = year.group(1)
		movieInfo.insert(1, "Year: " + yearOut)
	time = re.search('"Runtime":"(.+?)"', rawdata)
	if time:
		timeOut = time.group(1)
		movieInfo.insert(2, "Runtime: " + timeOut)
	rate = re.search('"imdbRating":"(.+?)"', rawdata)
	if rate:
		rateOut = rate.group(1)
		movieInfo.insert(3, "Rating: "+ rateOut)
	error = re.search('"Error":"(.+?)"', rawdata)
	if error:
		errorOut = error.group(1)
		movieInfo.insert(4, errorOut)

	return movieInfo


def Bitcoin():
	cookieJar = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))

	url = "http://data.mtgox.com/api/2/BTCUSD/money/ticker"
	request = urllib2.Request(url)
	page = opener.open(request)

	# This is one big string
	rawdata = page.read()

	last = re.search('"last":{"value":"(.+?)"', rawdata)
	if last:
		lastOut = last.group(1)
		bitcoinInfo.insert(0, "Last: " + lastOut)
	buy = re.search('"buy":{"value":"(.+?)"', rawdata)
	if buy:
		buyOut = buy.group(1)
		bitcoinInfo.insert(1, "Buy: " + buyOut)
	sell = re.search('"sell":{"value":"(.+?)"', rawdata)
	if sell:
		sellOut = sell.group(1)
		bitcoinInfo.insert(2, "Sell: " + sellOut)
	high = re.search('"high":{"value":"(.+?)"', rawdata)
	if high:
		highOut = high.group(1)
		bitcoinInfo.insert(3, "High: " + highOut)
	low = re.search('"low":{"value":"(.+?)"', rawdata)
	if low:
		lowOut = low.group(1)
		bitcoinInfo.insert(4, "Low: " + lowOut)

	return bitcoinInfo

def CoinEx():
	cookieJar = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))

	url = "https://btc-e.com/api/2/btc_usd/ticker"
	request = urllib2.Request(url)
	page = opener.open(request)

	# This is one big string
	rawdata = page.read()

	last = re.search('"last":(.+?),"', rawdata)
	if last:
		lastOut = last.group(1)
		coinInfo.insert(0, "Last:" + lastOut)
	buy = re.search('"buy":(.+?),"', rawdata)
	if buy:
		buyOut = buy.group(1)
		coinInfo.insert(1, "Buy:" + buyOut)
	sell = re.search('"sell":(.+?),"', rawdata)
	if sell:
		sellOut = sell.group(1)
		coinInfo.insert(2, "Sell:" + sellOut)
	high = re.search('"high":(.+?),"', rawdata)
	if high:
		highOut = high.group(1)
		coinInfo.insert(3, "High:" + highOut)
	low = re.search('"low":(.+?),"', rawdata)
	if low:
		lowOut = low.group(1)
		coinInfo.insert(4, "Low:" + lowOut)

	return coinInfo

##### Bot Framework #####

class MessageLogger:
	# An independent logger class (because separation of application and protocol logic is a good thing).
	def __init__(self, file):
		self.file = file
	 
	def log(self, message):
		"""Write a message to the file."""
		timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
		self.file.write('%s %s\n' % (timestamp, message))
		self.file.flush()
	 
	def close(self):
		self.file.close()
 
 
class LogBot(irc.IRCClient):
	nickname = 'Kitten' # nickname

	def connectionMade(self):
		irc.IRCClient.connectionMade(self)
		print "connectionMade"
		self.logger = MessageLogger(open(self.factory.filename, "a"))
		self.logger.log("[connected at %s]" %
						time.asctime(time.localtime(time.time())))
	 
	def connectionLost(self, reason):
		irc.IRCClient.connectionLost(self, reason)
		self.logger.log("[disconnected at %s]" %
						time.asctime(time.localtime(time.time())))
		self.logger.close()
	 
	# callbacks for events
	 
	def signedOn(self):
		"""Called when bot has succesfully signed on to server."""
		self.join(self.factory.channel)
	 
	def joined(self, channel):
		"""This will get called when the bot joins the channel."""
		self.logger.log("[I have joined %s]" % self.factory.channel)

	 
	def privmsg(self, user, channel, msg):
		"""This will get called when the bot receives a message."""
		user = user.split('!', 1)[0]
		self.logger.log("%s <%s> %s" % (channel, user, msg))

		# Check to see if they're sending me a private message
		if channel == self.nickname:
			msg = "Meow"
			self.msg(user, msg)
			return
		 
		##Kitten speech stuff here.

		if re.search(r'slut|slutty|whore', msg, re.I) and re.search(r'%s' % self.nickname, msg, re.I):
			pride = 'scratches %s'
			self.describe(channel, pride %(user))
			return

		elif msg.startswith(command + "forcemeow"):
			msg = CAT_NOISE[random.randint(0, len(CAT_NOISE))]
			self.msg(channel, msg)
			self.logger.log("%s <%s> %s" % (channel, self.nickname, msg))
			return

		elif msg.startswith(command + "forceplay"):
			action = CAT_ACTION[random.randint(0, len(CAT_ACTION))]
			msg = self.describe(channel, action)
			self.msg(channel, msg)
			self.logger.log("%s %s %s" % (channel, self.nickname, msg))
			return

		elif msg.startswith(command + "forceheil"):
			msg = 'Sieg Meow'
			self.msg(channel, msg)
			self.logger.log("%s <%s> %s" % (channel, self.nickname, msg))
			return

	##### Function Calls #####

		elif msg.startswith(command + "weather"):
			numbers = re.search('&weather (.+)', msg)
			if numbers:
				areaCode = numbers.group(1)
				areaCode = areaCode.replace(' ', '+')
				Weather(areaCode)
			msg = "%s" % (sections)
			self.msg(channel, msg)
			self.logger.log("%s <%s> %s" % (channel, user, msg))
			return

		elif msg.startswith(command + "movie"):
			movieTitle = re.search('&movie (.+)', msg)
			if movieTitle:
				movieName = movieTitle.group(1)
				movieName = movieName.replace(' ','+')
				Movie(movieName)
			msg = "%s" % (movieInfo)
			del movieInfo[:]
			self.msg(channel, msg)
			self.logger.log("%s <%s> %s" % (channel, user, msg))
			return

		elif msg.startswith(command + "mtgox"):
			Bitcoin()
			msg = "%s" % (bitcoinInfo)
			del bitcoinInfo[:]
			self.msg(channel, msg)
			self.logger.log("%s <%s> %s" % (channel, user, msg))
			return

		elif msg.startswith(command + "btce"):
			CoinEx()
			msg = "%s" % (coinInfo)
			del coinInfo[:]
			self.msg(channel, msg)
			self.logger.log("%s <%s> %s" % (channel, user, msg))
			return
		
		elif msg.startswith(command + "8ball"):
			msg = EIGHT_BALL[random.randint(0, len(EIGHT_BALL) - 1)]
			self.msg(channel, msg)
			self.logger.log("%s <%s> %s" % (channel, self.nickname, msg))
			return


		elif msg.startswith(command + 'help'):
			channel = user
			msg = "&weather (ex. &weather 12345, &weather NYC, NY), &movie <title>, &8ball, &mtgox, &btce"
			self.msg(user, msg)

	#### Regular speaking

		elif msg.startswith(msg) and user != "Denice" and random.random() < 0.015:
			f.open("catText/catNoise.txt", "r")
			data = f.readlines()
			num_lines = sum(1 for line in data) - 1
			msg = data[random.randint(1, num_lines)]
			self.msg(channel, msg)
			self.logger.log("%s <%s> %s" % (channel, self.nickname, msg))
			f.close()
			return

		elif msg.startswith(msg) and user != "Denice" and random.random() > 0.985:
			f.open("catText/catAction.txt","r")
			data = f.readlines()
			num_lines = sum(1 for line in data) - 1
			action = data[random.randint(1, num_lines)]
			msg = self.describe(channel, action)
			self.msg(channel, msg)
			self.logger.log("%s <%s> %s" % (channel, self.nickname, msg))
			f.close()
			return
	 
	def alterCollidedNick(self, nickname):
		return nickname+'2'
	 
	def action(self, user, channel, msg):
		"""This will get called when the bot sees someone do an action."""
		user = user.split('!', 1)[0]
		self.logger.log("* %s %s" % (user, msg))
		
		if re.search(r'pet|pat|scratch|nuzzle|rub|stroke', msg, re.I) and re.search(r'%s' % self.nickname, msg, re.I):
			interact = CAT_INTERACT[random.randint(0, len(CAT_INTERACT)-1)]
			self.describe(channel, interact %(user))
			return

		elif re.search(r'feeds|food|fed|chicken', msg, re.I) and re.search(r'%s' % self.nickname, msg, re.I):
			fed = CAT_EAT[random.randint(0, len(CAT_EAT)-1)]
			self.describe(channel, fed)
			return

		elif re.search(r'poop|kick|hit|punch|stab|throw|kill|hurt|bite|spank|fuck|penetrate|finger', msg, re.I) and re.search(r'%s' % self.nickname, msg, re.I):
			self.describe(channel, 'yowls and scratches %s' % (user))
			return
	 
	# irc callbacks
	 
	def irc_NICK(self, prefix, params):
		"""Called when an IRC user changes their nickname."""
		old_nick = prefix.split('!')[0]
		new_nick = params[0]
		self.logger.log("%s is now known as %s" % (old_nick, new_nick))
	 
	 
	# For fun, override the method that determines how a nickname is changed on
	# collisions. The default method appends an underscore.
	def alterCollidedNick(self, nickname):
		"""
		Generate an altered version of a nickname that caused a collision in an
		effort to create an unused related name for subsequent registration.
		"""
		return nickname + '^'

class LogBotFactory(protocol.ClientFactory):
	"""
	A factory for LogBots. 
	A new protocol instance will be created each time we connect to the server.
	"""
	protocol = LogBot
	 
	def __init__(self, filename):
		self.channel = 'TestingTests' #channel
		self.filename = filename
	 
	def clientConnectionLost(self, connector, reason):
		"""If we get disconnected, reconnect to server."""
		connector.connect()
	 
	def clientConnectionFailed(self, connector, reason):
		print "connection failed:", reason
		reactor.stop()
 
 
if __name__ == '__main__':
	# initialize logging
	log.startLogging(sys.stdout)

	# create factory protocol and application
	f = LogBotFactory(sys.argv[1])
	#f = "wordshere.txt"
	 
	# connect factory to this host and port
	hostname = 'localhost' # irc-server-hostname
	port = 6697	#port
	reactor.connectSSL(hostname, port, f, ssl.ClientContextFactory())
	 
	# run bot
	reactor.run()
