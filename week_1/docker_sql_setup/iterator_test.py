
import pandas as pd

df_iterator = pd.read_csv("yellow_head.csv", iterator = True ,chunksize = 10)

first_chunk = next(df_iterator)
print(first_chunk)
print(next(df_iterator))


#for chunk in df_iterator:
#    print(chunk)