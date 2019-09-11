#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np
import copy
import math


# In[12]:


v = np.zeros([5,5])
gamma = 0.9
print(v[0][0])


# In[4]:


rA = 0; cA = 0;
rB = 3; cB = 3;


# In[76]:


T = 1000 #stop after these many steps
noa = 4;


# In[44]:


def getNewState(a):
    if a == 0:                      #UP
        s_next = [s[0]-1, s[1]]
    elif a == 1:                    #LEFT
        s_next = [s[0], s[1]-1]
    elif a == 2:                    #DOWN
        s_next = [s[0]+1, s[1]]
    else:                           #RIGHT
        s_next = [s[0], s[1] + 1]
        
    return s_next    


# In[38]:


def getNewState_A(a,s):
    if a == 0:                      #UP
        s_next = [s[0]-1, s[1]]
        if s_next[0] < 0:
            s_next[0] = 0;
            
    elif a == 1:                    #LEFT
        s_next = [s[0], s[1]-1]
        if s_next[1] < 0:
            s_next[1] = 0;
            
    elif a == 2:                    #DOWN
        s_next = [s[0]+1, s[1]]
        if s_next[0] > 3:
            s_next[0] = 3;        
    else:                           #RIGHT
        s_next = [s[0], s[1] + 1]
        if s_next[1] > 3:
            s_next[1] = 3;
            
    return s_next    


# In[44]:


def getReward(s):
    if s == 0:
        r = 0;
    elif s == 15:
        r = 0
    else:
        r = -1;
        
    return r;    


# In[172]:


def policy_eval(V, gamma, noa, th, p):
    V_tmp = copy.deepcopy(V)
    flag = 0;
    steps = 0;
    while flag == 0:
        delta = 0;
        for i in range(1,15):
            v = V_tmp[i]
            p_cur = p[i]
            tmp = 0;
            #iterate over actions
            for a in range(4):
                s = [i/4, i%4]
                s_next = getNewState_A(a,s)
                #change s_next into one integer
                s_next = 4*s_next[0] + s_next[1]
                #using old V here while updating in a new V
                tmp += (getReward(s) + gamma*V[s_next])
            tmp = tmp/4.0

            V_tmp[i] = tmp;
        

        if max(delta, abs(v - V[i])) < th:
            flag = 1;
        
        steps += 1;

    return V_tmp    


# In[186]:


#Initialization
V = np.zeros(4*4)

p = [[0,1,2,3] for i in range(4*4)]
#first and last states are terminal and hence no actions performed
p[0] = []; p[15] = []

gamma = 0.9
noa = 4;
th = 0.001
#policy_stable = False
policy_flag = 0;


# In[187]:


step = 0;
while policy_flag == 0:
    #Policy Evaluation
    print("STEP: " , step)
    print("V " )
    print(V.reshape([4,4]))
    print("")
    print("Policy:")
    print(p)
    print("")
    V = policy_eval(V, gamma, noa, th, p)
    policy_stable = True
    

    #Policy Updation
    p_tmp = [[] for i in range(4*4)]
    for i in range(1,15):
        a_old = p[i] #entire list
        r = []
        
        for a in range(noa):
            s = [i/4, i%4];
            s_next = getNewState_A(a,s)
            s_next = 4*s_next[0] + s_next[1]
            r.append(getReward(s) + gamma*V[s_next])
            
        max_val = np.max(r)
        ind = np.where(r == max_val)[0]
        for j in range(np.size(ind)):
            #if ind[j] not in p[i]:
            p_tmp[i].append(ind[j])
        #we need to check for all the actions which give max returns
        if np.size(np.setdiff1d(np.array(a_old), np.array(p_tmp[i]))) != 0:
            policy_stable = False
            
        #Below leads to infinte interation as the optimal action can be multiple        
        #if a_old != p[i]: 
            #policy_stable = False;
            #break; #works without this too
            #print("policy needs change")

    #Policy updation!!
    p = p_tmp
    #STOPPING when optimal policy found
    if policy_stable:
        policy_flag = 1;
        print("FINAL Value function")
        print(V.reshape([4,4]))
        print("Policy")
        print(p)
        print("STOPP DONE")
      
        
    step += 1;    

        


# In[ ]:





# In[ ]:





# In[ ]:




