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
		self.p = 1
		self.n = 0
		self.balances = 0
		self.balanceDepth = 0


	"""
	Insert:
	Insert a key into the appropriate tree if it is positive and unique

	Input: key value
	Output: void 
	"""
	def insert(self, key):
		if key<0:
			#Negative key
			return

		if self.member(key) is not None:
			#Duplicate key
			return

		index = 1
		size = self.n

		if size == 0:
			#First key
			self.a = key
			self.insertInTree(1, key)

		elif size == 1:
			#Second key
			if key < self.a:
				#Range needs to be corrected and keys get moved
				self.b = self.a
				self.a = key
				self.deleteInTree(1,self.b)
				self.insertInTree(2,self.b)
				self.insertInTree(1,key)


			else:
				#Second key is greater than first key
				self.b = key
				self.insertInTree(2,key)
			#First p assignment is manual  
			self.p = self.b - self.a

		else:
			#Any element after size > 1
			index = self.getIndex(key)
			self.insertInTree(index, key)
					
		self.incrementForestSize() 		

	"""
	Member:
	Search the appropriate tree to see if a key exists in the forest 

	Input: key value
	Output: if key exists, return the node. Else return None. If input
	is not valid return void
	"""
	def member(self, key):
		if key < 0:
			#Negative key
			return 
		else:
			index = self.getIndex(key)

		return self.directory[index].member(key)
	
	"""
	Remove:
	Delete a node if it exists in the forest. 
	If the last node is removed from a tree, check if balancing is needed

	Input: key value
	Output: void
	"""
	def remove(self, key):
		index = self.getIndex(key)
		startCount = self.directory[index].elements_count
		self.deleteInTree(index, key)
		if startCount > self.directory[index].elements_count:
			self.decrementForestSize()

		if self.treeSizes[index] == 0:
			self.emptyCheck(index)


	"""
	Minimum:
	Return the smallest key value found in the forest

	Input: none
	Output: if forest is empty, return none. Else return the node with the smallest key value
	"""
	def minimum(self):
		if self.n == 0:
			return None
		index = 0
		while self.directory[index].root is None:
			index += 1
		return self.treeMin(index)


	"""
	Maximum:
	Return the largest key value found in the forest

	Input: none
	Output: if the forest is empty, return none. Else return the node with the largest key value
	"""
	def maximum(self):
		if self.n == 0:
			return None
		index = self.k+1
		while self.directory[index].root is None:
			index -= 1
		return self.treeMax(index)

	"""
	Successor:
	If a key k exists in a totally ordered set, return the next key larger than k

	Input: key value
	Output: if key exists and isn't the maximum value in the forest, return the successor node
	Else return None
	"""
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

	"""
	Predecessor:
	If a key k exists in a totally ordered set, return the next key smaller than k

	Input: key value
	Output: if a key exists and is not the minimum value of the forest, return the predecessor node
	Else return None
	"""
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
	
	"""
	Empty Check:
	Checks sections of the forest of sizes log2(k+2) to see if they only contain empty trees
	If a section contains keys, no action is taken and the method exits
	If a section is empty, an empty-balance is performed for that section
	
	Input: index of tree that has just become empty
	Output: void 
	"""
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
	
	"""
	Empty Balance:
	If a section is entirely empty, the inner forest range is decreased
	The appropriate endpoint will be moved inward based on the location of the empty section
	
	Input: section index
	Output: void
	"""
	def emptyBalance(self,section):
		if section == 0:
			self.adjustA(1)
		if section == 1:
			self.adjustP(self.p*2)
		if section == 3:
			self.adjustB(-1)
		self.reassign()

	"""
	Overflow Balance:
	If a tree exceeds the size threshold, the forest range values will be altered
	If the offending tree is an outer tree, the appropriate endpoint is adjusted
	If the offending tree is an inner tree, the PVI size is adjusted
	After these values are updated, we reassign displaced nodes
	To track the recursive depth of the balancing process,
	balanceDepth is decremented after a successful reassignment

	Input: index of offending tree
	Output: void
	"""
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

				self.adjustP(b-a)
		else:
			self.adjustP(self.p/2)

		self.reassign()
		self.balanceDepth -= 1

	"""
	Worst Case Balance:
	A safety net to prevent expensive balancing when recursive depth equals log(n)
	This balancing process ensures that no further rebalancing will be required. 
	The PVI size is set equal to the threshold
	If the offending tree is an outer-tree, the endpoints will be chosen from existing minimum keys
	After these values have been updated,
	Recursive balance depth is set to 0 and displaced nodes are reassigned
	
	Input: index of offending tree
	Output: void
	"""
	def worstCaseBalance(self, index):
		print("WORST CASE")
		if index == 0:
			#index 0's min will be > 0 
			self.a = self.treeMin(0).key
		if index == self.k+1:
			#Don't want to overcorrect b since theres no cap
			self.b = self.treeMin(self.k+1).key
		
		self.adjustP(self.t)
		
		self.reassign()
		self.balanceDepth = 0

	"""
	Reassign:
	Search through every tree in the forest, locate displaced nodes, and move them to their expected tree
	When a displaced node is discovered, it is added to a list maintained for each tree
	The validation of a tree is completed before the list is iterated through and each displaced node is deleted from the tree
	After each tree has been validated and displaced nodes have been deleted, all displaced nodes are reinserted using updated indices 
	It is possible that while inserting displaced nodes, another balance is triggered.
	Since instance lists are used to keep track of displaced nodes and indices are calculated on the fly,
	All nodes will eventually get re-inserted properly no matter how many recursive layers are used. 

	Input: none
	Output: void 
	"""
	def reassign(self):
		displacements = []
		for i in range(len(self.directory)):
			if self.directory[i].root is not None:
				tempDis = []
				self.validateTree(self.directory[i].root, i, tempDis)
				for dis in tempDis:
					self.deleteInTree(i, dis)
					displacements.append(dis)
			
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
		for dis in displacements:	
			exp = self.getIndex(dis)
			self.insertInTree(exp,dis)
		


	"""
	Validate Tree:
	Recursively visit each node in a tree and collect list of displacements
	If the index of the tree being searched does not match the expected index of a key, 
	add the key value to displacement list

	Input: current node, index of tree being validated, list of displacements
	Output: complete list of displaced nodes in the tree 
	"""
	def validateTree(self, node, index, dis):
		if node.left is not None:
			self.validateTree(node.left,index, dis)

		if node.right is not None:
			self.validateTree(node.right,index, dis)

		expected = self.getIndex(node.key)
		if expected != index:
			dis.append(node.key)


	"""
	Adjust P:
	Assign a new size to the possible-range-intervals and update related values

	Input: value to assign P to 
	Output: void
	"""
	def adjustP(self, val):
		self.p = val
		forestRange = self.b - self.a
		self.k = math.ceil(forestRange/self.p)
		if self.k > forestRange:
			#Array Mode
			self.k = math.floor(forestRange)
			self.p = 1
			adjustA(-1)
			adjustB(1)

	"""
	Adjust A:
	Assign a new lower endpoint to the forest range.
	The larger adjustment is selected between two options
	Direction parameter indicates if the range is growing or shrinking
	d<0 is growing, d>0 is shrinking 

	Input: enumerated direction value
	Output: void 
	"""
	def adjustA(self, direction):
		a = self.a 
		if direction < 0:
			#Growing range
			optionA = math.floor(math.sqrt(self.n)) * self.p
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
		self.k = math.ceil((self.b-self.a)/self.p)


	"""
	Adjust B:
	Assign a new high endpoint to the forest range.
	The larger adjustment is selected between two options
	Direction parameter indicates if the range is growing or shrinking
	d>0 is growing, d<0 is shrinking 

	Input: enumerated direction value
	Output: void 
	"""
	def adjustB(self,direction):
		b = self.b
		if direction > 0:
			#Growing Range
			optionA = math.floor(math.sqrt(self.n)) * self.p
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
		self.k = math.ceil((self.b-self.a)/self.p)


	"""
	Insert In Tree:
	A key is inserted into a specfic tree in the forest. 
	After the key is inserted and the size of the tree is updated, determine if balancing is needed
	If the tree size exceeds the size threshold, start the appropriate balance process
	
	Input: index of the tree, key value to be inserted
	Output: void
	"""
	def insertInTree(self, index, key):
		self.incrementTreeSize(index)
		self.directory[index].insert(key)
		if self.treeSizes[index] > self.t+1:				
				self.balanceDepth += 1
				self.overflowBalance(index)	
		

	"""
	Delete in Tree:
	A node with the corresponding key value is removed from a specific tree
	It is assumed that the key exists in the tree.

	Input: index of the tree, key value of node to be deleted
	Output: void
	"""
	def deleteInTree(self, index, key):
		startCount = self.directory[index].elements_count	
		self.directory[index].remove(key)
		if startCount > self.directory[index].elements_count:
			self.decrementTreeSize(index)
			

	"""
	Get Index:
	Hash function that returns the index of the tree that a key belongs in 

	Input: key value
	Output: index of the tree that the key belongs in
	"""
	def getIndex(self, key):
		#TODO GET RID OF N==1 check
		if self.n == 1:
			return 1 

		if key < self.a:
			return 0

		if key >= self.b:
			return self.k+1

		return (int)((key-self.a) // self.p) + 1 

	"""
	Tree Min:
	Return the node associated with the smallest key value in a given tree

	Input: index of tree
	Output: minimum key node. If tree is empty, None
	"""
	def treeMin(self, index):
		if self.directory[index].root is not None:
			return self.directory[index].minimum()
		return None
	
	"""
	Tree Max:
	Return the node associated with the largest key value in a given tree

	Input: index of tree
	Output: maximum key node. If tree is empty, None
	"""
	def treeMax(self, index):
		if self.directory[index].root is not None:
			return self.directory[index].maximum()
		return None

	"""
	Node Min:
	Starting at a given node with key k, find the node with the smallest key < k

	Input: index of tree
	Output: node with smallest key less than root. If no left children exist, None
	"""
	def nodeMin(self, node):
		while node.left is not None:
			node = node.left

		return node

	"""
	Node Max:
	Starting at a given node with key k, find the node with the largest key > k

	Input: index of tree
	Output: node with largest key greater than root. If no right children exist, None
	"""
	def nodeMax(self, node):
		while node.right is not None:
			node = node.right

		return node 

	"""
	Increment Tree Size:
	Increase the size of a given tree by 1 in the directory of tree sizes.

	Input: index of tree
	Output: None
	"""
	def incrementTreeSize(self, index):
		self.treeSizes[index] += 1

	"""
	Decrement Tree Size:
	Decrease the size of a given tree by 1 in the directory of tree sizes.

	Input: index of tree
	Output: None
	"""
	def decrementTreeSize(self, index):
		self.treeSizes[index] -= 1

	"""
	Increment Forest Size:
	Increase the size of the forest and update the threshold for tree sizes

	Input: index of tree
	Output: None
	"""
	def incrementForestSize(self):
		self.n += 1
		if self.n>1:
			self.t = self.calcThreshold()
		else:
			self.t = 1

	"""
	Decrement Forest Size:
	Decrease the size of the forest and update the threshold for tree sizes

	Input: index of tree
	Output: None
	"""
	def decrementForestSize(self):
		self.n -= 1
		if self.n>0:
			self.t = self.calcThreshold()
		else:
			self.t = 1

	"""
	calcThreshold:
	Calculate the current size threshold for trees based on the total number of elements

	Input: none
	Output: updated threshold value
	"""
	def calcThreshold(self):
		t = math.ceil(math.log2(self.n))
		if t != 0:
			return t
		return 1

	"""
	Helper for printing header values of forest
	"""
	def printHeader(self):
		print(self.a,"-->",self.b)
		print("n:",self.n)
		print("k:", self.k)
		print("t:",self.t)
		print("l:",self.p)
		print("balnces:",self.balances)


	"""
	Helper to print values in forest
	"""
	def printForest(self):
		for i in range(len(self.directory)):
			if self.directory[i].root is not None:
				print(i,self.treeSizes[i],":",self.directory[i].root.key,end='')
				print(self.directory[i].postorder(self.directory[i].root))