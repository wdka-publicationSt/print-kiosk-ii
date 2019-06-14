#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import stdin, stderr, stdout
from time import sleep

import slixmpp
import ssl

from argparse import ArgumentParser
import logging

import asyncio, aiohttp

class MUCBot(slixmpp.ClientXMPP):
	"""
	A xmpp bot that will print all messages to the stdout.
	"""

	def __init__(self, jid, password, room, nick):
		slixmpp.ClientXMPP.__init__(self, jid, password)

		self.room = room
		self.nick = nick

		self.add_event_handler("session_start", self.start)
		self.add_event_handler("groupchat_message", self.muc_message)

	
	def start(self, event):
		print("Wait a few moments while the connection is being established ...", file=stdout)

		self.get_roster()
		self.send_presence()

		# https://xmpp.org/extensions/xep-0045.html
		self.plugin['xep_0045'].join_muc(self.room,
										 self.nick,
										 # If a room password is needed, use:
										 # password=the_room_password,
										 wait=True)
		sleep(2)
		print("Done!", file=stdout)
		sleep(1)
		print("You're now in the Shadow Library chat room.", file=stdout)

		# Send a message to the room
		self.send_message(mto=self.room, mbody='Hello!', mtype='groupchat')

	def muc_message(self, msg):
		if msg['mucnick'] != xmpp.nick:
			print(msg['body'], file=stdout)

		# The script hangs here, untill a message is send from the terminal
		reply = stdin.readlines()
		if reply:
			self.send_message(mto=self.room, mbody=reply, mtype='groupchat')


if __name__ == '__main__':
	# Setup the command line arguments.
	parser = ArgumentParser()

	# output verbosity options.
	parser.add_argument("-q", "--quiet", help="set logging to ERROR",
						action="store_const", dest="loglevel",
						const=logging.ERROR, default=logging.INFO)
	parser.add_argument("-d", "--debug", help="set logging to DEBUG",
						action="store_const", dest="loglevel",
						const=logging.DEBUG, default=logging.INFO)

	# JID and password options.
	parser.add_argument("-j", "--jid", dest="jid",
						help="JID to use")
	parser.add_argument("-p", "--password", dest="password",
						help="password to use")
	parser.add_argument("-r", "--room", dest="room",
						help="MUC room to join")
	parser.add_argument("-n", "--nick", dest="nick",
						help="MUC nickname")

	args = parser.parse_args()

	# Setup logging.
	logging.basicConfig(level=args.loglevel,
						format='%(levelname)-8s %(message)s')

	# if args.jid is None:
	# 	args.jid = input("XMPP address: ")
	# if args.password is None:
	# 	args.password = getpass("Password: ")
	# if args.room is None:
	# 	args.room = input("MUC room: ")
	# if args.nick is None:
	# 	args.nick = input("MUC nickname: ")
	jid="bs@virtualprivateserver.space"
	password="shadow"
	room="ebini@muc.virtualprivateserver.space"
	nick="Shadow Library guest"

	# Setup the MUCBot and register plugins. Note that while plugins may
	# have interdependencies, the order in which you register them does
	# not matter.
	xmpp = MUCBot(jid, password, room, nick)

	# xmpp = MUCBot(args.jid, args.password, args.room, args.nick)
	xmpp.register_plugin('xep_0030') # Service Discovery
	xmpp.register_plugin('xep_0045') # Multi-User Chat
	xmpp.register_plugin('xep_0199') # XMPP Ping
	xmpp.register_plugin('xep_0066') # Process URI's (files, images)

	# Connect to the XMPP server and start processing XMPP stanzas.
	xmpp.connect()
	xmpp.process()
