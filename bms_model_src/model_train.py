import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Load dataset
df = pd.read_csv('/Users/rufbook/workss/threebits_hackgenx/bms_model_src/augmented_dataset.csv', sep=',')

# Preprocess features
features = ['temperature', 'humidity', 'motion_detected']
X = df[features].values.astype(np.float32)

# Encode time features
df['hour'] = pd.to_datetime(df['current_time']).dt.hour
X_time = df[['hour']].values.astype(np.float32)
X = np.hstack([X, X_time])

# Targets: hvac_target_temperature (regression), light_state (binary), fan_state (binary)
y_reg = df['hvac_target_temperature'].values.astype(np.float32)
y_light = df['light_state'].values.astype(np.int32)
y_fan = df['fan_state'].values.astype(np.int32)

# Split data
X_train, X_test, y_reg_train, y_reg_test, y_light_train, y_light_test, y_fan_train, y_fan_test = train_test_split(
    X, y_reg, y_light, y_fan, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Build a small multi-output model
inputs = tf.keras.Input(shape=(X_train.shape[1],))
x = tf.keras.layers.Dense(16, activation='relu')(inputs)
x = tf.keras.layers.Dense(16, activation='relu')(x)

# Regression head
reg_output = tf.keras.layers.Dense(1, name='hvac')(x)
# Classification heads
light_output = tf.keras.layers.Dense(1, activation='sigmoid', name='light')(x)
fan_output = tf.keras.layers.Dense(1, activation='sigmoid', name='fan')(x)

model = tf.keras.Model(inputs=inputs, outputs=[reg_output, light_output, fan_output])

model.compile(
    optimizer='adam',
    loss={'hvac': 'mse', 'light': 'binary_crossentropy', 'fan': 'binary_crossentropy'},
    metrics={'hvac': 'mae', 'light': 'accuracy', 'fan': 'accuracy'}
)

# Train
model.fit(
    X_train,
    {'hvac': y_reg_train, 'light': y_light_train, 'fan': y_fan_train},
    validation_data=(X_test, {'hvac': y_reg_test, 'light': y_light_test, 'fan': y_fan_test}),
    epochs=50,
    batch_size=32
)

# Save model
model.save('/Users/rufbook/workss/bms/bms_model.h5')

# Convert to TFLite with quantization
def representative_dataset():
    for i in range(min(100, X_train.shape[0])):
        yield [X_train[i:i+1]]

converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_dataset
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.int8
converter.inference_output_type = tf.int8
tflite_model = converter.convert()

# Save TFLite model
with open('/Users/rufbook/workss/threebits_hackgenx/bms_model_src/bms_model.tflite', 'wb') as f:
    f.write(tflite_model)

print("TFLite model is saved to /Users/rufbook/workss/threebits_hackgenx/bms_model_src/bms_model.tflite")