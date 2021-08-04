import time
import random
import math

from bsf import BalancedSearchForest
from avl import AVLTree


def testRound(roundSize):
	sampleRange = 1000
	sampleSize = math.floor(roundSize)
	bsf = BalancedSearchForest()
	#keys = [14,83,80,36,96,21,24,35,63,59,43,2,73,66,10,1,4,82,46,73]
	keys = random.sample(range(sampleRange),sampleSize)
	for k in keys:
		bsf.insert(k)
		bsf.printForest()
		print("~")
	bsf.printHeader()
	bsf.printForest()
	print("REM")
	for k in keys:
		bsf.remove(k)

	bsf.printForest()
	bsf.printHeader()
	return
	#Search for keys
	memberA = time.perf_counter()
	for k in keys:
		bsf.member(k)
	memberB = time.perf_counter()

	minA = time.perf_counter()
	bsf.minimum()
	minB = time.perf_counter()

	maxA = time.perf_counter()
	bsf.maximum()
	maxB = time.perf_counter()

	predA = time.perf_counter()
	for k in keys:
		bsf.predecessor(k)
	predB = time.perf_counter()

	sucA = time.perf_counter()
	for k in keys:
		bsf.successor(k)
	sucB = time.perf_counter()

	removeA = time.perf_counter()
	
	removeB = time.perf_counter()
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
	bsf.printHeader()
	return workingSet

def startTest():
	#first index size catgory
	#second index test round
	#third index test category

	timeSets =[]
	base = 10
	numSizes = 5
	for i in range(numSizes):
		timeSets.append([])
		print(math.pow(base,i),":")
		timeSets[i].append(testRound(math.pow(base,i)))	

	print(timeSets)



#startTest()
testRound(20)