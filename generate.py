import pandas as pd
import random as r
import datetime as dt

class DataGenerator:
  
        
    def csv_dumper(self,fp= "data.csv"):
        
        data = list()
        
        for i in range(1000):
            data.append([i+1,r.randrange(20,35),r.randrange(20,60),dt.datetime.now()])
        
        df = pd.DataFrame(data,columns = ["id","Temperature","Moisture","timestamp"])
      
        
        f = open(fp,"w",encoding = "utf-8")
        df.to_csv(f,index = False)
        

    def get_random_value(self):
        return [r.randrange(20,35),r.randrange(20,60)]


DataGenerator().csv_dumper()
    