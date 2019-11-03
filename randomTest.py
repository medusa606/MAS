import random
import os.path

save_path = 'E:/Q_learn/'
completeName = os.path.join(save_path, "random_log.txt")       


repeats = 3
mUP, mDW, mLT, mRT, mNO = 0,0,0,0,0

f = open(completeName, "w")

for nExp in range(1,repeats):
	random.seed(nExp)
	# print("1", random.randint(1,5))
	# random.seed(nExp)
	# print("2", random.randint(1,5))
	# random.seed(nExp)
	# print("3", random.randint(1,5))
	# random.seed(nExp)
	# print("4", random.randint(1,5))
	ran = random.randint(1,5)
	f.write("%d, %d \n" % (nExp, ran))


	if ran==1:
		mUP = mUP + 1
	if ran==2:
		mDW = mDW + 1
	if ran==3:
		mLT = mLT + 1
	if ran==4:
		mRT = mRT + 1
	if ran==5:
		mNO = mNO + 1

f.close()

total = mUP + mDW + mLT + mRT + mNO
pmU = mUP/total
pmD = mDW/total
pmL = mLT/total
pmR = mRT/total
pmN = mNO/total
print("percentage UDLR %.3f %.3f %.3f %.3f %.3f" % (pmU, pmD, pmL, pmR, pmN))
biasVERT = (pmU - pmD)*100
biasHORZ = (pmL - pmR)*100
print("bias pc VERT UP %.3f HORZ LEFT %.3f" % (biasVERT, biasHORZ))


	