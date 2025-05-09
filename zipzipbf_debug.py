from zipzip_tree import *
from math import isclose
import random

#random.seed(2) #fails test case 4
EPS = 4e-11

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
		old_root = self.root #im planning to use this to help update BRC in if cur == self.root
		while cur and (rank < cur.rank or (rank == cur.rank and key > cur.key)):
			prev = cur
			if (key < cur.key):
				cur = cur.left
			else:
				cur = cur.right
		
		if prev:
			print(f'\nfinished first while loop, prev = {prev.key}\n')
		if self.root:
			print(f'the current root is: {self.root.key}')
		if cur:
			print(f'cur is: {cur.key}')
		
		
		if cur == self.root:
			self.root = x
			self.parents[x] = None #  Track parent
		elif key < prev.key:
			prev.left = x
			self.parents[x] = prev  #  Track parent
		else:
			prev.right = x
			self.parents[x] = prev  #  Track parent
		#if self.root:
		#	print(f'updated root: {self.root}')
		if cur == None:
			x.left = None
			x.right = None
			#print(f"RETURNING EARLY AS IN RIGHT NOW, KEY IS {key}")
			self.backpropagate_best_remaining(x) #update all parent's best remaining

			return
		if key < cur.key:
			#print(f'key{key} is less than cur.key{cur.key}')
			x.right = cur
			self.parents[cur] = x  #  Update parent
			self.backpropagate_best_remaining(x.right)
		else:
			#print(f'key{key} is greater than cur.key{cur.key}')
			x.left = cur
			self.parents[cur] = x  #  Update parent
			self.backpropagate_best_remaining(x.left)
		prev = x
		
		print("Current parents:")
		for child, parent in self.parents.items():
			print(f"  Child: {child.key}, Parent: {parent.key if parent else None}")
		print('How the tree looks after section 2 ###########')
		self.print_tree()
		print(f'\nfinished section 3 if statements, prev is {prev.key}, cur is {cur.key}\n')
		
		
		while cur:
			fix = prev
			#print(f'\nin section 4 while loop, fix is {fix.key}, cur is {cur.key}, key is {key}\n')
			if cur.key < key:
				while cur and (cur.key < key or isclose(cur.key[0],key[0], rel_tol=EPS)):
					prev = cur
					cur = cur.right
			else:
				while cur and (cur.key > key or isclose(cur.key[0],key[0], rel_tol=EPS)):
					prev = cur
					cur = cur.left
			
			print(f'\nmid section 4 heres the tree\n')
			self.print_tree()
			print(f'\nmid section 4 fix.key {fix.key}, key: {key}, prev: {prev.key}, cur: {cur}, x: {x}')
			print(f'fix == x: {fix == x}')
			print(f'prev.key > key: {prev.key > key}')
			print(f'fix.key > key: {fix.key > key}')
			print(f'fix: {fix}')
			
			if fix.key > key or (fix == x and prev.key > key):
				fix.left = cur
				if cur: self.parents[cur] = fix  #  Update parent
			else:
				fix.right = cur
				if cur: self.parents[cur] = fix  #  Update parent
			self.backpropagate_best_remaining(fix)
		print(f'\nfinished section 4 heres the tree\n')
		self.print_tree()
		self.backpropagate_best_remaining(x) #update all parent's best remaining
		
	def remove(self, key: KeyType):
		print(f"REMOVING NODE WITH KEY {key}, TREE BEFORE REMOVAL:")
		self.print_tree()

		cur = self.root
		
		prev = None
		while key != cur.key:
			prev = cur
			if key < cur.key:
				cur = cur.left
			else:
				cur = cur.right
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
				while(left and left.rank >= right.rank):
					prev = left
					left = left.right

				prev.right = right
				if right:
					self.parents[right] = prev
			else:
				while(right and left.rank < right.rank):
					prev = right
					right = right.left
				prev.left = left
				if left:
					self.parents[left] = prev
		if prev:
			print(f"BACKPROPAGATING ON PREV: {prev.key}")
			print("HERE IS THE TREE BEFORE PROPAGATION:")
			self.print_tree()
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
			print("\n--- Backpropagating Node ---")
			print(f"Node      → key: {node.key}, val: {node.val}, best_remaining: {node.best_remaining}")
			if parent:
				print(f"Parent    → key: {parent.key}, val: {parent.val}, best_remaining: {parent.best_remaining}")
			else:
				print("Parent    → None")
			if node.left:
				print(f"Left      → key: {node.left.key}, val: {node.left.val}, best_remaining: {node.left.best_remaining}")
			else:
				print("Left      → None")
			if node.right:
				print(f"Right     → key: {node.right.key}, val: {node.right.val}, best_remaining: {node.right.best_remaining}")
			else:
				print("Right     → None")
			

			old_best = node.best_remaining
			self.update_best_remaining(node)
			print(f"Updated   → old_best: {old_best}, new_best: {node.best_remaining}")

			node = parent

	
	def find(self, size):
		print(f"Starting find with size: {size}")
		result = None
		x = self.root

		while x:
			print(f"Visiting node with best_remaining: {x.best_remaining}")
			print(f"Node key: {x.key}")
			if x.left:
				print(f"  Left child exists with best_remaining: {x.left.best_remaining}")
			else:
				print("  No left child")

			if x.left and (x.left.best_remaining > size + EPS or isclose(x.left.best_remaining, size, rel_tol=EPS)):
				print("  Going left: left child has sufficient space")
				x = x.left
			elif x.key[0] > size + EPS or isclose(x.key[0], size, rel_tol=EPS):
				#changed to use key because thats how we are storing capacity
				print(f"  Found suitable node {x.key}")
				print(f"x.key: {x.key}")
				print(f"size: {size}")
				print(f"x.key[0] > size: {x.key[0] > size}")
				print(f"isclose(x.best_remaining, size, rel_tol=EPS): {isclose(x.best_remaining, size, rel_tol=EPS):}")
				
				result = x
				break
			elif x.right:
				print(f"  Right child exists with best_remaining: {x.right.best_remaining}")
				if x.right.best_remaining > size + EPS or isclose(x.right.best_remaining, size, rel_tol=EPS):
					print("  Going right: right child has sufficient space")
					x = x.right
				else:
					print("  Right child doesn't have enough space")
					break
			else:
				print("  No suitable node found, breaking")
				break

		if result:
			print(f"Returning node with best_remaining: {result.best_remaining}")
		else:
			print("No suitable node found")

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
			new_key = (1.0-size,bin_index + 1)
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


