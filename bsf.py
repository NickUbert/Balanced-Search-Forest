from avl import AVLTree
import math
import random
import sys

#Enums
empty_rating = -2
low_rating = 0
med_rating = 1
high_rating = 2
full_rating = 5



low_adj = 1
med_adj = 2
large_adj = 3

class BalancedSearchForest:

	def __init__(self):
		self.directory = [AVLTree(),AVLTree(),AVLTree()]
		self.treeSizes = [0,0,0]
		self.a = 0
		self.b = 0
		self.t = 1
		self.k = 1
		self.l = 1
		self.n = 0
		self.balances = 0
		self.base = 1

	def insert(self, key):
		if key<0:
			return

		if self.member(key) is not None:
			return

		#starting out
		index = 1
		size = self.n
		if size == 0:
			self.a = key
			self.insertInTree(1, key)

		elif size == 1:
			if key < self.a:
				self.b = self.a
				self.a = key
				self.deleteInTree(1,self.b)
				self.insertInTree(2,self.b)
				self.insertInTree(1,key)


			else:
				self.b = key
				self.insertInTree(2,key)

			self.l = self.b - self.a

		else:
			index = self.getIndex(key)
			self.insertInTree(index, key)
				
			

	
		self.incrementForestSize() 
		#CHANGE TO U
		self.base = math.floor(self.n/10)
		if self.treeSizes[index] > self.t+1:
				self.balance()	


	def member(self, key):
		index = self.getIndex(key)
		return self.directory[index].member(key)

	def remove(self, key):
		index = self.getIndex(key)
		self.deleteInTree(index, key)
		self.decrementForestSize()



	def insertInTree(self, index, key):
			self.incrementTreeSize(index)
			self.directory[index].insert(key)
		

	def deleteInTree(self, index, key):
		self.decrementTreeSize(index)	
		self.directory[index].remove(key)

	def balance(self):
		treeRatings = [0]*(self.k+2)
		self.balances+=1
		
		#Interpret Phase
		for i in range(self.k+2):
			treeRatings[i] = self.treeRating(i)

		#Partition Phase
		sectionSize = math.ceil((self.k + 2)/4)
		sections = [0,0,0]
		index = 0
		while index < sectionSize:
			sections[0] += treeRatings[index]
			index += 1

		while index < (self.k+2)-sectionSize:
			sections[1] += treeRatings[index]
			index += 1

		while index < self.k+2:
			sections[2] += treeRatings[index]
			index += 1

		sections[0] /= sectionSize
		sections[1] /= (self.k+2)-sectionSize
		sections[2] /= sectionSize

		#Restructure Phase
		if sections[0] >= full_rating/3:
			self.adjustA(large_adj+self.base)
		elif sections[0] >= full_rating/4:
			self.adjustA(med_adj+self.base)
		elif sections[0] == empty_rating:
			self.adjustA(-1 * (sectionSize))
		else:
			self.adjustA(low_adj+self.base)
		
		if sections[2] >= full_rating/3:
			self.adjustB(large_adj+self.base)
		elif sections[2] >= full_rating/4:
			self.adjustB(med_adj+self.base)
		elif sections[2] == empty_rating:
			self.adjustB(-1 * (sectionSize))
		else:
			self.adjustB(med_adj+self.base)

		
		if sections[1] >= full_rating/2:
			self.adjustK(large_adj+self.base)
		elif sections[1] >= full_rating/3:
			self.adjustK(med_adj+self.base)
		elif sections[1] == empty_rating:
			self.adjustK(-1 * (sectionSize))
		else:
			self.adjustK(low_adj+self.base)

		#Reassign

		self.displacements = []
		for i in range(len(self.directory)):
			if self.directory[i].root is not None:
				self.tempDis = []
				self.validateTree(self.directory[i].root, i)
				for dis in self.tempDis:
					print("DEL",i, dis)
					self.deleteInTree(i, dis)
					self.displacements.append(dis)
		
		newDir = []
		newSizes = []
		for i in range(self.k+2):
			newDir.append(AVLTree())
			newSizes.append(0)

		for i in range(min(self.k+2, len(self.directory))):
			newDir[i] = self.directory[i]
			newSizes[i] = self.treeSizes[i]

		self.directory = newDir
		self.treeSizes = newSizes

		for dis in self.displacements:	
			exp = self.getIndex(dis)
			print("INS", dis, exp)
			self.insertInTree(exp,dis)

	def validateTree(self, node, index):
		if node.left is not None:
			self.validateTree(node.left,index)

		if node.right is not None:
			self.validateTree(node.right,index)

		expected = self.getIndex(node.key)
		if expected != index:
			self.tempDis.append(node.key)
			


	def treeRating(self, index):
		size = self.treeSizes[index]
		rangeSize = self.t // 3
		if size == 0:
			return empty_rating

		elif size >= self.t:
			return full_rating

		elif size >= (self.t-rangeSize):
			return high_rating

		elif size >= (self.t-(2*rangeSize)):
			return med_rating

		else:
			return low_rating




	def getIndex(self, key):
		#pre: key is unique, valid, and within a and b 
		if key < self.a:
			return 0

		if key >= self.b:
			return self.k+1

		return (int)((key-self.a) // self.l) + 1 

	def minNode(self, index):
		return self.directory[index].minimum()
		
	def maxNode(self, index):
		return self.directory[index].maximum()

	def incrementTreeSize(self, index):
		self.treeSizes[index] += 1

	def decrementTreeSize(self, index):
		self.treeSizes[index] -= 1

	def incrementForestSize(self):
		self.n += 1
		if self.n>1:
			self.t = math.floor(math.log2(self.n))
		else:
			self.t = 1

	def decrementForestSize(self):
		self.n -= 1
		if self.n>0:
			self.t = math.floor(math.log2(self.n)) 
		else:
			self.t = 0

	def adjustA(self, degree):
		if (self.a - (self.l * degree)) < self.b:
			self.a -= (self.l * degree)

		if self.a < 0:
			self.a = 0

		
	def adjustB(self, degree):
		optionA = self.b + (self.l * degree)
		#Shrink
		if degree < 0:
			if optionA > self.a:
				self.b = optionA
				self.adjustK(degree)
			return

		if optionA < self.a:
			optionA = 0

		optionB = 0
		if self.treeSizes[self.k+1] != 0:
				newB = self.minNode(self.k+1).key
				extra = self.l
				if self.treeSizes[self.k+1] > self.t:
					#This is the overflow tree so we add extra padding
					extra = self.l*2
				optionB = newB + extra 

		if optionB == 0 and optionA == 0:
			index = self.k
			while index >= 0 and self.treeSizes[index] == 0:
				index -= 1

			self.b = self.minNode(index)
			return

		choice = max(optionB, optionA)
		self.b = choice
		if choice == optionA:
				self.adjustK(degree)

	
	def adjustK(self,degree):
		forestRange = self.b-self.a
		self.k += degree

		if self.k > forestRange:
			self.k = math.floor(forestRange)

		if self.k < 1:
			self.k = 1

		self.l = forestRange/self.k




	def printHeader(self):
		print(self.a,"-->",self.b)
		print("n:",self.n)
		print("k:", self.k)
		print("t:",self.t)
		print("l:",self.l)
		print("balnces:",self.balances)

	def printForest(self):
		for i in range(len(self.directory)):
			if self.directory[i].root is not None:
				print(i,self.treeSizes[i],":",end='')
				print(self.directory[i].postorder(self.directory[i].root))			

# DO a full trace, the issue goes deep in removes. 
#We are reporting deleting a node but it remains present
#tree size still gets decremented