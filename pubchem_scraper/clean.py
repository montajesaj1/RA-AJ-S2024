import pandas as pd

data = pd.read_csv("30_second_wait.csv")
data['New CAS'] = data['New CAS'].apply(lambda x: 'No CAS info' if x == 'N/A' else x)
data['New Deprecated CAS'] = data['New Deprecated CAS'].apply(lambda x: 'No CAS info' if x == 'N/A' else x)

data.to_csv("30_second_wait_2.csv")
