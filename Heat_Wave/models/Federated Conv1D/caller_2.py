import numpy as np
from numpy import array
import pandas as pd
from numpy import hstack
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, ConvLSTM2D, Flatten, Conv1D, MaxPooling1D, Input, Concatenate,Conv2D
from tensorflow.keras.models import  Model
from tensorflow.keras import regularizers
import keras
import tensorflow as tf

class Reader():
    
    # Function initializer with city as input 
    def __init__(self, city):
        df = pd.read_csv("citywise/"+str(city)+".csv")
        self.client_names = df["Mandal"].unique()
        self.train_dataset = []
        for ele in self.client_names:
            self.train_dataset.append(df[df["Mandal"] == ele])

    # Clinet Dict creator
    def create_clients(self):
        return {self.client_names[i] : self.train_dataset[i] for i in range(len(self.client_names))}

    # Sequence creator for 1 D input
    def split_sequences(sequences, n_steps_in,n_steps_out):
        X, y = list(), list()
        for i in range(len(sequences)):

            end_ix = i + n_steps_in
            out_end_ix = end_ix + n_steps_out

            if out_end_ix > len(sequences)-1:
                break

            seq_x, seq_y = sequences[i:end_ix], sequences[end_ix:out_end_ix]
            X.append(seq_x)
            y.append(seq_y)
            
        return array(X), array(y)
    
    # Loader function for loading Nsteps input data and x steps output data
    def data_loader(self, data, n_steps_in, n_steps_out, feaat : str):
        
        df = data.copy()
        in_seq1 = df[feaat]
        # in_seq2 = df['Max Temp (°C)']

        # in_seq1 = np.asarray(in_seq1).reshape((len(in_seq1), 1))
        # in_seq2 = np.asarray(in_seq2).reshape((len(in_seq2), 1))

        # dataset = hstack((in_seq1, in_seq2))
        dataset = in_seq1
        X_train,y_train = Reader.split_sequences(dataset, n_steps_in, n_steps_out)
        X_test, y_test = Reader.split_sequences(dataset, n_steps_in, n_steps_out)

        return (X_train,y_train),(X_test,y_test)

    # Unused Speration function for loss calculation
    def sep_output(self, y_train, y_test):

        try:
            y1_train = y_train[:,:,0]
            y2_train = y_train[:,:,1]
        except:
            None

        y1_test = y_test[:,:,0]
        y2_test = y_test[:,:,1]

        return (y1_train,y2_train),(y1_test,y2_test)
    
    # Spliting Data in N steps by N steps input and Nsteps out as output
    def ndarray_split_sequences(sequences, n_steps_in,n_steps_out):
        X, y, ndarray, ydarray = list(), list(), [], []
        for i in range(len(sequences)):

            end_ix = i + n_steps_in
            out_end_ix = end_ix + n_steps_out

            if out_end_ix > len(sequences)-1:
                break

            seq_x, seq_y = sequences[i:end_ix], sequences[end_ix:out_end_ix]
            X.append(seq_x)
            y.append(seq_y)
        
        for i in range(int(len(X))-n_steps_in):
            ndarray.append(X[i:i+n_steps_in])
            ydarray.append(y[i+1])
            
        return array(ndarray), array(ydarray)

    # Loading Data for N by N image array 
    def ndarray_data_loader(self, data, n_steps_in, n_steps_out,feaat : str):
        
        df = data.copy()
        # in_seq1 = df['Max Humidity (%)']
        in_seq2 = df[feaat]

        # in_seq1 = np.asarray(in_seq1).reshape((len(in_seq1), 1))
        # in_seq2 = np.asarray(in_seq2).reshape((len(in_seq2), 1))

        # dataset = hstack((in_seq1, in_seq2))
        dataset = in_seq2
        X_train,y_train = Reader.ndarray_split_sequences(dataset, n_steps_in, n_steps_out)
        X_test, y_test = Reader.ndarray_split_sequences(dataset, n_steps_in, n_steps_out)

        return (X_train,y_train),(X_test,y_test)
    

    def TF_ndarray_data_loader(self, data, n_steps_in, n_steps_out,feaat : str):
        
        df = data.copy()
        # in_seq1 = df['Max Humidity (%)']
        in_seq2 = df[feaat]

        # in_seq1 = np.asarray(in_seq1).reshape((len(in_seq1), 1))
        # in_seq2 = np.asarray(in_seq2).reshape((len(in_seq2), 1))

        # dataset = hstack((in_seq1, in_seq2))
        dataset = in_seq2
        X_train,y_train = Reader.ndarray_split_sequences(dataset, n_steps_in, n_steps_out)
        train_dataset = tf.data.Dataset.from_tensor_slices((X_train, y_train))
        X_test, y_test = Reader.ndarray_split_sequences(dataset, n_steps_in, n_steps_out)
        test_dataset = tf.data.Dataset.from_tensor_slices((X_test, y_test))

        return train_dataset,test_dataset



class SmplMLP:

    @staticmethod
    def Conv2D_model(n_steps_in: int, n_steps_out: int, kernel_size=3, n_features=1, n_filters=10):
        new_model = keras.Sequential()

        input1 = Input(shape=(n_steps_in, n_steps_in, n_features))
        input2 = Input(shape=(n_steps_in, n_steps_in, n_features))

        cnn1 = Conv2D(n_filters,kernel_size=kernel_size, activation=tf.keras.layers.LeakyReLU())(input1)
        cnn2 = Conv2D(n_filters,kernel_size=kernel_size, activation=tf.keras.layers.LeakyReLU())(input2)

        mid = Concatenate()([cnn1, cnn2])
        mid = Conv2D(n_filters,kernel_size=kernel_size, activation=tf.keras.layers.LeakyReLU())(mid)
        # mid = Conv2D(n_filters,kernel_size=kernel_size, activation=tf.keras.layers.LeakyReLU())(mid)


        output1 =  Conv2D(n_filters,kernel_size=kernel_size, activation=tf.keras.layers.LeakyReLU())(mid)
        # output1 = Conv2D(n_filters,kernel_size=kernel_size, activation=tf.keras.layers.LeakyReLU())(output1)
        output1 = Flatten()(output1)
        output1 = Dense(250, activation='relu')(output1)
        output1 = Dense(n_steps_out, name = 'Output_1')(output1)

        output2 =  Conv2D(n_filters,kernel_size=kernel_size, activation=tf.keras.layers.LeakyReLU())(mid)
        # output2 = Conv2D(n_filters,kernel_size=kernel_size, activation=tf.keras.layers.LeakyReLU())(output2)
        output2 = Flatten()(output2)
        output2 = Dense(250, activation='relu')(output2)
        output2 = Dense(n_steps_out, name = 'Output_2')(output2)

        model = Model(inputs = [input1,input2], outputs = [output1,output2])

        return model


    def Conv1D_model(self, n_steps_in, n_steps_out):
        # define model
        n_features = 1
        visible1 = Input(shape=(n_steps_in, n_features))
        visible2 = Input(shape=(n_steps_in, n_features))

        cnn1 = Conv1D(filters=32, kernel_size=3, activation='relu')(visible1)
        cnn2 = Conv1D(filters=32, kernel_size=3, activation='relu')(visible2)

        mid = Concatenate()([cnn1, cnn2])
        mid = Conv1D(16,kernel_size=3, activation=tf.keras.layers.LeakyReLU())(mid)
        mid = Conv1D(16,kernel_size=3, activation=tf.keras.layers.LeakyReLU())(mid)

        # define output 1
        output1 = Conv1D(filters=16, kernel_size=2, activation='relu', kernel_regularizer=regularizers.L1L2(l1=1e-5, l2=1e-4), name = 'out1_conv1_2')(mid)
        output1 = Conv1D(filters=16, kernel_size=1, activation='relu', kernel_regularizer=regularizers.L1L2(l1=1e-5, l2=1e-4), name = 'out1_conv1_3')(output1)
        output1 = Conv1D(filters=32, kernel_size=1, activation='relu', kernel_regularizer=regularizers.L1L2(l1=1e-5, l2=1e-4), name = 'out1_conv1_4')(output1)
        output1 = Flatten(name = 'out1_flat_5')(output1)
        output1 = Dense(n_steps_out, name='humid_out')(output1)

        # define output 2
        output2 = Conv1D(filters=256, kernel_size=2, activation='relu', kernel_regularizer=regularizers.L1L2(l1=1e-5, l2=1e-4), name = 'out2_conv1_2')(mid)
        output2 = Conv1D(filters=128, kernel_size=1, activation='relu', kernel_regularizer=regularizers.L1L2(l1=1e-5, l2=1e-4), name = 'out2_conv1_3')(output2)
        output2 = Conv1D(filters=32, kernel_size=1, activation='relu', kernel_regularizer=regularizers.L1L2(l1=1e-5, l2=1e-4), name = 'out2_conv1_4')(output2)
        output2 = Flatten(name = 'out2_flat_5')(output2)
        output2 = Dense(n_steps_out, name='temp_out')(output2)


        model = Model(inputs=[visible1,visible2], outputs=[output1, output2])

        return model
    
    # def build(n_steps_in, n_steps_out):
    #     # define model
    #     n_features = 2
    #     visible = Input(shape=(n_steps_in, n_features))
    #     cnn = Conv1D(filters=512, kernel_size=2, activation='relu')(visible)

    #     # define output 1
    #     output1 = Conv1D(filters=256, kernel_size=2, activation='relu', kernel_regularizer=regularizers.L1L2(l1=1e-5, l2=1e-4), name = 'out1_conv1_2')(cnn)
    #     output1 = Conv1D(filters=128, kernel_size=1, activation='relu', kernel_regularizer=regularizers.L1L2(l1=1e-5, l2=1e-4), name = 'out1_conv1_3')(output1)
    #     output1 = Conv1D(filters=32, kernel_size=1, activation='relu', kernel_regularizer=regularizers.L1L2(l1=1e-5, l2=1e-4), name = 'out1_conv1_4')(output1)
    #     output1 = Flatten(name = 'out1_flat_5')(output1)
    #     output1 = Dense(n_steps_out, name='humid_out')(output1)

    #     # define output 2
    #     output2 = Conv1D(filters=256, kernel_size=2, activation='relu', kernel_regularizer=regularizers.L1L2(l1=1e-5, l2=1e-4), name = 'out2_conv1_2')(cnn)
    #     output2 = Conv1D(filters=128, kernel_size=1, activation='relu', kernel_regularizer=regularizers.L1L2(l1=1e-5, l2=1e-4), name = 'out2_conv1_3')(output2)
    #     output2 = Conv1D(filters=32, kernel_size=1, activation='relu', kernel_regularizer=regularizers.L1L2(l1=1e-5, l2=1e-4), name = 'out2_conv1_4')(output2)
    #     output2 = Flatten(name = 'out2_flat_5')(output2)
    #     output2 = Dense(n_steps_out, name='temp_out')(output2)


    #     model = Model(inputs=visible, outputs=[output1, output2])

    #     return model




