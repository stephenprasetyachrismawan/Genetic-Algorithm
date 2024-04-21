import random
import matplotlib.pyplot as plt
import numpy as np

def pisahkanbit(bit):
    halflen = len(bit) // 2
    bitx = bit[:halflen]
    bity = bit[halflen:]
    return bitx, bity
def bintodec(binary):
    sign = binary[0]
    bulat = binary[1:3]
    koma = binary[3:]
    decimalbulat = 0
    tertinggi_pangkat_bit = 1
    for k in bulat:
        decimalbulat = decimalbulat+ ( k * 2 ** tertinggi_pangkat_bit)
        tertinggi_pangkat_bit = tertinggi_pangkat_bit-1
    decimalkoma = 0
    tertinggi_pangkat_bit = 14
    for k in koma:
        decimalkoma = decimalkoma+ ( k / (2 ** tertinggi_pangkat_bit))
        tertinggi_pangkat_bit = tertinggi_pangkat_bit-1
    total =  round(decimalbulat + decimalkoma,4)
    if  sign == 0:
        return total
    else: 
        mintotal = 0-total
        return mintotal

def fitness(x1,x2):
    

    res = 0
    res1 = 0
    res2 = 0 

    for i in range(1, 5):
        res1 = res1 + (i*np.cos((i+1)*x1 + i))
        res2 = res2 + (i*np.cos((i+1)*x2 + i))
    
         
    res = res1 * res2
    return res

x1a = -2.2611
x1b = -1.2139
x1c = 0.667
x1d = 0.8805
x1e = 1.9277
x1f= 2.9749

print(f"\n X1 = {x1a} X2 = -0.1997, fitness = {fitness(x1a,-0.1997)}")
print(f"\n X1 = {x1b} X2 = -0.1997, fitness = {fitness(x1b,-0.1997)}")
print(f"\n X1 = {x1c} X2 = -0.1997, fitness = {fitness(x1c,-0.1997)}")
print(f"\n X1 = {x1d} X2 = -0.1997, fitness = {fitness(x1d,-0.1997)}")
print(f"\n X1 = {x1e} X2 = -0.1997, fitness = {fitness(x1e,-0.1997)}")
print(f"\n X1 = {x1f} X2 = -0.1997, fitness = {fitness(x1f,-0.1997)}")


populasi = []
jml_individu = 100
jml_gen = 34
p = 0.5
jumlah_generasi = 1000
sumbuy=[]
sumbuy2 = []
rentangatas = 2
rentangbawah=-2

def generate(jml_individu):
    res_total = []
   
    for i in range(1, jml_individu+1):
        res = []
        res2
        #melakukan pemilihan pengacakan antara 0 sampai 1 dengan digit maksimal 4
        r = round(random.uniform(0, 1), 4)
        if r<p :
            r = 0 #jika nilai random kurang dari 0,5 maka jadi 0
        else :
            r = 1 #jika nilai random lebih dari 0,5 maka jadi 1
            
        #Menyisipkan gen (nilai r) ke calon individu
        res.append(r)
        bitx1,bitx2 = pisahkanbit(res)
        decx1 = bintodec(bitx1)
        decx2 = bintodec(bitx2)
        res2= {
            "bit X1" : bitx1,
            "dec X1" : decx1,
            "bit X2" : bitx2,
            "dec X2" : decx2,
            "fitness" : fitness(decx1,decx2)
        }
        res_total.append(res2)
    return res_total

def ambil_data_fitness(populasi):
    res =[]
    for i in populasi :
        res.append(i["fitness"])
    return res

def min_max_normalisasi(data):
    min_val = min(data)
    max_val = max(data)
    scaled_data = [(x - min_val) / (max_val - min_val) for x in data]
    return scaled_data



def probabilitas(populasi):
    res = []
    
    sumfit = sum(i['fitness_scaled'] for i in populasi)
    for i in populasi :
        prob = 0
        fit = i['fitness_scaled']
        prob = fit/sumfit
        res.append(prob)
    return res

def probabilitas_kumulatif(populasi):
    res=[]
    sumProb = 0
    for i in populasi :
        sumProb = sumProb + i['probabilitas']
        res.append(sumProb)
    return res