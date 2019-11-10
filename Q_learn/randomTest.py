import random
import os.path
import csv
import numpy as np


# save_path = 'E:/Q_learn/'
# completeName = os.path.join(save_path, "random_log.txt")  

#useful one-liner
# [(x, y) for x in [1,2,3] for y in [3,1,4] if x != y]     

columns = 2
lines = 1000000

results = np.zeros(shape=(lines,columns+1))

mUP, mDW, mLT, mRT, mNO = 0,0,0,0,0

# f = open(completeName, "w")
f = open("random_action_test.txt", "w")
random.seed(0)

for col in range(0,columns):
	random.seed(0)
	for ln in range(1,lines):
		# random.seed(nExp)
		# print("1", random.randint(1,5))
		#random.seed(nExp)
		# print("2", random.randint(1,5))
		#random.seed(nExp)
		# print("3", random.randint(1,5))
		#random.seed(nExp)
		# print("4", random.randint(1,5))
		ran = random.randint(1,5)
		# f.write("%d, %d \n" % (nExp, ran))
		results[ln,col] = ran
		# f.write("%d \n" % ran)


		# if ran==1:
		# 	mUP = mUP + 1
		# if ran==2:
		# 	mDW = mDW + 1
		# if ran==3:
		# 	mLT = mLT + 1
		# if ran==4:
		# 	mRT = mRT + 1
		# if ran==5:
		# 	mNO = mNO + 1
# f.write("%d \n" % ran)
# f.close()

is_same = np.array_equal(results[:,0],results[:,1])
results[:,2] = is_same

# output = is_same.all()
print("random sets are the same? = ", is_same)

np.savetxt("random_action_test.csv", results, delimiter=",")


# total = mUP + mDW + mLT + mRT + mNO
# pmU = mUP/total
# pmD = mDW/total
# pmL = mLT/total
# pmR = mRT/total
# pmN = mNO/total
# print("percentage UDLR %.3f %.3f %.3f %.3f %.3f" % (pmU, pmD, pmL, pmR, pmN))
# biasVERT = (pmU - pmD)*100
# biasHORZ = (pmL - pmR)*100
# print("bias pc VERT UP %.3f HORZ LEFT %.3f" % (biasVERT, biasHORZ))


	