# ✅ 2. Import Libraries
import os, cv2, numpy as np
import matplotlib.pyplot as plt
from keras.utils import Sequence
from keras.models import Model
from keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D, Concatenate, ZeroPadding2D
from keras.callbacks import ModelCheckpoint
import tensorflow as tf
import pickle
from tqdm import tqdm

base_path = '/content'
sketch_dir = os.path.join(base_path, 'celeba_sketches_10k')
real_dir   = os.path.join(base_path, 'celeba_real_images_10k')
image_size = (218, 178)  # (height, width)
epochs = 80
batch_size = 8


class DataGenerator(Sequence):
    def __init__(self, image_ids, sketch_path, real_path, batch_size, image_size):
        self.image_ids = image_ids
        self.sketch_path = sketch_path
        self.real_path = real_path
        self.batch_size = batch_size
        self.image_size = image_size

    def __len__(self):
        return len(self.image_ids) // self.batch_size

    def __getitem__(self, index):
        ids = self.image_ids[index * self.batch_size:(index + 1) * self.batch_size]
        X = np.zeros((self.batch_size, *self.image_size, 3), dtype=np.float32)
        y = np.zeros((self.batch_size, *self.image_size, 3), dtype=np.float32)
        for i, img_name in enumerate(ids):
            sketch = cv2.imread(os.path.join(self.sketch_path, img_name))
            real = cv2.imread(os.path.join(self.real_path, img_name))

            sketch = cv2.cvtColor(sketch, cv2.COLOR_BGR2RGB)
            real = cv2.cvtColor(real, cv2.COLOR_BGR2RGB)

            sketch = cv2.resize(sketch, (self.image_size[1], self.image_size[0])) / 255.0
            real = cv2.resize(real, (self.image_size[1], self.image_size[0])) / 255.0

            X[i] = sketch
            y[i] = real
        return X, y


image_list = sorted(os.listdir(sketch_dir))[:10000]  
train_ids = image_list[:9000]
val_ids   = image_list[9000:]

print(f"Train size: {len(train_ids)} | Val size: {len(val_ids)}")

train_gen = DataGenerator(train_ids, sketch_dir, real_dir, batch_size, image_size)
val_gen   = DataGenerator(val_ids, sketch_dir, real_dir, batch_size, image_size)

def down_block(x, filters):
    c = Conv2D(filters, 3, activation='relu', padding='same')(x)
    c = Conv2D(filters, 3, activation='relu', padding='same')(c)
    p = MaxPooling2D((2, 2))(c)
    return c, p

def up_block(x, skip, filters):
    us = UpSampling2D((2, 2))(x)
    ch = skip.shape[1] - us.shape[1]
    cw = skip.shape[2] - us.shape[2]
    if ch > 0 or cw > 0:
        us = ZeroPadding2D(((ch//2, ch - ch//2), (cw//2, cw - cw//2)))(us)
    us = Concatenate()([us, skip])
    c = Conv2D(filters, 3, activation='relu', padding='same')(us)
    c = Conv2D(filters, 3, activation='relu', padding='same')(c)
    return c

def build_unet(input_shape):
    f = [16, 32, 64, 128, 256]
    inputs = Input(input_shape)

    c1, p1 = down_block(inputs, f[0])
    c2, p2 = down_block(p1, f[1])
    c3, p3 = down_block(p2, f[2])
    c4, p4 = down_block(p3, f[3])

    bn = Conv2D(f[4], 3, activation='relu', padding='same')(p4)
    bn = Conv2D(f[4], 3, activation='relu', padding='same')(bn)

    u1 = up_block(bn, c4, f[3])
    u2 = up_block(u1, c3, f[2])
    u3 = up_block(u2, c2, f[1])
    u4 = up_block(u3, c1, f[0])

    outputs = Conv2D(3, 1, activation='sigmoid', padding='same')(u4)
    return Model(inputs, outputs)


input_shape = (218, 178, 3)
model = build_unet(input_shape)
model.compile(optimizer='adam', loss='mse')
model.summary()


checkpoint = ModelCheckpoint('/content/drive/MyDrive/sketch2image_best.h5', save_best_only=True, verbose=1)
history = model.fit(train_gen, validation_data=val_gen, epochs=epochs, callbacks=[checkpoint])

with open('/content/drive/MyDrive/sketch2image_training_history.pkl', 'wb') as f:
    pickle.dump(history.history, f)

print("Training complete and history saved.")
