#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import InfoScreen
import pygame, logging, time
from datetime import datetime, timedelta
from .helper.fontsurface import FontSurface
from lxml import etree

class EventScreen(InfoScreen):
	"""Info screen that shows upcoming events."""
	def __init__(self, screen):
		"""Creates the event screen.

		Keyword arguments:
		screen -- screen to display on"""
		super(EventScreen, self).__init__(screen)

		# seconds to display this info screen
		self.displayTime = 15

	def getEvents(self):
		events = {}
		parser = etree.XMLParser(ns_clean=True)
		try:
			tree = etree.parse("http://freieslabor.org/wiki/Spezial:Semantische_Suche/-5B-5BKategorie:Event-5D-5D-20-5B-5BEnddate::-3E2015-2F01-2F28-5D-5D/-3FEventTitle/-3FDatum-23MEDIAWIKI/format%3Dfeed/sort%3DEnddate/order%3Dascending/headers%3Dplain/mainlabel%3D-2D/type%3Datom/title%3DFreies-20Labor-20e.V.-20-2D-20Termine/offset%3D0", parser)
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
		"""Shows date and time."""
		startTime = datetime.now()
		self.log(logging.DEBUG, "Showing date/time.")
		# choose nice font
		headlineFont = pygame.font.Font("fonts/blue_highway_bd.ttf", 70)
		stdFont = pygame.font.Font("fonts/blue_highway_bd.ttf", 30)

		# black screen
		self.screen.fill((0, 0, 0))

		headline = FontSurface(self.screen, u"Nächste Termine", headlineFont)
		headline.centerX()
		headline.pos.y = 0
		headline.blit()

		currentY = 100
		events = self.getEvents()
		for date, title in events.items()[:7]:
			eventStr = u"\u00BB %s: %s" % (date, title)
			event = FontSurface(self.screen, eventStr, stdFont)
			event.pos.x = 10
			event.pos.y = currentY
			event.blit()
			currentY += 100
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

