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
		self.displayTime = 10

	def getDaysSinceAccident(self):
		accident = datetime.strptime(self.config["last_accident"], '%Y-%m-%d')
		delta = datetime.now() - accident
		return delta.days

	def show(self):
		"""Shows date and time.

		Keyword arguments:
		screen -- screen to display on"""
		# fonts
		stdFont = pygame.font.Font("fonts/blue_highway_bd.ttf", 60)
		digitalFont = pygame.font.Font("fonts/LetsgoDigital-Regular.ttf", 110)

		# colors used
		red = (255, 0, 0)
		white = (255, 255, 255)
		black = (0, 0, 0)
		green = (0, 138, 82)

		# green screen
		self.screen.fill(green)
		surfaces = []

		# render text line by line (crazy y-values because of crappy fonts)
		msg1 = FontSurface(self.screen, "THIS LAB HAS", stdFont)
		msg1.centerX()
		msg1.pos.y = 5
		surfaces.append(msg1)

		msg2 = FontSurface(self.screen, "OPERATED", stdFont)
		msg2.centerX()
		msg2.pos.y = msg1.pos.y + 65
		surfaces.append(msg2)

		# day count
		dayCountStr = str(self.getDaysSinceAccident())
		msg3 = FontSurface(self.screen, dayCountStr, digitalFont, red)
		msg3.centerX()
		msg3.pos.y = msg2.pos.y + 75
		surfaces.append(msg3)

		msg4 = FontSurface(self.screen, "  DAYS", stdFont)
		# adjust position, because 2 surfaces in 1 line
		msg3.pos.x -= msg4.pos.width / 2
		msg4.pos.x = msg3.pos.right
		msg4.centerY(msg3)
		surfaces.append(msg4)

		msg5 = FontSurface(self.screen, "WITHOUT AN", stdFont)
		msg5.centerX()
		msg5.pos.y = msg3.pos.y + 120
		surfaces.append(msg5)

		msg6 = FontSurface(self.screen, "ACCIDENT.", stdFont)
		msg6.centerX()
		msg6.pos.y = msg5.pos.y + 65
		surfaces.append(msg6)

		msg7 = FontSurface(self.screen, "STAY SAFE!", stdFont, red)
		msg7.centerX()
		msg7.pos.y = msg6.pos.y + 70
		surfaces.append(msg7)

		# draw a black rectangle around counter
		pos = (msg3.pos.x-14, msg3.pos.y, msg3.pos.width+35, msg3.pos.height)
		pygame.draw.rect(self.screen, black, pos)

		# draw white border
		pygame.draw.rect(self.screen, white, self.screen.get_rect(), 17)

		# blit text on background
		for surface in surfaces: surface.blit()
		# show it
		pygame.display.flip()
		# no need to do anything else
		self.wait(self.displayTime)

