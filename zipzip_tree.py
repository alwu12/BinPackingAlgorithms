# explanations for member functions are provided in requirements.py
# each file that uses a Zip Tree should import it from this file

from __future__ import annotations

from typing import TypeVar
from dataclasses import dataclass
import random
import math

KeyType = TypeVar('KeyType')
ValType = TypeVar('ValType')


class Node: 
	def __init__(self, key: KeyType, val: ValType, rank: Rank, left = None, right = None):
		self.key = key
		self.val = val
		self.rank = rank
		self.left = left
		self.right = right

	def __str__(self):
		return (f"Node(key={self.key}, val={self.val}, "
		        f"rank=(g={self.rank.geometric_rank}, u={self.rank.uniform_rank}), "
		        f"left={self.left.key if self.left else None}, "
		        f"right={self.right.key if self.right else None})")

@dataclass
class Rank:
	geometric_rank: int
	uniform_rank: int

	def __lt__(self, other: 'Rank') -> bool: #custom comparator and yippie i dont needa write eq or gt
		if self.geometric_rank != other.geometric_rank:
			return self.geometric_rank < other.geometric_rank
		return self.uniform_rank < other.uniform_rank

class ZipZipTree:
	def __init__(self, capacity: int):
		self.capacity = capacity
		self.root = None
		self.size = 0

	def get_random_rank(self) -> Rank:
        # Geometric distribution with p=0.5 (0-based rank)
		# Using random.expovariate for a geometric-like distribution
		# Geometric rank: number of failures before success (0-based)
		geo_rank = math.floor(math.log(random.random()) / math.log(1 - 0.5))

		# Uniform distribution from 0 to floor(log(capacity)^3 - 1)
		if self.capacity <= 1:
			uni_rank = 0  # Handle edge case
		else:
			log_cubed = math.log(self.capacity) ** 3
			max_rank = math.floor(log_cubed - 1)
			max_rank = max(0, max_rank)  # Ensure non-negative
			uni_rank = random.randint(0, max_rank)
		
		return Rank(geometric_rank=geo_rank, uniform_rank=uni_rank)
        

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
		elif key < prev.key:
			prev.left = x
		else:
			prev.right = x


		if cur == None:
			x.left = x.right = None
			#print(f"RETURNING EARLY AS IN RIGHT NOW, KEY IS {key}")
			return
		if key < cur.key:
			x.right = cur
		else:
			x.left = cur
		prev = x

		
		while cur:
			fix = prev
			if cur.key < key:
				while cur and cur.key <= key:
					prev = cur
					cur = cur.right
			else:
				while cur and cur.key >= key:
					prev = cur
					cur = cur.right
			
			if fix.key > key or (fix == x and prev.key > key):
				fix.left = cur
			else:
				fix.right = cur

	def remove(self, key: KeyType):
		cur = self.root
		
		prev = None
		while key != cur.key:
			prev = cur
			if key < cur.key:
				cur = cur.left
			else:
				cur = cur.right

		if not cur:
			return  # Key not found
		left = cur.left
		right = cur.right

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
		elif key < prev.key:
			prev.left = cur
		else:
			prev.right = cur

		while left and right:
			if left.rank >= right.rank:
				while(left and left.rank >= right.rank):
					prev = left
					left = left.right

				prev.right = right
			else:
				while(right and left.rank < right.rank):
					prev = right
					right = right.left
				prev.left = left
		self.size -= 1


	def find(self, key: KeyType) -> ValType:
		node = self.root
		while node:
			if key == node.key:
				return node.val
			node = node.left if key < node.key else node.right
		
		raise KeyError(f"Key {key} not found")
	#should never get here cause we can assume item exists in tree
		

	def get_size(self) -> int:
		return self.size

	def get_height(self) -> int:
		def get_height_helper(node: Node):
			if not node:
				return -1
			return 1+max(get_height_helper(node.left),get_height_helper(node.right))
		#basically recursing to find the longest path, and that will determine our height
		return get_height_helper(self.root)


	def get_depth(self, key: KeyType):
		def get_depth_helper(node: Node, key: KeyType, depth: int) -> int:
			if not node:
				return -1
			if node.key == key:
				return depth #node was found!
			if key < node.key:
				return get_depth_helper(node.left,key,depth+1)
			return get_depth_helper(node.right,key,depth+1)
		
		return get_depth_helper(self.root,key,0)
			
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
			print(f"{indent}Node(key={node.key}, val={node.val}, "
				f"rank=(g={node.rank.geometric_rank}, u={node.rank.uniform_rank}), "
				f"left={left_key}, right={right_key})")
			# Print left subtree
			print_helper(node.left, level + 1)
		
		if not self.root:
			print("Empty tree")
		else:
			print("Tree nodes (in-order traversal):")
			print_helper(self.root)

	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define
