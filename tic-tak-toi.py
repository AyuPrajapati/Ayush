import math,random,sys

def print_board(b):
    print()
    for i in range(3):
        row=[]
        for j in range(3):
            k=3*i+j
            row.append(b[k] if b[k]!=" " else str(k+1))
        print(" "+ " | ".join(row))
        if i<2: print("---+---+---")
    print()

def lines():
    return [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

def winner(b):
    for a,c,d in lines():
        if b[a]!=" " and b[a]==b[c]==b[d]:
            return b[a]
    return None

def full(b):
    return all(x!=" " for x in b)

def eval_board(b,ai,hu):
    w=winner(b)
    if w==ai: return 1
    if w==hu: return -1
    return 0

def moves(b):
    return [i for i,x in enumerate(b) if x==" "]

def minimax(b,depth,alpha,beta,maxim,ai,hu):
    e=eval_board(b,ai,hu)
    if e!=0 or full(b): return e, None
    if maxim:
        best=(-math.inf,None)
        for m in moves(b):
            b[m]=ai
            v,_=minimax(b,depth+1,alpha,beta,False,ai,hu)
            b[m]=" "
            if v>best[0]: best=(v,m)
            alpha=max(alpha,v)
            if beta<=alpha: break
        return best
    else:
        best=(math.inf,None)
        for m in moves(b):
            b[m]=hu
            v,_=minimax(b,depth+1,alpha,beta,True,ai,hu)
            b[m]=" "
            if v<best[0]: best=(v,m)
            beta=min(beta,v)
            if beta<=alpha: break
        return best

def best_move(b,ai,hu):
    if b.count(" ")==9:
        return random.choice([0,2,4,6,8])
    _,m=minimax(b,0,-math.inf,math.inf,True,ai,hu)
    return m

def turn_input(b):
    while True:
        s=input("Choose a cell (1-9): ").strip()
        if s.lower() in ("q","quit","exit"): sys.exit()
        if not s.isdigit(): print("Invalid."); continue
        i=int(s)-1
        if i<0 or i>8: print("Invalid."); continue
        if b[i]!=" ": print("Taken."); continue
        return i

def main():
    print("Tic-Tac-Toe — unbeatable AI")
    human=""
    while human not in ("X","O"):
        human=input("Choose X or O: ").strip().upper()
    ai="O" if human=="X" else "X"
    playfirst=""
    while playfirst not in ("Y","N"):
        playfirst=input("Go first? (Y/N): ").strip().upper()
    while True:
        b=[" "]*9
        turn="H" if playfirst=="Y" else "A"
        while True:
            print_board(b)
            w=winner(b)
            if w or full(b):
                if w: print(("You win!" if w==human else "AI wins!"))
                else: print("Draw.")
                break
            if turn=="H":
                i=turn_input(b)
                b[i]=human
                turn="A"
            else:
                i=best_move(b,ai,human)
                b[i]=ai
                print(f"AI chooses {i+1}")
                turn="H"
        again=""
        while again not in ("Y","N"):
            again=input("Play again? (Y/N): ").strip().upper()
        if again=="N": break
        print()

if __name__=="__main__":
    main()
