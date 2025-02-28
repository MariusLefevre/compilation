from item import item
import graphviz

axiom = 'E'
nterm = ['E','T','F']
empty = '\u03b5' # mot vide
rules = [
{'left':'E','right':['E','+','T']},
 {'left':'E','right':['T']},
 {'left':'T','right':['T','*','F']},
 {'left':'T','right':['F']},
 {'left':'F','right':['(','E',')']},
 {'left':'F','right':['0']},
 {'left':'F','right':['9']}
]
symbols = ['E','T','F','+','*','(',')','0','9','$']
word = ['2'+'(','3','+','1',')'] # mot à parser

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
            #print("    symbole:",s)
            N = []
            for itm in L[i]:
                if itm.rightpoint and itm.rightpoint[0] == s:
                    new_item = item(itm.left, itm.leftpoint + [s], itm.rightpoint[1:])  # Éviter pop()
                    if isnotinensemble(N, new_item):  # Vérifier si l'élément existe déjà
                        #print("        item : ",new_item.left,"->","".join(new_item.leftpoint),"°","".join(new_item.rightpoint))
                        N.append(new_item)

                    if len(N) > 0:
                        N = fermeture(N)  # Appliquer la fermeture après avoir rempli N

                        if N not in L and N:  # Vérifier si c'est un nouvel état
                            L.append(N)
                            #for j in range(len(N)):
                                #print("             item : ",N[j].left,"->","".join(N[j].leftpoint),"°","".join(N[j].rightpoint))
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
                        if actionsTable[trans['from']].get(trans['symbol']):
                            retour=False
                        actionsTable[trans['from']][trans['symbol']]=("D",trans['to'])
            if not itm.rightpoint and itm.left != axiom:
                k=rules.index({"left":itm.left,"right":itm.leftpoint})
                for s in symbols:
                    if s not in nterm:
                        actionsTable[stateIndex][s]=("R",k)
    for i in actionsTable:
        print(i)
    
    return actionsTable , retour

        
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

actionsTable, isLR = constrActions(L,transitions)
if( not isLR): print ("erreur, conflit")