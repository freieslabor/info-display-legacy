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
		digitalFont70 = pygame.font.Font("fonts/LetsgoDigital-Regular.ttf", 200)
		digitalFont130 = pygame.font.Font("fonts/LetsgoDigital-Regular.ttf", 350)

		# show clock for specified time
		while startTime + timedelta(seconds=self.displayTime) > datetime.now():
			# black screen
			self.screen.fill((0, 0, 0))
			# nice date/time strings
			dateStr = datetime.now().strftime("%d.%m.%Y")
			timeStr = datetime.now().strftime("%H:%M:%S")
			# render red text with font
			red = (255, 0, 0)

			renderedDate = FontSurface(self.screen, dateStr, digitalFont70, red)
			renderedDate.centerX()
			renderedDate.pos.x -= 34*datetime.now().strftime("%d").count("1")
			renderedDate.pos.y = 100
			renderedDate.blit()

			renderedTime = FontSurface(self.screen, timeStr, digitalFont130, red)
			renderedTime.centerX()
			renderedTime.pos.x -= 60*datetime.now().strftime("%H").count("1")
			renderedTime.pos.y = 400
			renderedTime.blit()

			# show it
			pygame.display.flip()
			# this is a clock exact to the second, so sleep 1 sec
			self.wait(1)

