

import numpy as np 
import tensorflow as tf 
from tensorflow.keras import layers, models 

np.random.seed(1)
tf.random.set_seed(1)

IMG_SIZE = 32

# 1. SENTETIK VERI SETI OLUSTURMA (Daire vs Kare)

def draw_circle(img):
    yy, xx = np.ogrid[:IMG_SIZE, :IMG_SIZE]
    cx, cy = np.random.randint(10, 22, 2)
    r = np.random.randint(6, 10)
    mask = (xx - cx)**2 + (yy - cy)**2 <= r**2
    img[mask] = np.random.randint(150, 255, 3)
    return img

def draw_square(img):
    x1, y1 = np.random.randint(4, 14, 2)
    size = np.random.randint(10, 16)
    img[y1:y1+size, x1:x1+size] = np.random.randint(150, 255, 3)
    return img

def generate_dataset(n_samples):
    X = np.random.randint(0, 40, (n_samples, IMG_SIZE, IMG_SIZE, 3)).astype(np.uint8)
    y = np.random.randint(0, 2, n_samples)
    for i in range(n_samples):
        if y[i] == 0:
            X[i] = draw_circle(X[i])
        else:
            X[i] = draw_square(X[i])
    return X.astype("float32") / 255.0, y

print("Sentetik veri seti olusturuluyor (Daire=0, Kare=1)...")
X_train, y_train = generate_dataset(800)
X_test, y_test = generate_dataset(150)
print(f"Egitim seti: {X_train.shape}, Test seti: {X_test.shape}\n")

# 2. CNN MIMARISI TANIMLAMA
model = models.Sequential([

    # 2.1 Layers

    layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3)),

    layers.Conv2D(16, (3, 3), activation='relu', padding='same'),
    layers.MaxPooling2D((2, 2)),          # 32x32 -> 16x16

    layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
    layers.MaxPooling2D((2, 2)),          # 16x16 -> 8x8

    layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
    layers.MaxPooling2D((2, 2)),          # 8x8 -> 4x4

    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(2, activation='softmax')  # 2 sinif: Daire / Kare
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# 3. EGITIM
print("\nEgitim basliyor...\n")
history = model.fit(
    X_train, y_train,
    epochs=8,
    batch_size=32,
    validation_split=0.15,
    verbose=2
)

# 4. DEGERLENDIRME
test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
print(f"\nTest Kaybi: {test_loss:.4f}")
print(f"Test Dogrulugu: {test_acc*100:.2f}%")

# 5. TEK BIR ORNEK UZERINDE TAHMIN
sample = X_test[0:1]
pred = model.predict(sample, verbose=0)
predicted_class = np.argmax(pred)
class_names = ["Daire", "Kare"]
print(f"\nOrnek tahmin -> Gercek: {class_names[y_test[0]]}, "
      f"Model tahmini: {class_names[predicted_class]} "
      f"(guven: {pred[0][predicted_class]*100:.1f}%)")