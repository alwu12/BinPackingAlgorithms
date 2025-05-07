from zipzip_tree import *
from math import isclose


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
			old_best = node.best_remaining
			self.update_best_remaining(node)
			if isclose(node.best_remaining, old_best, rel_tol=EPS):
				break  # Early exit if no change
			node = self.parents.get(node)

	def find(self, size):
		result = None
		x = self.root
		
		while x:
			# First, check if the left child has enough space
			if x.left and (x.left.best_remaining > size + EPS or isclose(x.left.best_remaining, size, rel_tol=EPS)):
				# Go left if the left subtree could have a better fit
				x = x.left
			# Then, check if the current node has enough space
			elif x.best_remaining > size + EPS or isclose(x.best_remaining, size, rel_tol=EPS):
				result = x  # This is the best fit for now
				break
			# Lastly, check the right child if there's no fit yet
			elif x.right and (x.right.best_remaining > size + EPS or isclose(x.right.best_remaining, size, rel_tol=EPS)):
				# Go right if the left and current nodes are not suitable
				x = x.right
			else:
				# If no valid space left, break
				break
		
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


