# Most of the code comes from  Twisted Matrix Laboratories. Their imports and what not.
# All the kitten actions belong to me I'm pretty sure. I could be wrong.
# To run the script: $ python ircLogBot.py <file>

# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, ssl
from twisted.python import log

# system imports
import cookielib
import random
import re
import time, sys, unicodedata, os
import urllib2

#Module imports
sys.path.append(r'./modules')
import weather

##### Global Variables #####

command = '*'
movieInfo = []
bitcoinInfo = []
coinInfo = []

##### Applications #####

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
	nickname ='Sol' # nickname

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
		self.join("#wetfish")
	 
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
			f = open("catText/catNoise.txt", "r")
			data = f.readlines()
			num_lines = sum(1 for line in data) - 1
			msg = data[random.randint(1, num_lines)].rstrip('\n')
			self.msg(channel, msg)
			self.logger.log("%s <%s> %s" % (channel, self.nickname, msg))
			f.close()
			return

		elif msg.startswith(command + "forceplay"):
			f = open("catText/catAction.txt","r")
			data = f.readlines()
			num_lines = sum(1 for line in data) - 1
			action = data[random.randint(1, num_lines)].rstrip('\n')
			self.describe(channel, action)
			self.logger.log("%s %s %s" % (channel, self.nickname, msg))
			return

		elif msg.startswith(command + "forceheil"):
			msg = 'Sieg Meow'
			self.msg(channel, msg)
			self.logger.log("%s <%s> %s" % (channel, self.nickname, msg))
			return

	##### Function Calls #####

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

		elif msg.startswith(command + "btce"):
			CoinEx()
			msg = "%s" % (coinInfo)
			del coinInfo[:]
			self.msg(channel, msg)
			self.logger.log("%s <%s> %s" % (channel, user, msg))
			return

		elif msg.startswith(command + "8ball"):
			f = open("catText/eightBall.txt","r")
			data = f.readlines()
			num_lines = sum(1 for line in data) - 1
			msg = data[random.randint(1, num_lines)].rstrip('\n')
			self.msg(channel, msg)
			self.logger.log("%s <%s> %s" % (channel, self.nickname, msg))
			f.close()
			return


		elif msg.startswith(command + 'help'):
			channel = user
			f = open("catText/catHelp.txt", "r")
			data = f.readlines()
			for line in data:
				self.msg(user, line)
			f.close()
			return


	#### Regular speaking

		elif msg.startswith(msg) and user != "Denice" and random.random() < 0.010:
			f = open("catText/catNoise.txt", "r")
			data = f.readlines()
			num_lines = sum(1 for line in data) - 1
			msg = data[random.randint(1, num_lines)].rstrip('\n')
			self.msg(channel, msg)
			self.logger.log("%s <%s> %s" % (channel, self.nickname, msg))
			f.close()
			return

		elif msg.startswith(msg) and user != "Denice" and random.random() > 0.985:
			f = open("catText/catAction.txt","r")
			data = f.readlines()
			num_lines = sum(1 for line in data) - 1
			action = data[random.randint(1, num_lines)].rstrip('\n')
			self.describe(channel, action)
			self.logger.log("%s <%s> %s" % (channel, self.nickname, msg))
			f.close()
			return


                elif re.search(r'\b(hi|hello|hey|sup|howdy|good ?morning|good ?night)\b', msg, re.I) and re.search(r'%s' % self.nickname, msg, re.I):
                        f = open("catText/catNoise.txt","r")
			data = f.readlines()
                        num_lines = sum(1 for line in data) - 1
                        msg = data[random.randint(1, num_lines)].rstrip('\n')
                        self.msg(channel, msg)
                        self.logger.log("%s <%s> %s" % (channel, self.nickname, msg))
                        f.close()
                        return

		elif re.search(r'\b(pomf|furaffinity|furry|pelvis|climax|kawaii|silicone|circumsision|sheathe|arse|spew|vulpine|fart|tentacle)\b|:3', msg, re.I):
			f = open("catText/catYiffed.txt","r")
                        data = f.readlines()
                        num_lines = sum(1 for line in data) - 1
                        interact = data[random.randint(1, num_lines)].rstrip('\n')
                        self.describe(channel, interact.format(user))
                        f.close()
                        return



	def alterCollidedNick(self, nickname):
		return nickname+'2'

	def action(self, user, channel, msg):
		"""This will get called when the bot sees someone do an action."""
		user = user.split('!', 1)[0]
		self.logger.log("* %s %s" % (user, msg))

		if re.search(r'nigga|poop|kick|\bhit|punch|stab|kill|hurt|bite|spank|fuck|penetrate|finger', msg, re.I) and re.search(r'%s' % self.nickname, msg, re.I):
                        self.describe(channel, 'yowls and scratches %s' % (user))
			return

		elif re.search(r'pet|pat|scratch|nuzzle|rub|stroke|cuddle', msg, re.I) and re.search(r'%s' % self.nickname, msg, re.I):
			f = open("catText/catInteract.txt","r")
			data = f.readlines()
			num_lines = sum(1 for line in data) - 1
			interact = data[random.randint(1, num_lines)].rstrip('\n')
			self.describe(channel, interact %(user))
			f.close()
			return

		elif re.search(r'feeds|food|fed|chicken|fish', msg, re.I) and re.search(r'%s' % self.nickname, msg, re.I):
			f = open("catText/catEat.txt","r")
			data = f.readlines()
			num_lines = sum(1 for line in data) - 1
			fed = data[random.randint(1, num_lines)].rstrip('\n')
			self.describe(channel, fed)
			f.close()
			return

		elif re.search(r'sie|xie|hir|pomf|furaffinity|furry|mounts|pelvis|climax|breast|kawaii|silicone|circumsision|sheathe|arse|cum|spew|penis|knot|vulpine|fart|tentacle|cock|butt|ass|yiff', msg, re.I) and  re.search(r'%s' % self.nickname, msg, re.I):
			f = open("catText/catYiffed.txt","r")
			data = f.readlines()
			num_lines = sum(1 for line in data) - 1
			interact = data[random.randint(1, num_lines)].rstrip('\n')
			self.describe(channel, interact.format(user))
			f.close()
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
	hostname = 'irc.wetfish.net' # irc-server-hostname
	port = 6697	#port
	reactor.connectSSL(hostname, port, f, ssl.ClientContextFactory())
	 
	# run bot
	reactor.run()
