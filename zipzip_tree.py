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

class ZipZipTree:
	def __init__(self, capacity: int):
		self.capacity = capacity
		self.root = None
		#self.size = 0

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
		if rank is None:
			rank = self.get_random_rank()

		x = Node(key,val,rank)
		cur = self.root
		prev = None
		while cur and (rank.geometric_rank < cur.rank.geometric_rank or (rank.geometric_rank == cur.rank.geometric_rank and key > cur.key)):
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
		elif left.rank.geometric_rank >= right.rank.geometric_rank:
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
			if left.rank.geometric_rank >= right.rank.geometric_rank:
				while(left and left.rank.geometric_rank >= right.rank.geometric_rank):
					prev = left
					left = left.right

				prev.right = right
			else:
				while(right and left.rank.geometric_rank < right.rank.geometric_rank):
					prev = right
					right = right.left
				prev.left = left
			


	def find(self, key: KeyType) -> ValType:
		pass

	def get_size(self) -> int:
		pass

	def get_height(self) -> int:
		pass

	def get_depth(self, key: KeyType):
		pass

	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define
