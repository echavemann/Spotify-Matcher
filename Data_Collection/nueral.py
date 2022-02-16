import numpy
import datetime
import tensorflow as tf
import pandas as pd

# Load up the data with pandas
r_cols = ['user_id', 'genre', 'affinity']
train_data_df = pd.read_csv('train_data.csv', sep='\t', names=r_cols)
test_data_df = pd.read_csv('test_data.csv', sep='\t', names=r_cols)

