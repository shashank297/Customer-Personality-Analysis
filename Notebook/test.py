df = df.dropna()
df['Age'] = 2015 - df.Year_Birth
df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'])
df['Month_Customer'] = 12.0 * (2015 - df.Dt_Customer.dt.year ) + (1 - df.Dt_Customer.dt.month)
df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'],format="%d-%m-%Y")
df['Month_Customer'] = 12.0 * (2015 - df.Dt_Customer.dt.year ) + (1 - df.Dt_Customer.dt.month)
df['TotalSpendings'] =  df.MntWines + df.MntFruits + df.MntMeatProducts + df.MntFishProducts + df.MntSweetProducts + df.MntGoldProds
df.loc[(df['Age'] >= 13) & (df['Age'] <= 19), 'AgeGroup'] = 'Teen'
df.loc[(df['Age'] >= 20) & (df['Age']<= 39), 'AgeGroup'] = 'Adult'
df.loc[(df['Age'] >= 40) & (df['Age'] <= 59), 'AgeGroup'] = 'Middle Age Adult'
df.loc[(df['Age'] > 60), 'AgeGroup'] = 'Senior Adult'
df['Children'] = df['Kidhome'] + df['Teenhome']
df.Marital_Status = df.Marital_Status.replace({'Together': 'Partner',
                                                           'Married': 'Partner',
                                                           'Divorced': 'Single',
                                                           'Widow': 'Single', 
                                                           'Alone': 'Single',
                                                           'Absurd': 'Single',
                                                           'YOLO': 'Single'})
#removing outliers
df = df[df.Age < 100]
df = df[df.Income < 120000]
