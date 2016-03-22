# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 18:21:26 2016

@author: Modza

v. 0.0.2
"""

import random
import argparse

def turn_state(state):
	if state == comp_turn:
		return "It's computer turn."
	else:
		return "It's your turn."

def draw(state):
	print("Number of stones: ", state['stones'])
	print(turn_state(state['turn']))

def player_turn(state):
	print("How much to take (1,2,3) ?")
	return [int(input()), comp_turn]

def comp_turn(state):
	moves_variants = list(map(lambda x,y: x-y, [state for i in range(3)], [1,2,3]))
	print('variants: ', moves_variants)
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
	elif state['stones'] == 0:
		return 'You lose!'

def monte_carlo(state, K=1000):
	games = [state for game in range(K)]
	return list(map(random_moves, games)).count(True)

def random_moves(number, turn=False):
	if number <= 1:
		return turn
	else:
		
		return random_moves((number - random.choice([1,2,3])), (not turn))
		

def game(state):
	draw(state)
	if check(state):
		print(check(state))
	else:
		res = state['turn'](state['stones'])
		game({'stones': (state['stones'] - res[0]), 'turn': res[1]})

def arg_parse_func():
    parser = argparse.ArgumentParser(description='Nim game')
    parser.add_argument('-s', '--stones', type=int, help='the number of stones')
    parser.add_argument('-p', '--player', action='store_true', help='player goes first')
    args = parser.parse_args()
    return {'stones': (args.stones or 10), 'turn': ((args.player and player_turn) or (comp_turn))}


#init
game(arg_parse_func())