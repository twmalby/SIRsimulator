# −*− coding : utf−8 −*− # python2.7
import math
import numpy
import random
import csv

############### USER CUSTOM DATA              ### #Let G = (V,E) graph ##########################
nodes = 1200 # |V| = nodes, population								#
ite = 10 # final iterations										#
percentuale = 0.7 #percentage of flips of the edges	(figure the mutability of 2 nodes to match or less anymore randmoly)				#
alfa1 = 0.60 # percentage of contagiousity between one infected node and one healty node				#
beta1 = 0.40 # percentage of surviving of one infected node								#
S = 10  # infected-spreaders	at the beginning	of the simulation					#
####################################################################################################
flag = 0
edges = random.sample(range(2*nodes,int(((nodes*nodes)-nodes)*0.5)),1)[0]# |E| = edges ( archi )
valore = int(edges*percentuale)# calcolo percentuale discretizzata
G = 0 # guariti
 # inizializzazione degli Spreaders
R = 0 # inizializzazione Refrattari
I = nodes-S
alfa = 1-alfa1
beta = 1-beta1
K = 1 # Spreaders cumulativi
C = 0 # c i c l i t o t a l i azioni compiute dagli Spreaders
SpreaderRate = K / nodes # i l rosso nella grafica è associato agli Spreaders

giallo = 3
rosso = 2
verde = 1 # i l verde nella grafica è associato agli Ignorants
bianco =0 # i l bianco nella grafica è associato agli S t i f l e r s
RegistroColoriCoord = None
curati = 0
def SmeetIC() : # (I ,S,R) |− (I−1, S+1,R)
	global I
	global S
	global C

	I=I-1
	S=S+1


	print "One is infected ",[ I ,S ,R ,C ]

def ProllyToCare() :
    global I
    global R
    global C
    global S
    global flag

    if S>0 :
        if random.uniform(0,1)> beta  : #percentuale di guarire
            S=S-1

            I=I+1

            flag = 1
            C=C+1 # curati
            print "An infected is recovered :)",[I,S,R,C]

        else:
            S=S-1
            R=R+1
            I=I

            C=C
            flag = 0 # dec
            print "An infected died!  :(",[I,S,R,C]
    print "Nobody can be cared!",[I,S,R,C]




def RegistroColoriCoordVerdi () : # coloro tutto di verde , quindi resetto lo scenario per una nuova iterazione
	global I
	global R
	global S
	global C
	global K
	global nodes
	global RegistroColoriCoord

	RegistroColoriCoord = numpy.zeros(shape=(nodes,3))
	for x in range (0,nodes ) :

		(RegistroColoriCoord[x,0]) = verde

	
	I = nodes-S
	R = 0
	C = 0
	K = 1

def CreaScenario() : # piazza uno Spreader a random, g l i a l t r i restano verdi
	global I
	global S
	global R
	global RegistroColoriCoord
	S = 3

	I = I - S
	for t in range(0,S):
		RegistroColoriCoord[t,0]=rosso

def CreaGrafoCompleto() : # crea una matrice di adiacenza per i l grafo completo .
	global M
	global nodes
	M = numpy.zeros(shape=(nodes,nodes))
	for y1 in range (0,nodes):
		for y2 in range (0,nodes) :
			M[y1,y2] = M[y2,y1]=1
			M[y1,y1]=0

def CreaGrafoRandom() : # crea una matrice di adiacenza randomizzata
	global M
	global nodes
	global edges
	x=0
	edges = random.sample(range(2*nodes,int((nodes*nodes-nodes)*0.5)),1)[0] # |E| = edges ( archi )
	M = numpy.zeros(shape=(nodes,nodes))
	while x<edges :
		i = random.sample(range(0,nodes),1)[0] # associo ad i un valre {0 ,... ,n−1} random
		j = random.sample(range(0,nodes),1)[0] # associo ad j un valre {0 ,... ,n−1} random
		if(M[i,j] == 1 ) :
			x=x+1
		elif( M[i,j]== 0 & i != j ) :
			M[i,j] = M[j,i]=1
		else :
			M[i,i]=0
			x=x-1
		x=x+1

def ComputingRandomNoGUI() : # Algoritmo casuale
	global RegistroColoriCoord

	randspreadid = random.sample(numpy.where(RegistroColoriCoord[:,0]== rosso)[0],1)[0]
	z = random.sample(numpy.where(M[randspreadid,:]==1)[0],1)[0] # Tra i contatti di randspreadid seleziono un nodo a caso connesso

	if RegistroColoriCoord[z,0]==verde : # Se i l nodo z−esimo selezionato è verde
		if random.uniform(0,1)> alfa : # Controllo se è tendenzialmente Rosso
			RegistroColoriCoord[z,0]= rosso # In questo caso coloro i l nodo z−esimo di Rosso
			SmeetIC()

			ProllyToCare()
		if flag == 0 :
			random.sample(numpy.where(RegistroColoriCoord[:,0]== rosso)[0],1)[0] = 0
		if flag == 1 :
			random.sample(numpy.where(RegistroColoriCoord[:,0]== rosso)[0],1)[0] = 1





def SalvaFileStaticoNormale () :

	RegistroColoriCoordVerdi()
	CreaGrafoRandom()
	CreaScenario()

	with open('RandomStat4b.csv','w') as csvfile :
		spamwriter = csv.writer(csvfile,delimiter=',',quotechar='|',quoting=csv.QUOTE_MINIMAL)
		spamwriter.writerow(['incontaminati+guariti','s-spread','r-deceduti','sologuariti'])
		for x in range (0,ite) :
			with open('RandomFlip4b.csv','w') as csvfile :
				spamwriter = csv.writer(csvfile,delimiter=',',quotechar='|',quoting=csv.QUOTE_MINIMAL)
				spamwriter.writerow([I,S,R,C])
			print "Saving data base f i l e . . . "
			RegistroColoriCoordVerdi()
			CreaGrafoRandom()
			CreaScenario()

			while S>0:
				ComputingRandomNoGUI()






def CambiaMatrice () : # Modifica la matrice di adiacenza
	x=0
	global M
	while x<valore :
		i=random.sample(range(0,nodes),1)[0]
		j=random.sample(range(0,nodes),1)[0]
		if( i != j ) :
			if ( M[i,j]== 1) :
				M[i,j]=M[j,i]  = 0 # se c 'è collegamento lo rompe
			elif(M[i,j]==0):
				M[i,j]=M[j,i]=1 # se non c 'è collegamento lo crea
		else :
			x=x-1 # se i=j i l contatore torna indietro di un passo
		x=x+1


def SalvaFileVariabileNormale() :
	RegistroColoriCoordVerdi()
	CreaGrafoRandom()
	CreaScenario()

	with open('RandomFlip4b.csv','w') as csvfile :
		spamwriter = csv.writer(csvfile,delimiter=',',quotechar='|',quoting=csv.QUOTE_MINIMAL)
		spamwriter.writerow(['incontaminato+guariti','s-spread','r-deceduti','sologuariti'])
		for x in range (0,ite) :
			print "Saving data base f i l e . . . "
			with open('RandomFlip4b.csv','w') as csvfile :
				spamwriter = csv.writer(csvfile,delimiter=',',quotechar='|',quoting=csv.QUOTE_MINIMAL)
				spamwriter.writerow([I,S,R,C])
			RegistroColoriCoordVerdi()
			CreaGrafoRandom()
			CreaScenario()

			while S>0:
				if random.uniform (0,1) > 0.40 :
					CambiaMatrice()
				ComputingRandomNoGUI()









print "START RANDOM STAT"
SalvaFileStaticoNormale()
print "START RANDOM FLIP"
SalvaFileVariabileNormale()
