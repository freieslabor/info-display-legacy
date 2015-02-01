#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame, pygame.mouse, logging, os
from screens.base import InfoScreen

# windowed mode if True
DEBUG = True

class InfoDisplay:
	""""""
	def __init__(self):
		"Ininitializes a new pygame screen using the framebuffer"
		self.infoScreens = []

		if DEBUG:
			logging.info("DEBUG MODE")
			self.screen = pygame.display.set_mode((640, 480))
			pygame.display.set_caption("Info-Display")
		else:
			# Based on "Python GUI in Linux frame buffer"
			# http://www.karoltomala.com/blog/?p=679
			dispNo = os.getenv("DISPLAY")
			if dispNo:
				logging.info("I'm running under X display = %s" % dispNo)

			# Check which frame buffer drivers are available
			# Start with fbcon since directfb hangs with composite output
			drivers = ["fbcon", "directfb", "svgalib"]
			found = False
			for driver in drivers:
				# Make sure that SDL_VIDEODRIVER is set
				if not os.getenv("SDL_VIDEODRIVER"):
					os.putenv("SDL_VIDEODRIVER", driver)
				try:
					pygame.display.init()
				except pygame.error:
					logging.warning("Driver: %s failed." % driver)
					continue
				found = True
				break

			if not found:
				err = "No suitable video driver found! Are you root?"
				logging.critical(err)
				raise Exception(err)

			displayInfo = pygame.display.Info()
			size = (displayInfo.current_w, displayInfo.current_h)
			logging.info("Framebuffer size: %d x %d" % (size[0], size[1]))
			self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

		pygame.mouse.set_visible(False)
		pygame.font.init()

	def start(self):
		"""Initializes and runs through screens infinitely."""
		self.initScreens()
		while True:
			self.cycleScreens()

	def initScreens(self):
		"""Initializes all screens."""
		for currentScreen in InfoScreen.__subclasses__():
			logging.debug("Initializing %s." % currentScreen.__name__)
			self.infoScreens.append(currentScreen(self.screen))

	def cycleScreens(self):
		"""Cycle through all screens in subdirectory."""
		for infoScreen in self.infoScreens:
			logging.debug("Showing %s." % infoScreen.__class__.__name__)
			infoScreen.show()

if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG,
		format="%(asctime)s %(levelname)-8s %(message)s",
		datefmt="%Y.%m.%d %H:%M:%S")
	display = InfoDisplay()
	display.start()
	pygame.quit()
