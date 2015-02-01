#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import InfoScreen
import pygame, logging, time
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
		self.displayTime = 10

	def show(self):
		"""Shows date and time."""
		startTime = datetime.now()
		self.log(logging.DEBUG, "Showing date/time.")
		# choose nice font
		digitalFont70 = pygame.font.Font("fonts/LetsgoDigital-Regular.ttf", 70)
		digitalFont130 = pygame.font.Font("fonts/LetsgoDigital-Regular.ttf", 130)

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
			renderedDate.protoStr("88.88.8888")
			renderedDate.centerX()
			renderedDate.pos.y = 100
			renderedDate.blit()

			renderedTime = FontSurface(self.screen, timeStr, digitalFont130, red)
			renderedTime.protoStr("88:88:88")
			renderedTime.centerX()
			renderedTime.pos.y = 200
			renderedTime.blit()

			# show it
			pygame.display.flip()
			# this is a clock exact to the second, so sleep 1 sec
			self.wait(1)

