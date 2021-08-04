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


class node:
	def __init__(self,value=None):
		self.value=value
		self.left_child=None
		self.right_child=None
		self.parent=None # pointer to parent node in tree
		self.height=1 # height of node in tree (max dist. to leaf) NEW FOR AVL

class AVLTree:
	def __init__(self):
		self.root=None

	def __repr__(self):
		if self.root==None: return ''
		content='\n' # to hold final string
		cur_nodes=[self.root] # all nodes at current level
		cur_height=self.root.height # height of nodes at current level
		sep=' '*(2**(cur_height-1)) # variable sized separator between elements
		while True:
			cur_height+=-1 # decrement current height
			if len(cur_nodes)==0: break
			cur_row=' '
			next_row=''
			next_nodes=[]

			if all(n is None for n in cur_nodes):
				break

			for n in cur_nodes:

				if n==None:
					cur_row+='   '+sep
					next_row+='   '+sep
					next_nodes.extend([None,None])
					continue

				if n.value!=None:       
					buf=' '*int((5-len(str(n.value)))/2)
					cur_row+='%s%s%s'%(buf,str(n.value),buf)+sep
				else:
					cur_row+=' '*5+sep

				if n.left_child!=None:  
					next_nodes.append(n.left_child)
					next_row+=' /'+sep
				else:
					next_row+='  '+sep
					next_nodes.append(None)

				if n.right_child!=None: 
					next_nodes.append(n.right_child)
					next_row+='\ '+sep
				else:
					next_row+='  '+sep
					next_nodes.append(None)

			content+=(cur_height*'   '+cur_row+'\n'+cur_height*'   '+next_row+'\n')
			cur_nodes=next_nodes
			sep=' '*int(len(sep)/2) # cut separator size in half
		return content

	def insert(self,value):
		if self.root==None:
			self.root=node(value)
		else:
			self._insert(value,self.root)

	def _insert(self,value,cur_node):
		if value<cur_node.value:
			if cur_node.left_child==None:
				cur_node.left_child=node(value)
				cur_node.left_child.parent=cur_node # set parent
				self._inspect_insertion(cur_node.left_child)
			else:
				self._insert(value,cur_node.left_child)
		elif value>cur_node.value:
			if cur_node.right_child==None:
				cur_node.right_child=node(value)
				cur_node.right_child.parent=cur_node # set parent
				self._inspect_insertion(cur_node.right_child)
			else:
				self._insert(value,cur_node.right_child)

	def print_tree(self):
		if self.root!=None:
			self._print_tree(self.root)

	def _print_tree(self,cur_node):
		if cur_node!=None:
			self._print_tree(cur_node.left_child)
			print ('%s, h=%d'%(str(cur_node.value),cur_node.height))
			self._print_tree(cur_node.right_child)

	def height(self):
		if self.root!=None:
			return self._height(self.root,0)
		else:
			return 0

	def _height(self,cur_node,cur_height):
		if cur_node==None: return cur_height
		left_height=self._height(cur_node.left_child,cur_height+1)
		right_height=self._height(cur_node.right_child,cur_height+1)
		return max(left_height,right_height)

	def find(self,value):
		if self.root!=None:
			return self._find(value,self.root)
		else:
			return None

	def _find(self,value,cur_node):
		if value==cur_node.value:
			return cur_node
		elif value<cur_node.value and cur_node.left_child!=None:
			return self._find(value,cur_node.left_child)
		elif value>cur_node.value and cur_node.right_child!=None:
			return self._find(value,cur_node.right_child)

	def delete_value(self,value):
		return self.delete_node(self.find(value))

	def delete_node(self,node):

		## -----
		# Improvements since prior lesson

		# Protect against deleting a node not found in the tree
		if node==None or self.find(node.value)==None:
			if node is not None:
				print("Node to be deleted not found in the tree!", node.value)
			else:
				print("Node to be deleted not found in the tree! NONE")
			return None 
		## -----

		# returns the node with min value in tree rooted at input node
		def min_value_node(n):
			current=n
			while current.left_child!=None:
				current=current.left_child
			return current

		# returns the number of children for the specified node
		def num_children(n):
			num_children=0
			if n.left_child!=None: num_children+=1
			if n.right_child!=None: num_children+=1
			return num_children

		# get the parent of the node to be deleted
		node_parent=node.parent

		# get the number of children of the node to be deleted
		node_children=num_children(node)

		# break operation into different cases based on the
		# structure of the tree & node to be deleted

		# CASE 1 (node has no children)
		if node_children==0:

			if node_parent!=None:
				# remove reference to the node from the parent
				if node_parent.left_child==node:
					node_parent.left_child=None
				else:
					node_parent.right_child=None
			else:
				self.root=None

		# CASE 2 (node has a single child)
		if node_children==1:

			# get the single child node
			if node.left_child!=None:
				child=node.left_child
			else:
				child=node.right_child

			if node_parent!=None:
				# replace the node to be deleted with its child
				if node_parent.left_child==node:
					node_parent.left_child=child
				else:
					node_parent.right_child=child
			else:
				self.root=child

			# correct the parent pointer in node
			child.parent=node_parent

		# CASE 3 (node has two children)
		if node_children==2:

			# get the inorder successor of the deleted node
			successor=min_value_node(node.right_child)

			# copy the inorder successor's value to the node formerly
			# holding the value we wished to delete
			node.value=successor.value

			# delete the inorder successor now that it's value was
			# copied into the other node
			self.delete_node(successor)

			# exit function so we don't call the _inspect_deletion twice
			return

		if node_parent!=None:
			# fix the height of the parent of current node
			node_parent.height=1+max(self.get_height(node_parent.left_child),self.get_height(node_parent.right_child))

			# begin to traverse back up the tree checking if there are
			# any sections which now invalidate the AVL balance rules
			self._inspect_deletion(node_parent)

	def search(self,value):
		if self.root!=None:
			return self._search(value,self.root)
		else:
			return False

	def _search(self,value,cur_node):
		if value==cur_node.value:
			return True
		elif value<cur_node.value and cur_node.left_child!=None:
			return self._search(value,cur_node.left_child)
		elif value>cur_node.value and cur_node.right_child!=None:
			return self._search(value,cur_node.right_child)
		return False 


	# Functions added for AVL...

	def _inspect_insertion(self,cur_node,path=[]):
		if cur_node.parent==None: return
		path=[cur_node]+path

		left_height =self.get_height(cur_node.parent.left_child)
		right_height=self.get_height(cur_node.parent.right_child)

		if abs(left_height-right_height)>1:
			path=[cur_node.parent]+path
			self._rebalance_node(path[0],path[1],path[2])
			return

		new_height=1+cur_node.height 
		if new_height>cur_node.parent.height:
			cur_node.parent.height=new_height

		self._inspect_insertion(cur_node.parent,path)

	def _inspect_deletion(self,cur_node):
		if cur_node==None: return

		left_height =self.get_height(cur_node.left_child)
		right_height=self.get_height(cur_node.right_child)

		if abs(left_height-right_height)>1:
			y=self.taller_child(cur_node)
			x=self.taller_child(y)
			self._rebalance_node(cur_node,y,x)

		self._inspect_deletion(cur_node.parent)

	def _rebalance_node(self,z,y,x):
		if y==z.left_child and x==y.left_child:
			self._right_rotate(z)
		elif y==z.left_child and x==y.right_child:
			self._left_rotate(y)
			self._right_rotate(z)
		elif y==z.right_child and x==y.right_child:
			self._left_rotate(z)
		elif y==z.right_child and x==y.left_child:
			self._right_rotate(y)
			self._left_rotate(z)
		else:
			raise Exception('_rebalance_node: z,y,x node configuration not recognized!')

	def _right_rotate(self,z):
		sub_root=z.parent 
		y=z.left_child
		t3=y.right_child
		y.right_child=z
		z.parent=y
		z.left_child=t3
		if t3!=None: t3.parent=z
		y.parent=sub_root
		if y.parent==None:
				self.root=y
		else:
			if y.parent.left_child==z:
				y.parent.left_child=y
			else:
				y.parent.right_child=y		
		z.height=1+max(self.get_height(z.left_child),
			self.get_height(z.right_child))
		y.height=1+max(self.get_height(y.left_child),
			self.get_height(y.right_child))

	def _left_rotate(self,z):
		sub_root=z.parent 
		y=z.right_child
		t2=y.left_child
		y.left_child=z
		z.parent=y
		z.right_child=t2
		if t2!=None: t2.parent=z
		y.parent=sub_root
		if y.parent==None: 
			self.root=y
		else:
			if y.parent.left_child==z:
				y.parent.left_child=y
			else:
				y.parent.right_child=y
		z.height=1+max(self.get_height(z.left_child),
			self.get_height(z.right_child))
		y.height=1+max(self.get_height(y.left_child),
			self.get_height(y.right_child))

	def get_height(self,cur_node):
		if cur_node==None: return 0
		return cur_node.height

	def taller_child(self,cur_node):
		left=self.get_height(cur_node.left_child)
		right=self.get_height(cur_node.right_child)
		return cur_node.left_child if left>=right else cur_node.right_child

	def minNode(self):
		node = self.root
		while node.left_child is not None:
			node = node.left_child
		return node

	def maxNode(self):
		node = self.root
		while node.right_child is not None:
			node = node.right_child
		return node


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
		self.unfound = 0
		self.doubles = 0

	def insert(self, key):
		if key<0:
			return

		if self.member(key) is not None:
			self.doubles+=1
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
		if self.treeSizes[index] > self.t:
				self.balance()	


	def member(self, key):
		index = self.getIndex(key)
		return self.directory[index].find(key)

	def remove(self, key):
		index = self.getIndex(key)
		self.deleteInTree(index, key)
		self.decrementForestSize()


	def insertInTree(self, index, key):
		if self.member(key) is not None:
			return
		self.incrementTreeSize(index)
		self.directory[index].insert(key)
		

	def deleteInTree(self, index, key):
		self.decrementTreeSize(index)
		self.directory[index].delete_value(key)

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
		#Increase directory AND treesizes
		self.displacements = []
		for i in range(len(self.directory)):
			if self.directory[i].root is not None:
				dis = self.validateNodes(i)
				if dis is not None:
					for d in dis:
						if d is not None:
							self.displacements.append(d)
							self.directory[i].delete_node(d)
							self.treeSizes[i] -= 1

		newDir = []
		for i in range(self.k+2):
			newDir.append(AVLTree())
		newSize = [0] * (self.k+2)

		for i in range(min(self.k+2, len(self.directory))):
			newDir[i] = self.directory[i]
			newSize[i] = self.treeSizes[i]

		self.directory = newDir
		self.treeSizes = newSize

		for d in self.displacements:
			index = self.getIndex(d.value)
			self.insertInTree(index, d.value)




	#Helpers
	def validateNodes(self, index):
		tree = self.directory[index]
		dis = []
		if tree.root is not None:
			self.traverseTree(tree.root, dis, index)
			return dis	

	def traverseTree(self, node, dis, actual):
		if node.left_child is not None:
			self.traverseTree(node.left_child, dis, actual)

		if node.right_child is not None:
			self.traverseTree(node.right_child, dis, actual)

		expected  = self.getIndex(node.value)
		if expected != actual:
			dis.append(node)
			


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
		return self.directory[index].minNode()
		
	def maxNode(self, index):
		return self.directory[index].maxNode()

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
		if self.treeSizes[self.k+1] != 0:
				newB = self.minNode(self.k+1).value
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
		for i in self.directory:
			print(i)
