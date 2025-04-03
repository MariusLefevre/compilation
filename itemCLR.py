class itemCLR():
    left=""
    leftpoint=[]
    rightpoint=[]
    lookahead=""
    def __init__(self,left,leftpoint,rightpoint,lookahead):
        self.left=left
        self.leftpoint=leftpoint
        self.rightpoint=rightpoint
        self.lookahead=lookahead
    
    def __eq__(self,other):
        return (self.left == other.left and 
                self.leftpoint == other.leftpoint and 
                self.rightpoint == other.rightpoint and self.lookahead == other.lookahead)
