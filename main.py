import getEvent
import random
import shop
import os
from colorama import Fore, init, Style
import pickle
import socket

sock = socket.socket()
BUFFER_SIZE = 4096
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
items = [[0,0], [-1, -1, 0, 0]] # drop[Bone, Meat], equipment[swordId, shieldId, upgradeSword, upgradeShield]
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
citesList = [["One", 0], ["Two", 0]] # City name, unlocked?(0 - False, 1 - True)
# Cards types: 0 - attack, 1 - def, 2 - heal
allCards = [[0, "Basic attack", 0, 0], [1, "Basic shield", 1, 0], [2, "Basic heal", 2, 0], [3, "Ultra attack", 0, 1], [4, "Heal potion", 2, 1]] # IdCard, Name, Type, id in allCardInfo
allCardsInfo = [[[0, 10], [1, 50]], [[0, 5]], [[0, 20]]] # AtkType[id, points], DefType[id, points], HealType[id, points]
plDeck = [] # Card id

cityH = shop.cites

weather = getEvent.getWeather()
event = getEvent.setEvent()

chunkList = open('gen.txt')

init(autoreset=True)

def sandboxAI(hp, hpE):
	idC = -1
	if hp < 20:
		idC = 0
	elif hpE < 51:
		idC = 2
	else:
		idC = 0
	return idC

def sandbox(plDeck):
	global allCards, allCardsInfo
	os.system('cls')
	os.system('clear')
	print(" Enter maxhp opponent")
	maxhpE = int(input())
	# print(" Enter atk opponent")
	# atkE = int(input())
	print(" Enter defense opponent")
	defE = int(input())
	# print(" Enter speed opponent")
	# spdE = int(input())
	hpE = maxhpE
	print(" Enter your maxhp")
	maxhp = int(input())
	# print(" Enter atk opponent")
	# atkE = int(input())
	print(" Enter your defense")
	defense = int(input())
	hp = maxhp
	currCard = [0]
	currDeck = plDeck
	turn = True
	while hpE > 0:
		os.system('cls')
		os.system('clear')
		print("   Enemy info: ")
		print(" HP: " + str(hpE) + "/" + str(maxhpE))
		print(" Defense: " + str(defE))
		print("   Your info: ")
		print(" HP: " + str(hp) + "/" + str(maxhp))
		print(" Defense: " + str(defense))
		print("   Your deck: ")
		for x in range(len(currDeck)):
			if(currDeck[x] != -1):
				print(str(allCards[currDeck[x]][0]) + ") " + str(allCards[currDeck[x]][1]))
		if(turn == True):
			b = input()
			idC = int(b)
			x = 0
			for x in range(len(allCards)):
				if(allCards[x][0] == idC):
					currCard = allCardsInfo[allCards[x][2]][allCards[x][3]]
					typeId = allCards[x][2]
					nxt = False
					for p in range(len(currDeck)):
						if(int(currDeck[p]) == int(idC)):
							nxt = True
							# del currDeck[p]
							break
					# currCard = [id, points]
					break
			if(nxt == True):
				if(typeId == 0):
					hpE -= currCard[1]
				elif(typeId == 1):
					defense += currCard[1]
				elif(typeId == 2):
					hp += currCard[1]
					if(hp > maxhp):
						hp = maxhp
				turn = False
			elif(nxt == False):
				currDeck = plDeck
		else:
			idC = sandboxAI(hp, hpE)
			x = 0
			for x in range(len(allCards)):
				if(allCards[x][0] == idC):
					print(x)
					currCard = allCardsInfo[allCards[x][2]][allCards[x][3]]
					typeId = allCards[x][2]
					print(currCard)
					# currCard = [id, points, type]
					break
			if(typeId == 0):
				hp -= currCard[1]
			elif(typeId == 1):
				defE += currCard[1]
			elif(typeId == 2):
				hpE += currCard[1]
				if(hpE > maxhpE):
					hpE = maxhpE
			turn = True
		if(hp < 1):
			break
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
	global currMob, hp, shards, money, xp, items, dungChunk, atk, plDeck, allCards
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
				if(rand >= 50 and rand <= 60):
					print("You got a random card!")
					dropCard = random.randrange(0, len(allCards))
					plDeck.append(dropCard)
					print("You got a " + str(allCards[dropCard][1]))
					input()
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

def server():
	global hp, defense, atk
	sock.bind(('', 9090))
	sock.listen(1)

	while True:
		conn, addr = sock.accept()
		print('Connected:', addr)

		all_data = bytearray()
		while True:
				data = conn.recv(BUFFER_SIZE)
				if not data:
					break
				print('Recv: {}: {}'.format(len(data), data))
				all_data += data

		obj = pickle.loads(all_data)
		conn.close()
		break
	hpE = obj[0]
	defE = obj[1]
	atkE = obj[2]
	while True:
		print("------------")
		print("My hp: " + str(hp))
		print("My defense: " + str(defense))
		print("My atk: " + str(atk))
		print("------------")
		print("Enemy hp: " + str(hpE))
		print("Defense enemy: " + str(defE))
		print("Atk enemy: " + str(atkE))
		print("------------")
		dmg = atk - random.randrange(0, defE)
		if dmg < 1:
			dmg = 0
		hpE -= dmg
		dmg = atkE - random.randrange(0, defense)
		if dmg < 1:
			dmg = 0
		hp -= dmg
		if hpE < 1:
			print("     You win!!!")
			input()
			money += 100
			hp = maxhp
			break
		if hp < 1:
			print("You lose")
			hp = maxhp
			break
	input()
	menu()
def client():
	print("Enter ip")
	ip = input()
	sock.connect((ip, 9090))
	obj = [hp, defense, atk, hpE]
	data = pickle.dumps(obj)
	sock.sendall(data)
	sock.close()

def menu():
	global plDeck, showItems, autosave, hp, maxhp, defense, atk, xp, lvl, money, waves, items, stones, shards
	print("1. Load save")
	print("2. New game")
	print("3. Options")
	print("4. Info about current world generation")
	print("5. Multiplayer")
	b = input()
	if(b == ""):
		menu()
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
				items[1][2] = int(line)
			if(i == 6):
				items[1][3] = int(line)
			if(i == 7):
				shards[0] = int(line)
			if(i == 8):
				shards[1] = int(line)
			if(i == 9):
				shards[2] = int(line)
			if(i == 10):
				stones[0] = int(line)
			if(i == 11):
				stones[1] = int(line)
			if(i == 12):
				stones[2] = int(line)
			if(i > 12):
				plDeck.append(int(line))
		f.close()
		main()
	elif(int(b) == 2):
		hp = 100
		maxhp = 100
		defense = 5
		atk = 10
		xp = 0
		lvl = 1
		money = 0
		waves = 1
		items = [[0,0], [-1, -1, 0, 0]]
		stones = [0,0,0]
		shards = [0,0,0]
		plDeck = []
		main()
	elif(int(b) == 3):
		print("1) Settings")
		print("2) Sandbox")
		b = input()
		if(int(b) == 1):
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
		elif(int(b) == 2 and plDeck != []):
			sandbox(plDeck)
		elif(plDeck == []):
			print("You don't have cards")
		menu()
	elif(int(b) == 4):
		i = 0
		for z in range(0, len(infoChunk)):
			if(int(infoChunk[z]) == 3):
				print("City one at " + str(z) + " chunk")
			elif(int(infoChunk[z]) == 4):
				print("City two at " + str(z) + " chunk")
	elif(int(b) == 5):
		print("1) Create server")
		print("2) Connect")
		b = input()
		if(int(b) == 1):
			server()
		elif(int(b) == 2):
			client()
	else:
		menu()
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
	for x in range(0, len(plDeck)): f.write(str(plDeck[x]) + '\n')
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
chunkList.close()
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
			buffs[0] += items[1][2]
		elif(items[1][0] == 1):
			buffs[0] += 15
			buffs[0] += items[1][2]
		elif(items[1][0] == 2):
			buffs[0] += 25
			buffs[0] += items[1][2]
		elif(items[1][0] == 'D'):
			buffs[0] += 40
			buffs[0] += items[1][2]
		if(items[1][1] == 0):
			buffs[1] += 5
			buffs[1] += items[1][3]
		elif(items[1][1] == 1):
			buffs[1] += 7
			buffs[1] += items[1][3]
		elif(items[1][1] == 2):
			buffs[1] += 13
			buffs[1] += items[1][3]
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
		if(int(infoChunk[waves]) == 3):
			print("You unlocked city " + str(citesList[0][0]))
			citesList[0][1] = 1
		elif(int(infoChunk[waves]) == 4):
			print("You unlocked city " + str(citesList[1][0]))
			citesList[1][1] = 1
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
		if(citesList[0][1] == 1 or citesList[1][1] == 1):
			print("7) Teleport")
		try:
			b = input()
			if(b == ""):
				main()
			if(b == "Q" or b == 'q'):
				save()
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
			if(int(b) == 7):
				if(citesList[0][1] == 1):
					print("1) Tp to city " + str(citesList[0][0]))
				if(citesList[1][1] == 1):
					print("2) Tp to city " + str(citesList[1][0]))
				if(citesList[0][1] == 1 or citesList[1][1] == 1):
					b = input()
					if(int(b) == 1):
						newItem = cityH(0, citesList, items, money)
						items = newItem[0]
						money = newItem[1]
					elif(int(b) == 2):
						newItem = shop.cites(1, citesList, items, money)
						items = newItem[0]
						money = newItem[1]
					else:
						pass
				main()
			else:
				main()
		except ValueError:
			main()
menu()