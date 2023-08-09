import numpy as np
import pandas as pd
import random as rn

class Dice:
    '''
    This is a Dice object.
    '''

    df  = pd.DataFrame({"faces":[],
                        "weights":[]}).set_index("faces")
    
    def __init__(self, n, w=1):
        '''
        This is a initializer for the Dice object. It takes a numpy array with the faces 
        of the die (n) and the weight for each face (w) and performs methods onto 
        the given array.
        
        INPUT:
        n    numpy array of int or str
        w    int or numpy array, default 1
        
        OUTPUT:
        NONE
        
        Result:
        Saves your faces and weights as a private dataframe.
        '''
        
        if not isinstance(n, np.ndarray):
            raise TypeError("Hey, you need to use an numpy.array!")
        if len(set(n)) != len(n):
            raise ValueError("Hey, you've got some repeats in your array!")
        self.df  = pd.DataFrame({"faces":n,
                       "weights":w}).set_index("faces")
        
    def change_weight(self, face, weight):
        '''
        This is a change weight method. It takes a number representing the face of the die that
        you want to change the weight of (face) and finds the face in the private dataframe. It 
        updates the dataframe with the new weight for the given face.
        
        INPUT:
        face      int, str
        weight    int, float
        
        OUTPUT:
        NONE
        
        Result:
        Updates and saves your changes to the dataframe.
        '''
        
        if face not in self.df.index:
            raise IndexError("Hey, this face value is not in the current record of faces!")
        if not isinstance(float(weight), float):
            raise TypeError("Hey, your weight value is not a number!")
        self.df.loc[face] = weight
        
    def rolldie(self, r=1):
        '''
        This is a roll die method. It takes a number representing the number of times you 
        want to roll a die and outputs all the outcomes for each roll in one list.
        
        INPUT:
        r          int
        
        OUTPUT:
        myrolls    list
        
        Result:
        NONE
        '''        
        
        myrolls = rn.choices(self.df.index, weights=self.df.weights, k=r)
        return myrolls
    
    def currentdie(self):
        '''
        This is a current die method. This allows you to check the current state of the given 
        die faces and weights.
        
        INPUT:
        NONE
        
        OUTPUT:
        df    dataframe
        
        Result:
        NONE
        '''
        
        return self.df
    
class Game:
    '''
    This is a Game object.
    '''
    
    mylist = []
    df_rolls = pd.DataFrame({"Roll Number":[],
                           "Dice Number":[]}).set_index("Roll Number")
    
    def __init__(self, mylist):
        '''
        This is an initilzer for the Game object. It takes a list of Dice objects and 
        performs methods on the given list.
        
        INPUT:
        mylist    list
        
        OUTPUT:
        NONE
        
        Result:
        Saves your list.
        '''
        
        face1 = set(mylist[0].df.index)
        for each_obj in mylist:
            if not isinstance(each_obj, Dice):
                raise TypeError("Hey, one or more of your inputs is not a Dice object!")
            if not face1 == set(each_obj.df.index):
                raise ValueError("Hey, your inputs need to all have the same faces!")
        self.mylist = mylist
    
    def play(self, n):
        '''
        This is a play method for the Game object. It takes a list of Dice object and rolls
        all dice a given number of times and saves the results in a dataframe with a wide
        format.
        
        INPUT:
        n    int
        
        OUTPUT:
        NONE
        
        Result:
        Saves a dataframe with the results in wide format.
        '''
        
        roll_results = sum([x.rolldie(n) for x in self.mylist], [])
        die_num = np.repeat(np.arange(1,len(self.mylist)+1),n)
        roll_num = np.tile(np.arange(1,n+1), len(self.mylist))
        
        df_rolls = pd.DataFrame({"Roll Number": roll_num, "Dice Number": die_num, "y": roll_results}, 
                        index=roll_num)
        self.df_rolls = df_rolls.pivot(index="Roll Number", columns="Dice Number", values="y")
        
    def recent_play(self, narrow=False):
        '''
        This is a recent play method for the Game object. It returns the most recent results 
        from the play method in either wide format (default) or long format.
        
        INPUT:
        **narrow    bool
        
        OUTPUT:
        df_rolls    dataframe
        
        Result:
        **optional argument
        '''
        
        if not isinstance(narrow, bool):
            raise ValueError("Hey, this method takes 0 or 1 arguements. If 1 arguement, \
            it must be a boolean value!")
        if narrow==False:
            return self.df_rolls
        else:
            return pd.melt(self.df_rolls, value_name="Roll Results", ignore_index=False)\
        .set_index([pd.melt(self.df_rolls, value_name="Roll Results", ignore_index=False).index, "Dice Number"])
    
class Analyzer:
    '''
    This is an Analyzer object.
    '''
    
    mygame = pd.DataFrame()
    
    def __init__(self, mygame):
        '''
        This is an initilzer for the Analyzer object. It takes a Game object's dataframe
        and performs methods on the given Game object dataframe.
        
        INPUT:
        mygame    dataframe
        
        OUTPUT:
        NONE
        
        Result:
        Saves your dataframe.
        '''
        
        if not isinstance(mygame, Game):
                raise ValueError("Hey, your input is not a Game object!")
        self.mygame = mygame.df_rolls
        
    def jackpot(self):
        '''
        This is a jackpot method for the Analyzer object. It returns the number of 
        times a Game object has hit a jackpot. 
        
        INPUT:
        NONE
        
        OUTPUT:
        jackpot_results    int
        
        Result:
        NONE
        '''
        
        jackpot_results = self.mygame.iloc[np.where\
        (self.mygame.eq(self.mygame.iloc[:, 0], axis=0).all(1))]
        return len(jackpot_results)
    
    def face_counts(self):
        '''
        This is a face counts method for the Analyzer object. Computes how many times a 
        given face is rolled in the Game object and returns a data frame of results. 
        
        INPUT:
        NONE
        
        OUTPUT:
        new_df    dataframe
        
        Result:
        NONE
        '''
        
        new_df = self.mygame.apply(pd.Series.value_counts, axis=1).fillna(0)
        new_df = new_df.rename_axis("Face Number", axis="columns")
        return new_df
    
    def combo_count(self):
        '''
        This is a combination count method for the Analyzer object. Calculates the distinct number 
        of combinations of faces rolled. Returns a data frame of results.
        
        INPUT:
        NONE
        
        OUTPUT:
        df    dataframe
        
        Result:
        NONE
        '''
        
        return pd.DataFrame(np.sort(self.mygame.values, axis=1), columns=self.mygame.columns) \
        .value_counts().to_frame(name="Combo Count")
    
    def perm_count(self):
        '''
        This is a permutation count method for the Analyzer object. Calculates the distinct 
        number of permutations of faces rolled and returns a data frame of results.
        
        INPUT:
        NONE
        
        OUTPUT:
        perm_df    dataframe
        
        Result:
        NONE
        '''
        
        perm_df = self.mygame.value_counts().to_frame(name="Permutation Count")
        return perm_df
    