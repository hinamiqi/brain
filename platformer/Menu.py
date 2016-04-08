#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import pyglet
import os

UNSELECTED = (184, 134, 11, 255)
SELECTED = (190, 34, 35, 255)

class GameMenu(object):
	"""
	Игровое меню. Содержит в себе все пункты меню. Передаваемые в аргументах
	координаты являются положением верхнего левого угла, чтобы можно было 
	легко располагать как справа, так и снизу от поля.
	Позволяет иметь вертикальное или горизонтальное расположение кнопок.
	Аргументом height передаётся высота окна/экрана, чтобы соответственно изменять
	размер шрифта (1/40 от высоты), делается это в place_buttons.
	(self.height — lambda-функция)
	self.x и self.y — функции определения отправной точки, передаются в 
	виде lambda-функции при создании объекта этого класса.
	"""
	def __init__(self, x, y, height, orientation = "vertical"):
		self.orientation = orientation
		self.x = x
		self.y = y
		self.height = height
		self.selected = None
		self.batch = pyglet.graphics.Batch()
		self.create_buttons()
		self.place_buttons()
	
	def create_buttons(self):
		"""
		В self.button_names записаны названия (текст) кнопок, далее for луп создаёт
		по кнопкке на каждый из элементов списка, присваивая атрибут в видео строчного
		написания текста кнопки без пробелов. Затем кнопка добавляюется в список уже
		пиглетовских объектов, которые затем используется в лупах расположения.
		"""
		self.levels = [f for f in os.listdir() if f[:3] == "map" and f[-4:] == ".bmp"]
		
		self.buttons = []
		for button in self.levels:
			setattr(self, button.lower().replace(".bmp",""), pyglet.text.Label(
				button.lower().replace(".bmp",""), anchor_x="left", anchor_y="top", 
				font_name='Arial', color=UNSELECTED, batch=self.batch))
			self.buttons.append(eval("self."+button.lower().replace(".bmp","")))
		
		if len(self.buttons) > 0:
			self.selected = 0
			self.buttons[self.selected].color = SELECTED
		else:
			setattr(self, "no_levels", pyglet.text.Label(
				"NO LEVELS!", anchor_x="left", anchor_y="top", font_name='Arial',
				color=UNSELECTED, batch=self.batch))
	
	def place_buttons(self):
		"""
		Располагает кнопки друг под другом или в одну строку. Размер шрифта высчитывается
		именно тут, чтобы одной этой функцией легко перерисовывать кнопки при изменении 
		размера окна.
		В горизонтальном расположении первая кнопка ставится вне лупа, потому что
		расположение кнопок зависит от предыдущей.
		self.x() и self.y() — функции, высчитывающие "нулевую" точку меню.
		"""
		self.fontsize = self.height()/40
		if self.orientation == "vertical":
			for i in range(0,len(self.buttons)):
				self.buttons[i].font_size = self.fontsize
				self.buttons[i].x = self.x()
				self.buttons[i].y = self.y() - self.fontsize * (i*2)

		elif self.orientation == "horizontal":
			self.buttons[0].x, self.buttons[0].y = self.x(), self.y()
			self.buttons[0].font_size = self.fontsize
			for i in range(1, len(self.buttons)):
				self.buttons[i].font_size = self.fontsize
				self.buttons[i].y = self.y()
				self.buttons[i].x = self.buttons[i-1].x + \
					self.buttons[i-1].content_width + self.fontsize
			
	def select_next(self):
		self.buttons[self.selected].color = UNSELECTED
		self.selected = (self.selected + 1) % len(self.buttons)
		self.buttons[self.selected].color = SELECTED

	def select_previous(self):
		self.buttons[self.selected].color = UNSELECTED
		self.selected = (self.selected + len(self.buttons) - 1) % len(self.buttons)
		self.buttons[self.selected].color = SELECTED
	
	def draw(self):
		self.batch.draw()

# GameMenu(1,2,3)