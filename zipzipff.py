from zipzip_tree import *
from math import isclose


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
			x.left = x.right = None
			#print(f"RETURNING EARLY AS IN RIGHT NOW, KEY IS {key}")
			return
		if key < cur.key:
			x.right = cur
			self.parents[cur] = x  #  Update parent
		else:
			x.left = cur
			self.parents[cur] = x  #  Update parent
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
					cur = cur.left
			
			if fix.key > key or (fix == x and prev.key > key):
				fix.left = cur
				if cur: self.parents[cur] = fix  #  Update parent
			else:
				fix.right = cur
				if cur: self.parents[cur] = fix  #  Update parent
		self.backpropagate_best_remaining(x) #update all parent's best remaining

	def remove(self, key: KeyType):
		cur = self.root
		
		prev = None
		while key != cur.key:
			prev = cur
			if key < cur.key:
				cur = cur.left
			else:
				cur = cur.right

		#if not cur:
			#return  # Key not found
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
			'''
			print(f"removing the root: {self.root.key}")
			print(f"next root will be cur: {cur}")
			if cur.left:
				print(f"cur left {cur.left.key}")
			if cur.right:
				print(f"cur right {cur.right.key}")
			print(f"left: {left}")
			print(f"right: {right}")
			'''
			
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
		
	def update_best_remaining(node: Node):
		if node is None:
			return
		
		left_best = node.left.best_remaining if node.left else float('-inf')
		right_best = node.right.best_remaining if node.right else float('-inf')

		node.best_remaining = max(node.val, left_best,right_best)
		
	
	def backpropagate_best_remaining(self, node: Node):
		while node is not None:
			old_best = node.best_remaining
			self.update_best_remaining(node)
			if isclose(node.best_remaining, old_best):
				break  # Early exit if no change
			node = self.parents.get(node)

	def find(self,size):
		result = None

		x = self.root
		while x.best_remaining > size or isclose(x.best_remaining,size):
			if x.left and (x.left.best_remaining > size or isclose(x.left.best_remaining,size)):
				x = x.left #if the left bin has enough space
			elif x.val > size or isclose(x.val, size):
				result = x #if the left bin is too small and the current bin is fine
				break
			elif x.right and (x.right.best_remaining > size or isclose(x.right.best_remaining, size)):
				x = x.right #if left and middle are too small, check right(lexicographically the last)
			else:
				break #current bin is too small, left and right are too small
			#and as a result need new bin
		return result
	
	def allocate_bin(self, size, bin_index):
		node = self.find(size)

		if node:
			node.val -= size
			self.backpropagate_best_remaining(node)
			return node.key
		else:
			new_key = bin_index + 1
			self.insert(new_key, 1.0-size)
			return new_key

	



