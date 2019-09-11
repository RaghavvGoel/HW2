#!/usr/bin/env python
# coding: utf-8

# In[101]:


import numpy as np
import copy
from math import e, factorial
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


# In[7]:


v = np.zeros([21,21])
gamma = 0.9
print(v[0][0])


# In[4]:


# rA = 0; cA = 0;
# rB = 3; cB = 3;


# In[8]:


T = 1000 #stop after these many steps
noa = 11;


# In[9]:


def getNewState(a,s):
    s_next = [s[0] + a, s[1] - a];
    if s_next[1] > 20:
        s_next[1] = 20
    elif s_next[1] < 0:
        s_next[1] = 0
        
    if s_next[0] > 20:
        s_next[0] = 20
    elif s_next[0] < 0:
        s_next[0] = 0        
    
    return s_next


# In[2]:


# def getNewState_A(a,s):
#     if a == 0:                      #UP
#         s_next = [s[0]-1, s[1]]
#         if s_next[0] < 0:
#             s_next[0] = 0;
            
#     elif a == 1:                    #LEFT
#         s_next = [s[0], s[1]-1]
#         if s_next[1] < 0:
#             s_next[1] = 0;
            
#     elif a == 2:                    #DOWN
#         s_next = [s[0]+1, s[1]]
#         if s_next[0] > 3:
#             s_next[0] = 3;        
#     else:                           #RIGHT
#         s_next = [s[0], s[1] + 1]
#         if s_next[1] > 3:
#             s_next[1] = 3;
            
#     return s_next    


# In[46]:


def getReward(s):
    n1 = s[0];
    n2 = s[1]
    #n1 = no. of cars at end of day at location1
    tmp1 = 0;
    for j in range(20-n2,20):
        for i in range(20-n1,20):
            tmp1 += prob(j,4)*prob(j-(20-n2),2)*prob(i,3)*prob(i-(20-n1),3)*(10*(i+j))
    
    tmp2 = 0;
#     for i in range(n2, 20):
#         tmp2 += prob(i,4)*prob(i-n2,2)*(10*i)
        
    return tmp1;    


# In[47]:


def getProb(pr, nos, l1, l2):
    for i in range(nos-1, 0):
        for j in range(i+1):
            pr[i] = prob(j,l1)*prob(j-nos+i+1,l2)
    
    return pr;


# In[49]:


getReward([20,20])


# In[18]:


def prob(n, tao):
    p = (tao**n)*(e**(-tao))/factorial(n)
    return p


# In[68]:


# def find_rewards(s):
#     for i in range(21*21):
#         for j1 in range(s[0]):
#             for j2 in range(s[1]):
                


# In[84]:


def penalty(a,s,s_next):
    s1 = s[0]; s2 = s[1];
    #return max(abs(s[0]-s_next[0]),abs(s[1]-s_next[1]))
    
    if s1-a<0 or s2+a<0:
        p = 0;
    else:
        p = -2*abs(a)
    
    return p


# In[90]:


def penalty_parking(s):
    p = 0;
    if s[0] > 10:
        p -= -4
    if s[1] > 10:
        p -= -4
        
    return p;    


# In[91]:


def getAction(a):
    return a - 5;


# In[92]:


def policy_eval(V, gamma, noa, th, p):
    V_tmp = copy.deepcopy(V)
    flag = 0;
    steps = 0;
    while flag == 0:
        delta = 0;
        for i in range(21*21):
            v = V_tmp[i]
            p_cur = p[i]
            tmp = 0;
            #iterate over actions
            for a in range(11):
                s = [i/21, i%21]
                A = getAction(a)
                s_next = getNewState(A,s)
                #change s_next into one integer
                pe = penalty(A,s,s_next) #penalty due to car shifting
                p_park = penalty_parking(s_next)
                s_next = 21*s_next[0] + s_next[1]
                
                #using old V here while updating in a new V
                tmp += getReward(s) + pe + p_park + gamma*V[s_next]
                        #V[s_next] will depend on returns as it'll take place next day
                
            tmp = tmp*(1.0/noa) #scaling when equiprobable

            V_tmp[i] = tmp;
        

        if max(delta, abs(v - V[i])) < th:
            flag = 1;
        
        steps += 1;

    return V_tmp    


# In[100]:


#Initialization
nos = 21
V = np.zeros([nos*nos])
noa = 11;
p = [[j for j in range(noa)] for i in range(nos*nos)]
#first and last states are terminal and hence no actions performed
#p[0] = []; p[15] = []

gamma = 0.9
noa = 4;
th = 0.001
#policy_stable = False
policy_flag = 0;
#print(p)


# In[88]:


step = 0;
while policy_flag == 0:
    #Policy Evaluation
    print("STEP: " , step)
    #print("V " )
    #print(V.reshape([21,21]))
    #print("")
    #print("Policy:")
    #print(p)
    print("")
    V = policy_eval(V, gamma, noa, th, p)
    policy_stable = True
    

    #Policy Updation
    p_tmp = [[] for i in range(nos*nos)]
    for i in range(nos*nos):
        a_old = p[i] #entire list
        r = []
        
        for a in range(noa):
            s = [i/nos, i%nos];
            A = getAction(a)
            s_next = getNewState(A,s)
            pe = penalty(A,s,s_next)
            s_next = nos*s_next[0] + s_next[1]
            r.append(getReward(s) + pe + gamma*V[s_next])
            
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
        print(V.reshape([21,21]))
        print("Policy")
        print(p)
        print("STOPP DONE")
      
        
    step += 1;    

        


# In[118]:


# v_plot = V.reshape([21,21])
# x = [i for i in range(21)]
# y = [i for i in range(21)]
# fig = plt.figure()
# ax = plt.axes(projection="3d")
# ax.plot3D(x, y, v_plot, 'gray')


# In[ ]:


#ADDING ANOTHER PENALTY AND CHANGING THE ACTIONS AS ONE CAR CAN BE TAKEN FOR FREE FROM Loc1 to Loc2


# In[113]:


#Changing for changed action
def getAction(a):
    return a - 4;


# In[114]:


#Initialization
nos = 21
V = np.zeros([nos*nos])
noa = 10;
p = [[j for j in range(noa)] for i in range(nos*nos)]
#first and last states are terminal and hence no actions performed
#p[0] = []; p[15] = []

gamma = 0.9
noa = 4;
th = 0.001
#policy_stable = False
policy_flag = 0;
#print(p)


# In[115]:


#Changes:
step = 0;
while policy_flag == 0:
    #Policy Evaluation
    print("STEP: " , step)
    #print("V " )
    #print(V.reshape([21,21]))
    #print("")
    #print("Policy:")
    #print(p)
    print("")
    V = policy_eval(V, gamma, noa, th, p)
    policy_stable = True
    

    #Policy Updation
    p_tmp = [[] for i in range(nos*nos)]
    for i in range(nos*nos):
        a_old = p[i] #entire list
        r = []
        
        for a in range(noa):
            s = [i/nos, i%nos];
            A = getAction(a)
            s_next = getNewState(A,s)
            pe = penalty(A,s,s_next)
            p_park = penalty_parking(s_next)
            s_next = nos*s_next[0] + s_next[1]
            r.append(getReward(s) + pe + p_park + gamma*V[s_next])
            
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
        print(V.reshape([21,21]))
        print("Policy")
        print(p)
        print("STOPP DONE")
      
        
    step += 1;    

        


# In[116]:


v_plot2 = V.reshape([21,21])



# In[117]:


plt.matshow(v_plot2)


# In[ ]:




