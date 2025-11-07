# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd

# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler, OneHotEncoder
# from sklearn.impute import SimpleImputer
# from sklearn.pipeline import make_pipeline
# from sklearn.compose import make_column_transformer

# from tensorflow import keras
# from tensorflow.keras import layer

# import joblib
# import tensorflow as tf




# # Setup plotting
# import matplotlib.pyplot as plt
# plt.style.use('seaborn-v0_8-whitegrid')
# # Set Matplotlib defaults
# plt.rc('figure', autolayout=True)
# plt.rc('axes', labelweight='bold', labelsize='large',
#        titleweight='bold', titlesize=18, titlepad=10)
# plt.rc('animation', html='html5')



# hotel = pd.read_csv('hotel.csv')

# X = hotel.copy()
# y = X.pop('is_canceled')

# X['arrival_date_month'] = \
#     X['arrival_date_month'].map(
#         {'January':1, 'February': 2, 'March':3,
#          'April':4, 'May':5, 'June':6, 'July':7,
#          'August':8, 'September':9, 'October':10,
#          'November':11, 'December':12}
#     )

# features_num = [
#     "lead_time", "arrival_date_week_number",
#     "arrival_date_day_of_month", "stays_in_weekend_nights",
#     "stays_in_week_nights", "adults", "children", "babies",
#     "is_repeated_guest", "previous_cancellations",
#     "previous_bookings_not_canceled", "required_car_parking_spaces",
#     "total_of_special_requests", "adr",
# ]
# features_cat = [
#     "hotel", "arrival_date_month", "meal",
#     "market_segment", "distribution_channel",
#     "reserved_room_type", "deposit_type", "customer_type",
# ]

# transformer_num = make_pipeline(
#     SimpleImputer(strategy="constant"), # there are a few missing values
#     StandardScaler(),
# )
# transformer_cat = make_pipeline(
#     SimpleImputer(strategy="constant", fill_value="NA"),
#     OneHotEncoder(handle_unknown='ignore'),
# )

# preprocessor = make_column_transformer(
#     (transformer_num, features_num),
#     (transformer_cat, features_cat),
# )

# # stratify - make sure classes are evenlly represented across splits
# X_train, X_valid, y_train, y_valid = \
#     train_test_split(X, y, stratify=y, train_size=0.75)

# X_train = preprocessor.fit_transform(X_train)
# X_valid = preprocessor.transform(X_valid)

# input_shape = [X_train.shape[1]]


# model = keras.Sequential([

#     layers.BatchNormalization(input_shape=input_shape),
    
#     layers.Dense(256, activation='relu'),
#     layers.BatchNormalization(),
#     layers.Dropout(0.3),
    
      
#     layers.Dense(256, activation='relu'),
#     layers.BatchNormalization(),
#     layers.Dropout(0.3),
    

#     layers.Dense(1, activation='sigmoid')
# ])

# model.summary()

# model.compile(
#     optimizer='adam',
#     loss='binary_crossentropy',
#     metrics=['binary_accuracy']
# )

# early_stopping = keras.callbacks.EarlyStopping(
#     patience=5,
#     min_delta=0.001,
#     restore_best_weights=True,
# )
# history = model.fit(
#     X_train, y_train,
#     validation_data=(X_valid, y_valid),
#     batch_size=512,
#     epochs=200,
#     callbacks=[early_stopping],
#     verbose=1
# )

# history_df = pd.DataFrame(history.history)
# history_df.loc[:, ['loss', 'val_loss']].plot(title="Cross-entropy")
# plt.show()
# history_df.loc[:, ['binary_accuracy', 'val_binary_accuracy']].plot(title="Accuracy")
# plt.show()

# print("Model Evaluation:")
# val_loss, val_accuracy = model.evaluate(X_valid, y_valid, verbose=0)
# print(f"Validation Loss: {val_loss:.4f}")
# print(f"Validation Accuracy: {val_accuracy:.4f}")


# y_pred_proba = model.predict(X_valid)
# y_pred = (y_pred_proba > 0.5).astype(int).flatten()



# model.save('hotel_cancellation_model.keras')
# print("✓ Model saved as 'hotel_cancellation_model.keras'")

# import joblib
# joblib.dump(preprocessor, 'preprocessor.pkl')
# print("✓ Preprocessor saved as 'preprocessor.pkl'")

# feature_info = {
#     'numeric_features': features_num,
#     'categorical_features': features_cat,
#     'all_features': features_num + features_cat
# }
# joblib.dump(feature_info, 'feature_info.pkl')
# print("✓ Feature information saved")


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer

from tensorflow import keras
from tensorflow.keras import layers  # Fixed: 'layer' to 'layers'

import joblib
import tensorflow as tf

# Setup plotting
import matplotlib.pyplot as plt
plt.style.use('seaborn-v0_8-whitegrid')
# Set Matplotlib defaults
plt.rc('figure', autolayout=True)
plt.rc('axes', labelweight='bold', labelsize='large',
       titleweight='bold', titlesize=18, titlepad=10)
plt.rc('animation', html='html5')

hotel = pd.read_csv('hotel.csv')

X = hotel.copy()
y = X.pop('is_canceled')

X['arrival_date_month'] = \
    X['arrival_date_month'].map(
        {'January':1, 'February': 2, 'March':3,
         'April':4, 'May':5, 'June':6, 'July':7,
         'August':8, 'September':9, 'October':10,
         'November':11, 'December':12}
    )

features_num = [
    "lead_time", "arrival_date_week_number",
    "arrival_date_day_of_month", "stays_in_weekend_nights",
    "stays_in_week_nights", "adults", "children", "babies",
    "is_repeated_guest", "previous_cancellations",
    "previous_bookings_not_canceled", "required_car_parking_spaces",
    "total_of_special_requests", "adr",
]
features_cat = [
    "hotel", "arrival_date_month", "meal",
    "market_segment", "distribution_channel",
    "reserved_room_type", "deposit_type", "customer_type",
]

transformer_num = make_pipeline(
    SimpleImputer(strategy="constant"), # there are a few missing values
    StandardScaler(),
)
transformer_cat = make_pipeline(
    SimpleImputer(strategy="constant", fill_value="NA"),
    OneHotEncoder(handle_unknown='ignore'),
)

preprocessor = make_column_transformer(
    (transformer_num, features_num),
    (transformer_cat, features_cat),
)

# stratify - make sure classes are evenlly represented across splits
X_train, X_valid, y_train, y_valid = \
    train_test_split(X, y, stratify=y, train_size=0.75)

X_train = preprocessor.fit_transform(X_train)
X_valid = preprocessor.transform(X_valid)

input_shape = [X_train.shape[1]]

model = keras.Sequential([
    layers.BatchNormalization(input_shape=input_shape),
    layers.Dense(256, activation='relu'),
    layers.BatchNormalization(),
    layers.Dropout(0.3),
    layers.Dense(256, activation='relu'),
    layers.BatchNormalization(),
    layers.Dropout(0.3),
    layers.Dense(1, activation='sigmoid')
])

model.summary()

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['binary_accuracy']
)

early_stopping = keras.callbacks.EarlyStopping(
    patience=5,
    min_delta=0.001,
    restore_best_weights=True,
)
history = model.fit(
    X_train, y_train,
    validation_data=(X_valid, y_valid),
    batch_size=512,
    epochs=200,
    callbacks=[early_stopping],
    verbose=1
)

history_df = pd.DataFrame(history.history)
history_df.loc[:, ['loss', 'val_loss']].plot(title="Cross-entropy")
plt.show()
history_df.loc[:, ['binary_accuracy', 'val_binary_accuracy']].plot(title="Accuracy")
plt.show()

print("Model Evaluation:")
val_loss, val_accuracy = model.evaluate(X_valid, y_valid, verbose=0)
print(f"Validation Loss: {val_loss:.4f}")
print(f"Validation Accuracy: {val_accuracy:.4f}")

y_pred_proba = model.predict(X_valid)
y_pred = (y_pred_proba > 0.5).astype(int).flatten()

# SAVE THE MODEL 
model.save('hotel_cancellation_model.keras')
print("✓ Model saved as 'hotel_cancellation_model.keras'")

print("✅ Training completed  model saved (no preprocessor files).")

# Save the fitted preprocessor
joblib.dump(preprocessor, 'hotel_preprocessor.pkl')
print("✓ Preprocessor saved as 'hotel_preprocessor.pkl'")