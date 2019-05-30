#!/usr/bin/env python3

from ircutils3 import bot
from ircutils3 import format as msgformat
from sys import stdin, stderr, stdout
from time import sleep
from getpass import getpass
import re
from shadow_library import grep_shadow_pdfs, get_pdf_filename
from utility_scripts.receiptprintercmds import escpos, asciiart, stdout, stderr

class bs_irc_user(bot.SimpleBot):

	def on_channel_message(self, event):
		user = ((event.prefix).split("!"))[0]
		#print("Answer:",  asciiart['flames1'], event.message, file=stdout)
		if "#shadowlibrary" in event.message.lower():
			selection = re.findall(r'\d\d\d', event.message)
			filename = get_pdf_filename(selection) # get name of pdf
			print('I selected this PDF for you:', filename, asciiart['flames1'], file=stdout)
			grep_shadow_pdfs(selection)
		else:
			print(user+":", event.message, asciiart['flames1'], file=stdout)
		if "bye" in event.message.lower() or "goodbye" in event.message.lower():
			print(escpos['reverse_print_on'], "YOU HAVE LEFT THE CHANNEL", escpos['reverse_print_off'],  asciiart['space'],  file=stdout)
			self.part_channel('#beyondsocial', "Bye. See you soon")
			self.disconnect(self)
			return # exit the function
		say = getpass(prompt="") # hack: to get only what user types at this moment
		# will not echo what s/he is printing atm
		print("You:", say,asciiart['flames1'], file=stdout)
		self.send_message(event.target, say)
		
	def on_join(self, event):
		if event.source == self.nickname:
			message = msgformat.bold("/me is here")
			message = msgformat.color(message, msgformat.RED)
			self.send_message(event.target, message)
			print(escpos['reverse_print_on'],"You are now chatting to ELAINE. Wait for her to start chatting with you", escpos['reverse_print_off'], asciiart['flames1'], file=stdout)

	# Create an instance of the bot
	# We set the bot's nickname here
def irc(username):
	bs_user = bs_irc_user(username)
		# Let's connect to the host n channel
	print("Wait a few moments while the connection is being established", asciiart['flames1'], file=stdout)
	bs_user.connect("irc.freenode.com", channel=["#beyondsocial"])
		# Start running the bot
	bs_user.start()

#irc("bs_user")
