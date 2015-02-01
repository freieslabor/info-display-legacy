#!/usr/bin/env python
# -*- coding: utf-8 -*-

class FontSurface:
	def __init__(self, screen, text, font, color=(255, 255, 255)):
		self.screen = screen
		self.text = text
		self.surface = font.render(text, True, color)
		self.pos = self.surface.get_rect()
		self.font = font

	def centerX(self, reference=None):
		"""Places surface on horizontal center of other surface
		(default: screen)."""
		if reference:
			self.pos.centerx = reference.pos.centerx
		else:
			self.pos.centerx = self.screen.get_rect().centerx

	def centerY(self, reference=None):
		"""Places surface on vertical center of other surface
		(default: screen)."""
		if reference:
			self.pos.centery = reference.pos.centery
		else:
			self.pos.centery = self.screen.get_rect().centery

	def protoStr(self, protoStr):
		"""Sets the position for a prototypical string (to avoid position
		shifting with smaller letters)."""

		protoSurface = self.font.render(protoStr, True, (0, 0, 0))
		self.pos = protoSurface.get_rect()

	def rect(self):
		return self.surface.get_rect()

	def blit(self):
		self.screen.blit(self.surface, self.pos)

