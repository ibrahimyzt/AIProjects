## 1. CNN Nedir?

**Evrişimli Sinir Ağı (Convolutional Neural Network - CNN)**, özellikle görüntü işleme ve bilgisayarlı görü (computer vision) görevlerinde kullanılan bir derin öğrenme mimarisidir. İnsan görsel korteksinin çalışma prensibinden esinlenmiştir; görüntüdeki yerel örüntüleri (kenarlar, köşeler, dokular) otomatik olarak öğrenip, bunları birleştirerek daha karmaşık ve soyut özellikleri (nesneler, yüzler vb.) tanıyabilir.

Geleneksel yapay sinir ağlarından (Fully Connected Networks) farkı, her pikseli ayrı ayrı bir nörona bağlamak yerine, **evrişim (convolution)** işlemiyle görüntünün küçük bölgelerini tarayarak parametre sayısını ciddi biçimde azaltmasıdır.

---

## 2. CNN'in Temel Katmanları

### 2.1 Evrişim Katmanı (Convolutional Layer)
- Görüntü üzerinde küçük bir **filtre/kernel** (örneğin 3x3 veya 5x5) kaydırılarak (convolve edilerek) özellik haritaları (**feature map**) üretilir.
- Her filtre, kenar, doku veya renk geçişi gibi belirli bir örüntüyü tespit etmeye "öğrenir".
- **Stride**: Filtrenin her adımda kaç piksel kaydığını belirler.
- **Padding**: Görüntü kenarlarına sıfır ekleyerek çıktı boyutunun küçülmesini kontrol eder (`valid` vs `same` padding).

### 2.2 Aktivasyon Fonksiyonu (Activation Layer)
- Genellikle evrişim katmanının hemen ardından uygulanır.
- En yaygın kullanılan: **ReLU (Rectified Linear Unit)** — `f(x) = max(0, x)`
- Ağa doğrusal olmayanlık (non-linearity) katarak karmaşık örüntülerin öğrenilmesini sağlar.

### 2.3 Havuzlama Katmanı (Pooling Layer)
- Özellik haritalarının boyutunu küçültür, böylece hesaplama yükü azalır ve modelin küçük konum değişikliklerine karşı daha dayanıklı (invariant) olması sağlanır.
- **Max Pooling**: Belirli bir bölgedeki en büyük değeri alır (en yaygın kullanılan).
- **Average Pooling**: Belirli bir bölgedeki ortalama değeri alır.

### 2.4 Düzleştirme (Flatten) Katmanı
- Evrişim ve havuzlama katmanlarından çıkan çok boyutlu (3D) özellik haritalarını, tam bağlı katmana verilebilmesi için tek boyutlu (1D) bir vektöre dönüştürür.

### 2.5 Tam Bağlı Katman (Fully Connected / Dense Layer)
- Klasik yapay sinir ağı katmanıdır; çıkarılan özellikleri kullanarak sınıflandırma veya regresyon görevini gerçekleştirir.
- Genellikle son katmanda **Softmax** (çoklu sınıflandırma) veya **Sigmoid** (ikili sınıflandırma) aktivasyonu kullanılır.

---

## 3. Genel CNN Akış Şeması

```
Girdi Görüntüsü
      │
      ▼
Evrişim Katmanı (Conv2D) + ReLU
      │
      ▼
Havuzlama Katmanı (Pooling)
      │
      ▼
   (Bu blok birkaç kez tekrarlanır)
      │
      ▼
Flatten (Düzleştirme)
      │
      ▼
Tam Bağlı Katman (Dense)
      │
      ▼
Çıktı Katmanı (Softmax / Sigmoid)
```

---

## 4. Önemli Kavramlar

| Kavram | Açıklama |
|--------|----------|
| **Kernel / Filtre** | Görüntü üzerinde kaydırılan küçük ağırlık matrisi |
| **Feature Map** | Evrişim sonucu elde edilen özellik haritası |
| **Receptive Field** | Bir nöronun görüntüde "gördüğü" bölgenin boyutu |
| **Parameter Sharing** | Aynı filtrenin görüntünün tamamında tekrar kullanılması → parametre tasarrufu |
| **Stride** | Filtrenin kayma adım miktarı |
| **Padding** | Kenarlara eklenen sıfır piksel miktarı |
| **Dropout** | Aşırı öğrenmeyi (overfitting) önlemek için rastgele nöronların devre dışı bırakılması |
| **Batch Normalization** | Katman çıktılarını normalize ederek eğitimi hızlandırma ve stabilize etme |

---

## 5. Bilinen CNN Mimarileri

| Mimari | Yıl | Öne Çıkan Özellik |
|--------|-----|---------------------|
| **LeNet-5** | 1998 | İlk başarılı CNN, el yazısı rakam tanıma |
| **AlexNet** | 2012 | ImageNet yarışmasını kazandı, derin öğrenmeyi popülerleştirdi |
| **VGGNet** | 2014 | Küçük (3x3) filtrelerle çok derin ağlar |
| **GoogLeNet (Inception)** | 2014 | "Inception modülü" ile paralel filtre boyutları |
| **ResNet** | 2015 | "Residual connections" (atlama bağlantıları) ile çok derin ağların eğitilebilmesi |
| **EfficientNet** | 2019 | Ölçeklendirme (derinlik/genişlik/çözünürlük) optimizasyonu |

---

## 6. CNN Nerelerde Kullanılır?
- **Görüntü sınıflandırma** (Image Classification)
- **Nesne tespiti** (Object Detection — YOLO, Faster R-CNN)
- **Görüntü segmentasyonu** (Semantic/Instance Segmentation — U-Net, Mask R-CNN)
- **Yüz tanıma** (Face Recognition)
- **Görüntü stili aktarımı** (Style Transfer)
- OpenCV ile birlikte kullanıldığında: önişleme (preprocessing — griye çevirme, yeniden boyutlandırma, normalizasyon) genellikle CNN'e veri hazırlamak için OpenCV fonksiyonlarıyla yapılır.