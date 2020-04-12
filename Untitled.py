#!/usr/bin/env python
# coding: utf-8

# In[1]:


from PIL import Image
from numpy import *
from collections import Counter , defaultdict


# In[2]:


def encode(raw_data,dict,block_size):  #raw data as an array or a list 
    length = len(raw_data)
    r = length%block_size
    encoded_data = []
    if(r != 0): 
        for p in range (block_size - r): #add padding
            raw_data= append(raw_data,raw_data[0])
        length = len(raw_data)
    for i in range(length//block_size):
        c = encode_unit(raw_data , dict , i*block_size , block_size) #encode each block separately
        encoded_data.append(c)
    return encoded_data


# In[3]:


def encode_unit(data , dict , offset , block_size):# takes a dict {char : (lower , higher)}
    p=1 #probability of the first level 
    code = 0 
    l  = offset + block_size #encode starting with the nth block
    for i in range(offset , l):
        code += dict[data[i]][0] * p #add the current level and the current probability to the block code
        if(i == l -1 ): # take the average of the last lower and upper bounds
            code = (2 * code +  (dict[data[i]][1] - dict[data[i]][0])  * p) / 2
        p *= (dict[data[i]][1]-dict[data[i]][0]) # next lvl  =  probability of the last level * the probability of the pixel 
    return code


# In[4]:


def decode(encoded_data , dict , raw_length , block_size):
    decoded_data = []
    for c in encoded_data:
        decode_unit(decoded_data , c , dict ,block_size)
    if(raw_length % block_size):
        for i in range (block_size - raw_length % block_size): # remove padding
            decoded_data.pop()
    return decoded_data


# In[5]:


def decode_unit(decoded , encoded , decode_dict , length): #takes a sorted list [(char , lower , higher)]
    l = 0 
    h = 1
    for i in range(length):
        x = binary_search(encoded,decode_dict,l,h-l,0,len(decode_dict))
        if(x is None):
            #if the code wasn't found due to float percesion add the last pixel instead
            decoded.append(decoded[len(decoded) -1])
        else :
            l = x[1]
            h = x[2]
            decoded.append(x[0])
    return decoded


# In[6]:


def binary_search(code,d,lower,p,left,right): # binary search that checks the bounderies
    if(left <= right):
        i = left + (right - left) // 2
        l = lower +p * d[i][1];
        h = l + p* (d[i][2]-d[i][1])
        if ( code >= l and code < h  ):
            res = (d[i][0] , l , h)
            return res
        elif(code < l):
            return binary_search(code,d,lower,p,left,i-1)
        elif(code > h):
            return binary_search(code,d,lower,p,i+1,right)
    else:
        raise ValueError('Could Not Decode ' + str(code))


# In[7]:


img = Image.open("mn.png").convert("L") #read an Image and convert it into a grayscale image 


# In[8]:


arr = array(img).flatten() #flatten the image 


# In[9]:


#build a counter of the probability of each pixel 
c = Counter(arr) 
prob_arr = []
for p in c:
    c[p] = c[p] / len(arr)
for i in range(256): #create the 1d array to be saved 
    prob_arr.append(c[i])
c = c.most_common() #sort it as a list of tubles
prob_arr = array(prob_arr)
save('prob',prob_arr)


# In[10]:


counter  = []
prob_arr = load('prob.npy')
for p in enumerate(prob_arr):
    if (p[1]):
        counter.append((p[0],p[1]))
counter.sort(key=lambda x:x[1], reverse=True)


# In[11]:


d = defaultdict(list)
sum = 0 
for i in counter:
    d[i[0]] = (sum , sum + i[1])
    sum += i[1]


# In[20]:


encoded = encode(arr,d,4)


# In[21]:


encoded = array(encoded)


# In[22]:


save('encoded2' , encoded )


# In[23]:


encoded = load('encoded2.npy')


# In[24]:


decode_dict = []
sum = 0 
for i in counter:
    decode_dict.append((i[0],sum , sum + i[1]))
    sum += i[1]


# In[25]:


photo = decode(encoded , decode_dict ,len(arr),4)


# In[26]:


p = reshape(array(photo , dtype = uint8),(-1 , img.width))


# In[27]:


Image.fromarray(p)


# In[ ]:




