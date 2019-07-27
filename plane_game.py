# -*- coding: utf-8 -*-

import pygame
from sys import exit
import random


##子弹类
class bullet:
	def __init__(self):
		self.x = 0
		self.y = -1
		self.image = pygame.image.load('bullet.png').convert_alpha()
		self.active = False

	def move(self):
		'''
		子弹移动函数

		每次主循环子弹向上飞；
		当子弹达到游戏界面的上边框的时候，子弹设置为失活状态。
		'''
		if self.active:
			self.y -= 2
		if self.y < 0:
			self.active = False

	def restart(self):
		'''
		子弹重置函数

		重置子弹的中心位置等于鼠标的坐标位置；
		设置子弹为活动状态。
		'''
		mouse_x, mouse_y = pygame.mouse.get_pos()
		self.x = mouse_x - self.image.get_width() / 2
		self.y = mouse_y - self.image.get_height() / 2
		self.active = True


##敌机类
class enemy:
	def __init__(self):
		self.restart(100)
		self.image = pygame.image.load('enemy.png').convert_alpha()

	def restart(self, scroe):
		'''
		敌机重置函数

		敌机重置的位置是在指定范围的随机坐标；
		敌机的下落速度是一个随机数加上一个 得分/100000。
		'''
		self.x = random.randint(0, 400)
		self.y = random.randint(-200, -50)
		# 随着分数的增加，敌机下落速度越来越快
		self.speed = random.random() + scroe / 100000

	def move(self, scroe):
		'''
		敌机移动函数

		每次主循环时:
		敌机在游戏界面下边框以上时，继续移动；
		敌机在游戏界面下边框以下时，重置敌机。
		'''
		if self.y < 700:
			self.y += self.speed
		else:
			self.restart(scroe)


class plane:
	def __init__(self):
		self.restart()
		self.image = pygame.image.load('plane.png').convert_alpha()

	def restart(self):
		'''
		重置飞机函数

		重置飞机坐标(200,600)
		'''
		self.x = 200
		self.y = 600

	def move(self):
		'''
		飞机移动函数

		每次主循环，飞机的中心位置为鼠标的坐标。
		'''
		mouse_x, mouse_y = pygame.mouse.get_pos()
		self.x = mouse_x - self.image.get_width() / 2
		self.y = mouse_y - self.image.get_height() / 2


def checkboom(enemy, bullet):
	'''
	子弹与敌机碰撞函数
	
	param:enemy 敌机对象;
	param:bullet 子弹对象;
	return:是否碰撞。
	'''
	if ((enemy.x < bullet.x and bullet.x < enemy.x + enemy.image.get_width()) and
			(enemy.y < bullet.y and bullet.y < enemy.y + enemy.image.get_height())):
		enemy.restart(scroe)
		bullet.active = False
		return True
	else:
		return False


def checkcrash(plane, enemy):
	'''
	敌机与飞机碰撞函数

	param:enemy 敌机对象;
	param:plane 飞机对象;
	return:是否碰撞。
	'''
	if ((plane.x + 0.7 * plane.image.get_width() > enemy.x and
	     plane.x + 0.3 * plane.image.get_width() < enemy.x + enemy.image.get_width()) and
			(plane.y + 0.7 * plane.image.get_height() > enemy.y and
			 plane.y + 0.3 * plane.image.get_height() < enemy.y + enemy.image.get_height())):
		return True
	else:
		return False


def enemy_restart():
	'''
	敌机重置函数
	
	全局enemies的list，重新设置enemies。
	'''
	global enemies
	enemies = []
	for _ in range(5):
		enemies.append(enemy())


pygame.init()
screen = pygame.display.set_mode((450, 700), 0, 32)
pygame.display.set_caption("GAME")
background = pygame.image.load('back.jpg').convert()
gg = pygame.image.load('gg.png').convert_alpha()
enemies = []
#初始化5个敌机。
for e in range(5):
	enemies.append(enemy())
bullets = []
#飞机初始化17个子弹
for i in range(17):
	bullets.append(bullet())
count_b = len(bullets)
interval_b = 0
index_b = 0
plane = plane()
gameover = False
scroe = 0.1
font = pygame.font.Font('my_font.ttf', 16)
f = open('max.txt')
lines = f.readline()
f.close()
line = int(lines.split(' ')[1])
sound = pygame.mixer.music.load('my_sound.mp3')
pygame.mixer.music.play(-1)

##游戏的主循环
while True:
	# 获取游戏状态事件
	for event in pygame.event.get():
		# 退出状态事件
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		# 游戏已经结束，并且鼠标处于buttonup事件；
		# 说明游戏结束以后，玩家重新点击界面，则重新开始游戏。
		if gameover and event.type == pygame.MOUSEBUTTONUP:
			plane.restart()
			for enemy_object in enemies:
				enemy_object.restart(100)
			for bullet_object in bullets:
				bullet_object.restart()
			scroe = 0.1
			enemy_restart()
			gameover = False
	screen.blit(background, (0, 0))
	# 游戏未结束，主循环，进行敌机，子弹，飞机移动，碰撞以及重置。
	if not gameover:
		interval_b -= 1
		# 主循环25次的时候，重置一个子弹，保证一直有子弹输出。
		if interval_b < 0:
			bullets[index_b].restart()
			interval_b = 25
			index_b = (index_b + 1) % count_b
		# 验证每个子弹是否与敌机有撞击。
		for b in bullets:
			if b.active:
				for e in enemies:
					if checkboom(e, b):
						scroe = int(scroe) + 100
				b.move()
				screen.blit(b.image, (b.x, b.y))
		# 验证每个敌机是否与飞机有碰撞。
		for e in enemies:
			if checkcrash(plane, e):
				gameover = True
			e.move(scroe)
			screen.blit(e.image, (e.x, e.y))
		plane.move()
		screen.blit(plane.image, (plane.x, plane.y))
		text = font.render('Score:%d Max:%d' % (scroe, line), 1, (0, 0, 0))
		screen.blit(text, (0, 0))
		# 每10000分的时候，增加一个敌机。
		if scroe % 10000 == 0:
			# 这里加上小数是防止：(分数不变的情况下，每次主循环都行产生一个敌机，这样会产生很多敌机)。
			scroe += 0.1
			enemies.append(enemy())
	else:
		# 保存新记录并展示
		if scroe >= line:
			line = scroe
			screen.blit(gg, (130, 200))
			text2 = font.render('Congratulations,New Score:%d ' % line, 1, (0, 0, 0))
			screen.blit(text2, (130, 370))
			text3 = font.render('Score:%d Max:%d' % (scroe, line), 1, (0, 0, 0))
			screen.blit(text3, (130, 400))
			result = 'MAX' + ' ' + str(int(line))
			p = open('max.txt', 'w')
			p.write(result)
			p.close()
		else:
			text = font.render('Score:%d Max:%d' % (scroe, line), 1, (0, 0, 0))
			text1 = font.render('Game Over!', 1, (0, 0, 0))
			screen.blit(gg, (130, 200))
			screen.blit(text, (130, 400))
			screen.blit(text1, (130, 370))
	pygame.display.update()
