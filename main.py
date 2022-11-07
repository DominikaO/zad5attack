
class Attack():
	def __init__(self):
		self.pc_pairs = {}
		self.c_ks = {}
		self.p_ks = {}
		self.aprox = 0
		self.LA1 = 0
		self.LA2 = 1
		self.LA3 = 2


	def read(self,path):
		pt = 0
		f = open(path, "r")
		lines = f.readlines()
		for line in lines:
			self.pc_pairs[pt] = int(line[0:4],base=16)
			pt +=1

	def inv_sbox(self, input):
		sb = [15, 8, 11, 4, 6, 5, 14, 0, 3, 13, 12, 7, 10, 9, 2, 1]
		out = 0
		left = (input & 0xF0) >> 4
		right = (input & 0x0F)

		out_left = sb[left]
		out_right = sb[right]
		out |= out_left << 4
		out |= out_right
		return out

	def trajektorie(self, x, u_4):
		res = 0
		if (self.aprox == self.LA1):
			res = ((x >> 5) ^ (x >> 6) ^ (x >> 7) ^ u_4 ^ (u_4 >> 4)) & 1 # 1 a 2
			# res = ((x >> 6) ^ (x >> 7) ^ u_4 ^ (u_4 >> 11)) & 1 # 1 a 4

		if (self.aprox == self.LA2):
			res = ((x >> 4) ^ (x >> 5) ^ (x >> 7) ^ u_4) & 1  # 3

		if (self.aprox == self.LA3):
			res = ((x >> 4)  ^ u_4) & 1  # 4

		return res

	def find_subkey1(self):
		counter = 0
		self.c_ks = {}
		self.p_ks = {}
		subsubkey = 0
		max_p = 0
		for pc in self.pc_pairs:
			ct = self.pc_pairs[pc]
			x = pc
			y = (ct & 0xFF00) >> 8;
			for k in range(256):
				input = y ^ k
				u_4 = self.inv_sbox(input)

				if (self.trajektorie(x, u_4) == 0):
					if (self.c_ks.get(k) != None):
						count = self.c_ks[k]
						count += 1
						self.c_ks[k] = count

					else:
						self.c_ks[k] = 1
		counter = len(self.pc_pairs)

		for kc in self.c_ks:
			k = kc
			count = self.c_ks[kc]
			p = abs(count - (counter / 2)) / counter
			self.p_ks[k] = p

			if (p > max_p):
				max_p = p
				subsubkey = k

		print("Cast podkluca: ", hex(subsubkey))
		return subsubkey

	def find_subkey2(self):
		counter = 0
		self.c_ks = {}
		self.p_ks = {}
		subsubkey = 0
		max_p = 0
		for pc in self.pc_pairs:
			ct = self.pc_pairs[pc]
			x = pc
			y = (ct & 0x00F0) >> 4
			for k in range(256):
				input = y ^ k
				u_4 = self.inv_sbox(input)

				if (self.trajektorie(x, u_4) == 0):
					if (self.c_ks.get(k) != None):
						count = self.c_ks[k]
						count += 1
						self.c_ks[k] = count

					else:
						self.c_ks[k] = 1
		counter = len(self.pc_pairs)

		for kc in self.c_ks:
			k = kc
			count = self.c_ks[kc]
			p = abs(count - (counter / 2)) / counter
			self.p_ks[k] = p

			if (p > max_p):
				max_p = p
				subsubkey = k

		print("Cast podkluca: ",hex(subsubkey))
		return subsubkey

	def find_subkey3(self):
		counter = 0
		self.c_ks = {}
		self.p_ks = {}
		subsubkey = 0
		max_p = 0
		for pc in self.pc_pairs:
			ct = self.pc_pairs[pc]
			x = pc
			y = (ct & 0x000F)
			for k in range(256):
				input = y ^ k
				u_4 = self.inv_sbox(input)

				if (self.trajektorie(x, u_4) == 0):
					if (self.c_ks.get(k) != None):
						count = self.c_ks[k]
						count += 1
						self.c_ks[k] = count

					else:
						self.c_ks[k] = 1
		counter = len(self.pc_pairs)

		for kc in self.c_ks:
			k = kc
			count = self.c_ks[kc]
			p = abs(count - (counter / 2)) / counter
			self.p_ks[k] = p

			if (p > max_p):
				max_p = p
				subsubkey = k

		print("Cast podkluca: ", hex(subsubkey))
		return  subsubkey

	def find_key(self):
		key = 0
		self.aprox = 0
		k1 = self.find_subkey1()
		key |= (k1 << 8);
		self.aprox = 1
		k2 = self.find_subkey2()
		key |= (k2 << 4);
		self.aprox = 2
		k3 = self.find_subkey3() & 0x000F;
		key |= k3

		print("Podkluc: ",  hex(key))
		return key

print("Zadanie 5 (7)")
print("Linearna kryptoanalyza")
print("Pre Sbox: 7fe8354b1dc2a960 ")
test = Attack()
#test.read("D:\\FEI\\NKS\\untitled1\\98044.7fe8354b1dc2a960.dat")
test.read("D:\\FEI\\NKS\\untitled1\\msk_todo['6203', '431c', '1b1e', '23e4', '5613'].dat")
test.find_key()













