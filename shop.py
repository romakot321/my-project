import os
from colorama import Fore, init, Style
import random

toolsName = [["Wooden sword", "Iron sword"], ["Wooden shield", "Iron shield"]] # Swords( 0id - +3 atk, 1id - +5 atk), Shields( 0id - +2 def, 1id - +3 def)

init(autoreset=True)
		
def shop(money, stones, items):
	print("0) Back")
	print("-------------" + Fore.CYAN + "Buy" + Fore.RESET + "--------------")
	print("1) Buy random stone(120 money)")
	print("2) Buy new sword(200-250-350-500 money)")
	print("3) Buy new shield(250-300-400-550 money)")
	print("-------------" + Fore.CYAN + "Sell" + Fore.RESET + "-------------")
	print("4) Sell bones(1 pc - 2 money) (You have: " + str(items[0][0]) + ")")
	print("5) Sell meat(1 pc - 4 money) (You have: " + str(items[0][1]) + ")")
	print("------------------------------")
	b = input()
	if(b == ""):
		shop(money, stones, items)
	if(int(b) == 0):
		pass
	if(int(b) == 1 and money > 119):
		ib = random.randrange(0, 2)
		stones[ib] += 1
		money -= 120
	if(int(b) == 2 and items[1][0] < 2):
		if(items[1][0] == 0):
			nm = 250
		elif(items[1][0] == 1):
			nm = 350
		elif(items[1][0] == 2):
			nm = 500
		else:
			nm = 200
		if(money > nm - 1):
			items[1][0] += 1
			money -= nm
		else:
			pass
	if(int(b) == 3 and items[1][1] < 2):
		if(items[1][1] == 0):
			nm = 300
		elif(items[1][1] == 1):
			nm = 400
		elif(items[1][1] == 2):
			nm = 550
		else:
			nm = 250
		if(money > nm - 1):
			items[1][1] += 1
			money -= nm
		else:
			pass
	if(int(b) == 4 and items[0][0] > 0):
		print("Enter amount to sell: ")
		b = input()
		if(items[0][0] < int(b)):
			print("Error or not enough items")
			input()
			shop(money, stones, items)
		else:
			items[0][0] -= int(b)
			money += (2 * int(b))
	if(int(b) == 5 and items[0][1] > 0):
		print("Enter amount to sell: ")
		b = input()
		if(items[0][1] < int(b)):
			print("Error or not enough items")
			input()
			shop(money, stones, items)
		else:
			items[0][1] -= int(b)
			money += (4 * int(b))
	else:
		input()
		pass
	items = [money, stones, items]
	return items 

def inv(stones, maxhp, defense, atk, items, hp):
	print("0) Back")
	print("---------" + Fore.CYAN + "Backpack" + Fore.RESET + "----------")
	if(stones[0] != 0):	
		print("1)    Water stones: " + str(stones[0]))
	if(stones[1] != 0):	
		print("2)    Sun stones: " + str(stones[1]))
	if(stones[2] != 0):	
		print("3)    Air stones: " + str(stones[2]))
	if(items[0][0] != 0):
		print("4)    Bones: " + str(items[0][0]))
	if(items[0][1] != 0):
		print("5)    Meat: " + str(items[0][1]))
	print("------------------------------")
	print("---------" + Fore.CYAN + "Inventory" + Fore.RESET + "-----------")
	if(items[1][0] != -1):
		print("Main hand: " + str(toolsName[0][items[1][0]]))
		if(items[1][2] != 0):
			print("    (+ " + str(item[1][2] + " atk"))
	if(items[1][1] != -1):
		print("Second hand: " + str(toolsName[1][items[1][1]]))
	print("------------------------------")
	b = input()
	if(b == ""):
		inv(stones, maxhp, defense, atk, items, hp)
	if(int(b) == 0):
		pass
	if(int(b) == 1 and stones[0] > 0):
		maxhp += 5
		stones[0] -= 1
	elif(int(b) == 2 and stones[1] > 0):
		atk += 2
		stones[1] -= 1
	elif(int(b) == 3 and stones[2] > 0):
		defense += 1
		stones[2] -= 1
	elif(int(b) == 5 and items[0][1] > 0):
		items[0][1] -= 1
		hp += 7
	else:
		pass
	items = [maxhp, atk, defense, stones, items, hp]
	return items

def Workshop(shards, stones):
	os.system('cls')
	print("------------" + Fore.CYAN + "Stones" + Fore.RESET + "------------")
	print("1) Craft a water stone(30 shards)")
	print("2) Craft a sun stone(30 shards)")
	print("3) Craft a air stone(30 shards)")
	print("------------------------------")
	a = input()
	if(int(a) == 0):
		pass
	if(int(a) == 1 and shards[0] > 29):
		stones[0] += 1
		shards[0] -= 30
	elif(int(a) == 2 and shards[1] > 29):
		stones[1] += 1
		shards[1] -= 30
	elif(int(a) == 3 and shards[2] >29):
		stones[2] += 1
		shards[2] -= 30
	else:
		print("Error or not enough shards")
		input()
		pass
	items = [stones, shards]
	return item

def cites(cityId, cites, items, money):
	os.system('cls')
	os.system('clear')
	print("            " + Fore.GREEN + Style.DIM + str(cites[cityId][0]))
	print("1) Upgrade items")
	b = input()
	if(int(b) == 1):
		print("1) Upgrade sword(550 money)(+10 atk)")
		print("2) Upgrade shield(700 money)(+7 defense)")
		b = input()
		if(int(b) == 1 and money > 549 and items[1][0] != -1):
			items[1][2] += 10
			money -= 550
		elif(int(b) == 2 and money > 699 and items[1][0] != -1):
			items[1][3] += 7
			money -= 700
	else:
		pass
	items = [items, money]
	return items