import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

# Generate synthetic dataset
np.random.seed(42)
n = 1000
# features: link_util (0-100), queue_len (0-100), bw_usage (0-100)
link_util = np.random.uniform(0,100,size=n)
queue_len = np.random.uniform(0,100,size=n)
bw = (link_util*0.6 + queue_len*0.4) + np.random.normal(0,10,size=n)
bw = np.clip(bw, 0, 100)
# label: congestion (1) if bw>70 or link_util>80 or queue_len>80
label = ((bw>70) | (link_util>80) | (queue_len>80)).astype(int)
df = pd.DataFrame({'link_util':link_util, 'queue_len':queue_len, 'bw_usage':bw, 'label':label})
print(df.head())

X = df[['link_util','queue_len','bw_usage']].values
y = df['label'].values

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X,y)

os.makedirs('model', exist_ok=True)
model_path = 'model/model.pkl'
with open(model_path,'wb') as f:
    pickle.dump(clf,f)

print('Model saved to', model_path)
