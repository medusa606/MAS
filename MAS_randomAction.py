# cd git/cav/Technical/MAS/Q_learn
# conda activate my_env
# python game.py


import sys
import numpy as np
import cv2
import time
import matplotlib.pyplot as plt
import random
import os.path

class Environment(object):
	
	def __init__(self, gridH, gridW, end_positions, end_rewards, blocked_positions, start_position, default_reward, road_positions, road_rewards, scale=25):
		
		self.action_space = 4
		self.state_space = gridH * gridW	
		self.gridH = gridH
		self.gridW = gridW
		self.scale = scale 

		self.end_positions = end_positions
		self.end_rewards = end_rewards
		self.blocked_positions = blocked_positions

		self.road_positions = road_positions
		self.road_rewards = road_rewards

		#perceptions
		self.on_road = 0
		self.diff_x = 0
		self.diff_y = 0
		self.euclid = 0
		self.inv_euclid = 0
		self.inv_euclid2 = 0
		self.inv_euclid3 = 0
		self.last_av_pos = -1
		
		self.start_position = start_position
		if self.start_position == None:
			self.position = self.init_start_state()
		else:
			self.position = self.start_position
						
		self.state2idx = {}
		self.idx2state = {}
		self.idx2reward = {}
		for i in range(self.gridH):
			for j in range(self.gridW):
				idx = i*self.gridW + j
				self.state2idx[(i, j)] = idx
				self.idx2state[idx]=(i, j)
				self.idx2reward[idx] = default_reward
				
		# set the AV reward
		for position, reward in zip(self.end_positions, self.end_rewards):
			self.idx2reward[self.state2idx[position]] = reward

		#update road rewards
		for position, reward in zip(self.road_positions, self.road_rewards):
			self.idx2reward[self.state2idx[position]] = reward

		self.frame = np.zeros((self.gridH * self.scale, self.gridW * self.scale, 3), np.uint8)	
		
		for position in self.blocked_positions:			
			y, x = position			
			cv2.rectangle(self.frame, (x*self.scale, y*self.scale), ((x+1)*self.scale, (y+1)*self.scale), (100, 100, 100), -1)
		
		for position, reward in zip(self.road_positions, self.road_rewards):
			text = str(int(reward))
			if reward > 0.0: text = '+' + text			
			if reward > 0.0: color = (0, 255, 0)
			else: color = (0, 0, 255)
			font = cv2.FONT_HERSHEY_SIMPLEX
			y, x = position		
			(w, h), _ = cv2.getTextSize(text, font, 1, 2)
			cv2.rectangle(self.frame, (x*self.scale, y*self.scale), ((x+1)*self.scale, (y+1)*self.scale), (100, 100, 100), -1) #from blocked positions
			cv2.putText(self.frame, text, (int((x+0.5)*self.scale-w/2), int((y+0.5)*self.scale+h/2)), font, 1, color, 2, cv2.LINE_AA)	

		for position, reward in zip(self.end_positions, self.end_rewards):
			text = str(int(reward))
			if reward > 0.0: text = '+' + text			
			if reward > 0.0: color = (0, 255, 0)
			else: color = (0, 0, 255)
			font = cv2.FONT_HERSHEY_SIMPLEX
			y, x = position		
			(w, h), _ = cv2.getTextSize(text, font, 1, 2)
			cv2.putText(self.frame, text, (int((x+0.5)*self.scale-w/2), int((y+0.5)*self.scale+h/2)), font, 1, color, 2, cv2.LINE_AA)	
			#cv2.putText(self.frame, text, (int((x+0.5)*self.scale)-w/2, int((y+0.5)*self.scale+h/2)), font, 1, color, 2, cv2.LINE_AA)
			
            

	def init_start_state(self):
		
		while True:
			
			preposition = (np.random.choice(self.gridH), np.random.choice(self.gridW))
			
			if preposition not in self.end_positions and preposition not in self.blocked_positions:
				
				return preposition

	def get_state(self):
		
		return self.state2idx[self.position]

	def update_state(self):
		
		#clear the board of previous blocked positions
		self.frame = np.zeros((self.gridH * self.scale, self.gridW * self.scale, 3), np.uint8)	

		#update blocked positions
		for position in self.blocked_positions:			
			y, x = position			
			cv2.rectangle(self.frame, (x*self.scale, y*self.scale), ((x+1)*self.scale, (y+1)*self.scale), (100, 100, 100), -1)

		# update the road rewards
		for position, reward in zip(self.road_positions, self.road_rewards):
			text = str(int(reward))
			if reward > 0.0: text = '+' + text			
			if reward > 0.0: color = (0, 255, 0)
			else: color = (0, 0, 255)
			font = cv2.FONT_HERSHEY_SIMPLEX
			y, x = position		
			(w, h), _ = cv2.getTextSize(text, font, 1, 2)
			#cv2.rectangle(self.frame, (x*self.scale, y*self.scale), ((x+1)*self.scale, (y+1)*self.scale), (100, 100, 100), -1) #from blocked positions
			cv2.putText(self.frame, text, (int((x+0.5)*self.scale-w/2), int((y+0.5)*self.scale+h/2)), font, 0.5, color, 1, cv2.LINE_AA)	

		#GC update the position of the AV and rewards
		for position, reward in zip(self.end_positions, self.end_rewards):
			self.idx2reward[self.state2idx[position]] = reward
			#update grid
			text = str(int(reward))
			if reward > 0.0: text = '+' + text			
			if reward > 0.0: color = (0, 255, 0)
			else: color = (0, 0, 255)
			font = cv2.FONT_HERSHEY_SIMPLEX
			y, x = position		
			(w, h), _ = cv2.getTextSize(text, font, 1, 2)
			cv2.putText(self.frame, text, (int((x+0.5)*self.scale-w/2), int((y+0.5)*self.scale+h/2)), font, 0.5, color, 1, cv2.LINE_AA)

	def percepts(self, AV_state):
		
		#shorthand - pedestrian position
		xp = self.position[1]
		yp = self.position[0]
		
		#av position
		xa = AV_state[1]
		ya = AV_state[0]

		# is agent on road
		if (xp > 1) | (xp < 4):
			self.on_road = 1
		if (xp <= 1) | (xp >= 4):
			self.on_road = 0
		
		# distance to AV
		self.diff_x = (xp - xa)
		self.diff_y = (yp - ya)
		self.euclid = np.sqrt(np.square(self.diff_x) + np.square(self.diff_y))

		# inverse distance to AV
		if self.euclid == 0:
			self.inv_euclid = 1
			self.inv_euclid2 = 1
			self.inv_euclid3 = 1
		else:
			self.inv_euclid = 1/self.euclid
			self.inv_euclid2 = 1/np.square(self.euclid)
			self.inv_euclid3 = 1/np.power(self.euclid,3)

		# set memory of last known position of the av
		# todo

		# find time to kerb
		# todo

		# find av time to samekerb level
		# todo

		# print("~~~~ env ~~~~")
		# print("xp yp ",xp, yp)
		# print("xa ya ",xa, ya)
		# print("on road ",self.on_road)
		# print("dif y ", self.diff_y)
		# print("diff x ", self.diff_x)
		# print("euclid ", self.euclid)
		# print("inv_euclid ", self.inv_euclid)
		# print("inv_euclid2 ", self.inv_euclid2)
		# print("inv_euclid3 ", self.inv_euclid3)
		# print("~~~~~~~~~~~~~~")

		#return (self.on_road, self.diff_x, self.diff_y, self.euclid, self.inv_euclid, self.inv_euclid2, self.inv_euclid3)
		return (self.on_road, self.diff_x, self.diff_y, self.euclid,0,0,0)

	def one_step_ahead_features(self, future_actions, AV_state):
		
		#shorthand - pedestrian position
		curr_xp = self.position[1]
		curr_yp = self.position[0]
		loop =0

		#print("old position ", curr_xp, curr_yp)
		#print("future_actions ", list(future_actions))

		for action in future_actions:

			#print("action from future_actions", action)

			# Update position based on future_action
			if action == 0:
				xp = curr_xp
				yp = curr_yp + 1 #proposed = (self.position[0] +1, self.position[1])			
			elif action == 1:
				xp = curr_xp
				yp = curr_yp - 1 #proposed = (self.position[0] -1, self.position[1])			
			elif action == 2:
				xp = curr_xp + 1 #proposed = (self.position[0], self.position[1] +1)			
				yp = curr_yp
			elif action == 3:
				xp = curr_xp - 1 #proposed = (self.position[0], self.position[1] -1)
				yp = curr_yp
			#print("new position ", xp, yp)

			#av position
			xa = AV_state[1]
			ya = AV_state[0]

			# is agent on road
			if (xp > 1) | (xp < 4):
				on_road = 1
			if (xp <= 1) | (xp >= 4):
				on_road = 0
			
			# distance to AV
			diff_x = (xp - xa)
			diff_y = (yp - ya)
			euclid = np.sqrt(np.square(diff_x) + np.square(diff_y))

			# inverse distance to AV
			if euclid==0:
				inv_euclid = 1
				inv_euclid2 = 1
				inv_euclid3 = 1
			else:
				inv_euclid = 1/euclid
				inv_euclid2 = 1/np.square(euclid)
				inv_euclid3 = 1/np.power(euclid,3)

			curr_features = np.array([on_road, diff_x, diff_y,euclid, inv_euclid, inv_euclid2, inv_euclid3])
			#print("curr_features ", curr_features)
			#print("loop ", loop)
			if loop == 0:
				features = curr_features
				loop =1
			else:
				features = np.vstack((features,curr_features))
				loop = loop + 1
			#print("features shape ", features.shape)
			#print("features ", features)
		return features

	def get_possible_actions(self):
		
		'''
		pos = self.position
		possible_actions = []
		
		if pos[0]+1<self.nH: and (pos[0]+1,pos[1]) not in self.blocked_positions:
			possible_actions.append(0)
				
		if pos[0]-1>=0 and (pos[0]-1,pos[1]) not in self.blocked_positions:
			possible_actions.append(1)
		
		if pos[1]+1<self.nW and (pos[0],pos[1]+1) not in self.blocked_positions:
			possible_actions.append(2)
				
		if pos[1]-1>=0 and (pos[0],pos[1]-1) not in self.blocked_positions:
			possible_actions.append(3)
		
		return possible_actions		
		'''
		
		return range(self.action_space) 
	
	def step(self, action):

		# Actions are:
		# 0 = down (+Y)
		# 1 = up   (-Y)
		# 2 = right (+X)
		# 3 = left  (-X)
		
		if action >= self.action_space:
			return

		if action == 0:
			proposed = (self.position[0] +1, self.position[1])
			
		elif action == 1:
			proposed = (self.position[0] -1, self.position[1])
			
		elif action == 2:
			proposed = (self.position[0], self.position[1] +1)
			
		elif action == 3:
			proposed = (self.position[0], self.position[1] -1)	
		
		y_within = proposed[0] >= 0 and proposed[0] < self.gridH
		x_within = proposed[1] >= 0 and proposed[1] < self.gridW
		free = proposed not in self.blocked_positions		
		
		if x_within and y_within and free:
			
			self.position = proposed
			
		next_state = self.state2idx[self.position] 
		reward = self.idx2reward[next_state]
		
		if self.position in self.end_positions:
			done = True
		else:
			done = False
			
		return next_state, reward, done
		
	def reset_state(self):
		
		print("\n ~ GAME RESTARTING ~\n")
		if self.start_position == None:
			self.position = self.init_start_state()
		else:
			self.position = self.start_position
	
	def render(self, qvalues_matrix, running_score, time, nA, agentState):
		
		frame = self.frame.copy()

		# for each state cell
		
		for idx, qvalues in enumerate(qvalues_matrix):
			
			position = self.idx2state[idx]
		
			if position in self.end_positions or position in self.blocked_positions:
				continue
			
			qvalues = np.tanh(qvalues*0.1) # for vizualization only
        	
        	# for each action in state cell
	        		
			for action, qvalue in enumerate(qvalues):

				# draw (state, action) qvalue traingle
				
				if action == 0:
					dx2, dy2, dx3, dy3 = 0.0, 1.0, 1.0, 1.0				
				if action == 1:
					dx2, dy2, dx3, dy3 = 0.0, 0.0, 1.0, 0.0				
				if action == 2:
					dx2, dy2, dx3, dy3 = 1.0, 0.0, 1.0, 1.0				
				if action == 3:
					dx2, dy2, dx3, dy3 = 0.0, 0.0, 0.0, 1.0	
					
				x1 = int(self.scale*(position[1] + 0.5))			
				y1 = int(self.scale*(position[0] + 0.5))				
				
				x2 = int(self.scale*(position[1] + dx2))
				y2 = int(self.scale*(position[0] + dy2))
				
				x3 = int(self.scale*(position[1] + dx3))
				y3 = int(self.scale*(position[0] + dy3))		
				
				pts = np.array([[x1, y1], [x2, y2], [x3, y3]], np.int32)
				pts = pts.reshape((-1, 1, 2))
				
				if qvalue > 0: color = (0, int(qvalue*255),0)
				elif qvalue < 0: color = (0,0, -int(qvalue*255))
				else: color = (0, 0, 0)

				cv2.fillPoly(frame, [pts], color)
			
			# draw crossed lines
			
			x1 = int(self.scale*(position[1]))			
			y1 = int(self.scale*(position[0]))
			
			x2 = int(self.scale*(position[1] + 1.0))			
			y2 = int(self.scale*(position[0] + 1.0))

			x3 = int(self.scale*(position[1]+ 1.0 ))			
			y3 = int(self.scale*(position[0]))
			
			x4 = int(self.scale*(position[1]))			
			y4 = int(self.scale*(position[0] + 1.0))
			
			cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
			cv2.line(frame, (x3, y3), (x4, y4), (255, 255, 255), 2)
			
			# draw arrow indicating best action
						
			best_action = 0
			best_qvalue = qvalues[0]
			for action, qvalue in enumerate(qvalues):
				if qvalue > best_qvalue:
					best_qvalue = qvalue
					best_action = action
			
			if best_action == 0:
				dx1, dy1, dx2, dy2 = 0.0, -0.25, 0.0, 0.25	
							
			elif best_action == 1:
				dx1, dy1, dx2, dy2 = 0.0, 0.25, 0.0, -0.25
								
			elif best_action == 2:
				dx1, dy1, dx2, dy2 = -0.25, 0.0, 0.25, 0.0
								
			elif best_action == 3:
				dx1, dy1, dx2, dy2 = 0.25, 0.0, -0.25, 0.0				
									
			x1 = int(self.scale*(position[1] + 0.5 + dx1))			
			y1 = int(self.scale*(position[0] + 0.5 + dy1))	
					
			x2 = int(self.scale*(position[1] + 0.5 + dx2))			
			y2 = int(self.scale*(position[0] + 0.5 + dy2))	
							
			cv2.arrowedLine(frame, (x1, y1), (x2, y2), (255, 100, 0), 8, line_type=8, tipLength=0.5)		
			
		# draw horizontal lines
		
		for i in range(self.gridH+1):
			cv2.line(frame, (0, i*self.scale), (self.gridW * self.scale, i*self.scale), (255, 255, 255), 2)
		
		# draw vertical lines
		
		for i in range(self.gridW+1):
			cv2.line(frame, (i*self.scale, 0), (i*self.scale, self.gridH * self.scale), (255, 255, 255), 2)
		#y, x = self.position

		#======================================
		# draw agent
		#======================================
		for agentID in range(0,nA):
			x,y = agentState[time, agentID,:]
			y1 = int((y + 0.3)*self.scale)
			x1 = int((x + 0.3)*self.scale)
			y2 = int((y + 0.7)*self.scale)
			x2 = int((x + 0.7)*self.scale)
			cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), -1)
		#======================================



		#print score
		text = 'score = ' + str(int(running_score))
		# if running_score > 0.0: text = '+' + text			
		if running_score > 0.0: color = (0, 255, 0)
		else: color = (0, 0, 255)
		font = cv2.FONT_HERSHEY_SIMPLEX
		# y, x = position		
		y = self.gridH - 1
		x = self.gridW - 1
		(w, h), _ = cv2.getTextSize(text, font, 1, 2)

		# cv2.putText(img, running_score, org, fontFace, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]]) 
		cv2.putText(frame, text, (int((x+0.5)*self.scale-w/2), int((y+0.5)*self.scale+h/2)), font, 0.5, color, 1, cv2.LINE_AA)


		cv2.imshow('frame', frame)
		cv2.moveWindow('frame', 0, 0)
		key = cv2.waitKey(1)
		if key == 27: sys.exit()
        


#---------------------------------------------------------------------------------------------
#-------------------------------- ~  Feature Based Agent ~ -----------------------------------
#---------------------------------------------------------------------------------------------
class FeatAgent:

	# This class uses a featured based representation of the world rather than explicit states
	# as such perception is required to inform the agent on the environment
	
	def __init__(self, alpha, epsilon, discount, action_space, state_space):
 
		self.feat_space = 7 #set this to the number of features
		self.action_space = action_space
		self.alpha = alpha
		self.epsilon = epsilon
		self.discount = discount
		# we remove the explicit state space and replace with feature based representation
		#self.qvalues = np.zeros((state_space, action_space), np.float32)
		#self.feat_weights = np.zeros((self.feat_space), np.float32)
		self.feat_weights = np.random.uniform(size=(self.feat_space),low=-1,high=1) #set random feature weights
		self.qvalues = np.zeros((self.feat_space, action_space), np.float32)

		# print("feat_weights ", self.feat_weights)
		# print("qvalues ", self.qvalues)
		# print("feat_space ", self.feat_space)
		# print("action_space ", self.action_space)

	def feat_q_update(self, state, AV_state, action, reward, next_state, next_state_possible_actions, done, features, q_val_dash):

		# calculate Q-values based on the feature representation
		# Q(s,a) = w1.f1(s,a) + w2.f2(s,a) + ... wi.fi(s,a)

		# features are:
		# f1 = on_road
		# f2 = x distance between av and ped
		# f3 = y distance between av and ped
		# f4 = euclidean distance between av and ped
		# f5 = inverse euclidean distance between av and ped
		# f6 = inverse euclidean distance^2 between av and ped
		# f7 = inverse euclidean distance^3 between av and ped

		qval = np.sum(np.multiply(self.feat_weights, features))

		# now update the feature weights given the reward
		difference = (reward + self.alpha * q_val_dash) - qval
		# print("features x weights ", np.multiply(self.feat_weights, features))
		# print("#############################")
		# print("reward ", reward)
		# print("self.discount ", self.discount)
		#print("next_state ", next_state)
		#print("next_state_possible_actions ", list(next_state_possible_actions))
		# print("qval ", qval)
		# print("q_val_dash ", q_val_dash)
		# print("self.feat_weights", self.feat_weights)
		# print("difference", difference)
		#print("self.feat_weights.shape", self.feat_weights.shape)

		for i in range(self.feat_weights.shape[0]):
			wi = self.feat_weights[i]
			self.feat_weights[i] = wi + self.alpha * difference * features[i]
			# print("~~~~~~~~~~~~~~~~~~~~~~~~")
			# print("i", i)
			# print("i w_old new ", i, wi, self.feat_weights[i])
			# print("self.feat_weights[i]", c)
			# print("self.alpha", self.alpha)
			# print("difference", difference)

			# print("wi shape", wi.shape)
			# print("self.feat_weights[i] shape", self.feat_weights[i].shape)
			# print("self.alpha shape", self.alpha)
			# print("difference shape", difference.shape)

			# print("features[i]", features[i])

			


	def update(self, state, action, reward, next_state, next_state_possible_actions, done):

		# Q(s,a) = (1.0 - alpha) * Q(s,a) + alpha * (reward + discount * V(s'))

		if done==True:
			qval_dash = reward
		else:
			qval_dash = reward + self.discount * self.get_value(next_state, next_state_possible_actions)
			
		qval_old = self.qvalues[state][action]      
		qval = (1.0 - self.alpha)* qval_old + self.alpha * qval_dash
		self.qvalues[state][action] = qval

	# def get_best_action(self, state, possible_actions, features):

	# 	print("------ QVAL ------")
	# 	# calculate q-val for all actions
	# 	all_q_val = np.sum(np.multiply(self.feat_weights, features),axis=1)

	# 	# find the best q-val and return the index
	# 	q_val_dash = np.max(all_q_val)
	# 	idx_best_q = np.argmax(all_q_val)

	# 	#retun the action for the best q-val
	# 	best_action = possible_actions[idx_best_q]

	# 	print("all_q_val ", all_q_val)
	# 	print("idx_best_q ", idx_best_q)
	# 	print("best_action ", best_action)

	# 	return best_action, q_val_dash, all_q_val


	def calc_new_feature_func(action, features):

		# if I take this action what will my new feature functions be?

		return new_features



	def get_action(self, state, possible_actions, features):
         
		# with probability epsilon take random action, otherwise - the best policy action
		epsilon = self.epsilon
		# find the best action an associated q-value

		# calculate q-val for all actions
		all_q_val = np.sum(np.multiply(self.feat_weights, features),axis=1)

		# find the best q-val and return the index
		#q_val_dash = np.max(all_q_val)
		idx_best_q = np.argmax(all_q_val)

		#retun the action for the best q-val
		best_action = possible_actions[idx_best_q]

		#chosen_action = self.get_best_action(state, possible_actions, features)
		# print("------------------")
		# print("------ QVAL ------")
		if epsilon > np.random.uniform(0.0, 1.0):
			chosen_action = random.choice(possible_actions)
			action_index = np.where(np.isclose(possible_actions,chosen_action))
			# print("possible_actions ", possible_actions)
			# print("chosen_action ", chosen_action)
			# print("action_index ", action_index)
			# print("action_index shape ", np.shape(action_index))
			# print("action_index[0] ", action_index[0])
			# print("action_index ", action_index)
			# print("random action taken")
			q_val_dash = all_q_val[action_index[0]]
			
		else:
			chosen_action = best_action
			q_val_dash = np.max(all_q_val)

		
		# print("all_q_val ", all_q_val)
		# print("idx_best_q ", idx_best_q)
		# print("best_action ", best_action)
		# print("chosen_action ", chosen_action)
		# print("q_val_dash ", q_val_dash)
		return chosen_action, q_val_dash
        
	def get_value(self, state, possible_actions):
		
		pass
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------




def randomStart(exclusions, simTime, agentID, agentState):
	
	# initialise each agent with random position based on exclusion principle
	x, y = 0, 0
	rand_x = random.randint(0,4)
	if rand_x==0:
		xy = 0
		y = random.randint(18,65)
	if rand_x==1:
		xy = 1
		y = random.randint(12,65)
	if rand_x==2:
		x = 10
		y = random.randint(36,65)
	if rand_x==3:
		x = 11
		y = random.randint(54,65)
	exclusions[agentID,0] = x
	exclusions[agentID,1] = y
	#print("exclusions",exclusions)

	# state is [simTime,ID,position(x,y)]
	agentState[simTime,agentID,0] = x
	agentState[simTime,agentID,1] = y
	

def randomMove(simTime, agentID, agentState):
	ran = random.randint(1,5)
	x, y = 0, 0
	if ran==1:
		log = "moving UP"
		y = y - 1
	if ran==2:
		log = "moving DOWN"
		y = y + 1
	if ran==3:
		log = "moving LEFT"
		x = x - 1
	if ran==4:
		log = "moving RIGHT"
		x = x + 1
	if ran==5:
		log = "moving NONE"

	# Add delta to previous state
	agentState[simTime,agentID,0] = agentState[simTime-1,agentID,0] + x
	agentState[simTime,agentID,1] = agentState[simTime-1,agentID,1] + y
	#print("x y state",x, y, agentState[simTime,agentID,:] )
	#print(log)
	return 0





# ======================================================================
# --- Experiment Params -----------------------------------------
# Number of experiements to run
nTests = 1

# Each grid unit is 1.5m square
gridH, gridW = 12, 66
pavement_rows = [0,1,10,11] #grid row of each pavement

# Agent speed is rounded to discretised units
vAV = 6 #6u/s ~9.1m/s ~20mph
vPed = 1 #1u/s ~1.4m/s ~3mph
nA = 2 # Number of agents
start_pos = None

# AV starts with nose on map???
end_positions = [(2,0),(3,0),(4,0),(5,0)] #format [height, width] of screen from top left down

# end_rewards = [-7 for i in range(0,4*gridH)] 
end_rewards = [20]
# np_end_rewards = np.zeros([gridH,gridW], dtype=int)
# np_end_rewards[:,1:2]=-7

# add penalty for being on the road
road_positions = [(i,j) for j in range(0,gridW) for i in [2,3,4,5,6,7,8,9]] 

# now update this list with where the AV is
AV_x = 0
AV_y = 3
AV_state = (AV_y,AV_x)

#blocked_positions = [(i, 1) for i in range(1, 7)]+ [(1, i) for i in range(1, 8)] + [(i, 7) for i in range(1, 7)]
blocked_positions = [AV_state]
default_reward	= 0#-1
road_rewards 	= [0 for i in range(4*gridH)] 

# record agentStates and excluded start positions
exclusions = np.empty(shape=(nA,2)) #ID, xy
maxT = round(gridW / vAV)
agentState = np.empty(shape=(maxT,nA,2)) #state is [time,ID,position(x,y)]

# ======================================================================

alpha = 0.04
epsilon = 0.2
discount = 0.99
action_space = env.action_space
state_space = env.state_space

# ======================================================================



running_score = 0
simTime = 0
#inital setup of agents, state is [time,ID,position(x,y)]
for agentID in range(nA):
	randomStart(exclusions,simTime,agentID,agentState) 
	# now render initial scene
	# logData()
agent = FeatAgent(alpha, epsilon, discount, action_space, state_space)
env = Environment(gridH, gridW, end_positions, end_rewards, blocked_positions, start_pos, default_reward, road_positions, road_rewards)
env.render(agent.qvalues, running_score, simTime, nA, agentState)
time.sleep(10)
state = env.get_state()



counter=1
nExp = 1 #experiment ounter for fixing random seed and logging data

# set the random seed for the experiment
random.seed(nExp)
print("Experiment Number", nExp)


while(nExp <= nTests):
	
	
		

	while(simTime<10):
		#increment time
		simTime = simTime + 1

		# move agents
		for agentID in range(nA):
			randomMove(simTime, agentID, agentState)
			#print("simTime,agentID,agentState[simTime,agentID,:]",simTime,agentID,agentState[simTime,agentID,:])

		# render the scene
		features = env.percepts(AV_state) # now features can be passed to agent
		possible_actions = env.get_possible_actions()
		predicted_features = env.one_step_ahead_features(possible_actions, AV_state) #predict best outcome from available actions
		action, q_val_dash = agent.get_action(state, possible_actions, predicted_features) # for feature-based
		next_state, reward, done = env.step(action)
		running_score = running_score + reward
		env.render(agent.qvalues, running_score, simTime, nA, agentState)
		next_state_possible_actions = env.get_possible_actions()
		agent.feat_q_update(state, AV_state, action, reward, next_state, next_state_possible_actions, done, features, q_val_dash)
		state = next_state
		time.sleep(1)

		# move AV
		for i in range(0,vAV):
			AV_x+=1
			# If collision occurs end the experiment
			if done == True:	
				env.reset_state()
				env.render(agent.qvalues, running_score, simTime, nA, agentState)
				state = env.get_state()
				running_score = 0
				nExp = nExp + 1
				print("Experiment Number", nExp)
				random.seed(nExp)
				#logData()
				continue
			# Reset the game if the AV reaches the end
			if AV_x>=gridW-1:
				AV_x=0
				env.reset_state()
				running_score = 0
				nExp = nExp + 1
				print("Experiment Number", nExp)
				random.seed(nExp)
				#logData()
				continue
			AV_state = (AV_y,AV_x)

			blocked_positions = [AV_state]
			env.end_positions[0] = AV_state
			env.update_state()
			# time.sleep(0.1)

		# check for assertions
		# calculate score
		# log data