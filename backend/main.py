import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from imblearn.over_sampling import SMOTE
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Conv1D, Flatten, Dropout, Input, Concatenate, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.regularizers import l2
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# Load dataset
df = pd.read_csv("alzheimers_disease_data_expanded_3.csv")

# Drop non-relevant columns
df.drop(columns=["PatientID", "DoctorInCharge"], inplace=True)

# Encode categorical variables
le = LabelEncoder()
categorical_columns = ["Gender", "Ethnicity"]
for col in categorical_columns:
    df[col] = le.fit_transform(df[col])

# Split features and target
X = df.drop(columns=["Diagnosis"])
y = df["Diagnosis"]

# Standardize numerical features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Handle Class Imbalance using SMOTE
smote = SMOTE(random_state=42, sampling_strategy='auto')
X_resampled, y_resampled = smote.fit_resample(X_scaled, y)

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42, stratify=y_resampled)

# Feature Selection using Decision Tree and Random Forest
dt = DecisionTreeClassifier(random_state=42, max_depth=10, min_samples_split=5)
dt.fit(X_train, y_train)
dt_importances = dt.feature_importances_

rf = RandomForestClassifier(
    n_estimators=1000,
    random_state=42,
    max_depth=20,
    min_samples_split=4,
    min_samples_leaf=2,
    n_jobs=-1,
    class_weight='balanced'
)
rf.fit(X_train, y_train)
rf_importances = rf.feature_importances_

# Select top 12 features
dt_top_features = set(np.argsort(dt_importances)[-15:])
rf_top_features = set(np.argsort(rf_importances)[-15:])
selected_features = list(dt_top_features.intersection(rf_top_features))

# Print selected feature names
feature_names = X.columns[selected_features]
print("Selected features:", feature_names.tolist())

# Select only the chosen features
X_train_selected = X_train[:, selected_features].astype(np.float32)
X_test_selected = X_test[:, selected_features].astype(np.float32)

# Standardize numerical features on selected features only
scaler = StandardScaler()
X_train_selected_scaled = scaler.fit_transform(X_train_selected)  # Fit only on 12 features
X_test_selected_scaled = scaler.transform(X_test_selected)

# Save the new scaler trained on 12 features
joblib.dump(scaler, "scaler.pkl")
print("Updated scaler.pkl saved with 12 features")

# Save selected feature indices relative to the reduced dataset
selected_features = list(range(len(selected_features)))  # Fix index mismatch issue
joblib.dump(selected_features, "selected_features.pkl")
print("Updated selected_features.pkl saved with correct indices.")


# Save feature names
with open("selected_feature_names.txt", "w") as f:
    f.write("\n".join(feature_names.tolist()))

# Reshape for CNN input
X_train_selected_cnn = X_train_selected.reshape(X_train_selected.shape[0], X_train_selected.shape[1], 1)
X_test_selected_cnn = X_test_selected.reshape(X_test_selected.shape[0], X_test_selected.shape[1], 1)

# CNN Model with ANN
cnn_input = Input(shape=(X_train_selected.shape[1], 1))
cnn_layer = Conv1D(filters=256, kernel_size=3, activation='relu', kernel_regularizer=l2(0.0005))(cnn_input)
cnn_layer = BatchNormalization()(cnn_layer)
cnn_layer = Flatten()(cnn_layer)
cnn_layer = Dense(512, activation='relu', kernel_regularizer=l2(0.0005))(cnn_layer)
cnn_layer = BatchNormalization()(cnn_layer)
cnn_layer = Dropout(0.3)(cnn_layer)

ann_input = Input(shape=(X_train_selected.shape[1],))
ann_layer = Dense(512, activation='relu', kernel_regularizer=l2(0.0005))(ann_input)
ann_layer = BatchNormalization()(ann_layer)
ann_layer = Dropout(0.3)(ann_layer)

merged_layer = Concatenate()([cnn_layer, ann_layer])
merged_layer = Dense(256, activation='relu', kernel_regularizer=l2(0.0005))(merged_layer)
merged_layer = BatchNormalization()(merged_layer)
merged_layer = Dropout(0.3)(merged_layer)
output_layer = Dense(1, activation='sigmoid')(merged_layer)

final_model = Model(inputs=[cnn_input, ann_input], outputs=output_layer)
final_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0005), loss='binary_crossentropy', metrics=['accuracy'])

# Train model
history = final_model.fit(
    [X_train_selected_cnn, X_train_selected],
    y_train,
    epochs=100,
    batch_size=16,
    validation_data=([X_test_selected_cnn, X_test_selected], y_test),
    verbose=1
)
# Evaluate Model
y_pred = final_model.predict([X_test_selected_cnn, X_test_selected])
y_pred_classes = (y_pred > 0.5).astype(int)

# Print detailed evaluation metrics
print("\nClassification Report:")
print(classification_report(y_test, y_pred_classes))

# Print confusion matrix
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred_classes))

# Calculate and print final accuracy
loss, accuracy = final_model.evaluate([X_test_selected_cnn, X_test_selected], y_test, verbose=0)
print(f'\nFinal Test Accuracy: {accuracy * 100:.2f}%')

# Save model
final_model.save("model.h5")
print("Model training complete. Model, scaler, and selected features saved.")
