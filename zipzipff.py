from zipzip_tree import *
from math import isclose
import random

random.seed(41)
#42 is a passed case
#41 is a failed case
EPS = 4e-11

#in this zipzip tree, key will be the bin index
#val will be the amount of space remaining
class ZipZipTreeFF(ZipZipTree):
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
		#if prev:
		#	print(f'\nfinished first while loop, prev = {prev.key}\n')
		if cur == self.root:
			self.root = x
			self.parents[x] = None #  Track parent
		elif key < prev.key:
			prev.left = x
			self.parents[x] = prev  #  Track parent
		else:
			prev.right = x
			self.parents[x] = prev  #  Track parent

		if cur == None:
			x.left = None
			x.right = None
			#print(f"RETURNING EARLY AS IN RIGHT NOW, KEY IS {key}")
			return
		if key < cur.key:
			x.right = cur
			self.parents[cur] = x  #  Update parent
		else:
			x.left = cur
			self.parents[cur] = x  #  Update parent
		prev = x

		#print(f'\nfinished section 3 if statements, prev is {prev.key}\n')
		while cur:
			fix = prev
			if cur.key < key:
				while cur and (cur.key < key or isclose(cur.key,key, rel_tol=EPS)):
					prev = cur
					cur = cur.right
			else:
				while cur and (cur.key > key or isclose(cur.key,key, rel_tol=EPS)):
					prev = cur
					cur = cur.left
			
			if fix.key > key or (fix == x and prev.key > key):
				fix.left = cur
				if cur: self.parents[cur] = fix  #  Update parent
			else:
				fix.right = cur
				if cur: self.parents[cur] = fix  #  Update parent
		self.backpropagate_best_remaining(x) #update all parent's best remaining
		
	def update_best_remaining(self, node: Node):
		if node is None:
			return
		
		left_best = node.left.best_remaining if node.left else float('-inf')
		right_best = node.right.best_remaining if node.right else float('-inf')

		node.best_remaining = max(node.val, left_best,right_best)
		
	
	def backpropagate_best_remaining(self, node: Node):
		while node is not None:
			parent = self.parents.get(node)#debug starts here
			#print("\n--- Backpropagating Node ---")
			#print(f"Node      → key: {node.key}, val: {node.val}, best_remaining: {node.best_remaining}")
			#if parent:
			#	print(f"Parent    → key: {parent.key}, val: {parent.val}, best_remaining: {parent.best_remaining}")
			#else:
			#	print("Parent    → None")
			#if node.left:
			#	print(f"Left      → key: {node.left.key}, val: {node.left.val}, best_remaining: {node.left.best_remaining}")
			#else:
			#	print("Left      → None")
			#if node.right:
			#	print(f"Right     → key: {node.right.key}, val: {node.right.val}, best_remaining: {node.right.best_remaining}")
			#else:
			#	print("Right     → None")

			old_best = node.best_remaining
			self.update_best_remaining(node)
			#print(f"Updated   → old_best: {old_best}, new_best: {node.best_remaining}")

			node = parent

	
	def find(self, size):
		#print(f"Starting find with size: {size}")
		result = None
		x = self.root

		while x:
			#print(f"Visiting node with best_remaining: {x.best_remaining}")
			#print(f"Node Value: {x.val}")
			#if x.left:
			#	print(f"  Left child exists with best_remaining: {x.left.best_remaining}")
			#else:
			#	print("  No left child")

			if x.left and (x.left.best_remaining > size + EPS or isclose(x.left.best_remaining, size, rel_tol=EPS)):
			#	print("  Going left: left child has sufficient space")
				x = x.left
			elif x.val > size + EPS or isclose(x.val, size, rel_tol=EPS):
			#	print(f"  Found suitable node {x.key}")
			#	print(f"x.val: {x.val}")
			#	print(f"size: {size}")
			#	print(f"x.val > size: {x.val > size}")
			#	print(f"isclose(x.best_remaining, size, rel_tol=EPS): {isclose(x.best_remaining, size, rel_tol=EPS):}")
				
				result = x
				break
			elif x.right:
			#	print(f"  Right child exists with best_remaining: {x.right.best_remaining}")
				if x.right.best_remaining > size + EPS or isclose(x.right.best_remaining, size, rel_tol=EPS):
			#		print("  Going right: right child has sufficient space")
					x = x.right
				else:
			#		print("  Right child doesn't have enough space")
					break
			else:
			#	print("  No suitable node found, breaking")
				break

		#if result:
		#	print(f"Returning node with best_remaining: {result.best_remaining}")
		#else:
		#	print("No suitable node found")

		return result

	
	def allocate_bin(self, size, bin_index):
		node = self.find(size)

		if node:
			if isclose(node.val, size, rel_tol=EPS):
				node.val = 0
			else:
				node.val -= size
			self.backpropagate_best_remaining(node)
			return node.key
		else:
			new_key = bin_index + 1
			self.insert(new_key, 1.0-size)
			return new_key

	

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
			print(f"{indent}Node(key={node.key}, val={node.val}, "
				f"rank=(g={node.rank.geometric_rank}, u={node.rank.uniform_rank}), "
				f"left={left_key}, right={right_key}, parent={parent_key})")
			# Print left subtree
			print_helper(node.left, level + 1)

		if not self.root:
			print("Empty tree")
		else:
			print("Tree nodes (in-order traversal):")
			print_helper(self.root)


