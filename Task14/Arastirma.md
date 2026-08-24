# OpenCV: HSV Renk Uzayı ve Trackbar ile Canlı Ayarlama

## Önce kavram: HSV nedir?

Şimdiye kadar hep **BGR** (Blue-Green-Red) renk uzayında çalıştık — her piksel üç sayıyla temsil ediliyordu: Mavi, Yeşil, Kırmızı miktarı. HSV ise rengi **tamamen farklı bir mantıkla** ifade eden alternatif bir renk uzayı.

**HSV = Hue, Saturation, Value**

| Bileşen | Türkçe | Ne anlama gelir | Değer aralığı (OpenCV'de) |
|---|---|---|---|
| **H** (Hue) | Ton/Renk tonu | Rengin "kendisi" — kırmızı mı, mavi mi, yeşil mi | 0-179 |
| **S** (Saturation) | Doygunluk | Rengin ne kadar "canlı/saf" olduğu — gri mi, parlak mı | 0-255 |
| **V** (Value) | Değer/Parlaklık | Rengin ne kadar aydınlık/koyu olduğu | 0-255 |

### Neden BGR yerine HSV kullanırız?

Bu, bu notun **en kritik kavramı**. Bir benzetmeyle başlayalım.

**Benzetme:** Bir boyacı dükkanına gittiğini düşün. Boyaları nasıl tarif edersin? "Biraz kırmızı, biraz mavi, biraz yeşil karışımı" demek yerine, muhtemelen "kırmızı", sonra "ama daha açık" (az doygun), sonra "ama daha karanlık bir ortamda" (düşük parlaklık) dersin. İşte HSV, tam olarak **insanların rengi doğal olarak düşünme şekline** yakındır — önce "hangi renk", sonra "ne kadar canlı", sonra "ne kadar aydınlık."

**Somut problem:** "Kırmızı bir topu" BGR ile tespit etmeye çalıştığını düşün. Güneşli bir günde kırmızı top parlak kırmızı (`[40, 40, 220]` gibi) görünür. Gölgede aynı top koyu kırmızı (`[15, 15, 90]` gibi) görünür. Bu iki BGR değeri **birbirinden çok farklı** — aynı eşik aralığıyla ikisini de yakalayamazsın!

HSV'de ise durum çok farklı: ışık değişse bile **Hue (ton) değeri neredeyse aynı kalır** — kırmızı, ister parlak ister karanlık ortamda olsun, hep "kırmızı tonundadır." Sadece **V (parlaklık)** değişir, **H (ton)** sabit kalır. Bu yüzden HSV, **ışık koşullarından bağımsız renk tespiti** için BGR'den çok daha güvenilirdir.

### Görsel benzetme: HSV'yi bir koni gibi düşün

- **H (Hue)**: koninin etrafındaki açı — 0° kırmızı, 60° sarı, 120° yeşil, 180°→0° tekrar kırmızıya döner (renk çemberi gibi düşün)
- **S (Saturation)**: koninin merkezinden dışına doğru uzaklık — merkeze yakın = gri/soluk, dışa yakın = canlı/saf renk
- **V (Value)**: koninin yüksekliği — tepe noktası = siyah (karanlık), taban = parlak/aydınlık

---

## BGR'den HSV'ye dönüşüm

```python
import cv2

img = cv2.imread("coins.jpg")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
```

Bunu, önceki notlardan tanıdığın `cv2.cvtColor()` ile yapıyoruz — tek fark, `COLOR_BGR2GRAY` yerine `COLOR_BGR2HSV` kullanmak. Çıktı, yine `(yükseklik, genişlik, 3)` şeklinde 3 kanallı bir dizi, ama bu sefer kanallar B/G/R değil, **H/S/V**.

**Tek bir pikselin HSV değerine bakma:**
```python
h, s, v = hsv[100, 150]
print(f"Hue: {h}, Saturation: {s}, Value: {v}")
```

---

## HSV ile renk filtreleme: `cv2.inRange()`

HSV'nin asıl gücü, belirli bir renk **aralığını** kolayca tanımlayabilmesi. Bunun için `cv2.inRange()` fonksiyonunu kullanırız — bu, thresholding'in HSV (3 kanallı) versiyonu gibi düşünülebilir.

```python
import numpy as np

alt_sinir = np.array([0, 100, 100])    # H, S, V alt sınırları
ust_sinir = np.array([10, 255, 255])   # H, S, V üst sınırları

mask = cv2.inRange(hsv, alt_sinir, ust_sinir)
```

**Ne yapıyor?** Her piksel için, H değeri `0`-`10` arasında **VE** S değeri `100`-`255` arasında **VE** V değeri `100`-`255` arasındaysa, o piksel maskede beyaz (255) olur; değilse siyah (0) olur. Bu, üç ayrı koşulun **hepsinin birden** sağlanmasını gerektiren bir thresholding gibi düşünülebilir.

**Neden `[0, 100, 100]` - `[10, 255, 255]` kırmızı için mantıklı?** Kırmızının Hue değeri OpenCV'de `0`'a yakın (renk çemberinin başlangıcı). `S` ve `V` için `100`'ün altını almıyoruz çünkü çok düşük doygunluk/parlaklık, griye yakın belirsiz renkler demek — biz **net, canlı** kırmızıyı arıyoruz.

---