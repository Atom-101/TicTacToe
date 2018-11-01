import numpy as np

# 0 = empty
# 1 = X
# -1 = O


def play(state):
    #s_list = None
    won = False
    if(is_win(state)):
        print("You won")
        won = True
    else:
        #AI's turn
        #print(1)
        s_list,state = ai_turn(state)
        print_board(state)
        if(0 not in state):
            return (state,True)
        
        if(is_win(state)):
            print("You lose")
            won = True
        else:
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
        return (s_list,state,won)
    except:
        return (state,won)
def ai_turn(state):
    state_list = expand(state,depth=1)
    for i in range(len(state_list)):
        if(is_win(state_list[i][0])):
            state_list[i][1] = 5
        else:
            sub_state_list = expand(state_list[i][0],depth=2)
            state_list[i][1] = get_state_value(sub_state_list,depth=2)
        #print("State value: "+str(state_list[i][1]))
    
    state_list = sorted(state_list,key=lambda tup:tup[1],reverse=True)
    #print_board(state_list[0][0])
    return state_list,state_list[0][0]

def get_state_value(state_list,depth=None):
    if(len(state_list)==1):
        return 0
    
    val = 0
    for i in range(len(state_list)):
        if is_win(state_list[i][0]):
            if(depth%2==1):
                state_list[i][1] = -5
            else:
                state_list[i][1] = 1        
        else:
            sub_state_list = expand(state_list[i][0],depth=depth)
            state_list[i][1] = 0.5*get_state_value(sub_state_list,depth=depth+1)

        val+=state_list[i][1]

    return val    


def expand(state,depth = None):
    sub_state_list = []
    ip = -1 if depth%2==0 else 1

    for i in range(state.shape[0]):
        for j in range(state.shape[0]):
            sub_state = state.copy()
            if(state[i,j] == 0): 
                sub_state[i,j] = ip
                sub_state_list.append([sub_state,0])   
    
    return sub_state_list

def is_win(state):
    for i in range(state.shape[0]):
        for j in range(state.shape[0]):
            if(state[i,j] != 0):
                #Horizontal
                if(j!=0 and j!=state.shape[0]-1):
                    if(state[i,j] == state[i,j-1] and state[i,j] == state[i,j+1]):
                        return True
                #Vertical
                if(i!=0 and i!=state.shape[0]-1):
                    if(state[i,j] == state[i-1,j] and state[i,j] == state[i+1,j]):
                        return True
                
                #Diagonal main
                if(i!=0 and j!=0 and i!=state.shape[0]-1 and j!=state.shape[0]-1):
                    if(state[i,j] == state[i-1,j-1] and state[i,j] == state[i+1,j+1]):
                        return True
                
                #Diagonal alt
                if(i!=0 and j!=0 and i!=state.shape[0]-1 and j!=state.shape[0]-1):
                    if(state[i,j] == state[i-1,j+1] and state[i,j] == state[i+1,j-1]):
                        return True
    return False


def print_board(state):
    for i in range(state.shape[0]):
        for j in range(state.shape[0]):
            print('O' if state[i,j]==-1 else 'X' if state[i,j]==1 else '-',end='\t')
        print()

if __name__ == '__main__':
    board = np.zeros((3,3))
    S = []
    while(True):
        try:
            s_list,board,win = play(board)
            S.append(s_list)
        except:
            board,win = play(board)
        if(win):
            #print('Won')
            break
    
