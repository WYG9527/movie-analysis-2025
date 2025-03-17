import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien


def check_keydown_events(event,ai_settings,screen,ship,bullets):		#处理KEYDOWN事件
	if event.key==pygame.K_RIGHT:	
		ship.moving_right = True
				
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
				
	elif event.key == pygame.K_UP:
		ship.moving_up = True
				
	elif event.key == pygame.K_DOWN:
		ship.moving_down = True
		
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings,screen,ship,bullets)
		
	elif event.key == pygame.K_q:
		sys.exit()
		
def fire_bullet(ai_settings,screen,ship,bullets):
	'''如果子弹未达到上限，则发射一颗子弹'''	
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings,screen,ship)					# 创建一颗子弹，并将其加入到编组bullets中
		bullets.add(new_bullet)

def check_keyup_events(event,ship):										#处理KEYUP事件
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
				
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False
				
	elif event.key == pygame.K_UP:
		ship.moving_up = False
				
	elif event.key == pygame.K_DOWN:
		ship.moving_down = False

def check_events(ai_settings,screen,ship,bullets):
	'''响应按键和鼠标事件'''
	for event in pygame.event.get():									#使用方法pygame.event.get()。所有键盘和鼠标事件都将促使for循环运行。
		if event.type==pygame.QUIT:										#在这个循环中，我们编写一系列的if语句来检测并响应特定的事件。玩家单击游戏窗口的关闭按钮时，将检测到pygame.QUIT事件，
			sys.exit()													#我们调用sys.exit()来退出游戏
			
		elif event.type==pygame.KEYDOWN:								#KEYDOWN 事件是处理键盘输入的核心机制之一
			check_keydown_events(event,ai_settings,screen,ship,bullets)
							
		elif event.type == pygame.KEYUP:								#我们修改了游戏在玩家按下右箭头键时响应的方式：不直接调整飞船的位置，而只是将moving_right设置为True。们添加了一个新的elif代码块，用于响应KEYUP事件：玩家松开右箭头键（K_RIGHT）时，我们将moving_right设置为False。
			check_keyup_events(event,ship)


def update_screen(ai_settings,stats,screen,ship,aliens,bullets):
	screen.fill(ai_settings.bg_color)									#调用方法screen.fill()，用背景色填充屏幕；这个方法只接受一个实参：一种颜色。
	
	for bullet in bullets.sprites():									#方法bullets.sprites()返回一个列表，其中包含编组bullets中的所有精灵。为在屏幕上绘制发射的所有子弹，我们遍历编组bullets中的精灵，并对每个精灵都调用draw_bullet()
		bullet.draw_bullet()
	
	ship.blitme()
	aliens.draw(screen)
					
	pygame.display.flip()												#让最近绘制的屏幕可见
	
	
def update_bullets(ai_settings,screen,ship,aliens,bullets):
	"""更新子弹的位置，并删除已消失的子弹"""
	bullets.update()													#bullets.update() 会遍历 bullets 精灵组中的每个子弹对象，并调用它们的 update() 方法。核心功能：移动控制：修改子弹的 rect 坐标（如 self.rect.x += speed）生命周期管理：检测子弹是否超出屏幕边界或需要销毁（如 self.kill()）动画/状态更新：若子弹有动态效果（如闪烁、缩放），在此处实现
		
	# 删除已消失的子弹
	for bullet in bullets.copy():										#当直接遍历原精灵组bullets时，若在循环中删除元素，会导致元素索引偏移。例如：假设原精灵组元素为[bullet1, bullet2, bullet3]遍历到bullet1时发现需要删除，删除后剩余元素变为[bullet2, bullet3]此时循环会继续尝试访问原索引位置的下一个元素（即原索引1的位置），但此时该位置已变为bullet3，导致bullet2未被处理。这种偏移会导致部分元素被跳过，引发逻辑错误（如未删除应消失的子弹）。
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
			
	check_bullet_alien_collisions(ai_settings,screen,ship,aliens,bullets)
			
def check_bullet_alien_collisions(ai_settings,screen,ship,aliens,bullets):
	'''检查是否有子弹击中了外星人
		如果是这样，就删除相应的子弹和外星人'''
	collisions = pygame.sprite.groupcollide(bullets,aliens,False,True)
	
	if len(aliens) == 0:
		# 删除现有的子弹并新建一群外星人
		bullets.empty()
		create_fleet(ai_settings,screen,ship,aliens)

def get_number_aliens_x(ai_settings,alien_width):
	"""计算每行可容纳多少个外星人"""
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x

def get_number_rows(ai_settings,ship_height,alien_height):
	"""计算屏幕可容纳多少行外星人"""
	available_space_y = (ai_settings.screen_height - 					#计算公式用括号括起来了，这样可将代码分成两行，以遵循每行不超过79字符的建议
							(3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows
	
	
def create_alien(ai_settings,screen,aliens,alien_number,row_number):
	"""创建一个外星人并将其放在当前行"""
	alien = Alien(ai_settings,screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number #alien.rect.height 表示 ​顶部安全边距，确保外星人不会紧贴屏幕边缘。2 * alien.rect.height 是 ​每行之间的垂直间距，包括外星人高度本身和一个空白区域（总间距为两倍高度）。row_number 是当前行号（从 0 开始），通过乘法逐行增加位置。
	aliens.add(alien)
	
	

def create_fleet(ai_settings,screen,ship,aliens):
	'''创建外星人群'''
	alien = Alien(ai_settings,screen,)
	number_aliens_x = get_number_aliens_x(ai_settings,
		alien.rect.width)
	number_rows = get_number_rows(ai_settings,ship.rect.height,
		alien.rect.height)

	for row_number in range(number_rows):								#创建第一行外星人
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings,screen,aliens,alien_number,
				row_number)
		
def check_fleet_edges(ai_settings,aliens):
	"""有外星人到达边缘时采取相应的措施"""
	for alien in aliens.sprites():										#sprites() 方法的主要作用是获取精灵组内所有精灵的列表。
		if alien.check_edges():
			change_fleet_direction(ai_settings,aliens)
			break
			
def change_fleet_direction(ai_settings,aliens):							#如果check_edges()返回True，我们就知道相应的外星人位于屏幕边缘，需要改变外星人群的方向，因此我们调用change_fleet_direction()并退出循环。在change_fleet_direction()中，我们遍历所有外星人，将每个外星人下移fleet_drop_speed设置的值；然后，将fleet_ direction的值修改为其当前值与-1的乘积。
	"""将整群外星人下移，并改变它们的方向"""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def ship_hit(ai_settings,stats,screen,ship,aliens,bullets):
	"""响应被外星人撞到的飞船"""
	stats.ships_left -= 1												# 将ships_left减1
	aliens.empty()														# 清空外星人列表和子弹列表
	bullets.empty()
	
	create_fleet(ai_settings,screen,ship,aliens)						# 创建一群新的外星人，并将飞船放到屏幕底端中央
	ship.center_ship()
	
	sleep(1.0)															#暂停
		
		
def update_aliens(ai_settings,stats,screen,ship,aliens,bullets):
	'''查是否有外星人位于屏幕边缘，并更新整群外星人的位置'''
	check_fleet_edges(ai_settings,aliens)
	aliens.update()
	'''检测外星人和飞船之间的碰撞'''
	if pygame.sprite.spritecollideany(ship,aliens):							#方法spritecollideany()接受两个实参：一个精灵和一个编组。它检查编组是否有成员与精灵发生了碰撞，并在找到与精灵发生了碰撞的成员后就停止遍历编组。在这里，它遍历编组aliens，并返回它找到的第一个与飞船发生了碰撞的外星人。
		ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
