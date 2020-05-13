import getEvent
import random
import shop
import os
from colorama import Fore, init, Style

showItems = True
autosave = False
mob = []
speed = 5
hp = 100
maxhp = 100
spwnId = -2
defense = 5
atk = 10
xp = 0
lvl = 1
waves = 1
i = 0 # счетчик
money = 0
buffs = [0,0,0] # atk, def, maxhp
currMob = []
items = [[0,0], [-1, -1]] # drop[Bone, Meat], equipment[swordId, shieldId]
dropList = [["Bone",5,30], ["Meat",2,50], ["Exp", 10, 20]] # [dropId,maxCount, dropChance]
monstersList = [["Small", 3, 50], ["Big", 3, 10], ["Strong", 3, 30], ["Fast", 3, 10], ['Zombie', 5, 50], ['Skeleton', 5, 30], ['Big zombie', 5, 10], ['Mega zombie', 7, 10]] # monsterName[maxLvl, rateSpawn]
dungMonsList = [['Dead', 3, 50], ['Mag', 3, 30], ['Necromancer', 3, 15]]
shards = [0, 0, 0] # water, sun, air
stones = [0, 0, 0] # ^^^^^^^^^^^^^^^
eventList = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
eventList = ["upHP", "upDef", "upAtk"
			 "upDrop", "upRateSpawn", "upLvlMonsters",
			 "downHp", "downDef", "downAtk",
			 "downDrop", "downRateSpawn", "downLvlMonsters",
			 "maxMobInChunk+", "maxMobInChunk-"]
monstersInfo = [[0, 4, 20, 1, 2], [1, 5, 35, 3, 1], [2, 7, 27, 2, 2], [3, 3, 22, 1, 5], [4, 10, 35, 1, 1], [5, 12, 40, 3, 2], [5, 10, 50, 3, 0], [6, 20, 60, 5, 4]] # SpawnId, atk, hp, def, speed
				# Small			   Big				Strong			  Fast				Zombie             Skeleton           Big zombie         Mega zombie
dungMonsInfo = [[0, 6, 30, 3, 3], [1, 8, 35, 1, 3], [2, 12, 35, 1, 4]]
mobsInChank = [] # SpawnId, lvl
maxMobInChunk = 5
citesList = [["One", 134, 20], ["Two", 20, 1]] # City name, x, y

weather = getEvent.getWeather()
event = getEvent.setEvent()

chunkList = open('gen.txt')

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
def mobSpawn(isdung):
	global i, spwnId, waves
	i = 0
	if(waves < 21):
		for i in range(0, 2):
			if(random.randrange(0, 100) <= monstersList[i][2]):
				spwnId = i
				break
		if(i > 2):
			spwnId = -1
	elif(isdung == True):
		i = 0
		for i in range(0, 2):
			if(random.randrange(0, 100) <= dungMonsList[i][2]):
				spwnId = i
				break
		if(i > 2):
			spwnId = -1
	else:
		i = 3
		for i in range(3, 6):
			if(random.randrange(0, 100) <= monstersList[i][2]):
				spwnId = i
				break
		if(i > 6):
			spwnId = -1
	return spwnId
def spawnChunk(isdung):
	global spwnId, waves, lvl, infoChunk, dungChunk
	waves += 1
	i = 0
	mobsInChank.clear()
	for i in range(0, maxMobInChunk):
		spwnId = mobSpawn(isdung)
		if(spwnId == -1):
			print("Monster: None")
		elif(spwnId >= 0 and isdung == True):
			name = dungMonsList[spwnId][0]
			monsLvl = random.randrange(1, 3)
			mobsInChank.append([spwnId, name, monsLvl])
		elif(spwnId >= 0 and isdung != True):
			name = monstersList[spwnId][0]
			if(lvl > 4):
				minlvl = 2
			else:
				minlvl = 1
			if(waves >= 29):
				maxlvl = 7
			elif(waves > 19 and waves < 29):
				maxlvl = 5
			else:
				maxlvl = 3
			monsLvl = random.randrange(minlvl, maxlvl)
			if(waves == 20 and dungChunk[0] != 2):
				mobsInChank.append([0, monstersList[0][0], random.randrange(4,5)])
			else:
				mobsInChank.append([spwnId, name, monsLvl])
	if(autosave == True):
		save()
def infoMob(num, isdung):
	if(isdung != True):
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
		if(mobsInChank[num][0] == monstersInfo[4][0]):
			mob = monstersInfo[4]
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
		if(mobsInChank[num][0] == monstersInfo[5][0]):
			mob = monstersInfo[5]
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
		if(mobsInChank[num][0] == monstersInfo[6][0]):
			mob = monstersInfo[6]
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
	elif(isdung == True):
		if(mobsInChank[num][0] == dungMonsInfo[0][0]):
			mob = dungMonsInfo[0]
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
		if(mobsInChank[num][0] == dungMonsInfo[1][0]):
			mob = dungMonsInfo[1]
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
		if(mobsInChank[num][0] == dungMonsInfo[2][0]):
			mob = dungMonsInfo[2]
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

def attackMob(num, isdung):
	global currMob, hp, shards, money, xp, items, dungChunk, atk
	print("You attack a " + str(mobsInChank[num][1] + " Monster"))
	currMob.append(infoMob(num, isdung))
	hpE = currMob[0][2]
	while hp > 0:
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
			if(isdung == True):
				rand = random.randrange(0, 100)
				if(rand >= 25 and rand <= 30):
					print("A dungeon sword has been dropped!(+40 atk)")
					print("Equip?")
					print("1) Yes, 2) No")
					b = input()
					if(int(b) == 1):
						items[1][0] = 'D'
					else:
						pass
			if(event[2] == 0):
				shards[0] += random.randrange(1,3)
				if(isdung == True):
					shards[0] += random.randrange(1,3)
			elif(event[2] == 1):
				shards[1] += random.randrange(1,3)
				if(isdung == True):
					shards[1] += random.randrange(1,3)
			elif(event[2] == 2):
				shards[2] += random.randrange(1,3)
				if(isdung == True):
					shards[2] += random.randrange(1,3)
			buffMoney = mobsInChank[num][2] * 4
			if(infoChunk[0] == 1):
				buffMoney += random.randrange(30, 100)
			if(lvl > 4):
				buffMoney += random.randrange(10,20)
			if(waves > 19):
				minMoney = 15
			else:
				minMoney = 1
			getmoney = random.randrange(minMoney, 50)
			getmoney += buffMoney
			money += getmoney
			print("You get " + Fore.YELLOW + str(getmoney) + Fore.RESET + " money")
			items[0][0] += random.randrange(0, dropList[0][1])
			items[0][1] += random.randrange(0, dropList[1][1])
			xp += random.randrange(1, dropList[2][1])
			del mobsInChank[num]
			break
		dmg = 0
		dmg = currMob[0][1] - random.randrange(0, defense) - buffs[1]
		if(dmg < 0):
			dmg = 0
		if((random.randrange(0, 10) + 1) > speed):
			hp -= dmg
			print("- " + str(dmg) + " hp to you.")
		else:
			print("You dont take damage")
		print("You hp is: " + str(hp))
		if(hp < 1):
			quit()
	currMob.clear()
	if(isdung == True):
		dung(items, mobsInChank)
def menu():
	global showItems, autosave, hp, maxhp, defense, atk, xp, lvl, money, waves, items, stones, shards
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
		hp = 100
		maxhp = 100
		defense = 5
		atk = 10
		xp = 0
		lvl = 1
		money = 0
		waves = 1
		items = [[0,0], [-1, -1]]
		stones = [0,0,0]
		shards = [0,0,0]
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
def checkChunk():
	global waves, infoChunk
	thisChunk = infoChunk[waves - 1]
	nextChunk = infoChunk[waves]
	dungChunk = [thisChunk, nextChunk]
	return dungChunk

def dung(items, mobsInChank):
	global hp
	if(mobsInChank == []):
		main()
	os.system('cls')
	os.system('clear')
	print("HP: " + str(hp))
	print("-----------" + Fore.CYAN + "Monsters" + Fore.RESET + "-----------")
	for a in range(0, len(mobsInChank)):
		print(str(a) + ") Monster: " + str(mobsInChank[a][1]) + ", Lvl: " + str(mobsInChank[a][2]))
	print("------------------------------")
	print("Enter 'exit' for exit")
	print("Enter number of a Monster to attack him: ")
	b = input()
	if(b == 'exit'):
		main()
	elif(b == ""):
		dung(items, mobsInChank)
	elif(int(b) > len(mobsInChank)):
		dung(items, mobsInChank)
	else:
		isdung = True
		attackMob(int(b), isdung)

infoChunk = chunkList.read().split()
dungChunk = checkChunk()
spawnChunk(isdung = False)
def main():
	global hp, maxhp, atk, defense, monstersInfo, monstersList, shards, stones, money, items, xp, lvl, dungChunk, speed, waves
	if(waves > len(infoChunk)):
		print("Wow! Max waves? Very good! But...")
		waves = 1
		money += 100000
	while hp > 0:
		buffs[1] = 0
		buffs[0] = 0
		eventHandler(event)
		if(items[1][0] == 0):
			buffs[0] += 10
		elif(items[1][0] == 1):
			buffs[0] += 15
		elif(items[1][0] == 2):
			buffs[0] += 25
		elif(items[1][0] == 'D'):
			buffs[0] += 40
		if(items[1][1] == 0):
			buffs[1] += 5
		elif(items[1][1] == 1):
			buffs[1] += 7
		elif(items[1][1] == 2):
			buffs[1] += 13
		os.system('cls')
		os.system('clear')
		if(mobsInChank == []):
			dungChunk = checkChunk()
			spawnChunk(isdung = False)
		if(int(dungChunk[0]) == 2):
			print("------------------------------")
			print("    This chunk is dungeon     ")
			print("            Enter?            ")
			print("0) Yes")
			print("1) No")
			print("2) Heal 50 hp(40 money, you have " + str(money) + " money and " + str(hp) + " hp") 
			print("------------------------------")
			b = input()
			if(int(b) == 0):
				spawnChunk(isdung = True)
				dung(items, mobsInChank)
			if(int(b) == 1):
				pass
			if(int(b) == 2 and money > 39 and hp < maxhp):
				hp += 50
				money -= 40
				if(hp > maxhp):
					hp = maxhp
				main()
		print("Event today: " + str(eventList[event[0]]))
		if(hp > maxhp):
			hp = maxhp
		if(xp > 99):
			lvl += 1
			xp -= 100
			atk += 3
			defense += 2
			hp = maxhp
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
		print("-------------" + Fore.CYAN + "Info" + Fore.RESET + "-------------")
		print("    This chunk is ", end = '')
		if(int(dungChunk[0]) == 0):
			print("empty", end = '')
		elif(int(dungChunk[0]) == 1):
			print("with chest", end = '')
		else:
			print("dungeon")
		print(", next chunk is ", end='')
		if(int(dungChunk[1]) == 0):
			print("empty")
		elif(int(dungChunk[1]) == 1):
			print("with chest")
		else:
			print("dungeon")
		print("    Money: " + Fore.YELLOW + str(money))
		print("----------" + Fore.CYAN + "Your stats" + Fore.RESET + "----------")
		print("    HP: " + Fore.RED + str(hp) + Fore.RESET + "/" + Fore.RED + str(maxhp + buffs[2]))
		print("    Speed: " + Fore.WHITE + str(speed))
		print("    Defense: " + Fore.WHITE + Style.DIM + str(defense) + " + " + str(buffs[1]))
		print("    Strength: " + Fore.BLUE + str(atk) + " + " + str(buffs[0]))
		print("    Exp: " + Fore.GREEN + str(xp) + Fore.RESET + "/" + Fore.GREEN + "100" + Fore.RESET + "; Lvl: " + Fore.MAGENTA + str(lvl))
		print("    Waves: " + str(waves))
		print("-----------" + Fore.CYAN + "Monsters" + Fore.RESET + "-----------")
		for a in range(0, len(mobsInChank)):
			print(str(a) + ") Monster: " + str(mobsInChank[a][1]) + ", Lvl: " + str(mobsInChank[a][2]))
		print("------------------------------")
		print("Q) Quit")
		print("0) Menu")
		print("1) Attack")
		print("2) Heal 50 HP(40 money)")
		print("3) Workshop")
		print("4) Open inventory")
		print("5) Shop")
		print("6) Save")
		try:
			b = input()
			if(b == ""):
				main()
			if(b == "Q" or b == 'q'):
				quit()
			if(int(b) == 0):
				menu()
			if(int(b) == 1):
				print("Enter number of monster: ")
				c = input()
				if(c == ""):
					main()
				if(int(c) > len(mobsInChank)):
					main()
				else:
					attackMob(int(c), isdung = False)
			elif(int(b) == 2 and money > 39 and hp < maxhp):
				money -= 40
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
		except ValueError:
			main()
menu()