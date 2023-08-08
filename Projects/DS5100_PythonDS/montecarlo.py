class Dice:
    '''
    This is a Dice object.
    '''

    df  = pd.DataFrame({"faces":[],
                        "weights":[]}).set_index("faces")
    
    def __init__(self, n, w=1):
        '''
        This is a initializer method. It takes a numpy array with the faces of the die (n)
        and the weight for each face (w) and performs some methods onto the given array with
        other methods.
        
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
        This is a change weight method. It takes a the number representing the face of the die that
        you want to change the weight of (face) and finds the face in the private dataframe. It 
        updates the dataframe with the new weight for the given face.
        
        INPUT:
        face      int, str
        weight    int, float
        
        OUTPUT:
        NONE
        
        Result:
        Saves your changes to the dataframe.
        '''
        
        if face not in self.df.index:
            raise IndexError("Hey, this face value is not in the current record of faces!")
        if not isinstance(float(weight), float):
            raise TypeError("Hey, your weight value is not a number!")
        self.df.loc[face] = weight
        
    def rolldie(self, r=1):
        myrolls = rn.choices(self.df.index, weights=self.df.weights, k=r)
        return myrolls
    
    def currentdie(self):
        return self.df
    
class Game:
    mylist = []
    df_rolls = pd.DataFrame({"Roll Number":[],
                           "Dice Number":[]}).set_index("Roll Number")
    
    def __init__(self, mylist):
        face1 = set(mylist[0].df.index)
        for each_obj in mylist:
            if not isinstance(each_obj, Dice):
                raise TypeError("Hey, one or more of your inputs is not a Dice object!")
            if not face1 == set(each_obj.df.index):
                raise ValueError("Hey, your inputs need to all have the same faces!")
        self.mylist = mylist
    
    def play(self, n):
        roll_results = sum([x.rolldie(n) for x in self.mylist], [])
        die_num = np.repeat(np.arange(1,len(self.mylist)+1),n)
        roll_num = np.tile(np.arange(1,n+1), len(self.mylist))
        
        df_rolls = pd.DataFrame({"Roll Number": roll_num, "Dice Number": die_num, "y": roll_results}, 
                        index=roll_num)
        self.df_rolls = df_rolls.pivot(index="Roll Number", columns="Dice Number", values="y")
        
    def recent_play(self, narrow=False):
        if not isinstance(narrow, bool):
            raise ValueError("Hey, this method takes 0 or 1 arguements. If 1 arguement, \
            it must be a boolean value!")
        if narrow==False:
            return self.df_rolls
        else:
            return pd.melt(self.df_rolls, value_name="Roll Results", ignore_index=False)\
        .set_index([pd.melt(self.df_rolls, value_name="Roll Results", ignore_index=False).index, "Dice Number"])
    
class Analyzer:
    
    def __init__(self, mygame):
        if not isinstance(mygame, Game):
                raise ValueError("Hey, your input is not a Game object!")
        self.mygame = mygame
        
    def jackpot(self):
        jackpot_results = self.mygame.df_rolls.iloc[np.where\
        (self.mygame.df_rolls.eq(self.mygame.df_rolls.iloc[:, 0], axis=0).all(1))]
        return len(jackpot_results)
    
    def face_counts(self):
        new_df = self.mygame.df_rolls.apply(pd.Series.value_counts, axis=1).fillna(0)
        new_df = new_df.rename_axis("Face Number", axis="columns")
        return new_df
    
    def combo_count(self):
        return pd.DataFrame(np.sort(self.mygame.df_rolls.values, axis=1), columns=self.mygame.df_rolls.columns) \
        .value_counts().to_frame(name="Combo Count")
    
    def perm_count(self):
        perm_df = self.mygame.df_rolls.value_counts().to_frame(name="Permutation Count")
        return perm_df
    
    
    
    
    
    
    