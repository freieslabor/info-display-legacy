#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import InfoScreen
import pygame, logging
from datetime import datetime, timedelta
from .helper.fontsurface import FontSurface

class ClockScreen(InfoScreen):
	"""Info screen that shows time and date."""
	def __init__(self, screen):
		"""Creates the clock screen.

		Keyword arguments:
		screen -- screen to display on"""
		super(ClockScreen, self).__init__(screen)

		# seconds to display this info screen
		self.displayTime = 5

	def show(self):
		"""Shows date and time."""
		startTime = datetime.now()
		self.log(logging.DEBUG, "Showing date/time.")
		# choose nice font
		ledFontFile = "fonts/LetsgoDigital-Regular.ttf"
		ledFontNormal = pygame.font.Font(ledFontFile, self.relH(.2))
		ledFontBig = pygame.font.Font(ledFontFile, self.relH(.4))

		# show clock for specified time
		while startTime + timedelta(seconds=self.displayTime) > datetime.now():
			# black screen
			self.screen.fill((0, 0, 0))
			# nice date/time strings
			dateStr = datetime.now().strftime("%d.%m.%Y")
			timeStr = datetime.now().strftime("%H:%M:%S")
			# render red text with font
			red = (255, 0, 0)

			renderedDate = FontSurface(self.screen, dateStr, ledFontNormal, red)
			renderedDate.centerX()
			# adjust date position if it starts with "1" (because of LED font)
			day = datetime.now().strftime("%d")
			dateXMulti = self.relW(.02)
			if day[0] == "1": renderedDate.pos.x -= dateXMulti
			renderedDate.pos.y = self.relH(.1)
			renderedDate.blit()

			renderedTime = FontSurface(self.screen, timeStr, ledFontBig, red)
			renderedTime.centerX()
			# adjust time position if it starts with "1" (because of LED font)
			hour = datetime.now().strftime("%H")
			timeXMulti = self.relW(.04)
			if hour[0] == "1": renderedTime.pos.x -= timeXMulti
			renderedTime.pos.y = self.relH(.4)
			renderedTime.blit()

			# show it
			pygame.display.flip()
			# this is a clock exact to the second, so sleep 1 sec
			self.wait(1)

