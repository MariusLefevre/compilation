class item():
    left=""
    leftpoint=[]
    rightpoint=[]
    def __init__(self,left,leftpoint,rightpoint):
        self.left=left
        self.leftpoint=leftpoint
        self.rightpoint=rightpoint
    
    def __eq__(self,other):
        return (self.left == other.left and 
                self.leftpoint == other.leftpoint and 
                self.rightpoint == other.rightpoint)

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
