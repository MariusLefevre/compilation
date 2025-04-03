from item import item
import graphviz
import pickle


axiom = 'S'
nterm = ['E','T','F','S']
empty = '\u03b5' # mot vide
rules = [
{'left':'S','right':['E']},
{'left':'E','right':['E','+','T']},
 {'left':'E','right':['T']},
 {'left':'T','right':['T','*','F']},
 {'left':'T','right':['F']},
 {'left':'F','right':['(','E',')']},
 {'left':'F','right':['0']},
 {'left':'F','right':['1']},
 {'left':'F','right':['2']},
 {'left':'F','right':['3']},
 {'left':'F','right':['4']},
 {'left':'F','right':['5']},
 {'left':'F','right':['6']},
 {'left':'F','right':['7']},
 {'left':'F','right':['8']},
 {'left':'F','right':['9']}
]
symbols = ['S','E','T','F','+','*','(',')','0','1','2','3','4','5','6','7','8','9','$']
ntermS = ['0','1','2','3','4','5','6','7','8','9','+','*','(',')','$']
word = ['5','+','(','2','+','8',')'] # mot à parser
follow = {}
first_symb = {}

def firstSymb():
    for a in ntermS :
        first_symb[a] = [a]
    for n in nterm :
        first_symb[n] = []
    first_symb[axiom] = []
    fin = False
    while not fin :
        fin = True
        for r in rules :
            if r['right'][0]==empty and empty not in first_symb[r['left']] :
                first_symb[r['left']].append(empty)
                fin = False
            else :
                for p in first_symb[r['right'][0]] :
                    if p not in first_symb[r['left']] :
                        first_symb[r['left']].append(p)
                        fin = False
                i = 0
                while i<len(r['right'])-1 and empty in first_symb[r['right'][i]] :
                    for p in first_symb[r['right'][i+1]] :
                        if p not in first_symb[r['left']] :
                            first_symb[r['left']].append(p)
                            fin = False
                    i += 1
                if i==len(r['right'])-1 :
                    if empty in first_symb[r['right'][i]] :
                        if empty not in first_symb[r['left']] :
                            first_symb[r['left']].append(empty)
                            fin = False
    for s,fs in first_symb.items() :
        print('DEBUT('+s+') = '+str(fs))


def first(exp) :
    f = [p for p in first_symb[exp[0]] if p!=empty]
    i = 0
    while i<len(exp)-1 and empty in first_symb[exp[i]] :
        f += [p for p in first_symb[exp[i+1]] if p!=empty]
        i += 1
    if i==len(exp)-1 :
        if empty in first_symb[exp[i]] and empty not in f :
            f.append(empty)
    return f

def Follow():
    firstSymb()
    for n in nterm :
        follow[n] = []
    follow[axiom] = ['$']
    fin = False
    while not fin :
        fin = True
        for r in rules :
            for i in range(len(r['right'])) :
                if r['right'][i] in nterm :
                    if i<len(r['right'])-1 :
                        add = [e for e in first(r['right'][i+1:]) if e!=empty and e not in follow[r['right'][i]]]
                        follow[r['right'][i]] += add
                        if len(add)!=0 :
                            fin = False
                        if empty in first(r['right'][i+1:]) :
                            add = [e for e in follow[r['left']] if e not in follow[r['right'][i]]]
                            follow[r['right'][i]] += add
                            if len(add)!=0 :
                                fin = False
                    else :
                        add = [e for e in follow[r['left']] if e not in follow[r['right'][i]]]
                        follow[r['right'][i]] += add
                        if len(add)!=0 :
                            fin = False

    for s,fs in follow.items() :
        print('SUIVANT('+s+') = '+str(fs))

#fermeture 

def isnotinensemble(ensemble,itm):
    for thing in ensemble:
        
        if (thing.left==itm.left and thing.leftpoint==itm.leftpoint and thing.rightpoint==itm.rightpoint):
            return False
    return True
        
#répéter tant qu’on ne peut plus ajouter d’item à l’ensemble
#pour tout item X → α • Yβ de l’ensemble avec Y non terminal
#pour toute règle Y → δ
#on ajoute l’item Y → • δ à l’ensemble

def fermeture(ensemble):
    added = True  
    while added:  # Répéter tant qu'on ajoute de nouveaux éléments
        added = False
        new_items = []
        for thing in ensemble:
            if thing.rightpoint and thing.rightpoint[0] in nterm:  # Vérifier si c'est un non-terminal
                Y = thing.rightpoint[0]
                for rule in rules:
                    if rule["left"] == Y:
                        new_item = item(rule["left"], [], rule["right"])
                        if isnotinensemble(ensemble, new_item) and isnotinensemble(new_items, new_item):
                            new_items.append(new_item)
                            added = True  # On a ajouté un nouvel élément, donc on continue la boucle
        if new_items:  
            ensemble.extend(new_items)  # Ajouter les nouveaux éléments en une seule fois
    return ensemble
#


#L = [ fermeture({ S → • E }) ] // ensemble des états
#i = 0
#tant qu’on peut ajouter un état
#   pour tout symbole s (terminal ou non)
#   N = { } // état atteignable par s à partir de L[i]
#   pour tout item X → α • sβ dans L[i]
#       ajouter X → αs • β dans N
#       si N ≠ vide alors
#           N = fermeture(N)
#       si N n'est pas dans L alors
#           on ajoute N dans L
#       on ajoute une transition de L[i] vers N avec le symbole s
#       i ++
#
 


 #probleme de duplication d'états ex {S->E.} et {S->E. , E->E.+T} en passant par E
def build_robot():
    added = True
    L = []  # Liste des états
    ensemble = []
    transitions = []

    # Ajouter les règles initiales pour l'axiome
    for rule in rules:
        if rule["left"] == axiom:
            ensemble.append(item(axiom, [], rule["right"]))

    L.append(fermeture(ensemble))  # Fermeture de l'état initial
    i = 0

    while i < len(L):  # Parcourir les états
        #print("etat",i)
        added = False
        for s in symbols:
            N = []
            #print("pour le symbole",s)


            for itm in L[i]:
                #print("----pour l'item")
                #print("----",itm.left,itm.leftpoint,itm.rightpoint)

                if itm.rightpoint and itm.rightpoint[0] == s:
                    new_item = item(itm.left, itm.leftpoint + [s], itm.rightpoint[1:])  # Éviter pop()
                    if new_item not in N:  # Vérifier si l'élément existe déjà
                        #print("        item : ",new_item.left,"->","".join(new_item.leftpoint),"°","".join(new_item.rightpoint))
                        N.append(new_item)
                    

            if len(N) > 0:
                N = fermeture(N)  # Appliquer la fermeture après avoir rempli N

                if N not in L and N:  # Vérifier si c'est un nouvel état
                           
                    #print("--------ajout de ")
                    #for tst in range(len(N)):print("--------",N[tst].left,N[tst].leftpoint,N[tst].rightpoint)
                    L.append(N.copy())
                    
                    state_index = len(L) - 1
                    added = True
                else:
                    state_index = L.index(N)

                # Ajouter la transition même si l'état existe déjà
                tmpTransition = {'from': i, 'to': state_index, 'symbol': s}
                if tmpTransition not in transitions:
                        #print("         transition",i,"->",state_index,"(",s,")")
                    transitions.append(tmpTransition)
        i += 1
        
    return L, transitions  # Retourner les états et transitions

def constrBranch(transitions,nbState):
    branch=[{} for _ in range(nbState)]
    for trans in transitions: 
        if(trans["symbol"] in nterm):
            branch[trans['from']][trans['symbol']]=trans['to']
    return branch

def constrActions(stateList,transitions):
    retour=True
    nbState=len(stateList)
    actionsTable=[{} for _ in range(nbState)]
    for state in stateList:
        for itm in state:
            stateIndex=stateList.index(state)
            if  itm.rightpoint and (itm.rightpoint[0] not in nterm):#si X → α • aβ est dans i avec a terminal
                for trans in transitions:
                    if trans["from"]==stateIndex:
                        if actionsTable[trans['from']].get(trans['symbol']) :
                            print("")
                            print("concurrence dans la case ",trans["from"],trans["symbol"],"entre",actionsTable[trans['from']].get(trans['symbol']),"et",("D",trans['to']))
                            retour=False
                        if trans['symbol'] not in nterm:
                            actionsTable[trans['from']][trans['symbol']]=("D",trans['to'])
                            #print('ajout de D',trans['to'],' a ',trans['from'] ,trans['symbol'])
            if not itm.rightpoint and itm.left != axiom:
                k=rules.index({"left":itm.left,"right":itm.leftpoint})
                for s in symbols:
                    if s not in nterm:
                        actionsTable[stateIndex][s]=("R",k)
            if itm.left==axiom and not itm.rightpoint:
                actionsTable[stateIndex]['$']="ACC"
            
    for i in range(len(actionsTable)):
        print(i,end="")
        for j in ntermS:
            if(actionsTable[i].get(j,0)):
                print("|",actionsTable[i][j], end="")
            else:
                print("|---------",end="")
        print("")
    
    return actionsTable , retour

def constrActionsSLR(stateList,transitions):
    retour=True
    nbState=len(stateList)
    actionsTable=[{} for _ in range(nbState)]
    for state in stateList:
        for itm in state:
            stateIndex=stateList.index(state)
            if  itm.rightpoint and (itm.rightpoint[0] not in nterm):#si X → α • aβ est dans i avec a terminal
                for trans in transitions:
                    if trans["from"]==stateIndex:
                        if actionsTable[trans['from']].get(trans['symbol']) :
                            if( actionsTable[trans['from']].get(trans['symbol'])!=("D",trans['to'])):
                                retour=False
                                print("")
                                print("concurrence dans la case ",trans["from"],trans["symbol"],"entre",actionsTable[trans['from']].get(trans['symbol']),"et",("D",trans['to']))
                        if trans['symbol'] not in nterm:
                            actionsTable[trans['from']][trans['symbol']]=("D",trans['to'])
                            #print('ajout de D',trans['to'],' a ',trans['from'] ,trans['symbol'])
            if not itm.rightpoint and itm.left != axiom:
                k=rules.index({"left":itm.left,"right":itm.leftpoint})
                for s in follow[itm.left]:
                    if s not in nterm:
                        actionsTable[stateIndex][s]=("R",k)
            if itm.left==axiom and not itm.rightpoint:
                actionsTable[stateIndex]['$']="ACC"
            
    for i in range(len(actionsTable)):
        print(i,end="")
        for j in ntermS:
            if(actionsTable[i].get(j,0)):
                print("|",actionsTable[i][j], end="")
            else:
                print("|---------",end="")
        print("")
    
    return actionsTable , retour

def parsing(mot,actionTable,branchTable,L):
    mot.append("$")
    pile=[0]

    while(1):
        p=pile[0]
        s=mot[0]
        A=actionTable[p].get(s,'crampté')
        print("pile",pile)
        print("symbole",s)
        if A=="ACC":
            acc=True
            break
        if A=='crampté':
            acc=False
            break
        if A[0]=="D":
            print("decalage:",A[1])
            mot.pop(0)
            pile.insert(0,A[1])
        if A[0]=="R":
            print("reduction:",A[1])
            for i in range(0,len(rules[A[1]]["right"])):
                del pile[0]
            p=pile[0]
            print("tete pile:",pile[0])
            print("regle:",rules[A[1]])
            print("ligne no:",p ,branchTable[p])
            pile.insert(0,(branchTable[p][rules[A[1]]['left']]))

    return acc


    

Follow()
print("hello")
transitions={"from":"","to":"","symbol":""}
L,transitions=build_robot()
dot = graphviz.Digraph('automate', comment="L'automate crampté") 
for i in range(len(L)):
    state_labelList=[]
    for rule in L[i]:
        state_labelList.append(''.join(map(str, [rule.left,"->","".join(rule.leftpoint),"¤","".join(rule.rightpoint)]))) # Join elements with commas
    statelabel= "\n".join(map(str,state_labelList))
    dot.node(str(i), statelabel)  # Use the joined string as the label  
for trans in transitions:
    dot.edge(str(trans["from"]),str(trans["to"]),label=trans["symbol"])

dot.render('output_graph', format='png', view=True)

branch=constrBranch(transitions,len(L))

actionsTable, isLR = constrActionsSLR(L,transitions)
if( not isLR): print ("erreur, conflit")

if parsing(word,actionsTable,branch,L):print("mot accepte")
else:print("mot non reconnu")