
import pandas as pd  
from PIL import Image


    
# making dataframe  
df = pd.read_csv("sustainable_energy_nl.csv")  
   
# output the dataframe 
# print(type(df["BevolkingAanHetEindeVanDePeriode_15"][0]))

image = Image.open('map.png')
image.show()