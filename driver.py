import time
import random
import math

from bsf import BalancedSearchForest
from avl import AVLTree


def testRound(struc, roundSize):
	workingSet = [0]*8
	
	sampleSize = math.floor(roundSize)
	sampleRange = 1000000000

	keys = []
	for i in range(sampleSize):
		keys.append(random.randint(0,sampleRange))

	opKeys = keys
	i = len(keys)//2
	while i < len(keys):
		opKeys[i] = random.randint(0,sampleRange)
		i+=1

	print("Insert")
	insertA = time.perf_counter()
	for k in keys:
		struc.insert(k)
	insertB = time.perf_counter()
	
	#Search for keys
	print("Search")
	memberA = time.perf_counter()
	for k in opKeys:
		struc.member(k)
	memberB = time.perf_counter()
	
	print("Min")
	minA = time.perf_counter()
	struc.minimum()
	minB = time.perf_counter()

	print("Max")
	maxA = time.perf_counter()
	struc.maximum()
	maxB = time.perf_counter()

	print("Pred")
	predA = time.perf_counter()
	for k in opKeys:
		struc.predecessor(k)
	predB = time.perf_counter()

	print("Succ")
	sucA = time.perf_counter()
	for k in opKeys:
		struc.successor(k)
	sucB = time.perf_counter()

	print("del")
	removeA = time.perf_counter()
	for k in keys:
		struc.remove(k)
	removeB = time.perf_counter()
	totalA = insertA
	totalB = removeB

	workingSet[0] = insertB - insertA
	workingSet[1] = memberB - memberA
	workingSet[2] = minB - minA
	workingSet[3] = maxB - maxA
	workingSet[4] = predB - predA
	workingSet[5] = sucB - sucA
	workingSet[6] = removeB - removeA
	workingSet[7] = totalB - totalA
	print(workingSet)

	return workingSet

def startTest():
	#first index size catgory
	#second index test round
	#third index test category
	bsf = BalancedSearchForest()
	avl = AVLTree()
	strucs = [bsf,avl]
	timeSets =[]
	base = 10
	numSizes = 9
	index = 0
	for s in strucs:
		bsf = BalancedSearchForest()
		avl = AVLTree()
		for i in range(numSizes):
			timeSets.append([])
			print(math.pow(base,i),":")
			timeSets[i].append(testRound(s, math.pow(base,i)))
			if index == 0:
				print("@@@@@@@@@@@@@", s.balances, s.k, s.n)
		
		index+=1


	#print(timeSets)



startTest()