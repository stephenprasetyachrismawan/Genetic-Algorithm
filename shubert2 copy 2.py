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

    for i in range(1, 6):
        res1 = res1 + (i*np.cos((i+1)*x1 + i))
        res2 = res2 + (i*np.cos((i+1)*x2 + i))
    
         
    res = res1 * res2
    return res

# x1a = -2.2611
# x1b = -1.2139
# x1c = 0.667
# x1d = 0.8805
# x1e = 1.9277
# x1f= 2.9749

# print(f"\n X1 = {x1a} X2 = -0.1997, fitness = {fitness(x1a,-0.1997)}")
# print(f"\n X1 = {x1b} X2 = -0.1997, fitness = {fitness(x1b,-0.1997)}")
# print(f"\n X1 = {x1c} X2 = -0.1997, fitness = {fitness(x1c,-0.1997)}")
# print(f"\n X1 = {x1d} X2 = -0.1997, fitness = {fitness(x1d,-0.1997)}")
# print(f"\n X1 = {x1e} X2 = -0.1997, fitness = {fitness(x1e,-0.1997)}")
# print(f"\n X1 = {x1f} X2 = -0.1997, fitness = {fitness(x1f,-0.1997)}")


populasi = []
jml_individu = 100
jml_gen = 34
p = 0.5
jumlah_generasi = 10000
sumbuy=[]
sumbuy2 = []
rentangatas = 3
rentangbawah=-3

def generate(jml_individu, jml_gen):
    res_total = []
   
    for i in range(1, jml_individu+1):
        
        tidak_sesuai_rentang = 1
        while tidak_sesuai_rentang == 1 :
            res = []
            res2={}
            for j in range(1,jml_gen+1):
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
                "bits": res,
                "bit X1" : bitx1,
                "dec X1" : decx1,
                "bit X2" : bitx2,
                "dec X2" : decx2,
                "fitness" : fitness(decx1,decx2)
            }
            if res2['dec X1'] >= rentangbawah and res2['dec X1']<=rentangatas and res2['dec X2'] >= rentangbawah and res2['dec X2']<=rentangatas :
                tidak_sesuai_rentang = 0
        res_total.append(res2)
    
    return res_total

# def ambil_data_fitness(populasi):
#     res =[]
#     for i in populasi :
#         res.append(i["fitness"])
#     return res

# def min_max_normalisasi(data):
#     min_val = min(data)
#     max_val = max(data)
#     # Handling ketika nilai minimum dan maksimum sama
#     if min_val == max_val:
#         scaled_data = [0.001 for _ in data]
#     else:
#         scaled_data = [(x - min_val) / (max_val - min_val) for x in data]
#     return scaled_data
def min_max_nonnegatif(data):
    min_val = min(data)
    scaled_data = [x + abs(min_val) + 0.1 for x in data]
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
# def urut_by_fitness_elite(populasi):
#     new = []
#     minFit = 0
#     a =0 
#     for i in populasi :
#         if a == 0 :
#             minFit = i['fitness']
#             new.append(i)
            
#         else :
#             if i['fitness']  < minFit:
#                 minFit = i['fitness']
#                 new.insert(0,i)
#             else:
#                 b = 0
#                 belum=1
#                 for j in new :
#                     if i['fitness'] <=  j['fitness'] :
#                         new.insert(b,i)
#                         belum = 0
#                         break
#                     b += 1
#                 if belum == 1 :
#                     new.append(i)
#         a +=1
#     return new

# def elite(populasi):
#     jml_elite = 0.4 * len(populasi)
#     newpopulasi = urut_by_fitness_elite(populasi)
#     elite = newpopulasi[:int(jml_elite)]
#     nonelite = newpopulasi[int(jml_elite):]
#     half1elite = elite[:int(len(elite)/4)]
#     half2elite = elite[int(len(elite)/4):]
#     return nonelite,half1elite,half2elite

def seleksi(populasi):
    parents_pair = []
    all_parents =[]
    
    #memasukkan fitness scaled
    fitness_populasi = []
    for i in populasi:
        fitness_populasi.append(i['fitness'])
    nonnegatif_populasi = min_max_nonnegatif(fitness_populasi)
    a=0
    for i in populasi:
        i['fitness_scaled']=nonnegatif_populasi[a]
        a+=1
        
    
    
    #memasukkan probabilitas
    
    probabilitas_populasi = probabilitas(populasi)
    a=0
    for i in populasi:
        i['probabilitas']=probabilitas_populasi[a]
        a+=1
        
    
    #memasukkan probabilitas kumulatif
    
    probabilitas_kumulatif_populasi = probabilitas_kumulatif(populasi)
    a=0
    for i in populasi:
        i['probabilitas_kumulatif']=probabilitas_kumulatif_populasi[a]
        i['jadiparent']=0
        a+=1
    
    
    #membangkitkan bilangan random untuk mencari select poin di probabilitas kumulatif
    #Mencari Parent 1
    for _ in range(int(len(populasi)/2)):
        Parent1 = []
        dapet = 0
        while dapet  == 0:
            s = round(random.uniform(0,1), 4)
            
            for l in populasi :
                if l['probabilitas_kumulatif'] < s or l['jadiparent']==1:
                    continue
                elif l['probabilitas_kumulatif'] >= s and l['jadiparent']==0:
                    l['jadiparent'] = 1
                    Parent1 = l['bits']
                    
                    dapet =1
                    break
        Parent2 = []
        dapet = 0
            
        while dapet  == 0:
            s = round(random.uniform(0,1), 4)
            for l in populasi :
                if l['probabilitas_kumulatif'] < s or l['jadiparent']==1:
                    continue
                elif l['probabilitas_kumulatif'] >= s and l['jadiparent']==0:
                    l['jadiparent'] = 1
                    Parent2 = l['bits']
                    dapet =1
                    break
        parents_pair.append(Parent1)
        parents_pair.append(Parent2)
        all_parents.append(parents_pair)
        
    for i in populasi:
        i['jadiparent']=0
    return all_parents

def crossover_mutation(all_parents):

    # Membuat list masking 
    masking_co1 = []
    # Mengisi list masking dengan nilai acak antara 0 dan 1
    for _ in range(jml_gen):
        nilai_acak = random.randint(0, 1)
        masking_co1.append(nilai_acak)
    
        
    childtotal = []
    for pairs in all_parents:
        ParentOne , ParentTwo = pairs[0] , pairs[1]
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
        
    return childtotal
def subtitusi(childtotal, populasi):
    childtotalbaru = []
    
    for i in childtotal:
        bitx1, bitx2 = pisahkanbit(i)
        decx1 = bintodec(bitx1)
        decx2 = bintodec(bitx2)
        fitness_value = fitness(decx1, decx2 )  # Menggunakan nama variabel yang berbeda
        childdata = {
            "bits": i,
            "bit X1": bitx1,
            "dec X1": decx1,
            "bit X2": bitx2,
            "dec X2": decx2,
            "fitness": fitness_value  # Menyimpan nilai fitness yang telah dihitung
        }
        childtotalbaru.append(childdata)
        
    for i in childtotalbaru:
        if i['dec X1'] < rentangbawah or i['dec X1'] > rentangatas or i['dec X2'] < rentangbawah or i['dec X2'] > rentangatas:
            continue
        
        for j in populasi:
            if i['fitness'] < j['fitness']: 
                j['bits'] = i['bits']
                j['bit X1']=i['bit X1']
                j['bit X2']=i['bit X2']
                j['dec X1']=i['dec X1']
                j['dec X2']=i['dec X2']
                j['fitness']=i['fitness']
                # Substitusi
                break
            else:
                
                continue
    
    return populasi

#Implementasi
             
#1. Melakukan generasi awal sebanyak 100 individu
populasi_awal = generate(100,34)
print(populasi_awal)
populasi_baru =populasi_awal
gen = 1
minFit = 0
minBit=[]
minX1 = 0
minX2 = 0
sumbuy = []
for i in range(1, jumlah_generasi+1) :
    semua_parent = seleksi(populasi_baru)
    childtotal = crossover_mutation(semua_parent)
    populasi_baru_baru = subtitusi(childtotal,populasi_baru)
    

    a = 1
    
    for i in populasi_baru:
        if a == 1:
            minFit = i['fitness']
            minBit =  i['bits']
            minX1 = i['dec X1']
            minX2 = i['dec X2']
            
        elif i['fitness'] < minFit :
            minFit=i['fitness']
            minBit =  i['bits']
            minX1 = i['dec X1']
            minX2 = i['dec X2']
        sumbuy.append(i['fitness'])
        a+=1
    print(f"\nGenerasi Ke {gen}")
    print(f"Minimum Fitness = {minFit}")
    print(f"Minimum Bit = {minBit}")
    print(f"X1 = {minX1}")
    print(f"X2 = {minX2}")
    
    gen+=1
sumbux = []
for i in range(1,jumlah_generasi+1):
    for j in range(1,jml_individu+1):
        sumbux.append(i)

grafik_fitness_vs_generasi = plt.figure()
plt.plot(sumbux,sumbuy,'o')
plt.xlabel('Generasi')
plt.ylabel('Nilai Fitness')
plt.title('Grafik Perkembangan Nilai Fitness vs Generasi')
plt.show()


    