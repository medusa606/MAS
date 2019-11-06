import random
# random.seed(1)

condition=True
a=0



while(condition):
			
	a = random.randint(1,10)
	print(a)
	if a>0 and a<6:
		condition=False
		print("exiting")
		
	else:
		print("continuing")
		