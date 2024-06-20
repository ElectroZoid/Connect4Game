import numpy as np
import copy

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.depth_limit=5                                                  # depth limit for alpha-beta-move
        self.depth_limit_st=4                                               # depth limit for expectimax-move

    def get_alpha_beta_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the alpha-beta pruning algorithm

        This will play against either itself or a human player

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """

        if self.player_number==1:
            value,move=self.max_value(board,0,None,None)
            return move
        elif self.player_number==2:
            value,move=self.min_value(board,0,None,None)
            return move

        raise NotImplementedError('Whoops I don\'t know what to do')

        

    def get_expectimax_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the expectimax algorithm.

        This will play against the random player, who chooses any valid move
        with equal probability

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        if self.player_number==1:
            value,move=self.max_value_stochastic(board,0)
            return move
        elif self.player_number==2:
            value,move=self.min_value_stochastic(board,0)
            return move
        
        raise NotImplementedError('Whoops I don\'t know what to do')




    def evaluation_function(self, board):
        """
        Given the current stat of the board, return the scalar value that 
        represents the evaluation function for the current player
       
        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The utility value for the current board
        """
        c14 = 0
        c24 = 0
        c13 = 0
        c23 = 0
        c12 = 0
        c22 = 0
        c11 = 0
        c21 = 0
        for row in range(6):
            row_ = ''.join(map(str, board[row]))

            c14 += row_.count("1111")
            c13 += row_.count("111")
            c12 += row_.count("11")
            c11 += row_.count("1")

            c24 += row_.count("2222")
            c23 += row_.count("222")
            c22 += row_.count("22")
            c21 += row_.count("2")

        for col in range(7):
            col_ = ''.join(map(str, board[:, col]))

            c14 += col_.count("1111")
            c13 += col_.count("111")
            c12 += col_.count("11")
            c11 += col_.count("1")

            c24 += col_.count("2222")
            c23 += col_.count("222")
            c22 += col_.count("22")
            c21 += col_.count("2")

        for offset_ in range(-2, 4):
            diagonal = ''.join(map(str, np.diagonal(board, offset=offset_)))

            c14 += diagonal.count("1111")
            c13 += diagonal.count("111")
            c12 += diagonal.count("11")
            c11 += diagonal.count("1")

            c24 += diagonal.count("2222")
            c23 += diagonal.count("222")
            c22 += diagonal.count("22")
            c21 += diagonal.count("2")

        for offset_ in range(-2, 4):
            diagonal = ''.join(map(str, np.diagonal(np.rot90(board), offset=offset_)))

            c14 += diagonal.count("1111")
            c13 += diagonal.count("111")
            c12 += diagonal.count("11")
            c11 += diagonal.count("1")

            c24 += diagonal.count("2222")
            c23 += diagonal.count("222")
            c22 += diagonal.count("22")
            c21 += diagonal.count("2")


        utility = c11 + 20*c12 + 400*c13 + 8000*c14 - (20*(c21 + 20*c22 + 400*c23 + 8000*c24))
        return utility
    
    
    def max_value(self,board,depth,a,b):

        if self.depth_limit==depth:
            return self.evaluation_function(board),None
        
        v,move=None,None

        actions=[]
        for i in range(7):
            if board[5][i]==0:
                temp=copy.copy(board)
                temp[5][i]=1
                actions.append([temp,i])
            elif board[0][i]!=0:
                pass
            else:
                loc=None
                for j in range(6):
                    if board[j][i]==0:
                        loc=j
                temp=copy.copy(board)
                temp[loc][i]=1
                actions.append([temp,i])
        
        for i in range(len(actions)):
            v1,a1=self.min_value(actions[i][0],depth+1,a,b)
            if v==None:
                v,move=v1,actions[i][1]
                a=v
            elif v1>v:
                    v,move=v1,actions[i][1]
                    a=max(a,v)
            if b!=None:
                if v>=b:
                    return v,move

        return v,move



    def min_value(self,board,depth,a,b):

        if self.depth_limit==depth:
            return self.evaluation_function(board),None
        
        v,move=None,None

        actions=[]
        for i in range(7):
            if board[5][i]==0:
                temp=copy.copy(board)
                temp[5][i]=2
                actions.append([temp,i])
            elif board[0][i]!=0:
                pass
            else:
                loc=None
                for j in range(6):
                    if board[j][i]==0:
                        loc=j
                temp=copy.copy(board)
                temp[loc][i]=2
                actions.append([temp,i])
        
        for i in range(len(actions)):
            v1,a1=self.max_value(actions[i][0],depth+1,a,b)
            if v==None:
                v,move=v1,actions[i][1]
                b=v
            elif v1<v:
                    v,move=v1,actions[i][1]
                    b=min(b,v)
            if a!=None:
                if v<=a:
                    return v,move
            
        return v,move
    
    def max_value_stochastic(self,board,depth):

        if self.depth_limit_st==depth:
            return self.evaluation_function(board),None
        
        v,move=None,None

        actions=[]
        for i in range(7):
            if board[5][i]==0:
                temp=copy.copy(board)
                temp[5][i]=1
                actions.append([temp,i])
            elif board[0][i]!=0:
                pass
            else:
                loc=None
                for j in range(6):
                    if board[j][i]==0:
                        loc=j
                temp=copy.copy(board)
                temp[loc][i]=1
                actions.append([temp,i])

        if depth==0:
            for i in range(len(actions)):
                v1,a1=self.min_value_stochastic(actions[i][0],depth+1)
                if v==None:
                    v,move=v1,actions[i][1]
                elif v1>v:
                        v,move=v1,actions[i][1]
        else:
            for i in range(len(actions)):
                v1,a1=self.min_value_stochastic(actions[i][0],depth+1)

                if v==None:
                    v,move=(v1/len(actions)),actions[i][1]
                else:
                    v=v+(v1/len(actions))

        return v,move

    
    def min_value_stochastic(self,board,depth):

        if self.depth_limit_st==depth:
            return self.evaluation_function(board),None
        
        v,move=None,None

        actions=[]
        for i in range(7):
            if board[5][i]==0:
                temp=copy.copy(board)
                temp[5][i]=2
                actions.append([temp,i])
            elif board[0][i]!=0:
                pass
            else:
                loc=None
                for j in range(6):
                    if board[j][i]==0:
                        loc=j
                temp=copy.copy(board)
                temp[loc][i]=2
                actions.append([temp,i])

        if depth==0:
            for i in range(len(actions)):
                v1,a1=self.max_value_stochastic(actions[i][0],depth+1)
                if v==None:
                    v,move=v1,actions[i][1]
                elif v1<v:
                        v,move=v1,actions[i][1]
        else: 
            for i in range(len(actions)):
                v1,a1=self.max_value_stochastic(actions[i][0],depth+1)

                if v==None:
                    v,move=(v1/len(actions)),actions[i][1]
                else:
                    v=v+(v1/len(actions))

        return v,move
               

class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state select a random column from the available
        valid moves.

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        return np.random.choice(valid_cols)


class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state returns the human input for next move

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """

        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move

