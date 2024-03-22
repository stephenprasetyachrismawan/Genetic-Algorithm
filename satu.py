# Mengimpor library random untuk dapat menggunakan fungsi random
import random

# Menginisiasikan nilai
populasi = []
jml_individu = 50
jml_gen = 10
p = 0.5

def fitness_function(x1,x2):
    return 3*x1 - 2*x2
#Membuat class individu untuk dapat mengenali bit dan fitness


#Membuat class Individu untuk dapat mengenali bit dan fitness
class Individu : 
    def __init__(self, bit,id) :
        self.id = id
        self.bit = bit
        self.jadiparent = 0
        self.probabilitas = 0
        self.probkumulatif = 0
        self.bitx1= self.bit[0:int(jml_gen/2)]
        self.bitx2= self.bit[int(jml_gen/2):int(jml_gen)]
        
        self.decimalx1 = 0
        jumlah_pangkat_bit = jml_gen/2-1 #karena jumlah pangkat nya 4 bukan 5
        
        #melakukan perulangan dari index pertama yaitu 2 pangkat 4 hingga pangkat 0
        
        for k in self.bitx1:
            #menjumlahkan nilai fitness dengan nilai sebelumnya
            self.decimalx1 = self.decimalx1+ ( k * 2 ** jumlah_pangkat_bit)
            jumlah_pangkat_bit = jumlah_pangkat_bit-1
            
        
        jumlah_pangkat_bitx = jml_gen/2-1 #karena jumlah pangkat nya 4 bukan 5
        
        #melakukan perulangan dari index pertama yaitu 2 pangkat 4 hingga pangkat 0
        decimal2=0
        for k in self.bitx2:
            #menjumlahkan nilai fitness dengan nilai sebelumnya
           decimal2 = decimal2+ ( k * 2 ** jumlah_pangkat_bitx)
           jumlah_pangkat_bitx = jumlah_pangkat_bitx-1
        self.decimalx2 = decimal2
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
        populasi.append(individu)
        iloop+=1
    else :
        continue
    #Menyisipkan individu ke populasi
    
    
#Menuliskan populasibaiblits = rbopabiliatsarfo  iin rnagr
urut = 1
for manusia in populasi   :
    print(f"Bit Individu ke - {urut} = {manusia.bit}")
    print(f"Decimal X1 Individu ke - {urut} = {manusia.decimalx1}")
    print(f"Decimal X2 Individu ke - {urut} = {manusia.decimalx2}")
    print(f"Fitness Individu ke - {urut} = {manusia.fitness}")
    urut +=1

# totalfit = 0
# for i in populasi :
   
#membuat persentase probabilitas

sum = 0
for i in populasi   :
    sum += i.fitness

urut = 1
probkumulatif = 0
for i in populasi   :
    i.probabilitas = i.fitness /sum
    probkumulatif+=i.probabilitas
    print(f"\nProbabilitas Individu ke -{urut}= {i.probabilitas}")
    print(f"\nProbabilitas Kumulatif = {probkumulatif}")
    i.probkumulatif = probkumulatif
    urut +=1

#Tahapan Cycle Generasi


jumlah_generasi = 30
igen = 1
while igen <=30 :
    # Tahap Seleksi menggunakan Probabilitas Kumulatif
    #random angka dari 0 - 1
    
    Parent1 =[]
    idp1 = 0
    dapet = 0
    while dapet  == 0:
        s = round(random.random(), 4)
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
        r = round(random.random(), 4)
        for j in populasi :
            if j.probkumulatif < r or j.jadiparent == 1 :
                continue
            elif j.probkumulatif >= r:
            
                j.jadiparent = 1
                Parent2 = j.bit.copy()
                idp2 = j.id
                dapet =1
                break
    
    #Crossover
    #uniform crossover1
    
    masking_co1 = [1,1,0,0,0,0,1,0,1,0]
    # masking_co2 = [0,1,0,1,1,0,1,0,1,0]
    # masking_co3 = [1,1,0,1,1,0,0,0,0,1]
    child1 = []
    child2 = []
    i = 0
    while i < len(masking_co1) and i < len(Parent1) and i < len(Parent2):
        if masking_co1[i]==1 :
            child1.append(Parent2[i])
            child2.append(Parent1[i])
        elif masking_co1[i]==0 :
            child1.append(Parent1[i])
            child2.append(Parent2[i])
        i+=1    

    #jadikan self.jadiparent = 0 lagi
    
    for j in populasi :
            j.jadiparent = 0

    #Mutasi
    #Probabilitas Mutasi
    prob_mutasi = 1/jml_gen
    
    #Mutasi Child 1
    child1termutasi = []
    randommutasi = random.random()
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
    randommutasi = random.random()
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
    
    print(f"\n GENERASi ke - {igen}")    
    print(f"\n Parent 1 = {Parent1}")
    print(f"\n Parent 2 = {Parent2}")
    print(f"\n child 1 = {child1termutasi}")
    print(f"\n child 2 = {child2termutasi}")
    print(f"\n")
    igen+=1
    