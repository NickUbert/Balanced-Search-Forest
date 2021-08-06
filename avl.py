import random, math


class Node():
    def __init__(self, key):
        self.key = key
        self.parent = None
        self.left = None
        self.right = None
        self.height = 0 
    
    def __str__(self):
        return str(self.key) + "(" + str(self.height) + ")"
    
    def is_leaf(self):
        return (self.height == 0)
   
    def max_children_height(self):
        if self.left and self.right:
            return max(self.left.height, self.right.height)
        elif self.left and not self.right:
            return self.left.height
        elif not self.left and  self.right:
            return self.right.height
        else:
            return -1
        
    def balance (self):
        return (self.left.height if self.left else -1) - (self.right.height if self.right else -1)

class AVLTree():
    def __init__(self, *args):
        self.root = None
        self.elements_count = 0
        self.rebalance_count = 0
        if len(args) == 1:
            for i in args[0]:
                self.insert (i)
        
    def height(self):
        if self.root:
            return self.root.height
        else:
            return 0
        
    def rebalance (self, node_to_rebalance):
        self.rebalance_count += 1
        A = node_to_rebalance 
        F = A.parent #allowed to be NULL
        if node_to_rebalance.balance() == -2:
            if node_to_rebalance.right.balance() <= 0:
                """Rebalance, case RRC """
                B = A.right
                C = B.right
                assert (not A is None and not B is None and not C is None)
                A.right = B.left
                if A.right:
                    A.right.parent = A
                B.left = A
                A.parent = B                                                               
                if F is None:                                                              
                   self.root = B 
                   self.root.parent = None                                                   
                else:                                                                        
                   if F.right == A:                                                          
                       F.right = B                                                                  
                   else:                                                                      
                       F.left = B                                                                   
                   B.parent = F 
                self.recompute_heights (A) 
                self.recompute_heights (B.parent)                                                                                         
            else:
                """Rebalance, case RLC """
                B = A.right
                C = B.left
                assert (not A is None and not B is None and not C is None)
                B.left = C.right
                if B.left:
                    B.left.parent = B
                A.right = C.left
                if A.right:
                    A.right.parent = A
                C.right = B
                B.parent = C                                                               
                C.left = A
                A.parent = C                                                             
                if F is None:                                                             
                    self.root = C
                    self.root.parent = None                                                    
                else:                                                                        
                    if F.right == A:                                                         
                        F.right = C                                                                                     
                    else:                                                                      
                        F.left = C
                    C.parent = F
                self.recompute_heights (A)
                self.recompute_heights (B)
        else:
            assert(node_to_rebalance.balance() == +2)
            if node_to_rebalance.left.balance() >= 0:
                B = A.left
                C = B.left
                """Rebalance, case LLC """
                assert (not A is None and not B is None and not C is None)
                A.left = B.right
                if (A.left): 
                    A.left.parent = A
                B.right = A
                A.parent = B
                if F is None:
                    self.root = B
                    self.root.parent = None                    
                else:
                    if F.right == A:
                        F.right = B
                    else:
                        F.left = B
                    B.parent = F
                self.recompute_heights (A)
                self.recompute_heights (B.parent) 
            else:
                B = A.left
                C = B.right 
                """Rebalance, case LRC """
                assert (not A is None and not B is None and not C is None)
                A.left = C.right
                if A.left:
                    A.left.parent = A
                B.right = C.left
                if B.right:
                    B.right.parent = B
                C.left = B
                B.parent = C
                C.right = A
                A.parent = C
                if F is None:
                   self.root = C
                   self.root.parent = None
                else:
                   if (F.right == A):
                       F.right = C
                   else:
                       F.left = C
                   C.parent = F
                self.recompute_heights (A)
                self.recompute_heights (B)
                
            
    def recompute_heights (self, start_from_node):
        changed = True
        node = start_from_node
        while node and changed:
            old_height = node.height
            node.height = (node.max_children_height() + 1 if (node.right or node.left) else 0)
            changed = node.height != old_height
            node = node.parent
       
    def add_as_child (self, parent_node, child_node):
        node_to_rebalance = None
        if child_node.key < parent_node.key:
            if not parent_node.left:
                parent_node.left = child_node
                child_node.parent = parent_node
                if parent_node.height == 0:
                    node = parent_node
                    while node:
                        node.height = node.max_children_height() + 1
                        if not node.balance () in [-1, 0, 1]:
                            node_to_rebalance = node
                            break #we need the one that is furthest from the root
                        node = node.parent     
            else:
                self.add_as_child(parent_node.left, child_node)
        else:
            if not parent_node.right:
                parent_node.right = child_node
                child_node.parent = parent_node
                if parent_node.height == 0:
                    node = parent_node
                    while node:
                        node.height = node.max_children_height() + 1
                        if not node.balance () in [-1, 0, 1]:
                            node_to_rebalance = node
                            break #we need the one that is furthest from the root
                        node = node.parent       
            else:
                self.add_as_child(parent_node.right, child_node)
        
        if node_to_rebalance:
            self.rebalance (node_to_rebalance)
    
    def insert (self, key):
        new_node = Node (key)
        if not self.root:
            self.root = new_node
        else:
            if not self.find(key):
                self.elements_count += 1
                self.add_as_child (self.root, new_node)
      
    def find_biggest(self, start_node):
        node = start_node
        while node.right:
            node = node.right
        return node 
    
    def find_smallest(self, start_node):
        node = start_node
        while node.left:
            node = node.left
        return node
     
    def inorder_non_recursive (self):
        node = self.root
        retlst = []
        while node.left:
            node = node.left
        while (node):
            retlst += [node.key]
            if (node.right):
                node = node.right
                while node.left:
                    node = node.left
            else:
                while ((node.parent)  and (node == node.parent.right)):
                    node = node.parent
                node = node.parent
        return retlst
 
    def preorder(self, node, retlst = None):
        if retlst is None:
            retlst = []
        retlst += [node.key]
        if node.left:
            retlst = self.preorder(node.left, retlst) 
        if node.right:
            retlst = self.preorder(node.right, retlst)
        return retlst         
           
    def inorder(self, node, retlst = None):
        if retlst is None:
            retlst = [] 
        if node.left:
            retlst = self.inorder(node.left, retlst)
        retlst += [node.key] 
        if node.right:
            retlst = self.inorder(node.right, retlst)
        return retlst
        
    def postorder(self, node, retlst = None):
        if retlst is None:
            retlst = []
        if node.left:
            retlst = self.postorder(node.left, retlst) 
        if node.right:
            retlst = self.postorder(node.right, retlst)
        retlst += [node.key]
        return retlst  
    
    def as_list (self, pre_in_post):
        if not self.root:
            return []
        if pre_in_post == 0:
            return self.preorder (self.root)
        elif pre_in_post == 1:
            return self.inorder (self.root)
        elif pre_in_post == 2:
            return self.postorder (self.root)
        elif pre_in_post == 3:
            return self.inorder_non_recursive()      
          
    def find(self, key):
        return self.find_in_subtree (self.root, key )

    def member(self, key):
        return self.find(key)

    def minimum(self):
        return self.find_smallest(self.root)

    def maximum(self):
        return self.find_biggest(self.root)
    
    def find_in_subtree (self,  node, key):
        if node is None:
            return None  # key not found
        if key < node.key:
            return self.find_in_subtree(node.left, key)
        elif key > node.key:
            return self.find_in_subtree(node.right, key)
        else:  # key is equal to node key
            return node
    
    def remove (self, key):
        # first find
        node = self.find(key)
        
        if node is not None:
            self.elements_count -= 1
            
            #     There are three cases:
            # 
            #     1) The node is a leaf.  Remove it and return.
            # 
            #     2) The node is a branch (has only 1 child). Make the pointer to this node 
            #        point to the child of this node.
            # 
            #     3) The node has two children. Swap items with the successor
            #        of the node (the smallest item in its right subtree) and
            #        delete the successor from the right subtree of the node.
            if node.is_leaf():
                self.remove_leaf(node)
            elif (bool(node.left)) ^ (bool(node.right)):  
                self.remove_branch (node)
            else:
                assert (node.left) and (node.right)
                self.swap_with_successor_and_remove (node)
            
    def remove_leaf (self, node):
        parent = node.parent
        if (parent):
            if parent.left == node:
                parent.left = None
            else:
                assert (parent.right == node)
                parent.right = None
            self.recompute_heights(parent)
        else:
            self.root = None
        del node
        # rebalance
        node = parent
        while (node):
            if not node.balance() in [-1, 0, 1]:
                self.rebalance(node)
            node = node.parent
        
        
    def remove_branch (self, node):
        parent = node.parent
        if (parent):
            if parent.left == node:
                parent.left = node.right or node.left
            else:
                assert (parent.right == node)
                parent.right = node.right or node.left
            if node.left:
                node.left.parent = parent
            else:
                assert (node.right)
                node.right.parent = parent 
            self.recompute_heights(parent)
        
        if self.root.key == node.key:
            if node.left is None:
                self.root = node.right
                self.root.parent= None
                self.recompute_heights(self.root)
            else:
                self.root = node.left
                self.root.parent = None
                self.recompute_heights(self.root)

        del node



        # rebalance
        node = parent
        while (node):
            if not node.balance() in [-1, 0, 1]:
                self.rebalance(node)
            node = node.parent
        
    def swap_with_successor_and_remove (self, node):
        successor = self.find_smallest(node.right)
        self.swap_nodes (node, successor)
        assert (node.left is None)
        if node.height == 0:
            self.remove_leaf (node)
        else:
            self.remove_branch (node)
            
    def swap_nodes (self, node1, node2):
        assert (node1.height > node2.height)
        parent1 = node1.parent
        left1 = node1.left
        right1 = node1.right
        parent2 = node2.parent
        assert (not parent2 is None)
        assert (parent2.left == node2 or parent2 == node1)
        left2 = node2.left
        assert (left2 is None)
        right2 = node2.right
        
        # swap heights
        tmp = node1.height 
        node1.height = node2.height
        node2.height = tmp
       
        if parent1:
            if parent1.left == node1:
                parent1.left = node2
            else:
                assert (parent1.right == node1)
                parent1.right = node2
            node2.parent = parent1
        else:
            self.root = node2
            node2.parent = None
            
        node2.left = left1
        left1.parent = node2
        node1.left = left2 # None
        node1.right = right2
        if right2:
            right2.parent = node1 
        if not (parent2 == node1):
            node2.right = right1
            right1.parent = node2
            
            parent2.left = node1
            node1.parent = parent2
        else:
            node2.right = node1
            node1.parent = node2           
           
    def predecessor(self, key):
        node = self.find(key)
        if node is not None:
            if node.left != None:
                node = node.left
                while node.right != None:
                    node = node.right
                return node
            p = node.parent
            while p != None and node == p.left:
                node = p
                p =p.parent
            return p 
        return None


    def successor(self, key):
        node = self.find(key)
        if node is not None:
            if node.right != None:
                node = node.right
                while node.left != None:
                    node = node.left
                return node
            p = node.parent
            while p != None and node == p.right:
                node = p
                p = p.parent
            return p 
        return None