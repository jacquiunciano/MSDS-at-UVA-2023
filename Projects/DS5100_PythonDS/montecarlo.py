class Dice:
    df  = pd.DataFrame({"faces":[],
                        "weights":[]}).set_index("faces")
    
    def __init__(self, n, w=1):
        if not isinstance(n, np.ndarray):
            raise TypeError("Hey, you need to use an numpy.array!")
        if len(set(n)) != len(n):
            raise ValueError("Hey, you've got some repeats in your array!")
        self.df  = pd.DataFrame({"faces":n,
                       "weights":w}).set_index("faces")
        
    def change_weight(self, face, weight):
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
        return jackpot_results
    
    def face_counts(self):
        new_df = self.mygame.df_rolls.apply(pd.Series.value_counts, axis=1).fillna(0)
        new_df = newdf.rename_axis("Face Number", axis="columns")
        return new_df
    
    def combo_count(self):
        combo_df = self.mygame.df_rolls.value_counts().to_frame(name="Combo Count")
        return combo_df
    
    
    
    
    
    
    