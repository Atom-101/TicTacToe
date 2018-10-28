#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <limits.h>
//#include "Stack.h"


char** initializeBoard(char**, int);
int play(char***, int);
int is_win(char**, int);
int empty_cells(char**, int);
char** ai_turn(char**, int);
struct STATE_STRUCT* expand(char**, int, int, int); 
void free_board(char**,int);
void print_board(char**, int);
float get_state_value(struct STATE_STRUCT*, int, int, int);

typedef struct STATE_STRUCT
{
    char **board;
    float value;
    // denotes depth of state
    //int num_empty;
}STATE;

float GREEDINESS = 0.9f;

int main(int argc, char *argv[])
{
    int size = atoi(argv[1]);//string to int
    char **current_board;
    current_board = initializeBoard(current_board,size);

    while(empty_cells(current_board,size)>0)
    {
        int i = play(&current_board,size);
        if(i != 0)
            return 0;
    }

    printf("It's a draw\n");
    return 0;   
}

char** initializeBoard(char** board, int size)
{
    board = (char**)malloc(size * sizeof(char*)); 
    for (int i=0; i<size; i++)
    {
        board[i] = (char *)malloc(size * sizeof(char));
        for(int j=0;j<size;j++)
            board[i][j] = '-';
    }
    return board;
}

int play(char*** board, int size)
{
    if(is_win(*board,size))
    {
        printf("You won\n");
        return -1;
    }    
    else
    {
        //AI's turn
        *board = ai_turn(*board,size);
        if(is_win(*board,size))
        {
            printf("You lose\n");
            return 1;
        }
        
        print_board(*board,size); 
        // Player's turn
        printf("Your turn\n Enter board position where you would like to make your move\n");
        int i,j;
        while(1)
        {
            scanf("%d,%d",&i,&j);
            if(i>=size || j>=size)
            {
                printf("Position indices larger than board size\n");
                continue;
            }
            if((*board)[i][j] != '-')
            {
                printf("Trying to make move on non-empty position\n");
                continue;
            }
            (*board)[i][j] = 'O';
            break;
        }
               
    return 0;
    }

}


char** ai_turn(char** board, int size)
{
    int len = empty_cells(board,size);
    STATE current;
    current.board = board;
    current.value = 0;
    
    STATE *arr = expand(board,size,len,1);

    for(int i = 0;i<len;i++)
    {
        if(is_win(arr[i].board,size)==1)
        {    
            arr[i].value = 100;
        }
        else
        {
            STATE *a  = expand(arr[i].board,size,len,2);
            arr[i].value = get_state_value(a,size,len-1,2);  
        }
    }
    //Sort state(s) by value
    for (int i=0;i<len-1;i++)
    {
        int max=i;
        for (int j=i+1;j<len;j++)
        {
            if(arr[j].value>arr[max].value)
                max = j;
        }
        STATE temp = arr[i];
        arr[i] = arr[max];
        arr[max] = temp;

        return arr[max].board;
    }
    //return arr[0].board;
}

float get_state_value(STATE* s, int size, int len, int depth)
{
    //Base case
    if(len == 0)
    {    
        free_board(s[0].board,size);
        return 0;
    }

    //Assignment loop
    for(int i = 0;i<len;i++)
    {
        if(is_win(s[i].board,size)==1)
        {    
            if(depth%2==0)
                s[i].value = -5;
            else
                s[i].value = 5;
        }
        else
        {
            STATE *a  = expand(s[i].board,size,len,depth);
            s[i].value = /*GREEDINESS**/get_state_value(a,size,len-1,depth+1);  
        }
    }

    float sum = 0;
    //Value calculation loop
    for(int i = 0;i<len;i++)
    {
        sum+=s[i].value;
        free_board(s[i].board,size);
    }
    return sum;
}

void free_board(char** board, int size)
{
    for(int i = 0; i< size; i++)
       free(board[i]);
       
    free(board);
}

int is_win(char** board, int size)
{
    for( int i=0;i<size;i++)
        for(int j=0;j<size;j++)
        {
            if(board[i][j]!='-')
            {
                //Horizontal
                if(j!=0 && j!=size-1)
                {
                    if(board[i][j] == board[i][j-1] && board[i][j] == board[i][j+1])
                        return 1;
                }

                //Vertical
                if(i!=0 && i!=size-1)
                {
                    if(board[i][j] == board[i-1][j] && board[i][j] == board[i+1][j])
                        return 1;
                }

                //Diagonal main
                if(i!=0 && j!=0 && i!=size-1 && j!=size-1)
                {
                    if(board[i][j] == board[i-1][j-1] && board[i][j] == board[i+1][j+1])
                        return 1;
                }

                //Diagonal alt
                if(i!=0 && j!=0 && i!=size-1 && j!=size-1)
                {
                    if(board[i][j] == board[i-1][j+1] && board[i][j] == board[i+1][j-1])
                        return 1;
                }
            }
        }

    return 0;
}

int empty_cells(char** board, int size)
{
    int count = 0;
    for(int i=0;i<size;i++)
        for(int j=0;j<size;j++)
            if(board[i][j] == '-')
                count++;
    return count;
}

STATE* expand(char** board, int size, int len, int depth)
{
    STATE* arr = (STATE*)malloc(len * sizeof(STATE));
    
    //Initialize state array
    for(int i=0;i<len;i++)
    {
        arr[i].board = initializeBoard(arr[i].board,size);
        arr[i].value = 0;
    }

    //Copy given state to all array elements
    for(int i=0;i<len;i++)
        for(int j=0;j<size;j++)
            for(int k=0;k<size;k++)
                arr[i].board[j][k] = board[j][k];

    //Populate next state
    char input = depth%2 == 0?'O':'X';
    //for(int i=0;i<len;i++)
    int i = 0;
    for(int j=0;j<size;j++)
    {
        int flag = 0;
        for(int k=0;k<size;k++)
        {
            if(arr[i].board[j][k]=='-')
            {
                arr[i].board[j][k] = input;
                //flag = 1;
                i++;
                if(i == len)
                {    
                    break;
                    flag = 1;
                }
                //break;
            }
        }
        if(flag==1)
            break;         
    }
    //printf("%d",empty_cells(arr[len-1].board,size));
    return arr;
}

void print_board(char** board,int size)
{
    for(int i=0;i<size;i++)
    {
        for(int j=0;j<size;j++)
            printf("%c\t",board[i][j]);
        printf("\n");
    }
}