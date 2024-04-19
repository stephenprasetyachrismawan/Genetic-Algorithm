import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

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

def fitness(bit):
    bitx = bit[:17]
    bity = bit[17:]
    decbitx = bintodec(bitx)
    decbity = bintodec(bity)
    res = 0
    res1 = 0
    res2 = 0 
    i = 1
    while i <= 5 :
        res1 = res1 + (i*math.cos((i+1)*decbitx + i))
        i += 1
    i = 1
    while i <= 5 :
        res2 = res2 + (i*math.cos((i+1)*decbity + i))
        i += 1
         
    res = res1 * res2
    return res


populasi = []
jml_individu = 100
jml_gen = 34
p = 0.5
jumlah_generasi = 10000
sumbuy=[]
sumbuy2 = []
rentangatas = 3
rentangbawah=-3

#Membuat class Individu untuk dapat mengenali bit dan fitness
class Individu : 
    def __init__(self, bit, id) :
        self.id = id
        self.bit = bit
        self.jadiparent = 0
        self.probabilitas = 0
        self.probkumulatif = 0
        self.fitness = fitness(bit)
        j = 0
        

iloop = 1
while iloop <= jml_individu :
    calon = []
    
    #Melakukan perulangan untuk membuat 1 per satu gen
    for j in range(jml_gen):
        #melakukan pemilihan pengacakan antara 0 sampai 1 dengan digit maksimal 4
        r = round(random.uniform(0, 1), 4)
        if r<p :
            r = 0 #jika nilai random kurang dari 0,5 maka jadi 0
        else :
            r = 1 #jika nilai random lebih dari 0,5 maka jadi 1
            
        #Menyisipkan gen (nilai r) ke calon individu
        calon.append(r)
        
    #pengecekan rentang
    bitx = calon[:17]
    bity = calon[17:]
    decbitx = bintodec(bitx)
    decbity = bintodec(bity)
    #Memasukan setiap individu ke kelas individu
    if (decbitx <= rentangatas and decbitx >=rentangbawah and decbity <= rentangatas and decbity >=rentangbawah) :
        individu = Individu(calon, iloop) 
    
        #Menyisipkan individu ke populasi
        populasi.append(individu)
        iloop+=1    
    
    
    
    
#membuat persentase probabilitas
sum = 0
for i in populasi   :
    sum += i.fitness
    sumbuy.append(i.fitness)



avg = sum/jml_individu
sumbuy2.append(avg)

urut = 1
probkumulatif = 0
for i in populasi   :
    i.probabilitas = abs(i.fitness /sum)
    probkumulatif+=i.probabilitas
    i.probkumulatif = probkumulatif
    urut +=1

urut = 1
for manusia in populasi   :
    ##print(f"Bit Individu ke - {urut} = {manusia.bit}")
    ##print(f"Fitness Individu ke - {urut} = {manusia.fitness}")
    ##print(f"Probabilitas Individu ke - {urut} = {manusia.probabilitas}")
    ##print(f"Prob Kumulatif Individu ke - {urut} = {manusia.probkumulatif}")
    urut +=1


#Tahapan Cycle Generasi



igen = 1
while igen <= jumlah_generasi:
    # Tahap Seleksi menggunakan Probabilitas Kumulatif
    #random angka dari 0 - 1
    semua_parent = []
    for _ in range(int(jml_individu/2)):
        parents_pair = []
        Parent1 =[]
        idp1 = 0
        dapet = 0
        while dapet  == 0:
            s = round(random.uniform(0,1), 4)
            for l in populasi :
                if l.probkumulatif < s or l.jadiparent == 1:
                    continue
                elif l.probkumulatif >= s:
                    l.jadiparent = 1
                    Parent1 = l.bit.copy()
                    idp1 = l.id
                    dapet =1
                    break
        Parent2 = []
        idp2 = 0
        dapet = 0
        while dapet  == 0:
            r = round(random.uniform(0,1), 4)
            for j in populasi :
                if j.probkumulatif < r or j.jadiparent == 1 :
                    continue
                elif j.probkumulatif >= r:
                
                    j.jadiparent = 1
                    Parent2 = j.bit.copy()
                    idp2 = j.id
                    dapet =1
                    break
        parents_pair.append(Parent1)
        parents_pair.append(Parent2)
        semua_parent.append(parents_pair)
    
    #Crossover
    #uniform crossover1
    
    # Membuat list masking 
    masking_co1 = []

    # Mengisi list masking dengan nilai acak antara 0 dan 1
    for _ in range(jml_gen):
        nilai_acak = random.randint(0, 1)
        masking_co1.append(nilai_acak)
    childtotal = []
    for pairs in semua_parent:
        ParentOne = []
        ParentTwo = []
       
        ParentOne = pairs[0]
        
        ParentTwo = pairs[1]
        #print(f"\n Parent 0 = {ParentOne}")
        #print(f"\n Parent 1 = {ParentTwo}\n")
        child1 = []
        child2 = []
        i = 0
        while i < len(masking_co1) and i < len(ParentOne) and i < len(ParentTwo):
            if masking_co1[i]==1 :
                child1.append(ParentTwo[i])
                child2.append(ParentOne[i])
            elif masking_co1[i]==0 :
                child1.append(ParentOne[i])
                child2.append(ParentTwo[i])
            i+=1    

        #jadikan self.jadiparent = 0 lagi
        
        for j in populasi :
                j.jadiparent = 0

        #Mutasi
        #Probabilitas Mutasi
        prob_mutasi = 1/(jml_gen)
        
        #Mutasi Child 1
        child1termutasi = []
        randommutasi = random.uniform(0,1)
        for k in child1 : 
            if randommutasi<prob_mutasi :
                if k==0:
                    child1termutasi.append(1)
                elif k==1:
                    child1termutasi.append(0)
            else :
                child1termutasi.append(k)
        #Mutasi Child 2
        child2termutasi = []
        randommutasi = random.uniform(0,1)
        for k in child1 :
            if randommutasi<prob_mutasi :
                if k==0:
                    child2termutasi.append(1)
                elif k==1:
                    child2termutasi.append(0)
            else :
                child2termutasi.append(k)

        #MUTASI KEDUA
        #menggunakan swap mutation
        #CHILD 1
        index1=0
        
        index2 =0
        while 1 :
            
            index1 = random.randint(0,(jml_gen)-1)
            index2 = random.randint(0,(jml_gen)-1)
            if index1!=index2:
                break
            
        child1termutasi[index1],  child1termutasi[index2] =  child1termutasi[index2],  child1termutasi[index1]
        
        #CHILD 2
        index1=0
        
        index2 =0
        while 1 :
            
            index1 = random.randint(0,(jml_gen)-1)
            index2 = random.randint(0,(jml_gen)-1)
            if index1!=index2:
                break
            
        child2termutasi[index1],  child2termutasi[index2] =  child2termutasi[index2],  child2termutasi[index1]
        
        childtotal.append(child1termutasi)
        childtotal.append(child2termutasi)
    #mencari dan menggantikan nilai fitness terendah
    for c in childtotal:
        
        fitnesschild = fitness(c)
        bitx = c[:17]
        bity = c[17:]
        decbitx = bintodec(bitx)
        decbity = bintodec(bity)
        #Perhitungan dan Penggantian dari Child 1
        if (decbitx >= rentangbawah and decbitx<=rentangatas) and (decbity >= rentangbawah and decbity<=rentangatas) :
            
            
            
            
            for q in populasi :
                if fitnesschild < q.fitness:
                    q.bit =  c
                    q.fitness = fitnesschild
                    
                    break
                else:
                    continue
        
    sum = 0
    for i in populasi   :
        sum += i.fitness

        sumbuy.append(i.fitness)

    urut = 1
    probkumulatif = 0
    for i in populasi   :
        i.probabilitas = abs(i.fitness /sum)
        probkumulatif+=i.probabilitas
        i.probkumulatif = probkumulatif
        urut +=1
    
    #Perhitungan best  nilai fitness generasi ke generasi
    
    
    avg = sum/jml_individu
    minfit = 0
    ax = 1
    for p in populasi :
        if ax == 1:
           
            minfit = p.fitness
        else :
            if p.fitness < minfit :
                
                minfit = p.fitness
        ax+=1
        
    sumbuy2.append(minfit)
    print(f"\nBest Fitness Generasi ke - {igen} = {minfit}")
    igen+=1
urut = 1
#print(f"\n50 Individu Hasil Iterasi Terakhir :")
for manusia in populasi   :
    
    #print(f"Bit Individu ke - {urut} = {manusia.bit}")
    #print(f"Fitness Individu ke - {urut} = {manusia.fitness}")
    #print(f"Probabilitas Individu ke - {urut} = {manusia.probabilitas}")
    #print(f"Prob Kumulatif Individu ke - {urut} = {manusia.probkumulatif}")
    urut +=1
i=0
sumbux=[]
while i <= jumlah_generasi:
    j = 0
    while j < jml_individu:
        sumbux.append(i)
        j+=1
    i+=1
xpoints = sumbux
ypoints = sumbuy
i=0
sumbux2=[]
while i <= jumlah_generasi:
    sumbux2.append(i)
    i+=1
plt.plot(xpoints, ypoints, 'o', markersize=2, label='Semua Fitness')
plt.plot(sumbux2, sumbuy2, 'o', markersize=3,color="red", linestyle="-", label='Best Fitness')
plt.xlabel('Generasi')
plt.ylabel('Fitness')
plt.title('Perkembangan Fitness pada Setiap Generasi')
plt.legend()
plt.show()

