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


class Node:
    def  __init__(self, data):
        self.data = data
        self.parent = None
        self.left = None
        self.right = None
        self.bf = 0

class BalancedSearchForest:

	def __init__(self):
		self.directory = [None,None,None]
		self.treeSizes = [0,0,0]
		self.a = 0
		self.b = 0
		self.t = 1
		self.k = 1
		self.l = 1
		self.n = 0
		self.balances = 0
		self.rejects = 0
		self.base = 1

	def insert(self, key):
		if key<0:
			return

		if self.member(key) is not None:
			self.rejects += 1
			return

		#starting out
		size = self.n
		if size == 0:
			self.a = key
			self.insertInTree(1, key)

		elif size == 1:
			if key < self.a:
				self.b = self.a
				self.a = key
				self.deleteNode(self.directory[1],self.b,1)
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
		self.base = math.floor(self.n/10)

	def member(self, key):
		if key < 0:
			return

		if self.n == 1:
			index = 1
		else:
			index = self.getIndex(key)

		root = self.directory[index]
		return self.searchTree(root,key)

	def delete(self,key):
		node = self.member(key)
		if node is None:
			return 
		index = self.getIndex(key)
		self.deleteNode(node,key, index)
		self.decrementTreeSize(index)
		self.decrementForestSize()

	def searchTree(self, node, key):
		if node is None or key == node.data:
			return node

		if key < node.data:
			return self.searchTree(node.left, key)
		return self.searchTree(node.right, key)

	def predecessor(self, key):
		node = self.member(key)
		if node != None:
			index = self.getIndex(node.data)
			m = self.minNode(self.directory[index])
			if m != node:
				#Tree search
				if node.left != None:
					return self.maxNode(x.left).data

				p = node.parent
				while p != None and node == p.left:
					node = p
					p = p.parent
				
				if p is None:
					return None

				return p.data
			else:
				#Forest Search
				index -= 1
				while index >= 0 and self.directory[index] is None:
					index -= 1

				if index < 0:
					return None

				return self.maxNode(self.directory[index]).data

	def successor(self, key):
		node = self.member(key)
		if node != None:
			index = self.getIndex(node.data)
			m = self.maxNode(self.directory[index])
			if m != node:
				if x.right != None:
					return self.minimum(x.right).data
				
				p = node.parent
				while p != None and node == p.right:
					node = p
					p = p.parent

				if p is None:
					return None

				return p.data
			else:
				#Forest Search
				index += 1
				while index <= self.k+1 and self.directory[index] is None:
					index += 1

				if index == self.k+2:
					return None

				return self.minNode(self.directory[index]).data




	def minNode(self, node):
		while node.left != None:
			node = node.left
		return node

	def maxNode(self,node):
		while node.right != None:
			node = node.right
		return node

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
			self.adjustA(-1 * (low_adj+self.base))
		else:
			self.adjustA(low_adj+self.base)
		
		if sections[2] >= full_rating/3:
			self.adjustB(large_adj+self.base)
		elif sections[2] >= full_rating/4:
			self.adjustB(med_adj+self.base)
		elif sections[2] == empty_rating:
			self.adjustB(-1 * (low_adj+self.base))
		else:
			self.adjustB(med_adj+self.base)

		
		if sections[1] >= full_rating/2:
			self.adjustK(large_adj+self.base)
		elif sections[1] >= full_rating/3:
			self.adjustK(med_adj+self.base)
		elif sections[1] == empty_rating:
			self.adjustK(-1 * (large_adj+self.base))
		else:
			self.adjustK(low_adj+self.base)

		#Reassign
		#Increase directory AND treesizes
		self.displacements = []
		for i in range(len(self.directory)):
			if self.directory[i] is not None:
				self.displacements.extend(self.validateNodes(i))

		newDir = [None] * (self.k+2)
		newSizes = [0] * (self.k+2)
		for i in range(min(self.k+2,len(self.directory))):
			newDir[i] = self.directory[i]
			newSizes[i] = self.treeSizes[i]

		self.directory = newDir
		self.treeSizes = newSizes

		for key in self.displacements:
			newIndex = self.getIndex(key.data)
			self.insertInTree(newIndex, key.data)


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



	#Helpers
	def getIndex(self, key):
		#pre: key is unique, valid, and within a and b 
		if key < self.a:
			return 0

		if key >= self.b:
			return self.k+1

		return (int)((key-self.a) // self.l) + 1 

	def incrementTreeSize(self, index):
		self.treeSizes[index] += 1

	def decrementTreeSize(self, index):
		self.treeSizes[index]-= 1

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
			self.t = 1

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
		if self.directory[self.k+1] is not None:
				newB = self.minNode(self.directory[self.k+1]).data
				extra = self.l
				if self.treeSizes[self.k+1] > self.t:
					extra = self.l*2
				optionB = newB + extra 

		if optionB == 0 and optionA == 0:
			index = self.k
			while index >= 0 and self.directory[index] is None:
				index -= 1

			self.b = self.minNode(self.directory[index])
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


	def insertInTree(self, index, key):
		node = Node(key)
		self.incrementTreeSize(index)
		y = None
		x = self.directory[index]
		
		while x != None:
			y = x
			if node.data < x.data:
				x = x.left
			else:
				x = x.right

		# y is parent of x
		node.parent = y
		if y == None:
			self.directory[index] = node
		elif node.data < y.data:
			y.left = node
		else:
			y.right = node

		# PART 2: re-balance the node if necessa
		self.updateLocalBalance(node)

		if self.treeSizes[index] > self.t + 1:
				self.balance()

		# update the balance factor the node
	def updateLocalBalance(self, node):
		if node.bf < -1 or node.bf > 1:
			self.localRebalance(node)
			return;

		if node.parent != None:
			if node == node.parent.left:
				node.parent.bf -= 1

			if node == node.parent.right:
				node.parent.bf += 1

			if node.parent.bf != 0:
				self.updateLocalBalance(node.parent)

	def localRebalance(self, node):
		if node.bf > 0:
			if node.right.bf < 0:
				self.rightRotate(node.right)
				self.leftRotate(node)
			else:
				self.leftRotate(node)
		elif node.bf < 0:
			if node.left.bf > 0:
				self.leftRotate(node.left)
				self.rightRotate(node)
			else:
				self.rightRotate(node)

	def leftRotate(self, x):
		y = x.right
		x.right = y.left
		if y.left != None:
			y.left.parent = x

		y.parent = x.parent;
		if x.parent == None:
			self.directory[self.getIndex(y.data)] = y
		elif x == x.parent.left:
			x.parent.left = y
		else:
			x.parent.right = y
		y.left = x
		x.parent = y

		# update the balance factor
		x.bf = x.bf - 1 - max(0, y.bf)
		y.bf = y.bf - 1 + min(0, x.bf)

		return y

	def rightRotate(self, x):
		
		y = x.left
		x.left = y.right;
		if y.right != None:
			y.right.parent = x
        
		y.parent = x.parent;
		if x.parent == None:
			self.directory[self.getIndex(y.data)] = y
		elif x == x.parent.right:
			x.parent.right = y
		else:
			x.parent.left = y
        
		y.right = x
		x.parent = y

		# update the balance factor
		x.bf = x.bf + 1 - min(0, y.bf)
		y.bf = y.bf + 1 + max(0, x.bf)

		return y


	def validateNodes(self, index):
		dis = []
		self.traverseTree(self.directory[index], index, dis)
		for node in dis:
			self.deleteNode(self.directory[index],node.data,index)
			self.decrementTreeSize(index)
		return dis

	def traverseTree(self, node, actualIndex, dis):
		#In Order Traversal
		if node != None:
			self.traverseTree(node.left,actualIndex, dis)
			self.traverseTree(node.right,actualIndex, dis)	
			expected = self.getIndex(node.data)
			if expected != actualIndex:
				dis.append(node)	
			

	

	def deleteNode(self, root, key, index):
		# Step 1 - Perform standard BST delete
		if not root:
			return root
 
		elif key < root.data:
			root.left = self.deleteNode(root.left, key, index)
 
		elif key > root.data:
 			root.right = self.deleteNode(root.right, key, index)
 
		else:
			if root.left is None:
				temp = root.right
				if self.directory[index].data is key:
					self.directory[index] = temp
				if temp is not None:
					temp.parent = root.parent
				root = None
				return temp
 
			elif root.right is None:
				temp = root.left
				if self.directory[index].data is key:
					self.directory[index] = temp
				if temp is not None:
					temp.parent = root.parent
				root = None
				return temp
 
			temp = self.minNode(root.right)
			root.data = temp.data
			root.right = self.deleteNode(root.right,temp.data, index)

 
		# If the tree has only one node,	
		# simply return it
		if root is None:
			self.directory[index] = root
			return root
 
		# Step 3 - Get the balance factor
		balance = root.bf
 
 		# Step 4 - If the node is unbalanced,
 		# then try out the 4 cases
 		# Case 1 - Left Left
		if balance > 1 and root.left.bf >= 0:
			newRoot = self.rightRotate(root)
			self.directory[index] = newRoot
			return newRoot
 
		# Case 2 - Right Right
		if balance < -1 and root.right.bf <= 0:
			newRoot = self.leftRotate(root)
			self.directory[index] = newRoot
			return newRoot
 
		# Case 3 - Left Right
		if balance > 1 and root.left.bf < 0:
			root.left = self.leftRotate(root.left)
			newRoot =  self.rightRotate(root)
			self.directory[index] = newRoot
			return newRoot
 
		# Case 4 - Right Left
		if balance < -1 and self.getBalance(root.right) > 0:
			root.right = self.rightRotate(root.right)
			newRoot = self.leftRotate(root)
			self.directory[index] = newRoot
			return newRoot
 	
		self.directory[index] = root
		return root


	def printForest(self):
		print("Forest:")
		for i in range(self.k+2):
			print(i,":",end='')
			r = self.directory[i]
			self.printHelper(r)
			print("")
			
	def printHelper(self,node):
		if node is not None:
			self.printHelper(node.left)
			print(node.data,end=' ')
			self.printHelper(node.right)

	def sanity(self):
		Header = False
		#if self.k > self.n:
		#	print("####### ERROR: K EXCEEDS N")
		#	Header = True

		if self.a >= self.b:
			if self.n > 5:
				print("####### ERROR: A EXCEEDS B")
				Header = True

		if self.l < 1:
			print("###### ERROR: L IS LESS THAN 1")
			Header = True

		if Header:
			self.printHeader()
			sys.exit()




	def printHeader(self):
		print(self.a,"-->",self.b)
		print("n:",self.n)
		print("N:", self.n+self.rejects)
		print("k:", self.k)
		print("t:",self.t)
		print("l:",self.l)
		print("balnces:",self.balances)



exK = 0
for i in range(5):
	print("~~~~~~~~~~~~~~~~~~~~TEST:",i,"~~~~~~~~~~~~~")
	bsf = BalancedSearchForest()
	nums = []
	for i in range(10000):
		n = i*5
		nums.append(n)
		bsf.insert(n)
		bsf.sanity()

	for k in nums:
		if bsf.member(k) is None:
			print("##### ERROR: CANT FIND",k)
			bsf.printForest()
			sys.exit()
	bsf.printHeader()
	if bsf.k > bsf.n:
		exK += 1

print("PASSED :", exK)
