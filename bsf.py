from avl import AVLTree
import math
import random
import sys


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
		if self.treeSizes[index] > self.t+1:
				self.overflowBalance(index)	


	def member(self, key):
		if key < 0:
			return
		else:
			index = self.getIndex(key)

		return self.directory[index].member(key)
	

	def remove(self, key):
		index = self.getIndex(key)
		self.deleteInTree(index, key)
		self.decrementForestSize()

		if self.treeSizes[index] == 0:
			self.emptyCheck(index)


	def minimum(self):
		if self.n == 0:
			return None
		index = 0
		while self.directory[index].root is None:
			index += 1
		return self.treeMin(index)


	def maximum(self):
		if self.n == 0:
			return None
		index = self.k+1
		while self.directory[index].root is None:
			index -= 1
		return self.treeMax(index)


	def successor(self, key):
		node = self.member(key)
		if node != None:
			index = self.getIndex(key)
			m = self.treeMax(index)
			if m != node:
				#Tree search
				if node.right != None:
					return self.nodeMin(node.right)
				
				p = node.parent
				while p != None and node == p.right:
					node = p
					p = p.parent

				return p
			else:
				#Forest Search
				index += 1
				while index <= self.k+1 and self.directory[index].root is None:
					index += 1

				if index == self.k+2:
					return None

				return self.treeMin(index)
		return None


	def predecessor(self, key):
		node = self.member(key)
		if node != None:
			index = self.getIndex(node.key)
			m = self.treeMin(index)
			if m != node:
				#Tree search
				if node.left != None:
					return self.nodeMax(node.left)

				p = node.parent
				while p != None and node == p.left:
					node = p
					p = p.parent
				
				return p
			else:
				#Forest Search
				index -= 1
				while index >= 0 and self.directory[index].root is None:
					index -= 1

				if index < 0:
					return None

				return self.treeMax(index)
		return None
	

	def emptyCheck(self,index):
		if self.n == 0:
			return
		sectionSize = math.ceil(math.log2(self.k + 2))
		if index < sectionSize:
			i = 0
			while i < sectionSize:
				if self.treeSizes[i] != 0:
					return
				i += 1
			self.emptyBalance(0)

		elif index > self.k+2 - sectionSize:
			i = self.k+2 - sectionSize
			while i < self.k+2:
				if self.treeSizes[i] != 0:
					return
				i += 1
			self.emptyBalance(2)

		else:
			i = sectionSize
			while i < self.k+2 - sectionSize:
				if self.treeSizes[i] != 0:
					return 
				i += 1 
			self.emptyBalance(1)
	

	def emptyBalance(self,section):
		if section == 0:
			self.adjustA(1)
		if section == 1:
			self.adjustL(self.l*2)
		if section == 3:
			self.adjustB(-1)
		self.reassign()


	def overflowBalance(self, index):
		self.balances+=1
		if self.treeSizes[index] > 3:
			if index == 0:
				self.adjustA(-1)
			elif index == self.k+1:
				self.adjustB(1)
			else:
				a = self.treeMin(index).key
				b = self.directory[index].root.key

				self.adjustL(b-a)
		else:
			self.adjustL(self.l/2)

		self.reassign()


	def reassign(self):
		self.displacements = []
		for i in range(len(self.directory)):
			if self.directory[i].root is not None:
				self.tempDis = []
				self.validateTree(self.directory[i].root, i)
				for dis in self.tempDis:
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
			self.insertInTree(exp,dis)


	def validateTree(self, node, index):
		if node.left is not None:
			self.validateTree(node.left,index)

		if node.right is not None:
			self.validateTree(node.right,index)

		expected = self.getIndex(node.key)
		if expected != index:
			self.tempDis.append(node.key)


	def adjustL(self, val):
		self.l = val
		forestRange = self.b - self.a
		self.k = math.ceil(forestRange/self.l)
		if self.k > forestRange:
			self.k = math.floor(forestRange)
			self.l = 1
			adjustA(-1)
			adjustB(1)


	def adjustA(self, direction):
		a = self.a 
		if direction < 0:
			#Growing range
			optionA = math.floor(math.sqrt(self.n)) * self.l
			optionB = self.treeMax(0)
			if optionB is not None:
				a -= max(optionA,optionB.key)
			else:
				a -= optionA
			
			if a < 0:
				a = 0
		else:
			#Shrinking range
			a += math.ceil(math.log2(self.k + 2))
			if a > self.b:
				return

		self.a = a
		self.k = math.ceil((self.b-self.a)/self.l)


	def adjustB(self,direction):
		b = self.b
		if direction > 0:
			#Growing Range
			optionA = math.floor(math.sqrt(self.n)) * self.l
			optionB = self.treeMin(self.k+1)
			if optionB is not None:
				b += max(optionA, optionB.key)
			else:
				b += optionA
		else:
			#Shrinking Range
			b -= math.ceil(math.log2(self.k+2))
			if b < self.a:
				return
		self.b = b
		self.k = math.ceil((self.b-self.a)/self.l)


	def insertInTree(self, index, key):
		self.incrementTreeSize(index)
		self.directory[index].insert(key)
		

	def deleteInTree(self, index, key):
		self.decrementTreeSize(index)	
		self.directory[index].remove(key)
			

	def getIndex(self, key):
		#pre: key is unique, valid, and within a and b 
		if self.n == 1:
			return 1 

		if key < self.a:
			return 0

		if key >= self.b:
			return self.k+1

		return (int)((key-self.a) // self.l) + 1 


	def treeMin(self, index):
		if self.directory[index].root is not None:
			return self.directory[index].minimum()
		return None
	

	def treeMax(self, index):
		if self.directory[index].root is not None:
			return self.directory[index].maximum()
		return None


	def nodeMin(self, node):
		while node.left is not None:
			node = node.left

		return node


	def nodeMax(self, node):
		while node.right is not None:
			node = node.right

		return node 


	def incrementTreeSize(self, index):
		self.treeSizes[index] += 1


	def decrementTreeSize(self, index):
		self.treeSizes[index] -= 1


	def incrementForestSize(self):
		self.n += 1
		if self.n>1:
			self.t = self.calcThreshold()
		else:
			self.t = 1


	def decrementForestSize(self):
		self.n -= 1
		if self.n>0:
			self.t = self.calcThreshold()
		else:
			self.t = 1


	def calcThreshold(self):
		return math.ceil(math.log2(self.n))


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
				print(i,self.treeSizes[i],":",self.directory[i].root.key,end='')
				print(self.directory[i].postorder(self.directory[i].root))