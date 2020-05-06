import getEvent
import random
import shop
import os
from colorama import Fore, init, Style

showItems = True
autosave = False
mob = []
hp = 100
maxhp = 100
spwnId = -2
defense = 5
atk = 10
xp = 0
lvl = 1
waves = 0
i = 0 # счетчик
money = 0
buffs = [0,0,0] # atk, def, maxhp
currMob = []
items = [[0,0], [-1, -1]] # drop[Bone, Meat], equipment[swordId, shieldId]
dropList = [["Bone",5,30], ["Meat",2,50], ["Exp", 10, 20]] # [dropId,maxCount, dropChance]
monstersList = [["Small", 3, 50], ["Big", 3, 10], ["Strong", 3, 30], ["Fast", 3, 10]] # monsterName[maxLvl, rateSpawn]
shards = [0, 0, 0] # water, sun, air
stones = [0, 0, 0] # ^^^^^^^^^^^^^^^
eventList = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
eventList = ["upHP", "upDef", "upAtk"
			 "upDrop", "upRateSpawn", "upLvlMonsters",
			 "downHp", "downDef", "downAtk",
			 "downDrop", "downRateSpawn", "downLvlMonsters",
			 "maxMobInChunk+", "maxMobInChunk-"]
monstersInfo = [[0, 4, 20, 1, 2], [1, 5, 35, 3, 1], [2, 7, 27, 2, 2], [3, 3, 22, 1, 5]] # SpawnId, atk, hp, def, speed
				# Small			   Big				Strong			  Fast				
mobsInChank = [] # SpawnId, lvl
maxMobInChunk = 5
citesList = [["One", 134, 20], ["Two", 20, 1]] # City name, x, y

weather = getEvent.getWeather()
event = getEvent.setEvent()

init(autoreset=True)

def eventHandler(event):
	global hp, defense, atk, dropList, monstersList
	if(event[0] == "upHP"):
		buffs[2] += 10
	elif(event[0] == "upDef"):
		buffs[1] += 3
	elif(event[0] == "upAtk"):
		buffs[0] += 5
	elif(event[0] == "upDrop"):
		dropList[2][1] += 10
	elif(event[0] == "upRateSpawn"):
		monstersList[0][2] += 20
	elif(event[0] == "upLvlMonsters"):
		monstersList[0][1] += 2
		monstersList[1][1] += 2
		monstersList[2][1] += 2
		monstersList[3][1] += 2
	elif(event[0] == "downHP"):
		buffs[2] -= 10
	elif(event[0] == "downDef"):
		buffs[1] -= 2
	elif(event[0] == "downAtk"):
		buffs[0] -= 3
	elif(event[0] == "downDrop"):
		dropList[1][1] -= 1
	elif(event[0] == "downRateSpawn"):
		monstersList[0][2] -= 15
	else:
		monstersList[1][1] -= 1
	if(event[1] == "maxMobInChunk+"):
		maxMobInChunk += 2
	elif(event[1] == "maxMobInChunk-"):
		maxMobInChunk -= 2
def mobSpawn():
	global i, spwnId
	for i in range(0, 3):
		if(random.randrange(0, 100) <= monstersList[i][2]):
			spwnId = i
			break
	if(i > 3):
		spwnId = -1
	return spwnId
def spawnInChunk():
	global spwnId, waves
	waves += 1
	i = 0
	mobsInChank.clear()
	for i in range(0, maxMobInChunk):
		spwnId = mobSpawn()
		if(spwnId == -1):
			print("Monster: None")
		elif(spwnId >= 0):
			name = monstersList[spwnId][0]
			monsLvl = random.randrange(1, 3)
			mobsInChank.append([spwnId, name, monsLvl])
	if(autosave == True):
		save()
def infoMob(num):
	if(mobsInChank[num][0] == monstersInfo[0][0]):
		mob = monstersInfo[0]
		if(mobsInChank[num][2] == 2):
			mob[1] += 2
			mob[2] += 15
		if(mobsInChank[num][2] == 3):
			mob[1] += 4
			mob[2] += 19
		if(mobsInChank[num][2] == 4):
			mob[1] += 5
			mob[2] += 22
		if(mobsInChank[num][2] == 5):
			mob[1] += 7
			mob[2] += 25
		return mob
	if(mobsInChank[num][0] == monstersInfo[1][0]):
		mob = monstersInfo[1]
		if(mobsInChank[num][2] == 2):
			mob[1] += 2
			mob[2] += 12
		if(mobsInChank[num][2] == 3):
			mob[1] += 3
			mob[2] += 13
		if(mobsInChank[num][2] == 4):
			mob[1] += 5
			mob[2] += 15
		if(mobsInChank[num][2] == 5):
			mob[1] += 6
			mob[2] += 19
		return mob
	if(mobsInChank[num][0] == monstersInfo[2][0]):
		mob = monstersInfo[2]
		if(mobsInChank[num][2] == 2):
			mob[1] += 1
			mob[2] += 15
		if(mobsInChank[num][2] == 3):
			mob[1] += 1
			mob[2] += 19
		if(mobsInChank[num][2] == 4):
			mob[1] += 3
			mob[2] += 22
		if(mobsInChank[num][2] == 5):
			mob[1] += 5
			mob[2] += 25
		return mob
	if(mobsInChank[num][0] == monstersInfo[3][0]):
		mob = monstersInfo[3]
		if(mobsInChank[num][2] == 2):
			mob[1] += 3
			mob[2] += 16
		if(mobsInChank[num][2] == 3):
			mob[1] += 5
			mob[2] += 20
		if(mobsInChank[num][2] == 4):
			mob[1] += 6
			mob[2] += 25
		if(mobsInChank[num][2] == 5):
			mob[1] += 8
			mob[2] += 28
		return mob
def attackMob(num, atk):
	global currMob, hp, shards, money, xp, items
	print("You attack a " + str(mobsInChank[num][1] + " Monster"))
	currMob.append(infoMob(num))
	hpE = currMob[0][2]
	while hpE > 0 or hp > 0:
		if( ( random.randrange(0,10) + 1 ) > currMob[0][4]):
			dmg = atk - random.randrange(0, currMob[0][3]) + buffs[0]
			if(dmg < 0):
				dmg = 0
			hpE -= dmg
			print("- " + str(dmg) + " hp to monster.")
			print("His hp is: " + str(hpE))	
		else:
			print("Monster not take damage")
		if(hpE < 1):
			if(event[2] == 0):
				shards[0] += random.randrange(1,3)
			if(event[2] == 1):
				shards[1] += random.randrange(1,3)
			if(event[2] == 2):
				shards[2] += random.randrange(1,3)
			buffMoney = mobsInChank[num][2] * 3
			money += random.randrange(1, ( 50 + buffMoney ))
			items[0][0] += random.randrange(0, dropList[0][1])
			items[0][1] += random.randrange(0, dropList[1][1])
			xp += random.randrange(0, dropList[2][1])
			del mobsInChank[num]
			break
		dmg = 0
		dmg = currMob[0][1] - random.randrange(0, defense) - buffs[1]
		if(dmg < 0):
			dmg = 0
		hp -= dmg
		print("- " + str(dmg) + " hp to you.")
		print("You hp is: " + str(hp))
		if(hp < 1):
			break
	currMob.clear()
def menu():
	global showItems, autosave
	print("1. Load save")
	print("2. New game")
	print("3. Settings")
	b = input()
	if(int(b) == 1):
		f = open('save.txt')
		i = 0
		for line in f:
			i += 1
			if(i == 1):
				hp = int(line)
			if(i == 2):
				maxhp = int(line)
			if(i == 3):
				defense = int(line)
			if(i == 4):
				atk = int(line)
			if(i == 5):
				xp = int(line)
			if(i == 6):
				lvl = int(line)
			if(i == 7):
				money = int(line)
			if(i == 8):
				waves = int(line)
		f.close()
		f = open('savem.txt')
		i = 0
		for line in f:
			i += 1
			if(i == 1):
				items[0][0] = int(line)
			if(i == 2):
				items[0][1] = int(line)
			if(i == 3):
				items[1][0] = int(line)
			if(i == 4):
				items[1][1] = int(line)
			if(i == 5):
				shards[0] = int(line)
			if(i == 6):
				shards[1] = int(line)
			if(i == 7):
				shards[2] = int(line)
			if(i == 8):
				stones[0] = int(line)
			if(i == 9):
				stones[1] = int(line)
			if(i == 10):
				stones[2] = int(line)

		f.close()
		main()
	if(int(b) == 2):
		main()
	if(int(b) == 3):
		print("1. Show Items(T/F)")
		print("2. Autosave every wave(T/F)")
		b = input()
		if(int(b) == 1):
			if(showItems):
				showItems = False
			else:
				showItems = True
		if(int(b) == 2):
			if(autosave):
				autosave = False
			else:
				autosave = True
		menu()
def save():
	f = open('save.txt', 'tw', encoding='utf-8')
	f.write(str(hp) + '\n')
	f.write(str(maxhp) + '\n')
	f.write(str(defense) + '\n')
	f.write(str(atk) + '\n')
	f.write(str(xp) + '\n')
	f.write(str(lvl) + '\n')
	f.write(str(money) + '\n')
	f.write(str(waves) + '\n')
	f.close()
	f = open('savem.txt', 'tw', encoding='utf-8')
	for x in range(0, len(items[0])): f.write(str(items[0][x]) + '\n')
	for x in range(0, len(items[1])): f.write(str(items[1][x]) + '\n')
	for x in range(0, len(shards)): f.write(str(shards[x]) + '\n')
	for x in range(0, len(stones)): f.write(str(stones[x]) + '\n')
	f.close()

spawnInChunk()
def main():
	global hp, maxhp, atk, defense, monstersInfo, monstersList, shards, stones, money, items, xp, lvl
	while hp > 0:
		buffs[1] = 0
		buffs[0] = 0
		eventHandler(event)
		if(items[1][0] == 0):
			buffs[0] += 3
		elif(items[1][0] == 1):
			buffs[0] += 5
		if(items[1][1] == 0):
			buffs[1] += 2
		elif(items[1][1] == 1):
			buffs[1] += 3
		os.system('cls')
		os.system('clear')
		print("Event today: " + str(eventList[event[0]]))
		if(mobsInChank == []):
			spawnInChunk()
		if(hp > maxhp):
			hp = maxhp
		if(xp > 99):
			lvl += 1
			xp -= 100
			atk += 3
			defense += 1
		if(showItems == True):
			print("------------" + Fore.CYAN + "Items" + Fore.RESET + "-------------")
			if(shards[0] != 0):	
				print("    Water shards: " + str(shards[0]))
			if(shards[1] != 0):	
				print("    Sun shards: " + str(shards[1]))
			if(shards[2] != 0):	
				print("    Air shards: " + str(shards[2]))
			if(stones[0] != 0):	
				print("    Water stones: " + str(stones[0]))
			if(stones[1] != 0):	
				print("    Sun stones: " + str(stones[1]))
			if(stones[2] != 0):	
				print("    Air stones: " + str(stones[2]))
			if(items[0] != 0):
				print("    Bones: " + str(items[0][0]))
			if(items[1] != 0):
				print("    Meat: " + str(items[0][1]))
		print("    Money: " + Fore.YELLOW + str(money))
		print("----------" + Fore.CYAN + "Your stats" + Fore.RESET + "----------")
		print("    HP: " + Fore.RED + str(hp) + Fore.RESET + "/" + Fore.RED + str(maxhp + buffs[2]))
		print("    Defense: " + Fore.WHITE + Style.DIM + str(defense) + " + " + str(buffs[1]))
		print("    Strength: " + Fore.BLUE + str(atk) + " + " + str(buffs[0]))
		print("    Exp: " + Fore.GREEN + str(xp) + Fore.RESET + "/" + Fore.GREEN + "100" + Fore.RESET + "; Lvl: " + Fore.MAGENTA + str(lvl))
		print("    Waves: " + str(waves))
		print("-----------" + Fore.CYAN + "Monsters" + Fore.RESET + "-----------")
		for a in range(0, len(mobsInChank)):
			print(str(a) + ") Monster: " + str(mobsInChank[a][1]) + ", Lvl: " + str(mobsInChank[a][2]))
		print("------------------------------")
		print("0) Menu")
		print("1) Attack")
		print("2) Heal 50 HP(15 money)")
		print("3) Workshop")
		print("4) Open inventory")
		print("5) Shop")
		print("6) Save")
		b = input()
		if(b == ""):
			main()
		if(int(b) == 0):
			menu()
		if(int(b) == 1):
			print("Enter number of monster: ")
			c = input()
			if(int(c) > len(mobsInChank)):
				main()
			else:
				attackMob(int(c), atk)
		elif(int(b) == 2 and money > 14):
			money -= 15
			hp += 50
		elif(int(b) == 3):
			newItem = shop.Workshop(shards, stones)
			shards = newItem[1]
			stones = newItem[0]
		elif(int(b) == 4):
			newItem = shop.inv(stones, maxhp, defense, atk, items, hp)
			maxhp = newItem[0]
			atk = newItem[1]
			defense = newItem[2]
			stones = newItem[3]
			items = newItem[4]
			hp = newItem[5]
		elif(int(b) == 5):
			newItem = shop.shop(money, stones, items)
			money = newItem[0]
			stones = newItem[1]
			items = newItem[2]
		elif(int(b) == 6):
			save()
		else:
			main()
menu()