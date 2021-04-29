from mainapp.models import Rating,Location,Member
from django_pandas.io import read_frame
import pandas as pd
import numpy as np
from sklearn.metrics import euclidean_distances
from sklearn.preprocessing import StandardScaler, MinMaxScaler

def get_skate_recommendations(df: pd.DataFrame, user_features: dict) -> pd.DataFrame: #ensures a pandas dataframe is returned. we pass the original df and the target anchor(who we compare against)
    features = ['ramps','indoor','paid','cruising','asphalt','concrete','wood','skateType'] #list of features that are used to compute similarity between the users average ratings  and the skate parks average
    

    #create the features in a seperate frame
    df_features = df[features].copy()
    #df_features = normalize_features(df_features)

    df_user = pd.DataFrame([user_features])
    df_features = pd.concat([df_user, df_features], sort=False)
    df_features = normalize_features(df_features)
    
    # compute the distances
    X = df_features.values
    Y = df_features.values[0].reshape(1, -1)
    distances = euclidean_distances(X, Y)
    
    df_sorted = df.copy()
    
    df_sorted['similarity_distance'] = distances[1:]
    return df_sorted.sort_values('similarity_distance').reset_index(drop=True)


def normalize_features(df):
    for col in df.columns:
        # fill any NaN's with the mean
        df[col] = df[col].fillna(df[col].mean())
        df[col] = StandardScaler().fit_transform(df[col].values.reshape(-1, 1))

    return df
