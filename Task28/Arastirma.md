# Eğitilmiş Modeli ONNX Formatına Dönüştürme

## 1. Neyi Yapmaya Çalışıyoruz?

Şu ana kadar `train.py` ile eğittiğin model, PyTorch'un kendi formatı olan **`.pt`** (best.pt gibi) dosyası olarak kayıtlı. Bu görevde bu modeli, **`.onnx`** adı verilen, farklı programlar/platformlar arasında taşınabilir bir formata dönüştüreceksin.

Bunu şöyle düşün: `.pt` dosyası, sadece PyTorch'un "anladığı" bir dil gibidir — bir nevi Word belgesi (`.docx`) gibi, sadece Microsoft Word'de tam uyumlu çalışır. `.onnx` ise PDF gibidir — hangi programda açarsan aç (Python, C++, mobil uygulama, tarayıcı), aynı şekilde çalışır.

## 2. Neden Böyle Bir Dönüşüme İhtiyaç Duyarız?

| Senaryo | Neden `.onnx` gerekir? |
|---|---|
| Modeli bir web sitesine entegre etmek | Tarayıcılar PyTorch çalıştıramaz, ama ONNX.js ile çalıştırabilir |
| Modeli bir telefon uygulamasına koymak | Mobil cihazlar PyTorch'un tam sürümünü taşıyamaz, ONNX daha hafiftir |
| Modeli C++ ile yazılmış bir programda kullanmak | PyTorch Python'a bağımlıdır, ONNX Runtime birçok dilde çalışır |
| Farklı donanımlarda (Intel, ARM işlemciler) hız kazanmak | ONNX Runtime, donanıma özel optimizasyonlar yapabilir |

## 3. Dönüştürme Komutu

YOLOv5 klasöründeyken (`aiprojects-gpu` ortamı aktifken) terminalde şunu çalıştır:

```bash
python3 export.py --weights runs/train/exp16/weights/best.pt --include onnx --img 640 --device 0
```

**Parametrelerin anlamı:**
- `--weights` → dönüştürmek istediğin eğitilmiş model dosyası
- `--include onnx` → hangi formata dönüştürüleceğini belirtir (aynı komutla `torchscript`, `tflite` gibi başka formatlara da dönüştürülebilir)
- `--img 640` → modelin eğitildiği resim boyutuyla aynı olmalı (eğitimde `--img 640` kullandıysan burada da 640 yaz)

Komut çalıştıktan sonra, `best.pt` dosyasının bulunduğu klasörde otomatik olarak **`best.onnx`** adlı yeni bir dosya oluşur.

## 4. .pt ve .onnx Formatlarının Farkları

| Özellik | `.pt` (PyTorch) | `.onnx` (Open Neural Network Exchange) |
|---|---|---|
| **Kim üretir** | PyTorch | Framework-bağımsız açık standart |
| **Nerede çalışır** | Sadece PyTorch kurulu ortamlarda | ONNX Runtime, TensorRT, OpenVINO gibi birçok "motor"da |
| **Dosya boyutu** | Genelde biraz daha büyük | Genelde biraz daha küçük/optimize |
| **Hız** | Eğitim ve esneklik için optimize | Çıkarım (inference/tahmin) için optimize, genelde daha hızlı |
| **Esneklik** | Modeli tekrar eğitebilir, katmanları değiştirebilirsin | Sadece "tahmin yapma" amaçlıdır, tekrar eğitilemez |
| **Kullanım amacı** | Geliştirme, eğitim, deneme | Üretim (production), dağıtım (deployment) |

### Basit bir benzetme
`.pt` dosyası, bir aşçının **el yazısı tarifi** gibidir — sadece o aşçı (PyTorch) tam olarak anlar, ama tarifi istediği gibi değiştirebilir (yeni eğitim, fine-tuning). `.onnx` ise bu tarifin **standart, basılı bir kitap haline getirilmiş** hali gibidir — herkes (farklı programlar) okuyup uygulayabilir, ama tarifi değiştiremezsin, sadece takip edersin.

## 5. Dönüşümü Test Etme

Dönüştürülen modelin gerçekten çalıştığını doğrulamak için:

```bash
python3 detect.py --weights runs/train/exp16/weights/best.onnx --source /path/to/test_resmi.jpg
```

Eğer `.pt` ile aldığın sonuçlara benzer bir çıktı alıyorsan, dönüşüm başarılı demektir.