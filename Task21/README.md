# YOLOv5 Model Sonuçları — Yorumlama Raporu

Bu doküman, `FIL` (fil), `KEDI` (kedi), `KOPEK` (köpek) sınıflarını tespit etmek üzere eğitilen özel YOLOv5 modelinin (`best.pt`) çıktılarını, her metriğin ne anlama geldiğini açıklayarak yorumlar.

---

## 1. Genel Özet

| Metrik | Değer |
|---|---|
| mAP@0.5 (tüm sınıflar) | **0.795** |
| En iyi F1 skoru | **0.77** (confidence = 0.403'te) |
| FIL sınıfı AP | 0.895 |
| KEDI sınıfı AP | 0.806 |
| KOPEK sınıfı AP | 0.684 |
| Eğitim epoch sayısı | ~50 |

Model genel olarak **iyi bir performans** sergiliyor (mAP@0.5 = 0.795), ama sınıflar arasında belirgin bir performans farkı var — bu fark, aşağıdaki bölümlerde veri seti dağılımıyla birlikte açıklanacak.

---

## 2. Precision-Recall (PR) Eğrisi Yorumu

### Bu eğri ne gösteriyor?

**Precision (Kesinlik):** Modelin "bu bir nesne" dediği tahminlerin yüzde kaçının **gerçekten doğru** olduğu. Düşük precision, modelin çok fazla **yanlış alarm (false positive)** verdiği anlamına gelir.

**Recall (Duyarlılık):** Görüntüde gerçekten var olan nesnelerin yüzde kaçını modelin **yakalayabildiği**. Düşük recall, modelin bazı gerçek nesneleri **kaçırdığı (false negative)** anlamına gelir.

Bu ikisi genelde **ters orantılıdır** — modeli daha "temkinli" yaparsan (sadece çok emin olduğunda tahmin yap) precision artar ama recall düşer; modeli daha "cesur" yaparsan tam tersi olur. PR eğrisi, bu iki değerin farklı eşik (confidence threshold) değerlerinde nasıl değiştiğini gösterir.

### Sonuçların yorumu

- **FIL (0.895):** En yüksek AP (Average Precision) değerine sahip sınıf. Eğri sağ üst köşeye en yakın duran çizgi — yani hem yüksek precision hem yüksek recall'u **aynı anda** koruyabiliyor. Bu, modelin fili tespit etme konusunda en güvenilir olduğunu gösteriyor.
- **KEDI (0.806):** Orta seviye bir performans. Recall arttıkça (yani modelin daha fazla kediyi yakalamaya çalıştığı noktalarda) precision daha hızlı düşüyor — yani model bazı durumlarda kedi olmayan şeyleri de "kedi" sanmaya başlıyor.
- **KOPEK (0.684):** En düşük performans gösteren sınıf. Eğrisi diğer ikisinin belirgin şekilde altında seyrediyor — özellikle recall %60'ı geçtiğinde precision hızla düşüyor. Bu, modelin köpekleri tespit etmekte **daha az güvenilir** olduğunu gösteriyor.
- **Kalın mavi çizgi (all classes, 0.795 mAP@0.5):** Üç sınıfın **ağırlıklı ortalaması**. FIL'in güçlü performansı, KOPEK'in zayıf performansını kısmen dengeliyor.

**Neden KOPEK en düşük performansı gösteriyor olabilir?** Bölüm 4'teki veri seti dağılımı incelendiğinde bunun olası sebebi netleşiyor.

---

## 3. F1-Confidence Eğrisi Yorumu

### Bu eğri ne gösteriyor?

**F1 skoru**, precision ve recall'un **harmonik ortalamasıdır** — ikisini tek bir sayıda dengeler. Formülü:
```
F1 = 2 * (Precision * Recall) / (Precision + Recall)
```

**Confidence (güven eşiği)**, modelin bir tahmini "geçerli" sayması için gereken minimum güven skorudur (0-1 arası). Bu eğri, **farklı eşik değerlerinde F1 skorunun nasıl değiştiğini** gösterir — amaç, F1'in en yüksek olduğu "tatlı noktayı (sweet spot)" bulmaktır.

### Sonuçların yorumu

- **En yüksek nokta: F1 = 0.77, confidence = 0.403'te.** Bu, modelin gerçek zamanlı kullanımda (`detect.py` ya da kendi kodunda) **confidence threshold'unu yaklaşık 0.40 civarında ayarlaman gerektiği** anlamına geliyor — bu değer, precision ve recall arasındaki en dengeli noktayı temsil ediyor.
- **Eğrinin şekli:** Düşük confidence değerlerinde (0.0-0.1 arası) F1 hızla yükseliyor — bu, çok düşük eşiklerde modelin gürültülü/güvenilmez tahminler verdiğini gösteriyor. Eğri 0.2-0.4 arasında bir "plato" (düzlük) oluşturuyor, sonra confidence arttıkça (model daha "temkinli" hale geldikçe) recall düşmeye başladığı için F1 de düşüyor.
- **FIL burada da en yüksek eğriye sahip**, **KOPEK en düşük** — bu, PR eğrisindeki sıralamayla tutarlı.

### Pratik sonuç

Gerçek zamanlı kullanım kodundaki (`CONFIDENCE_THRESHOLD`) değeri **0.40 civarına** ayarlamak, bu veri setine göre en dengeli sonucu verecektir. Daha yüksek bir eşik (örn. 0.6-0.7) daha az yanlış alarm ama daha fazla kaçırılan nesne anlamına gelir; daha düşük bir eşik (örn. 0.2) tam tersi bir etki yaratır.

---

## 4. Eğitim Eğrileri (Loss ve Metrik Grafikleri) Yorumu

Bu grafik seti, eğitim sürecinin **epoch'lar boyunca** (yaklaşık 50 epoch) nasıl ilerlediğini gösteriyor.

### Loss (kayıp) grafikleri — üst sıra ve alt sıranın ilk 3 sütunu

- **`train/box_loss`, `train/obj_loss`, `train/cls_loss`:** Eğitim setindeki üç ayrı hata türü — sırasıyla kutu konumu hatası, "burada bir nesne var mı" hatası, ve sınıf tahmini hatası. **Üçü de düzenli ve kesintisiz şekilde azalıyor** — bu, modelin eğitim verisinden **düzgün öğrendiğinin** işareti.
- **`val/box_loss`, `val/obj_loss`, `val/cls_loss`:** Aynı üç hata türü, ama **modelin hiç görmediği** doğrulama (validation) verisinde ölçülüyor. Bunlar da genel olarak azalıyor, ama eğitim kayıplarına göre **daha gürültülü/dalgalı** — bu normal, çünkü validation seti daha küçük ve model o veriyi hiç görmedi.

**Önemli gözlem:** `val/box_loss` ve `val/cls_loss` grafiklerinde bazı ani sıçramalar var (örneğin `val/cls_loss`'ta 15-20. epoch civarında bir zirve). Bu tür tekil sıçramalar, o epoch'ta rastgele zor bir validation batch'i ile karşılaşıldığını gösterebilir — eğer genel trend düşüşteyse (ki burada öyle), endişelenecek bir durum değildir.

### Metrik grafikleri — precision, recall, mAP_0.5, mAP_0.5:0.95

- **`metrics/precision` ve `metrics/recall`:** İkisi de eğitim ilerledikçe **yükseliyor** ve yaklaşık 30-40. epoch civarında **düzleşmeye (plato)** başlıyor. Bu düzleşme, modelin bu veri seti ve mimari için **öğrenebileceği kadarını öğrendiğini**, daha fazla epoch'un ciddi bir iyileşme sağlamayacağını gösteriyor.
- **`metrics/mAP_0.5`:** ~0.8 seviyesinde düzleşiyor — PR eğrisindeki 0.795 değeriyle tutarlı.
- **`metrics/mAP_0.5:0.95`:** ~0.5 civarında düzleşiyor. Bu metrik, `mAP_0.5`'ten daha **katı** bir ölçüttür (kutuların IoU — örtüşme oranı — 0.5'ten 0.95'e kadar farklı eşiklerde ortalaması alınır). Bu değerin `mAP_0.5`'ten belirgin şekilde düşük olması **normal ve beklenen** bir durum — model nesnenin **var olduğunu** iyi tespit ediyor ama kutu sınırlarını **piksel hassasiyetinde mükemmel** çizemiyor olabilir.

**Genel değerlendirme:** Eğrilerin plato yapması, modelin **overfitting'e girmeden** öğrenmeyi tamamladığını gösteriyor — yani `best.pt` muhtemelen bu eğitim sürecinin en sağlıklı noktasını yakalamış.

---

## 5. Veri Seti Dağılımı Yorumu (labels grafikleri)

### Sınıf dengesizliği (class imbalance)

Sol üstteki çubuk grafik, her sınıftan kaç örnek (instance) olduğunu gösteriyor:

| Sınıf | Yaklaşık örnek sayısı |
|---|---|
| FIL | ~400 |
| KEDI | ~250 |
| KOPEK | ~230 |

**Bu, KOPEK'in neden en düşük performansı gösterdiğini büyük ölçüde açıklıyor.** FIL, diğer iki sınıftan **belirgin şekilde daha fazla** örnekle temsil edilmiş — model, en çok gördüğü sınıfı en iyi öğrenir. KOPEK ve KEDI'nin görece az örneği, modelin bu sınıflarda **daha az güvenilir** olmasına yol açmış olabilir.

**Pratik öneri:** Eğer bu modelin köpek tespitini iyileştirmek istersen, en etkili yöntem muhtemelen **daha fazla köpek fotoğrafı** eklemek olur — model mimarisini değiştirmek yerine, veri dengesizliğini gidermek genelde daha büyük bir iyileşme sağlar.

### Bounding box konum dağılımı (x, y scatter)

Sol alttaki grafik, tüm kutuların **merkez konumlarının (x, y)** görüntü içinde nerede yoğunlaştığını gösteriyor. Noktalar **merkeze (0.5, 0.5)** doğru yoğun bir şekilde kümelenmiş — bu, veri setindeki fotoğrafların çoğunda nesnenin **kadrajın ortasına yakın** konumlandırıldığını gösteriyor.

**Bunun olası etkisi:** Eğer gerçek kullanımda nesneler genelde **kenarlarda veya köşelerde** çıkarsa, model bu durumlarda daha az güvenilir olabilir — çünkü eğitim verisinde bu tür örnekler azdı. Bu, modelin **genelleşme sınırlarından** biri olarak not edilebilir.

### Kutu boyutu dağılımı (width, height scatter ve histogramlar)

Sağ alttaki grafik, kutuların **genişlik (width) ve yükseklik (height)** arasındaki ilişkiyi gösteriyor. Noktalar belirgin bir **pozitif korelasyon** sergiliyor (width arttıkça height de artıyor) — bu mantıklı, çünkü hayvan/nesne fotoğrafları genelde kabaca kare ya da dikdörtgen oranlarında çekilir, aşırı ince/uzun kutular nadir.

Sağ üstteki iç içe geçmiş dikdörtgenler grafiği (bazen "box correlogram" denir), tüm kutuların **üst üste bindirilmiş halini** gösteriyor — merkeze yakın yoğunlaşma, çoğu kutunun benzer oranlarda ve orta büyüklükte olduğunu doğruluyor.

### Korelasyon matrisi (x, y, width, height pairplot)

Son görsel, dört değişkenin (x, y, width, height) birbirleriyle ikili ilişkisini gösteriyor. En dikkat çekici gözlem: **width ve height arasında güçlü bir pozitif ilişki** var (sağ alt köşedeki grafik) — bu, önceki gözlemi teyit ediyor. `x` ve `y` dağılımları (köşegen üzerindeki histogramlar) da merkeze yoğunlaşmış bir çan eğrisi şeklinde, bu da merkez-yoğun kompozisyon eğilimini tekrar doğruluyor.

---

## 6. Genel Sonuç ve Öneriler

1. **Model kullanıma hazır durumda** — mAP@0.5 = 0.795 ve F1 = 0.77 makul, kullanılabilir bir performans seviyesi.
2. **Gerçek zamanlı kullanımda confidence threshold'unu ~0.40** civarında ayarlamak, precision/recall dengesini optimize eder.
3. **KOPEK sınıfının performansını artırmak istersen**, önceliğin veri setine **daha fazla köpek örneği eklemek** olmalı — mevcut dengesizlik (400 FIL'e karşı 230 KOPEK), bu sınıfın diğerlerine göre geride kalmasının en olası sebebi.
4. **Model, nesnelerin kadraj merkezinde olduğu görüntülerde muhtemelen daha güvenilir** — kenarda/köşede olan nesnelerde ekstra dikkatli test edilmesi önerilir.
5. **`mAP_0.5:0.95` ile `mAP_0.5` arasındaki fark**, modelin nesnenin varlığını iyi tespit ettiğini ama kutu sınırlarının piksel hassasiyetinde geliştirilebilir olduğunu gösteriyor — eğer çok hassas konum bilgisi gerekiyorsa, daha fazla epoch ya da daha yüksek çözünürlüklü eğitim (`--img 640` yerine `--img 1280` gibi) denenebilir.