#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import InfoScreen
import pygame, logging
from datetime import datetime
from .helper.fontsurface import FontSurface
from lxml import etree

class EventScreen(InfoScreen):
	"""Info screen that shows upcoming events."""
	def __init__(self, screen, config):
		"""Creates the event screen.

		Keyword arguments:
		screen -- screen to display on"""
		super(EventScreen, self).__init__(screen)

		self.config = config
		# seconds to display this info screen
		self.displayTime = 15

	def getEvents(self):
		"""Parses event feed and returns events as date-title dict."""
		events = {}
		parser = etree.XMLParser(ns_clean=True)
		try:
			# xml parsing and xpath magic
			tree = etree.parse(self.config["feed"], parser)
			ns = {"ns": "http://www.w3.org/2005/Atom"}
			entries = tree.xpath("//ns:entry", namespaces=ns)
			for entry in entries:
				try:
					title = entry.xpath("ns:title/text()", namespaces=ns)[0]
					date = entry.xpath("ns:summary/text()", namespaces=ns)[0]
					events[date] = title
				except IndexError:
					continue
		except (IOError, etree.XMLSyntaxError):
			return {}
		return events

	def show(self):
		"""Shows upcoming events."""
		# fonts
		headlineFont = pygame.font.Font("fonts/blue_highway_bd.ttf", 70)
		stdFont = pygame.font.Font("fonts/blue_highway_bd.ttf", 30)

		# black screen
		self.screen.fill((0, 0, 0))

		# headline
		headline = FontSurface(self.screen, u"Nächste Termine", headlineFont)
		headline.centerX()
		headline.pos.y = 0
		headline.blit()

		# event loop
		currentY = 100
		events = self.getEvents()
		for date, title in events.items()[:7]:
			# FIXME: needs line wrapping
			eventStr = u"\u00BB %s: %s" % (date, title)
			event = FontSurface(self.screen, eventStr, stdFont)
			event.pos.x = 10
			event.pos.y = currentY
			event.blit()
			currentY += 100

		# no events available
		if len(events) == 0:
			msgStr = "Momentan sind keine Termine geplant."
			msg = FontSurface(self.screen, msgStr, stdFont)
			msg.centerX()
			msg.centerY()
			msg.blit()

		# show it
		pygame.display.flip()
		# nothing else to do
		self.wait(self.displayTime)

