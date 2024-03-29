#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import InfoScreen
import pygame, logging, locale
from datetime import datetime
from .helper.fontsurface import FontSurface
from lxml import etree
from .helper.textrect import render_textrect, TextRectException

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
		events = []
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
					events.append((date, title))
				except IndexError:
					self.log(logging.ERROR, "XPath did not return anything.")
					continue
		except (IOError, etree.XMLSyntaxError) as e:
			self.log(logging.ERROR, e)
			return []
		return events

	def show(self):
		"""Shows upcoming events."""
		# fonts
		headlineFont = pygame.font.Font("fonts/blue_highway_bd.ttf",
			self.relH(.1))
		stdFont = pygame.font.Font("fonts/DejaVuSansMono.ttf",
			self.relH(.06))

		# colors used
		black = (0, 0, 0)
		white = (255, 255, 255)

		# black screen
		self.screen.fill(black)

		# event loop
		currentY = self.relH(.2)
		events = self.getEvents()
		for date, title in events:
			# parse date
			locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
			try:
				date = datetime.strptime(date.encode("utf-8"), "%H:%M, %d. %b. %Y")
			except ValueError:
				date = datetime.strptime(date.encode("utf-8"), "%H:%M, %d. %b %Y")
			locale.setlocale(locale.LC_TIME, "")
			# render one event at a time with a bullet point
			eventStr = u"\u00BB %s: %s" % (date.strftime("%d.%m. %H:%M"), title)

			# this only acts as a container here
			event = FontSurface(self.screen, "", stdFont)
			scrRect = self.screen.get_rect()
			surface = render_textrect(eventStr, stdFont, scrRect, white, black)
			event.surface = surface
			event.pos.x = self.relW(.007)
			event.pos.y = currentY
			event.blit()
			currentY += event.pos.height * 2

		# no events available
		if len(events) == 0:
			self.log(logging.DEBUG, "No events found. Skipping.")
			return
			"""
			msgStr = "Momentan sind keine Termine geplant."
			msg = FontSurface(self.screen, msgStr, stdFont)
			msg.centerX()
			msg.centerY()
			msg.blit()
			"""

		# headline
		headline = FontSurface(self.screen, u"Nächste Termine", headlineFont)
		headline.centerX()
		headline.pos.y = 0
		headline.blit()

		# show it
		pygame.display.flip()
		# nothing else to do
		self.wait(self.displayTime)

