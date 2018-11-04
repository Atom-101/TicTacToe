import numpy as np

# 0 = empty
# 1 = X
# -1 = O


def play(state,d_flip):
    #s_list = None
    fin = False
    if(is_win(state)):
        print("You won")
        fin = True
    elif(0 not in state):
        fin = True
    else:
        #AI's turn
        #print(1)
        s_list,state = ai_turn(state,d_flip)
        print_board(state,d_flip)
        if(0 not in state):
            return (state,True)
        
        if(is_win(state)):
            print("You lose")
            fin = True
        else:
            #Player's turn
            ip = input('Your turn\n Enter board position where you would like to make your move\n')
            ip = ip.split(',')
            i,j = int(ip[0]),int(ip[1])
            while(True):
                if(i>=state.shape[0] or j>=state.shape[0]):
                    ip = input('Position indices larger than board size\n')
                    ip = ip.split(',')
                    i,j = int(ip[0]),int(ip[1])
                    continue
                if(state[i,j]!=0):
                    ip = input('Trying to make move on non-empty position\n')
                    ip = ip.split(',')
                    i,j = int(ip[0]),int(ip[1])
                    continue
                break
            state[i,j] = -1
    
    
    try:
        return (s_list,state,fin)
    except:
        return (state,fin)
def ai_turn(state,d_flip):
    state_list = expand(state,d_flip,depth=1+d_flip)
    for i in range(len(state_list)):
        if(is_win(state_list[i][0])):
            state_list[i][1] = 5
        else:
            sub_state_list = expand(state_list[i][0],d_flip,depth=2+d_flip)
            state_list[i][1] = get_state_value(sub_state_list,d_flip,depth=2+d_flip)
        #print("State value: "+str(state_list[i][1]))
    
    state_list = sorted(state_list,key=lambda tup:tup[1],reverse=True)
    #print_board(state_list[0][0])
    return state_list,state_list[0][0]

def get_state_value(state_list,d_flip,depth=None):
    if(len(state_list)==1):
        return 0
    
    val = 0
    for i in range(len(state_list)):
        if is_win(state_list[i][0]):
            if(depth%2==1 and  d_flip==0 or depth%2==0 and  d_flip==1):
                state_list[i][1] = -5
            else:
                state_list[i][1] = 2        
        else:
            sub_state_list = expand(state_list[i][0],d_flip,depth=depth+d_flip)
            state_list[i][1] = get_state_value(sub_state_list,d_flip,depth=depth+1+d_flip)

        val+=state_list[i][1]

    return val    


def expand(state,d_flip,depth = None):
    sub_state_list = []
    ip = -1 if depth%2==0 else 1
    if(d_flip==1):
        ip = -ip

    for i in range(state.shape[0]):
        for j in range(state.shape[1]):
            sub_state = state.copy()
            if(state[i,j] == 0): 
                sub_state[i,j] = ip
                sub_state_list.append([sub_state,0])   
    
    return sub_state_list

def is_win(state):
    for i in range(state.shape[0]):
        for j in range(state.shape[1]):
            if(state[i,j] != 0):
                #Horizontal
                if(j!=0 and j!=state.shape[1]-1):
                    if(state[i,j] == state[i,j-1] and state[i,j] == state[i,j+1]):
                        return True
                #Vertical
                if(i!=0 and i!=state.shape[0]-1):
                    if(state[i,j] == state[i-1,j] and state[i,j] == state[i+1,j]):
                        return True
                
                #Diagonal main
                if(i!=0 and j!=0 and i!=state.shape[0]-1 and j!=state.shape[1]-1):
                    if(state[i,j] == state[i-1,j-1] and state[i,j] == state[i+1,j+1]):
                        return True
                
                #Diagonal alt
                if(i!=0 and j!=0 and i!=state.shape[0]-1 and j!=state.shape[1]-1):
                    if(state[i,j] == state[i-1,j+1] and state[i,j] == state[i+1,j-1]):
                        return True
    return False


def print_board(state,d_flip):
    for i in range(state.shape[0]):
        for j in range(state.shape[1]):
            if(d_flip==0):
                print('O' if state[i,j]==-1 else 'X' if state[i,j]==1 else '-',end='\t')
            else:
                print('X' if state[i,j]==-1 else 'O' if state[i,j]==1 else '-',end='\t')
        print()

if __name__ == '__main__':
    board = np.zeros((3,3))
    S = []
    d_flip=0
    i = input('Do you want to go first?\n')
    if('Y' in i or 'y' in i):
        ip = input('Your turn\n Enter board position where you would like to make your move\n')
        ip = ip.split(',')
        i,j = int(ip[0]),int(ip[1])
        while(True):
            if(i>=board.shape[0] or j>=board.shape[0]):
                ip = input('Position indices larger than board size\n')
                ip = ip.split(',')
                i,j = int(ip[0]),int(ip[1])
                continue
            if(board[i,j]!=0):
                ip = input('Trying to make move on non-empty position\n')
                ip = ip.split(',')
                i,j = int(ip[0]),int(ip[1])
                continue
            break
        board[i,j] = -1
        d_flip=1
        
    while(True):
        try:
            s_list,board,fin = play(board,d_flip)
            S.append(s_list)
        except:
            board,fin = play(board,d_flip)
        if(fin):
            #print('Won')
            break
    
