# Imports
import pandas as pd
from pathlib import Path
import tensorflow as tf
import numpy as np
from sklearn.preprocessing import StandardScaler,OneHotEncoder
import hvplot.pandas
import holoviews as hv

#Import data for nn_continuous value prediction
def import_data_nn_predict(sector, select_ticker):
    #EH:  Create DataFrame from csv
    sector_data_df = pd.read_csv(Path(f'Data_Prep_Output/{sector}.csv'))
    sector_data_df=sector_data_df[sector_data_df['ticker']==select_ticker]
    actual_target_df=sector_data_df.loc[:,['date_x','q_roi']]
    actual_target_df=actual_target_df.reset_index()
    #EH:  Drop unnamed, currency, ticker, sector columns from the DataFrame
    sector_data_df = sector_data_df.drop(columns=['Unnamed: 0','reportedCurrency','ticker','Sector','date_x','q_roi'],axis=1)
    
    #EH: update int to float
    int_list=list(sector_data_df.dtypes[sector_data_df.dtypes == "int64"].index)
    sector_data_df[int_list]=sector_data_df[int_list].astype('float64')    
    
    # return data to predict, actual q_roi
    return sector_data_df, actual_target_df 


def scale(df):
    #Create the scaler instance
    X_scaler=StandardScaler()
    
    #Fit the scaler
    X_scaler.fit(df)
    
    #scale the features data
    X_scaled=X_scaler.transform(df)
    
    return X_scaled

def nn_predict(sector,select_ticker):
    
    #EH: set path of nn predict file
    model_path=Path(f'Models/nn_{sector}.h5')
    
    #EH: load the model to new object
    neuron=tf.keras.models.load_model(model_path)
    
    #EH:  create df for predict and actual roi
    ticker_feature, ticker_actual_roi=import_data_nn_predict(sector,select_ticker)
    
    #EH:  standard scale data
    ticker_feature_scaled=scale(ticker_feature)
    
    #EH: adjust data to array
    ticker_feature_scaled=np.asarray(ticker_feature_scaled).astype('float32')
    
    #EH:  make predictions
    predictions=(neuron.predict(ticker_feature_scaled))
    
    #EH: create a df to compare predictions with actual roi
    results = pd.DataFrame({"predictions": predictions.ravel()})

    #EH: round prediction amount
    results['predictions']=round(results['predictions'],4)

    # results=
    results = pd.concat([ticker_actual_roi,results],axis=1)
    
    #EH: update column to datetime
    results['date_x']=pd.to_datetime(results['date_x'])

    
    #EH: Sort date
    results=results.sort_values(by=['date_x'])
    
    #EH: set index
    results.set_index('date_x',inplace=True)
    
    #EH: Calculate cumulative quarter return
    results['q_roi cumulative retun']=((results['q_roi']+1).cumprod())-1
    results['predict cumulative retun']=round(((results['predictions']+1).cumprod())-1,4)
    
    #EH: drop extra column
    results.drop(columns=['index'],inplace=True)
    
    #EH:  plot
    results_plot=results.loc[:,['q_roi cumulative retun','predict cumulative retun']].hvplot(ylabel='%',title=f'{select_ticker} Quarterly cumulative return % - Neural Network Model')
    
    return results, results_plot