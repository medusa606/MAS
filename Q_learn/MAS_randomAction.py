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
import datetime

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
		
		# Check if action is blocked, then update position
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
		# print("###STEP### self.position",self.position)
		# print("###STEP### next_state",next_state)
		
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
	
	def render(self, qvalues_matrix, running_score, simTime, nA, agentState):
		
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
			
			# # draw crossed lines
			
			# x1 = int(self.scale*(position[1]))			
			# y1 = int(self.scale*(position[0]))
			
			# x2 = int(self.scale*(position[1] + 1.0))			
			# y2 = int(self.scale*(position[0] + 1.0))

			# x3 = int(self.scale*(position[1]+ 1.0 ))			
			# y3 = int(self.scale*(position[0]))
			
			# x4 = int(self.scale*(position[1]))			
			# y4 = int(self.scale*(position[0] + 1.0))
			
			# cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
			# cv2.line(frame, (x3, y3), (x4, y4), (255, 255, 255), 2)
			
			# # draw arrow indicating best action
						
			# best_action = 0
			# best_qvalue = qvalues[0]
			# for action, qvalue in enumerate(qvalues):
			# 	if qvalue > best_qvalue:
			# 		best_qvalue = qvalue
			# 		best_action = action
			
			# if best_action == 0:
			# 	dx1, dy1, dx2, dy2 = 0.0, -0.25, 0.0, 0.25	
							
			# elif best_action == 1:
			# 	dx1, dy1, dx2, dy2 = 0.0, 0.25, 0.0, -0.25
								
			# elif best_action == 2:
			# 	dx1, dy1, dx2, dy2 = -0.25, 0.0, 0.25, 0.0
								
			# elif best_action == 3:
			# 	dx1, dy1, dx2, dy2 = 0.25, 0.0, -0.25, 0.0				
									
			# x1 = int(self.scale*(position[1] + 0.5 + dx1))			
			# y1 = int(self.scale*(position[0] + 0.5 + dy1))	
					
			# x2 = int(self.scale*(position[1] + 0.5 + dx2))			
			# y2 = int(self.scale*(position[0] + 0.5 + dy2))	
							
			# cv2.arrowedLine(frame, (x1, y1), (x2, y2), (255, 100, 0), 8, line_type=8, tipLength=0.5)		
			
		# draw horizontal lines		
		for i in range(self.gridH+1):
			cv2.line(frame, (0, i*self.scale), (self.gridW * self.scale, i*self.scale), (255, 255, 255), 1)
		
		# draw vertical lines		
		for i in range(self.gridW+1):
			cv2.line(frame, (i*self.scale, 0), (i*self.scale, self.gridH * self.scale), (255, 255, 255), 1)
		
		#openCV rectangle function
		# cv2.rectangle(img, pt1, pt2, color, thickness, lineType, shift)
		# Parameters
		#     img   Image.
		#     pt1   Vertex of the rectangle.
		#     pt2    Vertex of the rectangle opposite to pt1 .
		#     color Rectangle color or brightness (grayscale image).
		#     thickness  Thickness of lines that make up the rectangle. Negative values,
		#     like CV_FILLED , mean that the function has to draw a filled rectangle.
		#     lineType  Type of the line. See the line description.
		#     shift   Number of fractional bits in the point coordinates.
		# Must be integers
		# Must have order (left, top) and (right, bottom)

		# # draw agent
		# for i in range(0,2):		
		# 	y, x = self.position
		# 	x = x + (i * 2)		 
		# 	y = y + (i * 2)		 
		# 	y1 = int((y + 0.3)*self.scale)
		# 	x1 = int((x + 0.3)*self.scale)
		# 	y2 = int((y + 0.7)*self.scale)
		# 	x2 = int((x + 0.7)*self.scale)
		# 	cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), -1)
			
		# 	cv2.imshow('frame', frame)
		# 	cv2.moveWindow('frame', 0, 0)
		# 	key = cv2.waitKey(1)
		# 	if key == 27: sys.exit()
		# 	#print('### RENDER1 ### xy',x,y,x1,x2,y1,y2)		
		# 	# cv2.rectangle(frame, (x1+50, y1+50), (x2+50, y2+50), (0, 255, 255), -1)


		#======================================
		# draw agent
		#======================================
		#print("simTime, nA",simTime, nA)
		for agentID in range(0,nA):
			y,x = agentState[simTime, agentID,:]
			y1 = int((y + 0.3)*self.scale)
			x1 = int((x + 0.3)*self.scale)
			y2 = int((y + 0.7)*self.scale)
			x2 = int((x + 0.7)*self.scale)
			cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), -1)
			#print('### RENDER2 ### xy',x,y,x1,x2,y1,y2)	
			#print("### RENDER ### simTime, agentID, x,y,x1,x2,y1,y2",simTime, agentID,x,y,x1,x2,y1,y2)
			#time.sleep(1)
			
		#======================================
		cv2.imshow('frame', frame)
		cv2.moveWindow('frame', 0, 0)
		key = cv2.waitKey(10)
		if key == 27: sys.exit()



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




def randomStart(exclusions, simTime, nA, agentState, rsLog, pLog, nExp):
	#print("### randomStart ###")
	# initialise each agent with random position based on "deadzone"
	log_string = ""
	for agentID in range(0,nA):
		x, y = 0, 0
		rand = random.randint(0,3)
		#print("### randomStart ### rand", rand)
		# print("rand",rand)
		if rand==0:
			x = 0
			y = random.randint(18,65)
		if rand==1:
			x = 1
			y = random.randint(12,65)
		if rand==2:
			x = 10
			y = random.randint(36,65)
		if rand==3:
			x = 11
			y = random.randint(54,65)
		
		# # add the start location to an exclusion list
		# exclusions[agentID,0] = x
		# exclusions[agentID,1] = y
		# # print("exclusions",exclusions[agentID,:])


		# # ensure unique starting locations
		# if agentID>0:
		# 	#print("testing unique starting positions...")
		# 	ex_x = agentState[simTime,0:agentID,0]
		# 	ex_y = agentState[simTime,0:agentID,1]
		# 	check_x = np.isin(ex_x,x)
		# 	check_y = np.isin(ex_y,y)
		# 	check = (check_x & check_y)
		# 	print("check_x,y",check_x,check_y)
		# 	print("check",check.all())
		# 	#if repetition  is found, regenerate values
		# 	if (check.all()):
		# 		print("### Resetting Agents ###")
		# 		randomStart(exclusions, simTime, nA, agentState, rLog)

		
		# state is [simTime,ID,position(x,y)]
		agentState[simTime,agentID,0] = x
		agentState[simTime,agentID,1] = y
		log_string = log_string + ", %4i, %4i" % (x,y)
		#print(log_string)
		
		#print("initial state for agent", agentID," is ",agentState[simTime,agentID,:])
	index = "%4i, %4i, %4i" % (0, nExp, simTime)
	rsLog.write(index + log_string + "\n")
	pLog.write(index + log_string + "\n")


	
def moveGen(simTime, agentID, rLog):

	ran = random.randint(1,5)
	#print("ran",ran)
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
	rLog.write("%d \n" % ran) #store the randome numbers to check consistency	
	return x,y #WARNING X and Y are used the wrong way around


def randomMove(simTime, nA, agentState, pLog, rLog, nExp, AV_x):
	#print("### randomMove ###")
	log_string = ""
	for agentID in range(0,nA):

		illegal_move=True
		while(illegal_move):
			
			#get a delta move randomly
			dx, dy = moveGen(simTime, agentID, rLog)

			# Add delta to previous state
			new_x = int(agentState[simTime-1,agentID,0] + dx)
			new_y = int(agentState[simTime-1,agentID,1] + dy)
			#print("new x y ", new_x, new_y)

			# check if agent has moved off the board
			if (new_x<0):
				#print("ILLEGAL move 1")
				continue
			elif(new_x>gridH-1):
				#print("ILLEGAL move 2")
				continue
			elif(new_y<0):
				#print("ILLEGAL move 3")
				continue
			elif(new_y>gridW-1):
				#print("ILLEGAL move 4")
				#print("y value ",new_y," is greater than grid limit ", gridH)
				continue
			else:
				illegal_move=False

		# Add delta to previous state
		agentState[simTime,agentID,0] = new_x
		agentState[simTime,agentID,1] = new_y
		# Log position data
		# pLog.write("%d, %d, %d, %d \n" % (simTime, agentID, x, y))
		#print("state for agent", agentID," is ",agentState[simTime,agentID,:])
		log_string = log_string + ", %4i, %4i" % (new_x,new_y)
		#print(log_string)
		
		#print("initial state for agent", agentID," is ",agentState[simTime,agentID,:])
	index = "%4i, %4i, %4i" % (nExp, simTime, AV_x)
	pLog.write(index + log_string + "\n")


#Check reward and end positions (overrules env.step)
def checkReward(nA, simTime, agentState, agentScores, nExp, roadPenaltyMaxtrix):
	for agentID in range (0,nA):
		reward = 0
		# Check agent location against reward matrix
		Ag_x = int(agentState[simTime,agentID,0])
		Ag_y = int(agentState[simTime,agentID,1])
		#print("###REWARD### Ag_x, Ag_y ", Ag_x, Ag_y)
		#next_state = env.state2idx[(Ag_x,Ag_y)]
		#reward = env.idx2reward[next_state]
		#print("###REWARD### Agent ID reward ", agentID, reward)

		# Update agent score profile
		reward = roadPenaltyMaxtrix[Ag_y, Ag_x]
		curr_score = agentScores[nExp,agentID]
		agentScores[nExp,agentID] = curr_score + reward		

		if reward==vt: break #no double accounting, only first agent counts!
	print("###REWARD### ID curr_score, reward ",agentID, curr_score, reward)
	return reward

def checkValidTest(nA, simTime, agentState):
	for agentID in range (0,nA):
		Ag_x = int(agentState[simTime,agentID,0])
		Ag_y = int(agentState[simTime,agentID,1])	
		# Check if valid test generated
		if (Ag_x,Ag_y) in env.end_positions:
			done = True
		else:
			done = False
		return done

def moveAV(gridW,gridH,AV_x):
	AVpositionMaxtrix = np.zeros(shape=(gridW,gridH))
	AVpositionMaxtrix[AV_x,[2,3,4,5]]=1
	return AVpositionMaxtrix


# ======================================================================
# --- User Experiment Params -----------------------------------------

nTests = 2					# Number of experiements to run
gridH, gridW = 12, 66#66		# Each grid unit is 1.5m square
pavement_rows = [0,1,10,11] #grid row of each pavement
vAV = 6 					# 6u/s ~9.1m/s ~20mph
vPed = 1 					# 1u/s ~1.4m/s ~3mph
nA = 5 						# Number of agents
delay = .02 					# delay between each frame, slows sim down
vt = 20						# points for a valid test
AV_x = 0					# AV start position along road
default_reward	= -1 		# Living cost
road_pen = -1				# Penalty for being in road


# ======================================================================
# --- Non-User Experiment Params -------------------------------------

roadPenaltyMaxtrix = np.zeros(shape=(gridW,gridH))
roadPenaltyMaxtrix[:,:] = road_pen
roadPenaltyMaxtrix[:,pavement_rows] = default_reward

road_positions = [(i,j) for j in range(0,gridW) for i in [2,3,4,5,6,7,8,9]] 
road_rewards 	= [road_pen for i in range(4*gridH)] 

AV_y = 0
AV_state = (AV_y,AV_x)
blocked_positions = [(2,AV_x),(3,AV_x),(4,AV_x),(5,AV_x)]

# generate a grid showing position of the AV_x
AVpositionMaxtrix = moveAV(gridW,gridH,AV_x)
#print(AVpositionMaxtrix)

start_pos = None
end_positions = [(2,0),(3,0),(4,0),(5,0)] 	# initial AV position
end_rewards = [0,0,0,0] 					# Rewards moved out of panalty matrix

# record agentStates and excluded start positions
exclusions = np.empty(shape=(nA,2)) #ID, xy
maxT = (int)(round(gridW / vAV)+1)
agentState = np.empty(shape=(maxT,nA,2)) #state is [time,ID,position(x,y)]

# store a score for each agent and each experiment
agentScores = np.zeros(shape=(nTests,nA,)) #state is [time,ID,position(x,y)]


# ======================================================================
# --- Agent Experiment Params ----------------------------------------

alpha = 0.04
epsilon = 0.2
discount = 0.99

# ======================================================================
# --- Logs -----------------------------------------------------------
ts = datetime.datetime.now().strftime("%d-%b-%Y-%H-%M-%S")

rsLog = open("initial_random_log_%s.txt" % ts, "w")	#random initial location log
rsLog.write("nExp, Time"+"".join(',  A%dx,  A%dy' % (i,i) for i in range(0,nA)) + " \n")

rLog = open("random_log_%s.txt" % ts, "w")	#random movement log
rLog.write("simTime, rand \n")

sLog = open("score_log_%s.txt" % ts, "w")	#score for each experiment per agent
sLog.write("nExp, agentScores \n")

pLog = open("position_log_%s.txt" % ts, "w")
pLog.write("nExp, Time,  AVy"+"".join(',  A%dx,  A%dy' % (i,i) for i in range(0,nA)) + " \n")
#pLog.close()
#print(header)


# ======================================================================

running_score = 0
simTime = 0
#inital setup of agents, state is [time,ID,position(x,y)]


nExp = 0 #experiment ounter for fixing random seed and logging data
random.seed(nExp)
randomStart(exclusions,simTime,nA,agentState,rsLog,pLog,nExp) 
# rsLog(simTime,nA,agentState)

#print("initial agent positions are ",agentState[simTime,:,:])

env = Environment(gridH, gridW, end_positions, end_rewards, blocked_positions, start_pos, default_reward, road_positions, road_rewards)
action_space = env.action_space
state_space = env.state_space
agent = FeatAgent(alpha, epsilon, discount, action_space, state_space)
env.render(agent.qvalues, running_score, simTime, nA, agentState)
time.sleep(delay)
state = env.get_state()





# Flag to indicate if a valid test has been generated
done = False

# while(nExp <= nTests):
while(not(done)) and (nExp <= nTests):

	#check if series complete
	if(nExp>nTests):
		done=True

	#increment time
	if simTime==0: print("Experiment Number", nExp)
	#print("simTime=", simTime)
	simTime = simTime + 1

	# move agents	
	randomMove(simTime, nA, agentState, pLog, rLog, nExp, AV_x)

	# render the scene
	features = env.percepts(AV_state) # now features can be passed to agent
	possible_actions = env.get_possible_actions()
	predicted_features = env.one_step_ahead_features(possible_actions, AV_state) #predict best outcome from available actions
	action, q_val_dash = agent.get_action(state, possible_actions, predicted_features) # for feature-based
	next_state, reward, done = env.step(action)

	
	reward = checkReward(nA, simTime, agentState, agentScores, nExp, roadPenaltyMaxtrix) #Check reward and end positions (overrules env.step)
	#print("Agent scores are: ", agentScores)

	#check done here?????


	running_score = running_score + reward
	env.render(agent.qvalues, running_score, simTime, nA, agentState)
	next_state_possible_actions = env.get_possible_actions()
	agent.feat_q_update(state, AV_state, action, reward, next_state, next_state_possible_actions, done, features, q_val_dash)
	state = next_state
	time.sleep(delay)

# move AV
	for i in range(0,vAV):

		# Move AV and update end positions and reward locations
		AV_x+=1
		AVpositionMaxtrix = moveAV(gridW,gridH,AV_x)
		AVlist = (np.transpose(np.nonzero(AVpositionMaxtrix)))
		#print("AVlist",AVlist)
		
		#see if AV has intersected an agent
		for agentID in range(0,nA):
			av_x = AVlist[:,1]
			av_y = AVlist[:,0]
			Ag_x = int(agentState[simTime,agentID,0])
			Ag_y = int(agentState[simTime,agentID,1])	
			check_x = np.isin(av_x,Ag_x)
			check_y = np.isin(av_y,Ag_y)
			check = (check_x & check_y)

			# print("check_x,y",check_x,check_y)
			# print("av_x Ag_x",agentID,av_x, Ag_x)
			# print("check_x ID",agentID, check_x)
			# print("av_y Ag_y",agentID,av_y, Ag_y)
			# print("check_y ID", check_y)

			print("check",check.all())
			print("av_x ,av_y",av_x ,av_y)
			print("Ag_x,Ag_y",Ag_x,Ag_y)
			print("check_x",check_x)
			print("check_y",check_y)

			#print("check",check.all())
			if(check.all()):
				print("Agent ",agentID, " has generated a valid test")
				# Add reward
				curr_score = agentScores[nExp,agentID]
				agentScores[nExp,agentID] = curr_score + reward	
				# reset level


		#blocked_positions = [(2,AV_x),(3,AV_x),(4,AV_x),(5,AV_x)] # Assume AV is width of road as simple approximation
		env.end_positions = [(2,AV_x),(3,AV_x),(4,AV_x),(5,AV_x)]
		env.update_state() #renders road and end positions/rewards

		# print("AV_x, gridW = ",AV_x, gridW)
		# env.render(agent.qvalues, running_score, simTime, nA, agentState)
		done = checkValidTest(nA, simTime, agentState)
		
		#print("Agent X: ", agentState[simTime,:,0])
		#print("Agent Y: ", agentState[simTime,:,1])
		#print("blocked_positions are: ", blocked_positions)
		#print("Agent scores are: ", agentScores)

		# If collision occurs end the experiment
		if done == True:
			print("Valid test generated!")
			env.reset_state()
			env.render(agent.qvalues, running_score, simTime, nA, agentState)
			state = env.get_state()
			running_score = 0
			nExp = nExp + 1
			#print("Experiment Number", nExp)
			random.seed(nExp)
			# Reset all agents
			AV_x=0
			exclusions = np.empty(shape=(nA,2)) #ID, xy
			maxT = (int)(round(gridW / vAV)+1)
			agentState = np.empty(shape=(maxT,nA,2)) #state is [time,ID,position(x,y)]
			simTime = 0
			randomStart(exclusions,simTime,nA,agentState,rsLog,nExp) 
			done = False 
			#logData()
			continue
		# Reset the game if the AV reaches the end
		if AV_x>=gridW-1:
			print("AV exit, resetting...")
			AV_x=0
			env.reset_state()
			running_score = 0
			nExp = nExp + 1
			#print("Experiment Number", nExp)
			random.seed(nExp)
			#logData()
			AV_x=0
			exclusions = np.empty(shape=(nA,2)) #ID, xy
			maxT = (int)(round(gridW / vAV)+1)
			agentState = np.empty(shape=(maxT,nA,2)) #state is [time,ID,position(x,y)]
			simTime = 0
			randomStart(exclusions,simTime,nA,agentState,rsLog,nExp)  
			done = False
			continue
		AV_state = (AV_y,AV_x)


print("Test complete, writing log files...")
rLog.close()
# check for assertions
# calculate score
# log data
rsLog.close()

