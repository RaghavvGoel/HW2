#!/usr/bin/env python
# coding: utf-8

# In[39]:


import numpy as np
import copy


# In[40]:


v = np.zeros([5,5])
gamma = 0.9
print(v[0][0])


# In[41]:


rA = 0; cA = 1;
rB = 0; cB = 3;


# In[42]:


T = 1000 #stop after these many steps
noa = 4;


# In[62]:


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


# In[63]:


def getReward(s, a):
    s_next = getNewState(a)
    if s_next[0] < 0 or s_next[0] >= 5 or s_next[1] < 0 or s_next[1] >= 5:
        r = -1;  
    else:
        r = 0;
        
    return r;    


# In[65]:


def getV(v,s,a):
    s_next = getNewState(a)
    if s_next[0] < 0 or s_next[0] >= 5 or s_next[1] < 0 or s_next[1] >= 5:
        v_s = v[s[0]][s[1]];
        
    else:
        v_s = v[s_next[0]][s_next[1]]
        
    return v_s    


# In[66]:


def getAction(v, s):
    r = np.zeros(4)
    
    if s[0] == rA and s[1] == cA :
        r = (10 + gamma*v[4][1])*np.ones(4)
    elif s[0] == rB and s[1] == cB:
        r = (5 + gamma*v[2][3])*np.ones(4)
    
    print(r)
    print("")
    if s[0] == 0:
        #Left movement will give reward -1
        r[0] = -1 + gamma*v[s[0]][s[1]]
    elif s[0] == 4:
        #right movement will give reward -1
        r[2] = -1 + gamma*v[s[0]][s[1]]
        
    if s[1] == 0:
        #Up movement will give reward -1
        r[1] = -1 + gamma*v[s[0]][s[1]]
    elif s[1] == 4:
        #Down movement will give reward -1
        r[3] = -1 + gamma*v[s[0]][s[1]]        
        
    actions_left = np.where(r == 0)[0]
    for i in range(np.size(actions_left)):
        s_ = getNewState(actions_left[i]);
        r[actions_left[i]] = getReward(s_) + gamma*v[s_[0]][s_[1]]
    
    return r


# In[67]:


s = [0,0]; #starting with this state
v = np.zeros([5,5])
steps = 0;
flag = 0;
th = 0.0001; #theshold for converging 
eps = 0.9;
# v[rA][cA] = 10;
# v[rB][cB] = 5;
while flag == 0:    
    print("steps: " , steps)
    tmp = 0;
    #if in cell A with reward 10
    if s[0] == rA and s[1] == cA: 
        s_next = [4,1];
        tmp = 10 + gamma*v[s_next[0]][s_next[1]];
    #if in cell B with reward 5    
    elif s[0] == rB and s[1] == cB: 
        s_next = [2,3];
        tmp = 5 + gamma*v[s_next[0]][s_next[1]]; 
    #any other cell    
    else:
        r_list = []
        for a in range(noa):    
            r_list.append((getReward(s,a) + gamma*getV(v,s,a))) 
        tmp = max(r_list)    
            
    #chekcing for convergence        
    if abs(tmp - v[s[0]][s[1]]) < th and v[s[0]][s[1]] != 0:
        #STOP
        print("DONE")
        flag = 1;
        break;
    #update v if no convergence
    else:
        v[s[0]][s[1]] = tmp;
        #s = s_
        
    #iterating over all the states    
    if s[0] == 4:
        s[0] = 0;
        if s[1] == 4:
            s[1] = 0;
        else:
            s[1] += 1;        
    else:
        s[0] += 1;
    
    print(v)
    print("")
        
    steps += 1;    


# In[68]:


print(v)


# In[69]:


def getState(s):
    
    return 5*s[0] + s[1]
    


# In[78]:


def getNewState_A(a):
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
        if s_next[0] > 4:
            s_next[0] = 4;        
    else:                           #RIGHT
        s_next = [s[0], s[1] + 1]
        if s_next[1] > 4:
            s_next[1] = 4;
            
    return s_next    


# In[74]:


#optmial plicy tells which is the best action to take
s = [0,0]; #starting with this state
q = np.zeros([25,4])
steps = 0;
flag = 0;
th = 0.0001; #theshold for converging 
eps = 0.9;
# v[rA][cA] = 10;
# v[rB][cB] = 5;
while flag == 0:    
    print("steps: " , steps)
    tmp = 0;
    r_list = []
    for a in range(noa):
        #if in cell A with reward 10
        if s[0] == rA and s[1] == cA: 
            s_next = [4,1];
            #r_list.append(q[getState(s_next)][a])
            tmp = 10 + gamma*np.max(q[getState(s_next)][:]) ;
        #if in cell B with reward 5    
        elif s[0] == rB and s[1] == cB: 
            s_next = [2,3];
            tmp = 5 + gamma*np.max(q[getState(s_next)][:]) ;
        #any other cell    
        else:                        
            tmp = getReward(s,a) + gamma*np.max(q[getState(getNewState_A(a))][:])
            
        #chekcing for convergence, also not converging if value of state action pair = 0 or -1 as in these cases
        #no change has been observed but this doesnt mean convergence
        if abs(tmp - q[getState(s)][a]) < th and (q[getState(s)][a] != 0 and q[getState(s)][a] != -1):
            #STOP
            print("DONE")
            flag = 1;
            break;
        #update v if no convergence
        else:
            q[getState(s)][a] = tmp;
        
        
    #iterating over all the states    
    if s[0] == 4:
        s[0] = 0;
        if s[1] == 4:
            s[1] = 0;
        else:
            s[1] += 1;        
    else:
        s[0] += 1;
    
    print(q)
    print("")
            
    steps += 1;    


# In[75]:


print(q)


# In[77]:


for i in range(25):
    print(np.max(q[i]))


# In[ ]:





# In[ ]:




