# OpenCV `flip()` Metodu

`cv2.flip()`, bir görüntüyü yatay, dikey veya her iki eksende çevirmek (aynalamak) için kullanılır.

## Söz Dizimi

```python
cv2.flip(src, flipCode)
```

**Parametreler:**
- `src`: Çevrilecek girdi görüntüsü (numpy array)
- `flipCode`: Çevirme yönünü belirleyen tam sayı

## flipCode Değerleri

| Değer | Anlamı | Açıklama |
|-------|--------|----------|
| `0` | Dikey çevirme | Görüntü yukarı-aşağı ters çevrilir (x eksenine göre) |
| `1` (pozitif) | Yatay çevirme | Görüntü sağa-sola ters çevrilir (y eksenine göre) — ayna görüntüsü gibi |
| `-1` (negatif) | Her iki eksende | Hem yatay hem dikey çevrilir (180° döndürmeye eşdeğer) |

## Kullanım Alanları
- **Webcam görüntüleri**: Kameradan gelen görüntü genelde ayna gibi ters gösterildiği için `flip(img, 1)` ile düzeltilir.
- **Veri artırma (data augmentation)**: Makine öğrenmesi modellerinin eğitiminde veri çeşitliliği artırmak için görüntüler çevrilir.
- **Görüntü işleme testleri**: Simetri kontrolü veya farklı yönelim senaryoları oluşturmak için kullanılır.

Not: `flip()` fonksiyonu orijinal görüntüyü değiştirmez, çevrilmiş yeni bir görüntü (array) döndürür.