#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging, pygame
from datetime import datetime, timedelta

class InfoScreen(object):
	"""Basic info screen that must be extended by the individual screen.
	See screens/clock.py for a demo.

	Keyword arguments:
	screen -- screen to blit on"""
	def __init__(self, screen):
		self.screen = screen
		self.lastCalled = None

	def show(self):
		"""Do your actual screen operations here."""
		raise NotImplementedError

	def showScreen(self):
		"""Wrapper around self.show() that resets state."""
		self.lastCalled = datetime.now()
		self.show()

	def log(self, lvl, msg):
		"""Logs message with given level. Message contains class name.

		Keyword arguments:
		lvl -- logging level (CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET)
		msg -- message to be logged"""
		logging.log(lvl, "%s: %s" % (self.__class__.__name__, msg))

	def wait(self, seconds):
		"""Wait specified timespan."""
		delta = timedelta(seconds=seconds)
		# consider processing time
		if self.lastCalled:
			delta -= datetime.now() - self.lastCalled

		# wait for short timespans to be able to respond to keyboard interrups
		leftMs = int(delta.seconds*1e3 + round(delta.microseconds/1e3))
		self.log(logging.DEBUG, "Wait for %d ms." % leftMs)
		while leftMs > 0:
			if leftMs > 1000:
				pygame.time.wait(1000)
				leftMs -= 1000
			else:
				pygame.time.wait(leftMs)
				leftMs = 0

		self.lastCalled = datetime.now()
