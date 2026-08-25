# Multispektral ve Hiperspektral Kameralar

## 1. Önce Temel Kavramı Anlayalım: Normal Kamera Ne Görür?

Kullandığın normal bir kamera (telefonundaki ya da `cv2.imread()` ile okuduğun resimler), dünyayı sadece **3 renk kanalı** ile görür: **Kırmızı (R), Yeşil (G), Mavi (B)** — buna RGB denir. Bu, insan gözünün algıladığı ışık aralığına (görünür ışık spektrumu) denk gelir.

Ama gerçekte ışık, çok daha geniş bir "elektromanyetik spektrum" içinde var olur — insan gözünün göremediği kızılötesi (infrared), morötesi (ultraviyole) gibi bölgeler de dahil. Multispektral ve hiperspektral kameralar, işte bu **görünmeyen** bölgeleri de "görebilen" özel kameralardır.

### Basit bir benzetme
Normal bir kamerayı, sadece 3 rengi ayırt edebilen (kırmızı, yeşil, mavi) bir insana benzet. Multispektral/hiperspektral kamera ise, aynı manzaraya bakıp *"burada 50 farklı renk tonu var, hatta gözünün göremediği ışık türlerini de sayabiliyorum"* diyebilen süper bir göz gibidir.

## 2. Multispektral Kamera Nedir?

**Tanım:** Görüntüyü, görünür ışığın ötesinde birkaç (genelde **3-15 arası**) ayrı "bant" (dalga boyu aralığı) halinde yakalayan kameradır.

### Nasıl çalışır?
- Her "bant", elektromanyetik spektrumun belirli, **birbirinden ayrı ve geniş** bir dilimini temsil eder (örneğin: kırmızı, yeşil, mavi, kızılötesi-yakın (NIR), kızılötesi-uzak gibi)
- Kamera, bu bantların her biri için **ayrı bir sensör veya filtre** kullanır
- Sonuç: her piksel için, örneğin 5 farklı sayı (5 bant değeri) elde edersin — normal RGB'de sadece 3 sayı vardı

### Örnek kullanım alanları
- **Tarım:** Bitkilerin sağlığını, klorofil (yeşillik) miktarını, su stresini tespit etmek (bitkiler kızılötesi ışığı farklı yansıtır)
- **Uydu görüntüleme:** Google Earth, hava durumu uyduları — kara, deniz, bulut, orman gibi yüzeyleri ayırt etmek
- **Güvenlik/Askeri:** Kamuflajı tespit etmek (insan gözüne yeşil görünen bir kamuflaj kumaşı, kızılötesi bantta bitkilerden farklı görünebilir)

## 3. Hiperspektral Kamera Nedir?

**Tanım:** Multispektral'in çok daha "detaylı" versiyonu — genelde **onlarca, hatta yüzlerce** (bazen 200+) dar ve **birbirine bitişik** bantta görüntü yakalayan kameradır.

### Nasıl çalışır?
- Her piksel için, adeta **mini bir ışık spektrumu grafiği (spektral imza)** elde edilir — her madde, yansıttığı ışığın dalga boyu dağılımıyla kendine özgü bir "parmak izi" bırakır
- Bantlar o kadar dar ve sık aralıklıdır ki, sonuç 2D bir resim değil, **3 boyutlu bir veri küpü (hyperspectral cube)** gibi düşünülür: (yükseklik × genişlik × bant sayısı)
- Bu sayede sadece "bu nesne yeşil mi kırmızı mı" değil, "bu nesne **hangi maddeden** yapılmış" gibi sorulara bile cevap bulunabilir

### Örnek kullanım alanları
- **Mineral/maden tespiti:** Kayaların içindeki mineral türünü, kazı yapmadan uzaktan belirlemek
- **Tıp:** Cilt altındaki dokuları, tümörleri, kan akışını görüntüleme (ameliyat sırasında sağlıklı/hastalıklı doku ayrımı)
- **Gıda kalite kontrolü:** Meyvenin çürük mü taze mi olduğunu, insan gözü fark etmeden önce tespit etmek
- **Çevre izleme:** Su kirliliğini, hava kalitesini uzaktan analiz etmek

## 4. Multispektral vs Hiperspektral: Karşılaştırma Tablosu

| Özellik | Multispektral | Hiperspektral |
|---|---|---|
| **Bant sayısı** | Az (3-15 civarı) | Çok (genelde 100-300+) |
| **Bant genişliği** | Geniş, birbirinden ayrı (discrete) | Dar, bitişik (continuous) |
| **Veri boyutu** | Küçük/orta | Çok büyük |
| **İşlem gücü ihtiyacı** | Düşük-orta | Yüksek |
| **Maliyet** | Görece ucuz | Pahalı, özel donanım gerektirir |
| **Kullanım örneği** | Tarım drone'ları, uydular | Laboratuvar analizleri, tıbbi görüntüleme |
| **Elde edilen bilgi** | "Bu alan sağlıklı bitki mi?" gibi genel kategoriler | "Bu bitkinin tam olarak hangi hastalığı var?" gibi detaylı analiz |

### Basit bir benzetme ile özetle
- **RGB kamera** → 3 renkli kalemle resim çizmek gibi
- **Multispektral kamera** → 10 renkli kalemle çizmek gibi, daha fazla detay yakalarsın
- **Hiperspektral kamera** → 200 tonlu profesyonel bir boya paleti kullanmak gibi, neredeyse her rengin tam tonunu ayırt edebilirsin

## 5. Bu Teknoloji AI/Bilgisayarlı Görü ile Nasıl Buluşuyor?

YOLOv5 ile yapılan çalışmalara benzer şekilde, bu kameralardan gelen veriler de **derin öğrenme modellerine** beslenebilir — ama önemli bir fark var:

- Normal YOLOv5, 3 kanallı (RGB) resimlerle eğitilmiştir
- Multispektral/hiperspektral veriyle çalışmak için, modelin **giriş katmanını** (kaç kanal kabul ettiğini) değiştirmek gerekir — örneğin 3 kanal yerine 8 ya da 200 kanal kabul edecek şekilde
- Bu alan, özellikle **hassas tarım (precision agriculture)** ve **uzaktan algılama (remote sensing)** alanlarında hızla büyüyen bir AI araştırma konusu


- **"Hyperspectral image classification deep learning"** — bu alanda kullanılan AI modelleri
- **NDVI (Normalized Difference Vegetation Index)** — multispektral tarım görüntülerinde bitki sağlığını ölçmek için kullanılan basit ama güçlü bir formül
- **Python kütüphaneleri:** `spectral` (Python) ve `rasterio`, bu tür çok bantlı görüntü verilerini okumak için kullanılan araçlardır — tıpkı  `cv2.imread()` gibi, ama çok kanallı veriler için