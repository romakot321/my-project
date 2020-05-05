import os
from colorama import Fore, init, Style
import random

init(autoreset=True)

def shop(money, stones):
	print("-------------" + Fore.CYAN + "Shop" + Fore.RESET + "-------------")
	print("1) Buy random stone(120 coins)")
	print("------------------------------")
	b = input()
	if(int(b) == 1 and money > 119):
		ib = random.randrange(0, 2)
		stones[ib] += 1
	else:
		print("Error or not enough shards")
		input()
	items = [money, stones]
	return items 

def inv(stones, maxhp, defense, atk):
	print("----------" + Fore.CYAN + "Inventory" + Fore.RESET + "----------")
	if(stones[0] != 0):	
		print("1)    Water stones: " + str(stones[0]))
	if(stones[1] != 0):	
		print("2)    Sun stones: " + str(stones[1]))
	if(stones[2] != 0):	
		print("3)    Air stones: " + str(stones[2]))
	print("------------------------------")
	b = input()
	if(int(b) == 1 and stones[0] > 0):
		maxhp += 5
		stones[0] -= 1
	elif(int(b) == 2 and stones[1] > 0):
		atk += 2
		stones[1] -= 1
	elif(int(b) == 3 and stones[2] > 0):
		defense += 1
		stones[2] -= 1
	items = [maxhp, atk, defense, stones]
	return items

def Workshop(shards, stones):
	os.system('cls')
	print("------------" + Fore.CYAN + "Stones" + Fore.RESET + "------------")
	print("1) Craft a water stone(30 shards)")
	print("2) Craft a sun stone(30 shards)")
	print("3) Craft a air stone(30 shards)")
	print("------------------------------")
	a = input()
	if(int(a) == 1 and shards[0] > 29):
		stones[0] += 1
		shards[0] -= 30
	elif(int(a) == 2 and shards[2] > 29):
		stones[1] += 1
		shards[1] -= 30
	elif(int(a) == 3 and shards[3] >29):
		stones[2] += 1
		shards[2] -= 30
	else:
		print("Error or not enough shards")
		input()
	items = [stones, shards]
	return items