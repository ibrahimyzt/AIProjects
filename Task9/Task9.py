

import cv2
import numpy as np

# Orijinal resmi oku (BGR - 3 kanallı)
orijinal = cv2.imread('image.jpg')

# Griye dönüştür (1 kanallı)
gri = cv2.cvtColor(orijinal, cv2.COLOR_BGR2GRAY)

# --- Boyut (shape) farkları ---
print("Orijinal resmin boyutu (shape):", orijinal.shape)   # (yükseklik, genişlik, 3)
print("Gri resmin boyutu (shape):     ", gri.shape)         # (yükseklik, genişlik)  -> kanal boyutu yok

# --- Veri tipi (dtype) ---
print("\nOrijinal dtype:", orijinal.dtype)   # uint8
print("Gri dtype:      ", gri.dtype)         # uint8

# --- Boyut (ndim) ---
print("\nOrijinal ndim:", orijinal.ndim)  # 3
print("Gri ndim:      ", gri.ndim)        # 2

# --- Toplam eleman sayısı ---
print("\nOrijinal eleman sayısı:", orijinal.size)
print("Gri eleman sayısı:      ", gri.size)

# --- Bellek boyutu (byte) ---
print("\nOrijinal bellek boyutu:", orijinal.nbytes, "byte")
print("Gri bellek boyutu:      ", gri.nbytes, "byte")

# --- Tek bir pikselin değerlerini karşılaştır ---
y, x = 50, 50  # örnek koordinat
print("\nOrijinal piksel (B, G, R):", orijinal[y, x])
print("Gri piksel (tek değer):    ", gri[y, x])

# --- Min / Max değerler ---
print("\nOrijinal min-max:", orijinal.min(), "-", orijinal.max())
print("Gri min-max:      ", gri.min(), "-", gri.max())