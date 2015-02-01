#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging, pygame

class InfoScreen(object):
	"""Basic info screen that must be extended by the individual screen.
	See screens/clock.py for a demo.

	Keyword arguments:
	screen -- screen to blit on"""
	def __init__(self, screen):
		self.screen = screen

	def show(self):
		"""Do your actual screen operations here."""
		raise NotImplementedError

	def log(self, lvl, msg):
		"""Logs message with given level. Message contains class name.

		Keyword arguments:
		lvl -- logging level (CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET)
		msg -- message to be logged"""
		logging.log(lvl, "%s: %s" % (self.__class__.__name__, msg))

	def wait(self, seconds):
		"""Wait specified timespan."""
		# use range to be able to respond to keyboard interrupts
		for i in range(seconds):
			pygame.time.wait(1000)
