# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 18:21:26 2016

@author: Modza

v. 0.0.1
"""

import random

def turn_state(state):
	if state == comp_turn:
		return "It's computer turn."
	else:
		return "It's your turn."

def draw(state): #функция вывода
	print("Number of stones: ", state['stones'])
	print(turn_state(state['turn']))

def player_turn(state): #функция хода игрока
	print("How much to take (1,2,3) ?")
	return [int(input()), comp_turn]

	'''
	Map применяет функцию (в данном случае monte_carlo) по очереди ко всем элементам moves_variants.
	Полученый список содержит число "проигрышей" человека из 1000 случайных партий. Порядок этого списка
	соответсвует moves_variants, т.е. варианты хода [3,2,1] - осталось четыре камня и комп видит что можно забрать 
	1, 2 или 3. Для каждого из этих чисел map применяет monte_carlo и в списке res_list оказывается что то типа
	[579, 432, 641]. Таким образом далее комп смотрит На наименьшее число в res_list и совершает такой ход, которому
	это число соответсвует (в данном случае наибольшее 641 и комп сходит 1 - т.е. заберет один камень). Что, конечно,
	неправильно - должен по сути всегда забирать три камня, например. Чтобы мне остался один и я точно проиграл. 
	'''
def comp_turn(state): #функция хода компа
	#moves_variants = [moves for moves in range(1,state)] #не функционально наверное создавать какие то переменные но тут я уже задолбался
	#moves_variants.reverse() 
	moves_variants = list(map(lambda x,y: x-y, [state for i in range(3)], [1,2,3]))
	print('variants: ', moves_variants) #сколько камней останется после хода
	res_list = (list(map(monte_carlo, moves_variants)))
	print(res_list)
	#res_list.reverse()
	print(min(res_list))
	print(res_list.index(min(res_list)))
	res = res_list.index(min(res_list))+1
	print("Computer takes ", res, " stones.")
	return [res, player_turn]

def how_much_left(x,y):
	return x-y

def check(state):
	if state['stones'] == 1:
		if state['turn'] == comp_turn:
			return 'Computer lose!'
		elif state['turn'] == player_turn:
			return 'You lose!'
		else:
			return state['turn']
	elif state['stones'] == 0: #ну компу то запрещено брать все камни, но человек может
		return 'You lose!'

	'''
	Нужно сыграть 1000 игр. В функцию передается число камней ПОСЛЕ гипотетического хода компа 
	(ну из рассматриваемого варианта действий). Создается списочек длиной 1000 состоящий из
	этого числ камней. Затем map применяет к каждому (но они все одинаковые) функцию random_moves
	которая возвращает результат в виде True или False. False значит что ход человека. На выходе map 
	список из тру-фолс получается длиной 1000. Вся функция monte_carlo возвращает число True в этом списке, 
	т.е. сколько поражений компа при таком варианте хода.
	'''
def monte_carlo(state, K=1000):
	games = [state for game in range(K)]
	return list(map(random_moves, games)).count(True)

	'''
	Random_moves ещё одна функция с рекурсией - реализует цикл без цикла вызывая сама себя. 
	Если на входе функции только один аргумент number (число камней оставшихся) то считается что
	сейчас был ход компа (и это первая итерация). Если остался один камень - тот чей сейчас ход проиграл и функция заканчивается.
	Если больше - вызывает сама себя с измененными параметрами: ход меняется на противоположный, из числа камней вычитается 
	случайное число но в допустимых пределах. В итоге рано или поздно останется один камень, вопрос только на чьем ходу. 
	
	'''
def random_moves(number, turn=False):
	if number <= 1:
		return turn
	else:
		
		return random_moves((number - random.choice([1,2,3])), (not turn))
		

def game(state):
	draw(state) #вызов функции отображения состояния
	if check(state): #вызов функции проверки, окончания игры
		print(check(state)) #если она есть - пишет кто проиграл и функция game заканчивается 
	else:
		res = state['turn'](state['stones']) #в противном случае вызываем функцию того игрока, чей сейчас ход (player_turn/comp_turn)
		game({'stones': (state['stones'] - res[0]), 'turn': res[1]}) #и вызываем саму же game но уже с измененными аргументами (типа цикл без тела цикла)



#Инициализация- передаем сколько камней и чей ход (comp_turn/player_turn)
game({'stones': 10, 'turn': comp_turn})