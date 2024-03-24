# Mengimpor library random untuk dapat menggunakan fungsi random
import random
import matplotlib.pyplot as plt
import numpy as np

# Menginisiasikan nilai
populasi = []
jml_individu = 50
jml_gen = 10
p = 0.5
jumlah_generasi = 30
sumbuy=[]
sumbuy2 = []
def fitness_function(x1,x2):
    return 3*x1 - 2*x2
def bintodecimal(X,jum_gen_asli):
    decimal = 0
    jumlah_pangkat_bit = jum_gen_asli/2-1 
    for k in X:
        decimal = decimal+ ( k * 2 ** jumlah_pangkat_bit)
        jumlah_pangkat_bit = jumlah_pangkat_bit-1
    return decimal     
#Membuat class individu untuk dapat mengenali bit dan fitness


#Membuat class Individu untuk dapat mengenali bit dan fitness
class Individu : 
    def __init__(self, bit, id) :
        self.id = id
        self.bit = bit
        self.jadiparent = 0
        self.probabilitas = 0
        self.bitx2= self.bit[int(jml_gen/2):int(jml_gen)]
        self.probkumulatif = 0
        self.bitx1= self.bit[0:int(jml_gen/2)]
        self.bitx2= self.bit[int(jml_gen/2):int(jml_gen)]
        
        self.decimalx1 = bintodecimal(self.bitx1, jml_gen)
        self.decimalx2 = bintodecimal(self.bitx2, jml_gen)
        self.fitness = fitness_function(self.decimalx1,self.decimalx2)

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
        
        
    #Memasukan setiap individu ke kelas individu
    individu = Individu(calon, iloop)
    if individu.decimalx1 >=3 and individu.decimalx1<=10 and individu.decimalx2 >=3 and individu.decimalx2<=10 and individu.fitness>0:
        #Menyisipkan individu ke populasi
        populasi.append(individu)
        iloop+=1
    else :
        continue
    
    
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
    i.probabilitas = i.fitness /sum
    probkumulatif+=i.probabilitas
    i.probkumulatif = probkumulatif
    urut +=1

urut = 1
for manusia in populasi   :
    print(f"Bit Individu ke - {urut} = {manusia.bit}")
    print(f"Fitness Individu ke - {urut} = {manusia.fitness}")
    print(f"Probabilitas Individu ke - {urut} = {manusia.probabilitas}")
    print(f"Prob Kumulatif Individu ke - {urut} = {manusia.probkumulatif}")
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
    
    # Membuat list masking dengan 10 elemen
    masking_co1 = []

    # Mengisi list masking dengan nilai acak antara 0 dan 1
    for _ in range(10):
        nilai_acak = random.randint(0, 1)
        masking_co1.append(nilai_acak)
    childtotal = []
    for pairs in semua_parent:
        ParentOne = []
        ParentTwo = []
       
        ParentOne = pairs[0]
        
        ParentTwo = pairs[1]
        print(f"\n Parent 0 = {ParentOne}")
        print(f"\n Parent 1 = {ParentTwo}\n")
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
        prob_mutasi = 1/jml_gen
        
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
            
            index1 = random.randint(0,jml_gen-1)
            index2 = random.randint(0,jml_gen-1)
            if index1!=index2:
                break
            
        child1termutasi[index1],  child1termutasi[index2] =  child1termutasi[index2],  child1termutasi[index1]
        
        #CHILD 2
        index1=0
        
        index2 =0
        while 1 :
            
            index1 = random.randint(0,jml_gen-1)
            index2 = random.randint(0,jml_gen-1)
            if index1!=index2:
                break
            
        child2termutasi[index1],  child2termutasi[index2] =  child2termutasi[index2],  child2termutasi[index1]
        
        childtotal.append(child1termutasi)
        childtotal.append(child2termutasi)
    #mencari dan menggantikan nilai fitness terendah
    for c in childtotal:
        childx1 = c[0:int(jml_gen/2)]
        childx2 = c[int(jml_gen/2):int(jml_gen)]
        decimalchildx1 = bintodecimal(childx1, jml_gen)
        decimalchildx2 = bintodecimal(childx2, jml_gen)
        fitnesschild = fitness_function(decimalchildx1,decimalchildx2)
    
        #Perhitungan dan Penggantian dari Child 1
        if decimalchildx1 >=3 and decimalchildx1<=10 and decimalchildx2 >=3 and decimalchildx2<=10:
            minimfitness = 24
            
            minimID = 0
            minimbit = []
            for p in populasi :
                if p.fitness <minimfitness and fitnesschild>=p.fitness:
                    minimfitness = p.fitness
                    minimbit = p.bit
                    minimID = p.id
                else:
                    continue
            for q in populasi :
                if q.id == minimID:
                    q.bit =  c
                    q.fitness = fitnesschild
                    q.decimalx1 = decimalchildx1
                    q.decimalx2 = decimalchildx2
                    
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
        i.probabilitas = i.fitness /sum
        probkumulatif+=i.probabilitas
        i.probkumulatif = probkumulatif
        urut +=1
    
    #Perhitungan rata rata nilai fitness generasi ke generasi
    
    avg = sum/jml_individu
    sumbuy2.append(avg)
    print(f"\nFitness average Generasi ke - {igen} = {avg}")
    igen+=1
urut = 1
print(f"\n50 Individu Hasil Iterasi Terakhir :")
for manusia in populasi   :
    
    print(f"Bit Individu ke - {urut} = {manusia.bit}")
    print(f"Fitness Individu ke - {urut} = {manusia.fitness}")
    print(f"Probabilitas Individu ke - {urut} = {manusia.probabilitas}")
    print(f"Prob Kumulatif Individu ke - {urut} = {manusia.probkumulatif}")
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
plt.plot(sumbux2, sumbuy2, 'o', markersize=3,color="red", linestyle="-", label='Rerata Fitness')
plt.xlabel('Generasi')
plt.ylabel('Fitness')
plt.title('Perkembangan Fitness pada Setiap Generasi')
plt.legend()
plt.show()

