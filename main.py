from item import item

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
symbols = ['E','T','F','+','*','(',')','0','9']
word = ['2'+'(','3','+','1',')'] # mot à parser

#fermeture 

def isnotinensemble(ensemble,itm):
    for thing in ensemble:
        
        if (thing.left==itm.left and thing.leftpoint==itm.leftpoint and thing.rightpoint==itm.rightpoint):
            return 0
    return 1
        
#répéter tant qu’on ne peut plus ajouter d’item à l’ensemble
#pour tout item X → α • Yβ de l’ensemble avec Y non terminal
#pour toute règle Y → δ
#on ajoute l’item Y → • δ à l’ensemble

def fermeture(ensemble):
    added = True  # Flag to track changes
    while added:  # Keep running until no new items are added
        added = False
        new_items = []
        for thing in ensemble:
            if thing.rightpoint and thing.rightpoint[0] in nterm:
                Y = thing.rightpoint[0]
                for rule in rules:
                    if rule["left"] == Y:
                        new_item = item(rule["left"], [], rule["right"])
                        if isnotinensemble(ensemble + new_items, new_item):
                            new_items.append(new_item)
                            added = True 
        ensemble.extend(new_items) 
    return ensemble
     
     
     
#
#────────────▄▀░░░░░▒▒▒█─ 
# ───────────█░░░░░░▒▒▒█▒█ 
# ──────────█░░░░░░▒▒▒█▒░█ 
# ────────▄▀░░░░░░▒▒▒▄▓░░█ 
# ───────█░░░░░░▒▒▒▒▄▓▒░▒▓ 
# ──────█▄▀▀▀▄▄▒▒▒▒▓▀▒░░▒▓ 
# ────▄▀░░░░░░▒▀▄▒▓▀▒░░░▒▓ 
# ───█░░░░░░░░░▒▒▓▀▒░░░░▒▓ 
# ───█░░░█░░░░▒▒▓█▒▒░░░▒▒▓ 
# ────█░░▀█░░▒▒▒█▒█░░░░▒▓▀ 
# ─────▀▄▄▀▀▀▄▄▀░█░░░░▒▒▓─ 
# ───────────█▒░░█░░░▒▒▓▀─ 
# ────────────█▒░░█▒▒▒▒▓── 
# ─────────────▀▄▄▄▀(


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
    L = []  # List of states
    ensemble = []
    transitions=[]
    

    # Add initial rules for the axiom
    for rule in rules:
        if rule["left"] == axiom:
            ensemble.append(item(axiom, [], rule["right"]))

    L.append(fermeture(ensemble))  # Compute closure of initial set
    i = 0

    while added and i < len(L):  # Process each state in L
        added = False
        for s in symbols:
            N = []
            for itm in L[i]:
                if itm.rightpoint and itm.rightpoint[0] == s:
                    new_item = item(itm.left, itm.leftpoint + [s], itm.rightpoint[1:])  # Avoid pop()
                    if isnotinensemble(N, new_item):
                        N.append(new_item)

                    if len(N) > 0:
                        N = fermeture(N)  # Compute closure of new state
                    if N not in L:  # Avoid duplicates
                        L.append(N)
                        state_index = len(L) - 1
                    else:
                        state_index = L.index(N)
                    added = True  # Signal that a new state was added
                    tmpTransition = [{'from':i,'to':state_index,'symbol':s}]
                    if( tmpTransition not in transitions):
                        transitions.append(tmpTransition)
        i+=1

    # Print final states
    for state in L:
        for itm in state:
            print(itm.left, itm.leftpoint, itm.rightpoint)
        print("")
    for trans in transitions:
        print(trans)

print("hello")
build_robot()
    