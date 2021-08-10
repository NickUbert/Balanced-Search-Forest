import time
import random
import math

from bsf import BalancedSearchForest
from avl import AVLTree


def testRound(struc, keys, opKeys):
	workingSet = [0]*8
	
	insertA = time.perf_counter()
	for k in keys:
		struc.insert(k)
	insertB = time.perf_counter()
	
	#Search for keys
	memberA = time.perf_counter()
	for k in opKeys:
		struc.member(k)
	memberB = time.perf_counter()
	
	minA = time.perf_counter()
	struc.minimum()
	minB = time.perf_counter()

	maxA = time.perf_counter()
	struc.maximum()
	maxB = time.perf_counter()

	predA = time.perf_counter()
	for k in opKeys:
		struc.predecessor(k)
	predB = time.perf_counter()

	sucA = time.perf_counter()
	for k in opKeys:
		struc.successor(k)
	sucB = time.perf_counter()

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
	print(len(keys),":",workingSet)
	return workingSet

def startTest():
	#first index size catgory
	#second index test round
	#third index test category
	
	sampleRange = 1000000000
	base = 10
	numSizes = 7
	output = open("bsf_out.txt",'a')
	for i in range(numSizes):
		roundSize =math.pow(base,i)
		sampleSize = math.floor(roundSize)
		bsf = BalancedSearchForest()
		avl = AVLTree()
		strucs = [None,None]
		strucs[0] = bsf
		strucs[1] = avl
		keys = []
		for i in range(sampleSize):
			keys.append(random.randint(0,sampleRange))
			
		opKeys = keys
		i = len(keys)//2
		while i < len(keys):
			opKeys[i] = random.randint(0,sampleRange)
			i+=1
		index = 0
		for s in strucs:
			output.write(str(index)+" "+str(sampleSize)+":")
			result = testRound(s,keys,opKeys)
			if index == 0:
				result.append(s.balances)
				result.append(s.k)
			index+=1
			result = ''.join(str(e)+',' for e in result)
			output.write(result)
			output.write("\n")





startTest()