import getEvent
import random
import shop
import os
from colorama import Fore, init, Style

mob = []
hp = 100
maxhp = 100
spwnId = -2
defense = 5
atk = 10
i = 0 # счетчик
money = 0
currMob = []
dropList = [["Bone",5,30], ["Meat",2,50], ["Exp",210, 20]] # [dropId,maxCount, dropChance]
monstersList = [["Small", 3, 50], ["Big", 3, 10], ["Strong", 3, 30], ["Fast", 3, 10]] # monsterName[maxLvl, rateSpawn]
shards = [0, 0, 0] # water, sun, air
stones = [0, 0, 0] # ^^^^^^^^^^^^^^^
eventList = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
eventList = ["upHP", "upDef", "upAtk"
			 "upDrop", "upRateSpawn", "upLvlMonsters",
			 "downHp", "downDef", "downAtk",
			 "downDrop", "downRateSpawn", "downLvlMonsters",
			 "maxMobInChunk+", "maxMobInChunk-"]
monstersInfo = [[0, 4, 20, 1, 3], [1, 5, 35, 3, 1], [2, 7, 27, 2, 2], [3, 3, 22, 1, 5]] # SpawnId, atk, hp, def, speed
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
		hp += 10
	elif(event[0] == "upDef"):
		defense += 3
	elif(event[0] == "upAtk"):
		atk += 5
	elif(event[0] == "upDrop"):
		dropList[2][1] += 10
	elif(event[0] == "upRateSpawn"):
		monstersList[0][2] += 20
	elif(event[0] == "upLvlMonsters"):
		monstersList[0][1] += 3
		monstersList[1][1] += 1
		monstersList[2][1] += 2
		monstersList[3][1] += 3
	elif(event[0] == "downHP"):
		hp -= 10
	elif(event[0] == "downDef"):
		defense -= 2
	elif(event[0] == "downAtk"):
		atk -= 3
	elif(event[0] == "downDrop"):
		dropList[2][1] -= 3
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
	global spwnId
	i = 0
	mobsInChank.clear()
	for i in range(0, maxMobInChunk):
		spwnId = mobSpawn()
		if(spwnId == -1):
			print("Monster: None")
		elif(spwnId >= 0):
			name = monstersList[spwnId][0]
			monsLvl = random.randrange(1, monstersList[spwnId][1])
			mobsInChank.append([spwnId, name, monsLvl])
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
	global currMob, hp, shards, money
	print("You attack a " + str(mobsInChank[num][1] + " Monster"))
	currMob.append(infoMob(num))
	hpE = currMob[0][2]
	while hpE > 0 or hp > 0:
		if(random.randrange(0,10) > currMob[0][4]):
			dmg = atk - random.randrange(0, currMob[0][3])
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
			del mobsInChank[num]
			break
		hp -= currMob[0][1]
		print("- " + str(currMob[0][1]) + " hp to you.")
		print("You hp is: " + str(hp))
	currMob.clear()

eventHandler(event)
spawnInChunk()
def main():
	global hp, maxhp, atk, defense, monstersInfo, monstersList
	while hp > 0:
		os.system('cls')
		os.system('clear')
		print("Event today: " + str(eventList[event[0]]))
		if(mobsInChank == []):
			spawnInChunk()
		if(hp > maxhp):
			hp = maxhp
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
		print("    Money: " + Fore.YELLOW + str(money))
		print("----------" + Fore.CYAN + "Your stats" + Fore.RESET + "----------")
		print("    HP: " + Fore.RED + str(hp) + Fore.RESET + "/" + Fore.RED + str(maxhp))
		print("    Defense: " + Fore.WHITE + Style.DIM + str(defense))
		print("    Strength: " + Fore.BLUE + str(atk))
		print("-----------" + Fore.CYAN + "Monsters" + Fore.RESET + "-----------")
		for a in range(0, len(mobsInChank)):
			print(str(a) + ") Monster: " + str(mobsInChank[a][1]) + ", Lvl: " + str(mobsInChank[a][2]))
		print("------------------------------")
		print("1) Attack")
		print("2) Heal 50 HP(15 money)")
		print("3) Workshop")
		print("4) Open inventory")
		print("5) Shop")
		b = input()
		if(int(b) == 1):
			print("Enter number of monster: ")
			c = input()
			if(int(c) > len(mobsInChank)):
				pass
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
			newItem = shop.inv(stones, maxhp, defense, atk)
			maxhp = newItem[0]
			atk = newItem[1]
			defense = newItem[2]
			stones = newItem[3]
		elif(int(b) == 5):
			newItem = shop.shop(money, stones)
			money = newItem[0]
			stones = newItem[1]
		else:
			main()
main()