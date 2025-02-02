import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from matplotlib.colors import ListedColormap
from sklearn.preprocessing import LabelEncoder
import os

"""# Read And Merge"""

labels = pd.read_csv('labels.csv')
distances = pd.read_csv('3d_distances.csv')
angles = pd.read_csv('angles.csv')

features = pd.merge(distances, angles, on="pose_id")
all_data = pd.merge(labels, features, on="pose_id")

# Exporting the DataFrame to a CSV file
# all_data.to_csv(r'C:\Users\tariq\OneDrive\Desktop\Bitirme Projesi\newData\all_data.csv',index=False)
#inputs as numpy array
X = all_data.drop(['pose','pose_id'],axis=1).values

y = all_data['pose'].values

# Encoding
le = LabelEncoder()
y = le.fit_transform(y)
print("classes_",list(le.classes_))

# Splitting
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=0)


# Training
from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators = 300, criterion = 'entropy', random_state = 0)
classifier.fit(X_train, y_train)

# Prediction
y_pred = classifier.predict(X_test)

#Accuracy Score
cm = confusion_matrix(y_test, y_pred)
print(cm)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')


# Saving the model
joblib.dump(classifier, "./random_forest.joblib")
joblib.dump(le, "./label_encoder.joblib")