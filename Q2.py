#!/usr/bin/env python
# coding: utf-8

# In[13]:


import numpy as np
import copy


# In[12]:


v = np.zeros([5,5])
gamma = 0.9
print(v[0][0])


# In[4]:


rA = 0; cA = 1;
rB = 0; cB = 3;


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


# In[82]:


def getReward(a,s):
    s_next = getNewState(a)
    if s_next[0] < 0 or s_next[0] >= 5 or s_next[1] < 0 or s_next[1] >= 5:
        r = -1;       
    else:
        r = 0;
        
    return r;    


# In[83]:


def getV(v,s,a):
    s_next = getNewState(a)
    if s_next[0] < 0 or s_next[0] >= 5 or s_next[1] < 0 or s_next[1] >= 5:
        v_s = v[s[0]][s[1]];
    else:
        v_s = v[s_next[0]][s_next[1]]
        
    return v_s    


# In[84]:


s = [0,0]; #starting with this state
v = np.zeros([5,5])
steps = 0;
flag = 0;
th = 0.0001; #theshold for converging 
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
        for a in range(noa):    
            tmp += (getReward(a,s) + gamma*getV(v,s,a))*(1.0/noa)
            
    #chekcing for convergence        
    if abs(tmp - v[s[0]][s[1]]) < th:
        #STOP
        print("DONE")
        flag = 1;
        break;
    #update v if no convergence
    else:
        v[s[0]][s[1]] = tmp;
        
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


# In[85]:


print(v)


# In[ ]:





# In[ ]:




