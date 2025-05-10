from zipzip_tree import *
from math import isclose
from decimal import Decimal
import random

#random.seed(2) #fails test case 4
EPS = Decimal('4e-11')

class Node: 
	def __init__(self, key: KeyType, val: ValType, rank: Rank, left = None, right = None):
		self.key = key
		self.val = val
		self.rank = rank
		self.left = left
		self.right = right
		self.best_remaining = key[0] #the key will always be a tuple


	def __str__(self):
		return (f"Node(key={self.key}, val={self.val}, "
		        f"rank=(g={self.rank.geometric_rank}, u={self.rank.uniform_rank}), "
		        f"left={self.left.key if self.left else None}, "
		        f"right={self.right.key if self.right else None})")
#in this zipzip tree, key will be the bin index
#val will be the amount of space remaining
class ZipZipTreeBF(ZipZipTree):
	#do an inorder traversal
	#the first node that has enough capacity given our size, return that node
	#if we return none, we should be inserting a new bin
	def __init__(self, capacity: int):
		self.capacity = capacity
		self.root = None
		self.size = 0
		self.parents = {}
		#update parents dict whenever we modify left or right

	def insert(self, key: KeyType, val: ValType, rank: Rank = None):
		self.size += 1
		if rank is None:
			rank = self.get_random_rank()

		x = Node(key,val,rank)
		cur = self.root
		prev = None
		while cur and (rank < cur.rank or (rank == cur.rank and key > cur.key)):
			prev = cur
			if (key < cur.key):
				cur = cur.left
			else:
				cur = cur.right
		
		if cur == self.root:
			self.root = x
			self.parents[x] = None #  Track parent
		elif key < prev.key:
			prev.left = x
			self.parents[x] = prev  #  Track parent
		else:
			prev.right = x
			self.parents[x] = prev  #  Track parent
		if self.root:
		if cur == None:
			x.left = None
			x.right = None
			self.backpropagate_best_remaining(x) #update all parent's best remaining

			return
		if key < cur.key:
			x.right = cur
			self.parents[cur] = x  #  Update parent
			self.backpropagate_best_remaining(x.right)
		else:
			x.left = cur
			self.parents[cur] = x  #  Update parent
			self.backpropagate_best_remaining(x.left)
		prev = x
		
		while cur:
			fix = prev
			if cur.key < key:
				while cur and (cur.key < key or cur.key == key):
					prev = cur
					cur = cur.right
			else:
				while cur and (cur.key > key or cur.key ==key):
					prev = cur
					cur = cur.left


			if fix.key > key or (fix == x and prev.key > key):
				fix.left = cur
				if cur: self.parents[cur] = fix  #  Update parent
			else:
				fix.right = cur
				if cur: self.parents[cur] = fix  #  Update parent
			self.backpropagate_best_remaining(fix)

		self.backpropagate_best_remaining(x) #update all parent's best remaining
		
	def remove(self, key: KeyType):
		cur = self.root
		
		# Early return if tree is empty or key not found
		if cur is None:
			return

		prev = None
		while key != cur.key:
			prev = cur
			if key < cur.key:
				cur = cur.left
			else:
				cur = cur.right
			if cur is None:
				return

		left = cur.left
		right = cur.right

		self.parents.pop(cur, None)

		if left is None:
			cur = right
		elif right is None:
			cur = left
		elif left.rank >= right.rank:
			cur = left
		else:
			cur = right

		if self.root and self.root.key == key:
			self.root = cur
			if cur:
				self.parents[cur] = None
		elif key < prev.key:
			prev.left = cur
			if cur:
				self.parents[cur] = prev
		else:
			prev.right = cur
			if cur:
				self.parents[cur] = prev

		while left and right:
			if left.rank >= right.rank:
				while left and left.rank >= right.rank:
					prev = left
					left = left.right
				prev.right = right
				if right:
					self.parents[right] = prev
			else:
				while right and left.rank < right.rank:
					prev = right
					right = right.left
				prev.left = left
				if left:
					self.parents[left] = prev

		if prev:
			self.backpropagate_best_remaining(prev)
		
		self.size -= 1


	def update_best_remaining(self, node: Node):
		if node is None:
			return
		
		left_best = node.left.best_remaining if node.left else float('-inf')
		right_best = node.right.best_remaining if node.right else float('-inf')

		node.best_remaining = max(node.key[0], left_best,right_best)
		
	
	def backpropagate_best_remaining(self, node: Node):
		while node is not None:
			parent = self.parents.get(node)#debug starts here
			self.update_best_remaining(node)
			node = parent

	
	def find(self, size):
		result = None
		x = self.root

		while x:
			if x.left and (x.left.best_remaining > size + EPS or isclose(x.left.best_remaining, size, rel_tol=EPS)):

				x = x.left
			elif x.key[0] > size + EPS or isclose(x.key[0], size, rel_tol=EPS):
				#changed to use key because thats how we are storing capacity

				result = x
				break
			elif x.right:				
				if x.right.best_remaining > size + EPS or isclose(x.right.best_remaining, size, rel_tol=EPS):
					x = x.right
				else:
					break
			else:
				break


		return result

	
	def allocate_bin(self, size, bin_index):
		node = self.find(size)

		if node:
			temp = tuple()
			if isclose(node.key[0], size, rel_tol=EPS):
				temp = (0,node.key[1])
			else:
				temp = (node.key[0] - size, node.key[1])
			

			self.remove(node.key)
			if(temp[0] != 0):
				self.insert(temp,1)
			#self.backpropagate_best_remaining(temp)
			return temp[1]
		else:
			new_key = (Decimal('1.0')-size,bin_index + 1)
			self.insert(new_key, 1)
			return new_key[1]

	

	def print_tree(self):
		def print_helper(node, level=0):
			if not node:
				return
			# Print right subtree first (for readability, top-down)
			print_helper(node.right, level + 1)
			# Print current node with indentation
			indent = "  " * level
			left_key = node.left.key if node.left else None
			right_key = node.right.key if node.right else None
			parent = self.parents.get(node)
			parent_key = parent.key if parent else None
			best_remaining = node.best_remaining if hasattr(node, 'best_remaining') else None
			
			print(f"{indent}Node(key={node.key}, val={node.val}, "
				f"rank=(g={node.rank.geometric_rank}, u={node.rank.uniform_rank}), "
				f"best_remaining={best_remaining}, "
				f"left={left_key}, right={right_key}, parent={parent_key})")
			# Print left subtree
			print_helper(node.left, level + 1)

		if not self.root:
			print("Empty tree")
		else:
			print("Tree nodes (in-order traversal):")
			print_helper(self.root)


