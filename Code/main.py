import eurostat
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine


# func to process only the necessary columns(data)
def filter_data(df):
    df = df.rename(columns={'geo\\time': 'country'})
    df.drop(['c_resid', 'unit', 'nace_r2'], axis='columns', inplace=True)  # drops the unnecessary columns

    df = df.melt(id_vars="country", var_name="year", value_name="value")  # reshape dataFrame to desired format
    # rename columns
    df = df.sort_values(by='year', ascending=True)  # change the year order(2016-2019)
    return df


nights_dataset_df = eurostat.get_data_df(code='tour_occ_ninat')  # download Eurostat dataset of given code return
                                                                 # it as a pandas dataframe.

# using specific codes to select the necessary data(codes taken by eurostat database)
nights_tot_df = nights_dataset_df[nights_dataset_df['c_resid'].isin(['TOTAL'])
                                  & nights_dataset_df['unit'].isin(['NR'])
                                  & nights_dataset_df['nace_r2'].isin(['I551-I553'])
                                  & nights_dataset_df['geo\\time'].isin(['EL', 'ES'])].loc[:, 'c_resid': 2016]

nights_tot_df = filter_data(nights_tot_df)
print('Nights spent at tourist accommodation establishments')
print(nights_tot_df)

nights_for_df = nights_dataset_df[nights_dataset_df['c_resid'].isin(['FOR'])
                                  & nights_dataset_df['unit'].isin(['NR'])
                                  & nights_dataset_df['nace_r2'].isin(['I551-I553'])
                                  & nights_dataset_df['geo\\time'].isin(['EL', 'ES'])].loc[:, 'c_resid': 2016]

nights_for_df = filter_data(nights_for_df)
print('\nNights spent by non-residents at tourist accommodation establishments')
print(nights_for_df)

arrivals_dataset_df = eurostat.get_data_df(code='tour_occ_arnat')  # download Eurostat dataset of given code return
# it as a pandas dataframe.

arrivals_tot_df = arrivals_dataset_df[arrivals_dataset_df['c_resid'].isin(['TOTAL'])
                                      & arrivals_dataset_df['unit'].isin(['NR'])
                                      & arrivals_dataset_df['nace_r2'].isin(['I551-I553'])
                                      & arrivals_dataset_df['geo\\time'].isin(['EL', 'ES'])].loc[:, 'c_resid': 2016]

arrivals_tot_df = filter_data(arrivals_tot_df)
print('\nArrivals at tourist accommodation establishments')
print(arrivals_tot_df)

arrivals_for_df = arrivals_dataset_df[arrivals_dataset_df['c_resid'].isin(['FOR'])
                                      & arrivals_dataset_df['unit'].isin(['NR'])
                                      & arrivals_dataset_df['nace_r2'].isin(['I551-I553'])
                                      & arrivals_dataset_df['geo\\time'].isin(['EL', 'ES'])].loc[:, 'c_resid': 2016]

arrivals_for_df = filter_data(arrivals_for_df)
print('\nArrivals of non-residents at tourist accommodation establishments')
print(arrivals_for_df)


# line-2D plot of the data for Greece,Spain
def plot_func(df):
    el_df = df[df.country == 'EL']  # df with data from greece
    es_df = df[df.country == 'ES']  # df with data from spain

    plt.plot(el_df.year, el_df.value / 10 ** 6)  # divide by 10**6 the value column
    plt.plot(es_df.year, es_df.value / 10 ** 6)
    plt.legend(['Greece', 'Spain'])
    plt.xlabel('Year')
    plt.ylabel('Values')
    return df


nights_tot_df = plot_func(nights_tot_df)
plt.title("Nights spent at tourist accommodation establishments")
plt.figure()  # create a figure

nights_for_df = plot_func(nights_for_df)
plt.title("Nights spent by non-residents at tourist accommodation establishments")
plt.figure()

arrivals_tot_df = plot_func(arrivals_tot_df)
plt.title("Arrivals at tourist accommodation establishments")
plt.figure()

arrivals_for_df = plot_func(arrivals_for_df)
plt.title("Arrivals of non-residents at tourist accommodation establishments")

plt.show()  # dislpay all open figures


# Create sqlalchemy engine to connect to localhost database

engine = create_engine("mysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="794613852",
                               db="eurostat_db"))

# Insert whole DataFrame into MySQL
nights_tot_df.to_sql('nights_total', con=engine, if_exists='append', index=False)
nights_for_df.to_sql('nights_nonresidents', con=engine, if_exists='append', index=False)

arrivals_tot_df.to_sql('arrivals_total', con=engine, if_exists='append', index=False)
arrivals_for_df.to_sql('arrivals_nonresidents', con=engine, if_exists='append', index=False)

print("Data loaded!")


# We can export the .csv via pandas func or Mysql workbench IDE
nights_tot_df.to_csv('Nights at tourist accommodation establishments.csv', sep='\t', index=False)
nights_for_df.to_csv('Nights spent by non-residents at tourist accommodation establishments.csv', sep='\t', index=False)
arrivals_tot_df.to_csv('Arrivals at tourist accommodation establishments.csv', sep='\t', index=False)
arrivals_for_df.to_csv('Arrivals of non-residents at tourist accommodation establishments.csv', sep='\t', index=False)
