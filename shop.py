import os

def Workshop(shards, stones):
	os.system('cls')
	print("------------Stones------------")
	print("1) Craft a water stone(10 shards)")
	print("2) Craft a sun stone(10 shards)")
	print("3) Craft a air stone(10 shards)")
	print("------------------------------")
	a = input()
	if(int(a) == 1 and shards[0] > 9):
		print("isafhoshdaois")
		stones[0] += 1
		shards[0] -= 10
	elif(int(a) == 2 and shards[2] > 9):
		stones[1] += 1
		shards[1] -= 10
	elif(int(a) == 3 and shards[3] > 9):
		stones[2] += 1
		shards[2] -= 10
	else:
		print("Error or not enough shards")
	items = [stones, shards]
	return items