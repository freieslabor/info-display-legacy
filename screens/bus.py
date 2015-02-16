#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import InfoScreen
import pygame, logging
from .helper.fontsurface import FontSurface
from lxml import etree
from datetime import datetime, timedelta
from .helper.textrect import render_textrect, TextRectException

class BusScreen(InfoScreen):
	"""Bus screen that shows next departures."""
	def __init__(self, screen, config):
		"""Creates the bus screen.

		Keyword arguments:
		screen -- screen to display on"""
		super(BusScreen, self).__init__(screen)

		self.config = config
		# seconds to display this info screen
		self.displayTime = 15
		self.buses = []
		self.lastUpdate = datetime(1970, 1, 1)

	def getBuses(self):
		"""Parses bus feed and returns bus departures (queries if last update
		is older than 30 min otherwise cached results)."""
		if self.lastUpdate + timedelta(minutes=30) > datetime.now():
			return self.buses
		self.log(logging.DEBUG, "Querying efa.de..")

		self.buses = []
		parser = etree.XMLParser(ns_clean=True)
		try:
			# xml parsing and xpath magic
			url = "http://mobil.efa.de/mobile3/XSLT_DM_REQUEST"
			args = "?outputFormat=xml&mode=direct&name_dm=%s&limit=30&type_dm=stopID" % self.config["station_id"]

			tree = etree.parse(url + args, parser)
			deps = tree.xpath("/itdRequest/itdDepartureMonitorRequest/itdDepartureList/itdDeparture[*]")
			for dep in deps:
				try:
					# parse date and time
					dateElement = dep.xpath("./itdDateTime/itdDate")[0]
					day = dateElement.get("day")
					month = dateElement.get("month")
					year = dateElement.get("year")
					timeElement = dep.xpath("./itdDateTime/itdTime")[0]
					hour = timeElement.get("hour")
					minute = timeElement.get("minute")

					dateTimeStr = "%s.%s.%s %s:%s" \
						% (day, month, year, hour, minute)

					dateTime = datetime.strptime(dateTimeStr, "%d.%m.%Y %H:%M")

					# parse line and direction
					lineElem = dep.xpath("./itdServingLine")[0]
					number = lineElem.get("number")
					direction = lineElem.get("direction")

					transport = lineElem.xpath("./itdNoTrain")[0].get("name")

					self.buses.append((dateTime, number, direction, transport))
				except IndexError:
					self.log(logging.ERROR, "XPath did not return anything.")
					continue
		except (IOError, etree.XMLSyntaxError) as e:
			self.log(logging.ERROR, e)
			return []
		self.lastUpdate = datetime.now()
		return self.buses

	def filterBuses(self, bus):
		date = bus[0]
		deltaSecs = (datetime.now() - date).total_seconds()
		return deltaSecs < 0

	def show(self):
		"""Shows departing buses."""
		# fonts
		headlineFont = pygame.font.Font("fonts/blue_highway_bd.ttf",
			self.relH(.15))
		stdFont = pygame.font.Font("fonts/DejaVuSansMono.ttf",
			self.relH(.06))
		digitalFont = pygame.font.Font("fonts/LetsgoDigital-Regular.ttf",
			self.relH(.13))

		# colors used
		black = (0, 0, 0)
		white = (255, 255, 255)
		red = (255, 0, 0)

		startTime = datetime.now()
		while startTime + timedelta(seconds=self.displayTime) > datetime.now():
			# black screen
			self.screen.fill(black)

			# bus loop
			currentY = self.relH(.25)
			# ignore buses that departed or will depart in > 99 min
			buses = filter(self.filterBuses, self.getBuses())
			for date, number, direction, transport in buses[:3]:
				# calculate delta
				delta = datetime.now() - date
				deltaMins = int(abs(delta.total_seconds() / 60))

				# render one bus departure at a time with a bullet point
				if deltaMins == 0:
					remaining = "jetzt  "
				elif delta.total_seconds() < -60*99:
					remaining = date.strftime("%H:%M  ")
				else:
					remaining = "%02d Min:" % deltaMins

				transport = " %s" % transport if transport != "Bus" else ""
				busStr = u"\u00BB %s  %s %s%s" \
					% (remaining, number, direction, transport)

				# this only acts as a container here
				bus = FontSurface(self.screen, "", stdFont)
				scrRect = self.screen.get_rect()
				surface = render_textrect(busStr, stdFont, scrRect, white, black)
				bus.surface = surface
				bus.pos.x = self.relW(.007)
				bus.pos.y = currentY
				bus.blit()

				# draw circle around bus line number
				border = self.relW(.005)
				if len(number) == 1:
					pos = (self.relW(.275) - border, currentY + self.relH(.036))
					radius = self.relH(.042)
				elif len(number) == 3:
					pos = (self.relW(.293), currentY + self.relH(.038))
					radius = self.relH(.073)

				pygame.draw.circle(self.screen, white, pos, radius, border)

				currentY += bus.pos.height + self.relH(.14)

			# no buses departing
			if len(buses) == 0:
				self.log(logging.ERROR, "No buses found. Skipping.")
				return
				"""
				msgStr = "Momentan fahren keine Busse."
				msg = FontSurface(self.screen, msgStr, stdFont)
				msg.centerX()
				msg.centerY()
				msg.blit()
				"""

			# headline
			headline = FontSurface(self.screen, u"Nächste Busse", headlineFont)
			headline.centerX()
			headline.pos.y = 0
			headline.blit()

			# clock
			timeStr = datetime.now().strftime("%H:%M:%S")
			renderedDate = FontSurface(self.screen, timeStr, digitalFont, red)
			renderedDate.protoStr("88.88.8888")
			renderedDate.pos.x = self.relW(.70)
			renderedDate.pos.y = self.relH(.86)
			renderedDate.blit()

			# show it
			pygame.display.flip()
			# update deltas every second
			self.wait(1)

