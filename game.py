# cd git/cav/Technical/MAS/Q_learn
# conda activate my_env
# python game.py


import sys
import numpy as np
import cv2
import time
import matplotlib.pyplot as plt

class Environment(object):
	
	def __init__(self, gridH, gridW, end_positions, end_rewards, blocked_positions, start_position, default_reward, road_positions, road_rewards, scale=100):
		
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
			cv2.putText(self.frame, text, (int((x+0.5)*self.scale-w/2), int((y+0.5)*self.scale+h/2)), font, 1, color, 2, cv2.LINE_AA)	

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
			cv2.putText(self.frame, text, (int((x+0.5)*self.scale-w/2), int((y+0.5)*self.scale+h/2)), font, 1, color, 2, cv2.LINE_AA)

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

		print("~~~~ env ~~~~")
		print("xp yp ",xp, yp)
		print("xa ya ",xa, ya)
		print("on road ",self.on_road)
		print("dif y ", self.diff_y)
		print("diff x ", self.diff_x)
		print("euclid ", self.euclid)
		print("inv_euclid ", self.inv_euclid)
		print("inv_euclid2 ", self.inv_euclid2)
		print("inv_euclid3 ", self.inv_euclid3)
		print("~~~~~~~~~~~~~~")

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
		
		print("/n ~ GAME RESTARTING ~/ n")
		if self.start_position == None:
			self.position = self.init_start_state()
		else:
			self.position = self.start_position
	
	def render(self, qvalues_matrix, running_score):
		
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
					
		# draw agent
		
		y, x = self.position
		
		y1 = int((y + 0.3)*self.scale)
		x1 = int((x + 0.3)*self.scale)
		y2 = int((y + 0.7)*self.scale)
		x2 = int((x + 0.7)*self.scale)

		cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), -1)
		
		#print score
		#cv2.putText(img, running_score, org, fontFace, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]]) 


		cv2.imshow('frame', frame)
		cv2.moveWindow('frame', 0, 0)
		key = cv2.waitKey(1)
		if key == 27: sys.exit()
        
        
#import agent
        
import random

# ------------------------------------------------------------------------------------------
# ------------------------------------- Base Agent -----------------------------------------
# ------------------------------------------------------------------------------------------

class BaseAgent:
	
	def __init__(self, alpha, epsilon, discount, action_space, state_space):
 
		self.action_space = action_space
		self.alpha = alpha
		self.epsilon = epsilon
		self.discount = discount
		self.qvalues = np.zeros((state_space, action_space), np.float32)
		
	def update(self, state, action, reward, next_state, next_state_possible_actions, done):

		# Q(s,a) = (1.0 - alpha) * Q(s,a) + alpha * (reward + discount * V(s'))

		if done==True:
			qval_dash = reward
		else:
			qval_dash = reward + self.discount * self.get_value(next_state, next_state_possible_actions)
			
		qval_old = self.qvalues[state][action]      
		qval = (1.0 - self.alpha)* qval_old + self.alpha * qval_dash
		self.qvalues[state][action] = qval
       
	def get_best_action(self, state, possible_actions):

		best_action = possible_actions[0]
		value = self.qvalues[state][possible_actions[0]]
        
		for action in possible_actions:
			q_val = self.qvalues[state][action]
			if q_val > value:
				value = q_val
				best_action = action

		return best_action

	def get_action(self, state, possible_actions):
         
		# with probability epsilon take random action, otherwise - the best policy action

		epsilon = self.epsilon

		if epsilon > np.random.uniform(0.0, 1.0):
			chosen_action = random.choice(possible_actions)
		else:
			chosen_action = self.get_best_action(state, possible_actions)

		return chosen_action
        
	def get_value(self, state, possible_actions):
		
		pass


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
		print("features x weights ", np.multiply(self.feat_weights, features))
		print("#############################")
		print("reward ", reward)
		print("self.discount ", self.discount)
		#print("next_state ", next_state)
		#print("next_state_possible_actions ", list(next_state_possible_actions))
		print("qval ", qval)
		print("q_val_dash ", q_val_dash)
		print("self.feat_weights", self.feat_weights)
		print("difference", difference)
		#print("self.feat_weights.shape", self.feat_weights.shape)

		for i in range(self.feat_weights.shape[0]):
			wi = self.feat_weights[i]
			self.feat_weights[i] = wi + self.alpha * difference * features[i]
			# print("~~~~~~~~~~~~~~~~~~~~~~~~")
			# print("i", i)
			print("i w_old new ", i, wi, self.feat_weights[i])
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
		print("------------------")
		print("------ QVAL ------")
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





# ------------------------------------------------------------------------------------------
# ---------------------------------- Q-Learning Agent --------------------------------------
# ------------------------------------------------------------------------------------------

class QLearningAgent(BaseAgent):

	def get_value(self, state, possible_actions):

		# estimate V(s) as maximum of Q(state,action) over possible actions

		value = self.qvalues[state][possible_actions[0]]
       
		for action in possible_actions:
			q_val = self.qvalues[state][action]
			if q_val > value:
				value = q_val

		return value

# ------------------------------------------------------------------------------------------
# ------------------------------ Expected Value SARSA Agent --------------------------------
# ------------------------------------------------------------------------------------------
    
class EVSarsaAgent(BaseAgent):
    
	def get_value(self, state, possible_actions):
		
		# estimate V(s) as expected value of Q(state,action) over possible actions assuming epsilon-greedy policy
		# V(s) = sum [ p(a|s) * Q(s,a) ]
          
		best_action = possible_actions[0]
		max_val = self.qvalues[state][possible_actions[0]]
		
		for action in possible_actions:
            
			q_val = self.qvalues[state][action]
			if q_val > max_val:
				max_val = q_val
				best_action = action
        
		state_value = 0.0
		n_actions = len(possible_actions)
		
		for action in possible_actions:
            
			if action == best_action:
				trans_prob = 1.0 - self.epsilon + self.epsilon/n_actions
			else:
				trans_prob = self.epsilon/n_actions
                   
			state_value = state_value + trans_prob * self.qvalues[state][action]

		return state_value


# ------------------------------------ environment 1 -----------------------------------------
#gridH, gridW = 4, 4
#start_pos = None
#end_positions = [(0, 3), (1, 3)]
#end_rewards = [10.0, -60.0]
#blocked_positions = [(1, 1), (2, 1)]
#default_reward= -0.2
# ------------------------------------ environment 2 -----------------------------------------

#gridH, gridW = 8, 4
#start_pos = (7, 0)
#end_positions = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)]
#end_rewards = [10.0, -40.0, -40.0, -40.0, -40.0, -40.0, -40.0]
#blocked_positions = []
#default_reward= -0.2

# ------------------------------------ environment 3 -----------------------------------------

#gridH, gridW = 8, 9
#start_pos = None
#end_positions = [(2, 2), (3, 5), (4, 5), (5, 5), (6, 5)]
#end_rewards = [10.0, -30.0, -30.0, -30.0, -30.0]
#blocked_positions = [(i, 1) for i in range(1, 7)]+ [(1, i) for i in range(1, 8)] + [(i, 7) for i in range(1, 7)]
#default_reward= -0.5

# ------------------------------------ environment 4 -----------------------------------------
'''
gridH, gridW = 9, 7
start_pos = None
end_positions = [(0, 3), (2, 4), (6, 2)]
end_rewards = [20.0, -50.0, -50.0]
blocked_positions = [(2, i) for i in range(3)] + [(6, i) for i in range(4, 7)]
default_reward = -0.1
'''
# --------------------------------------------------------------------------------------------

gridH, gridW = 10, 8
start_pos = None
#end_positions = [(2, 2), (3, 5), (4, 5), (5, 5), (6, 5)] #Format (Down-y,Right-x)
end_positions = [(0,2)]

# end_rewards = [-7 for i in range(0,4*gridH)] 
end_rewards = [20]
# np_end_rewards = np.zeros([gridH,gridW], dtype=int)
# np_end_rewards[:,1:2]=-7

# add penalty for being on the road
road_positions = [(i,j) for i in range(0,gridH) for j in [2,3,4,5]] 

# now update this list with where the AV is
AV_x = 2
AV_y = 0
AV_state = (AV_y,AV_x)

#blocked_positions = [(i, 1) for i in range(1, 7)]+ [(1, i) for i in range(1, 8)] + [(i, 7) for i in range(1, 7)]
blocked_positions = [AV_state]
default_reward	= 0#-1
road_rewards 	= [0 for i in range(4*gridH)] 


# --------------------------------------------------------------------------------------------

#env = environment.Environment(gridH, gridW, end_positions, end_rewards, blocked_positions, start_pos, default_reward)
env = Environment(gridH, gridW, end_positions, end_rewards, blocked_positions, start_pos, default_reward, road_positions, road_rewards)

alpha = 0.04
epsilon = 0.2
discount = 0.99
action_space = env.action_space
state_space = env.state_space

running_score = 0

# agent = QLearningAgent(alpha, epsilon, discount, action_space, state_space)
#agent = EVSarsaAgent(alpha, epsilon, discount, action_space, state_space)
#agent = EVSarsaAgent(alpha, epsilon, discount, action_space, state_space)

agent = FeatAgent(alpha, epsilon, discount, action_space, state_space)

env.render(agent.qvalues)
state = env.get_state()
counter=1
fig = plt.figure()

while(True):
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# 1) Get the agent perceptions
	print("____MAIN_01_____")
	features = env.percepts(AV_state) # now features can be passed to agent
	possible_actions = env.get_possible_actions()
	#print("possible_actions ",list(possible_actions))
	
	
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# 2) Take an action based on epsilon-ploicy
	print("____MAIN_02_____")
	predicted_features = env.one_step_ahead_features(possible_actions, AV_state) #predict best outcome from available actions
	action, q_val_dash = agent.get_action(state, possible_actions, predicted_features) # for feature-based
	# action = agent.get_action(state, possible_actions)
	#print("action chosen ", action)

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# 3) Take the chosen action and expected reward. if action not possible do nothing
	print("____MAIN_03_____")
	next_state, reward, done = env.step(action)
	#print("next_state ", next_state)
	#print("reward ", reward)
	#print("done ", done)

	print("____MAIN_03b____")
	#update running score
	running_score = running_score + reward

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# 4) Update the graphics - TODO make seperate board with weight/action display
	print("____MAIN_04_____")
	env.render(agent.qvalues, running_score)

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# Calcualte q-value based on (s,a,r,s')
	print("____MAIN_04b____")
	next_state_possible_actions = env.get_possible_actions() #this currently returns all theoretical actions, not just possible ones
	# agent.update(state, action, reward, next_state, next_state_possible_actions, done)
	agent.feat_q_update(state, AV_state, action, reward, next_state, next_state_possible_actions, done, features, q_val_dash)
	state = next_state



	# x axis values 
	print("____MAIN_04c____")
	#print("counter ", counter)
	x = np.arange(len(agent.feat_weights))
	if counter==1: 
		y=agent.feat_weights
		counter=counter+1
	else: 
		temp = np.transpose(agent.feat_weights)
		y = np.vstack((y,temp))
		counter=counter+1

	if counter>2:
		tags = ('on_road', 'diff_x', 'diff_y', 'euclid', 'inv_euclid', 'inv_euclid2', 'inv_euclid3') 
		plt.plot(y, label=tags)
		plt.title('Agent Feature Weights') 
		fig.canvas.draw()
		img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8,	sep='')
		img  = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
		img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
		cv2.imshow("plot",img)
	#time.sleep(1)

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# 5) move the AV
	print("____MAIN_05_____")
	AV_y+=1
	if AV_y>=gridH-1:
		AV_y=0
		env.reset_state()
	# print(env.end_positions[0])
	# print(type(env.end_positions[0]))
	AV_state = (AV_y,AV_x)

	blocked_positions = [AV_state]
	env.end_positions[0] = AV_state
	env.update_state()

	# TODOs
	# update graphics, skipping every other step
	# present feature weights in graph
	# on_road feature looks wrong - test
	# get weights graph showing in time series


	if done == True:	
		env.reset_state()
		env.render(agent.qvalues)
		state = env.get_state()
		running_score = 0
		continue
