#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base import InfoScreen
import pygame, logging
from datetime import datetime
from .helper.fontsurface import FontSurface

class AccidentScreen(InfoScreen):
	"""Info screen that shows days since last accident ;)."""

	def __init__(self, screen, config):
		"""Creates accident info screen.

		Keyword arguments:
		screen -- screen to display on"""
		super(AccidentScreen, self).__init__(screen)

		self.config = config
		# seconds to display this info screen
		self.displayTime = 7

	def getDaysSinceAccident(self):
		"""Returns time delta as days."""
		accident = datetime.strptime(self.config["last_accident"], '%Y-%m-%d')
		delta = datetime.now() - accident
		return delta.days

	def show(self):
		"""Shows date and time.

		Keyword arguments:
		screen -- screen to display on"""
		# fonts
		stdFont = pygame.font.Font("fonts/blue_highway_bd.ttf", self.relH(.135))
		digitalFont = pygame.font.Font("fonts/LetsgoDigital-Regular.ttf", self.relH(.2))

		# colors used
		red = (255, 0, 0)
		white = (255, 255, 255)
		black = (0, 0, 0)
		green = (0, 138, 82)

		# green screen
		self.screen.fill(green)
		surfaces = []

		# render text line by line (crazy y-values because of crappy fonts)
		msg1 = FontSurface(self.screen, "THIS LAB HAS OPERATED", stdFont)
		msg1.centerX()
		msg1.pos.y = self.relH(.095)
		surfaces.append(msg1)

		# day count
		dayCountStr = str(self.getDaysSinceAccident())
		msg2 = FontSurface(self.screen, dayCountStr, digitalFont, red)
		msg2.centerX()
		msg2.pos.y = msg1.pos.y + self.relH(.19)
		surfaces.append(msg2)

		msg3 = FontSurface(self.screen, "  DAYS WITHOUT AN", stdFont)
		# adjust position, because 2 surfaces in 1 line
		msg2.pos.x -= msg3.pos.width / 2
		msg3.pos.x = msg2.pos.right
		msg3.centerY(msg2)
		surfaces.append(msg3)

		msg5 = FontSurface(self.screen, "ACCIDENT.", stdFont)
		msg5.centerX()
		msg5.pos.y = msg3.pos.y + self.relH(.215)
		surfaces.append(msg5)

		msg6 = FontSurface(self.screen, "STAY SAFE!", stdFont, red)
		msg6.centerX()
		msg6.pos.y = msg5.pos.y + self.relH(.22)
		surfaces.append(msg6)

		# draw a black rectangle around counter
		startX = msg2.pos.x - self.relW(.01)
		endX = msg2.pos.width + self.relW(.025)

		pos = (startX, msg2.pos.y, endX, msg2.pos.height)
		pygame.draw.rect(self.screen, black, pos)

		# draw white border
		radius = self.relH(.04)
		pygame.draw.rect(self.screen, white, self.screen.get_rect(), radius)

		# blit text on background
		for surface in surfaces: surface.blit()
		# show it
		pygame.display.flip()
		# no need to do anything else
		self.wait(self.displayTime)

