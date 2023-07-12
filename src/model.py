import tensorflow as tf
import tensorflow.keras.models as MK
import tensorflow.keras.layers as LK
import pathlib

entrada = LK.Input(shape=(369, 496, 3))
conv1 = LK.Conv2D(filters=8, kernel_size=(3,3), padding='same', activation='relu')(entrada)
conv2 = LK.Conv2D(filters=8, kernel_size=(3,3), padding='same', activation='relu')(conv1)
pool1 = LK.MaxPool2D(pool_size=(2,2), strides=(2,2))(conv2)

conv3 = LK.Conv2D(filters=16, kernel_size=(3,3), padding='same', activation='relu')(pool1)
conv4 = LK.Conv2D(filters=16, kernel_size=(3,3), padding='same', activation='relu')(conv3)
pool2 = LK.MaxPool2D(pool_size=(2,2), strides=(2,2))(conv4)

conv5 = LK.Conv2D(filters=32, kernel_size=(3,3), padding='same', activation='relu')(pool2)
conv6 = LK.Conv2D(filters=32, kernel_size=(3,3), padding='same', activation='relu')(conv5)
pool3 = LK.MaxPool2D(pool_size=(2,2), strides=(2,2))(conv6)

conv7 = LK.Conv2D(filters=64, kernel_size=(3,3), padding='same', activation='relu')(pool3)
conv8 = LK.Conv2D(filters=64, kernel_size=(3,3), padding='same', activation='relu')(conv7)
pool4 = LK.MaxPool2D(pool_size=(2,2), strides=(2,2))(conv8)

conv8 = LK.Conv2D(filters=128, kernel_size=(3,3), padding='same', activation='relu')(pool4)
conv9 = LK.Conv2D(filters=128, kernel_size=(3,3), padding='same', activation='relu')(conv8)
pool5 = LK.MaxPool2D(pool_size=(2,2), strides=(2,2))(conv9)

#FLATTEN

flat = LK.Flatten()(pool5)

# NEURONAL NETWORK

fc1 = LK.Dense(units=512, activation='relu', kernel_regularizer= tf.keras.regularizers.L2(0.01))(flat)
drop = LK.Dropout(0.35)(fc1)
fc2 = LK.Dense(units=512, activation='relu', kernel_regularizer= tf.keras.regularizers.L2(0.01))(drop)
drop1 = LK.Dropout(0.4)(fc2)
fc3 = LK.Dense(units=512, activation='relu', kernel_regularizer= tf.keras.regularizers.L2(0.01))(drop1)
drop2 = LK.Dropout(0.35)(fc3)
salida = LK.Dense(units=5, activation='softmax')(drop2)

gonodactylus_simithii = MK.Model(entrada, salida)

# Obtenemos el path actual del archivo main.py
current_path = pathlib.Path(__file__).parent
# modelo_ruta = pathlib.Path(current_path / "assets" / "models" / "Model081.joblib")
modelo_ruta = pathlib.Path(current_path / "assets" / "models" / "good_weights.h5")

gonodactylus_simithii.load_weights(modelo_ruta)

