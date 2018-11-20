#!/usr/bin/env python3

from ircutils3 import bot
from ircutils3 import format as msgformat
from sys import stdin, stderr, stdout
from time import sleep
from getpass import getpass
import re
from shadow_library import grep_shadow_pdfs, get_pdf_filename
from receiptprintercmds import escpos, stdout, stderr

class bs_irc_user(bot.SimpleBot):

	def on_channel_message(self, event):
		user = ((event.prefix).split("!"))[0]
		print(user+":", event.message, '\n\n\n\n\n\n\n', file=stdout)
		print("Answer:",  '\n\n\n\n\n\n\n', event.message, file=stdout)
		if "#shadowlibrary" in event.message.lower():
			selection = re.findall(r'\d\d\d', event.message)
			filename = get_pdf_filename(selection) # get name of pdf
			print('I selected this PDF for you:', filename, '\n\n\n\n\n\n\n', file=stdout)
			grep_shadow_pdfs(selection) # execute script that collects the PDFs, and unites them into one a tmp file: shadow_library.pdf
			# The #shadowlibrary code can only be used once, as it will overwrite the tmp pdf file, each time that it is triggered.
		if "bye" in event.message.lower() or "goodbye" in event.message.lower():
			print("LEAVE channel",  '\n\n\n\n\n\n\n',  file=stdout)
			self.part_channel('#beyondsocial', "Bye. See you soon")
			self.disconnect(self)
			return # exit the function
		say = getpass(prompt="") # hack: to get only what user types at this moment
		# will not echo what s/he is printing atm
		print(say, file=stdout)
		self.send_message(event.target, say)
		
	def on_join(self, event):
		if event.source == self.nickname:
			message = msgformat.bold("/me is here")
			message = msgformat.color(message, msgformat.RED)
			self.send_message(event.target, message)
			print("You are now chatting to ELAINE. Wait for her to start chating with you", '\n\n\n\n\n\n\n', file=stdout)

	# Create an instance of the bot
	# We set the bot's nickname here
def irc(username):
	bs_user = bs_irc_user(username)
		# Let's connect to the host n channel
	print("Wait a few moments while the connection is being established", '\n\n\n\n\n\n\n', file=stdout)
	bs_user.connect("irc.freenode.com", channel=["#beyondsocial"])
		# Start running the bot
	bs_user.start()

# irc("bs_user")
