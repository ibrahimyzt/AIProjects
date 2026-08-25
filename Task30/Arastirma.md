 # Vision Transformers (ViT): Teknik Rapor

## Özet

Bu rapor, Vision Transformer (ViT) mimarisinin çalışma prensibini, geleneksel Evrişimli Sinir Ağları (CNN — YOLOv5'in de temelini oluşturan mimari) ile farkını ve pratikteki kullanım alanlarını ele almaktadır. ViT, orijinal olarak doğal dil işleme (NLP) için geliştirilen **Transformer** mimarisinin, görüntü işleme problemlerine uyarlanmış halidir.

---

## 1. Giriş: Neden Yeni Bir Yaklaşım Gerekti?

YOLOv5 gibi modeller, görüntüyü işlemek için **CNN (Convolutional Neural Network / Evrişimli Sinir Ağı)** kullanır. CNN'ler, resmi küçük "pencerelerle" (filtrelerle) tarayarak kenar, köşe, doku gibi yerel örüntüleri öğrenir — sonra bu örüntüleri katman katman birleştirerek daha karmaşık şekilleri (göz, kulak, tekerlek gibi) tanır.

2017 yılında yayımlanan "Attention Is All You Need" makalesiyle **Transformer** mimarisi tanıtıldı — başta metin/dil problemleri için (örneğin ChatGPT'nin de temelinde bu mimari var). 2020'de araştırmacılar şunu sordu: *"Transformer'ı resimlere de uygulayabilir miyiz?"* Cevap **evet** oldu, ve bu **Vision Transformer (ViT)** olarak adlandırıldı.

### Temel Fark (Basit Bir Benzetme)
- **CNN**, bir resme küçük bir büyüteçle bakıp yavaş yavaş, yerel olarak inceleyen bir dedektif gibidir — önce köşeleri, sonra parçaları, en son bütünü anlar.
- **ViT**, resmin tamamına aynı anda bakıp, **her parçanın diğer tüm parçalarla ilişkisini** değerlendiren bir stratejist gibidir — "sol üstteki köşe ile sağ alttaki köşe arasında bir bağlantı var mı?" sorusunu doğrudan sorabilir.

---

## 2. ViT Mimarisi: Adım Adım Çalışma Prensibi

### Adım 1 — Görüntüyü Parçalara (Patch) Bölme
ViT, resmi tek parça olarak değil, sabit boyutlu küçük karelere ("patch") böler. Örneğin 224×224 piksellik bir resim, her biri 16×16 piksel olan **196 küçük parçaya** ayrılır.

> Bunu bir yapboz (puzzle) gibi düşün: resmi önce küçük parçalara ayırıyoruz.

### Adım 2 — Parçaları Sayısal Vektöre Çevirme (Linear Embedding)
Her küçük resim parçası, düzleştirilip (flatten) bir sayı dizisine (vektöre) dönüştürülür. Bu, tıpkı bir kelimenin "kelime vektörüne" (word embedding) çevrilmesi gibi — burada her resim parçası, bir "görsel kelime" gibi ele alınır.

### Adım 3 — Pozisyon Bilgisi Ekleme (Positional Encoding)
Transformer, doğası gereği parçaların **sırasını bilmez** — bu yüzden her parçaya "ben resmin neresindeyim" bilgisini taşıyan ekstra bir sayısal etiket (pozisyon kodlaması) eklenir. Bu olmazsa, model resmin yukarısı ile aşağısını karıştırabilir.

### Adım 4 — Transformer Encoder'a Gönderme
Bu parçalar (artık sayısal vektörler haline gelmiş), bir dizi **Transformer Encoder** katmanından geçirilir. Bu katmanların kalbinde **Self-Attention (Öz-Dikkat)** mekanizması bulunur.

#### Self-Attention Nedir? (En Kritik Kavram)
Self-Attention, her parçanın "diğer tüm parçalara ne kadar dikkat etmesi gerektiğini" hesaplayan bir mekanizmadır. Örneğin bir kedi resminde, "kulak" parçası, "kuyruk" parçasından çok "göz" ve "burun" parçalarına daha fazla "dikkat" edebilir çünkü bunlar birlikte "kedi yüzü" kavramını oluşturur.

> Benzetme: Bir sınıf toplantısında, herkesin konuşurken sadece kendi yanındakini değil, **odadaki herkesi** dinleyip, kimin söylediğinin kendisi için daha "önemli/ilgili" olduğuna karar vermesi gibi.

**Multi-Head Attention:** ViT, bu dikkat mekanizmasını **paralel olarak birden fazla kez** (birden fazla "kafa" ile) çalıştırır — her biri farklı bir ilişki türüne odaklanabilir (biri renk benzerliğine, biri şekil benzerliğine bakabilir gibi).

### Adım 5 — Sınıflandırma (MLP Head)
Tüm bu işlemlerden sonra, özel bir "[CLS] token" (sınıflandırma jetonu) adı verilen ekstra bir vektör, tüm parçalardan topladığı bilgiyle son bir katmandan (MLP — çok katmanlı algılayıcı) geçirilir ve nihai tahmin (örneğin "bu resim bir kedi") üretilir.

---

## 3. CNN ile ViT Karşılaştırması

| Özellik | CNN (YOLOv5'in kullandığı) | ViT |
|---|---|---|
| **Görüntüyü işleme şekli** | Yerel filtrelerle, adım adım (hiyerarşik) | Tüm resme aynı anda, global ilişkilerle |
| **Veri ihtiyacı** | Az veri ile bile iyi çalışabilir | Genelde **çok büyük** veri setleri gerektirir |
| **Hesaplama maliyeti** | Görece düşük | Yüksek (özellikle büyük resimlerde) |
| **Yerleşik önyargı (inductive bias)** | Var — "yakın pikseller ilişkilidir" varsayımı gömülü | Yok — model bu ilişkiyi sıfırdan öğrenmek zorunda |
| **Küçük veri setinde performans** | Genelde daha iyi | Genelde daha zayıf (veri azsa overfitting riski yüksek) |
| **Büyük veri setinde performans** | İyi | Genelde CNN'i geçebilir |

### Önemli Not
Senin şu ana kadar eğittiğin fil/kedi/köpek modelin gibi **küçük-orta boyutlu veri setlerinde**, CNN tabanlı YOLOv5 hâlâ pratik ve güçlü bir seçimdir — çünkü CNN'in "yakın pikseller birbiriyle ilişkilidir" varsayımı, az veriyle bile işe yarar. ViT'nin gerçek gücünü göstermesi için genelde **milyonlarca** görüntüden oluşan veri setleri (örneğin ImageNet) gerekir.

---

## 4. Pratik Kullanım Alanları

- **Görüntü sınıflandırma:** Google'ın orijinal ViT makalesinde tanıttığı temel görev
- **Nesne tespiti:** DETR (Detection Transformer) gibi modeller, ViT mantığını nesne tespiti için uyarlar (senin YOLOv5'in yaptığı işi farklı bir mimariyle yapar)
- **Görüntü segmentasyonu:** SAM (Segment Anything Model, Meta tarafından geliştirildi) ViT tabanlıdır
- **Hibrit modeller:** Bazı modern YOLO sürümleri (örneğin YOLOv8'in bazı varyantları) CNN ve Transformer bileşenlerini birlikte kullanır — "en iyi iki dünyayı" birleştirmeye çalışır

---

## 5. Sonuç

ViT, görüntü işlemeye "yerel/hiyerarşik" bakış yerine "global/ilişkisel" bir bakış açısı getirerek alanda önemli bir paradigma değişikliği yarattı. Ancak bu, CNN'in "öldüğü" anlamına gelmez. İki mimari de birbirini tamamlayan güçlü yönlere sahiptir ve modern araştırmalar giderek bu ikisini **hibrit** şekilde birleştirmeye yönelmektedir.

---

## 6. Öğrenme Notu / Sıradaki Adım

Bu kavramları daha somut hale getirmek istersen:
- `transformers` (Hugging Face) kütüphanesini kurup, önceden eğitilmiş bir ViT modelini (`google/vit-base-patch16-224`) senin fil/kedi/köpek resimlerinden biriyle test edebilirsin
- Kendi ViT modelini sıfırdan eğitmek, veri seti boyutun göz önüne alındığında şu an için pratik olmayabilir — bu genelde büyük şirketlerin/araştırma laboratuvarlarının önceden eğittiği modelleri "fine-tune" ederek (küçük bir veri setiyle ince ayar yaparak) kullanılır