# Thresholding (Eşikleme) Nedir?

Bir görüntüdeki piksel değerlerini, belirlenen bir eşik (threshold) değerine göre ikiye (veya birkaç sınıfa) ayırma işlemidir. Genellikle gri tonlamalı bir görüntüde her piksel, eşik değerinin üstündeyse beyaz (255), altındaysa siyah (0) yapılır. Sonuç olarak binary (ikili) görüntü elde edilir.

# Temel mantık

    python
    import cv2

    img = cv2.imread('resim.jpg', cv2.IMREAD_GRAYSCALE)
    _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

Burada 127 eşik değeri, 255 ise eşiği geçen piksellere atanacak değer.

# Thresholding Türleri (OpenCV'de)

Tür	                            Açıklama

THRESH_BINARY	        Eşik üstü → 255, altı → 0
THRESH_BINARY_INV	    Tam tersi
THRESH_TRUNC	        Eşik üstü değerler eşik değerine sabitlenir
THRESH_TOZERO	        Eşik altı pikseller 0 yapılır, üstü aynı kalır
THRESH_OTSU	            Eşik değeri otomatik (istatistiksel olarak) belirlenir
Adaptive Thresholding	Görüntünün farklı bölgeleri için farklı eşik değerleri hesaplanır. 
                        (ışık değişimi olan görüntülerde daha iyi sonuç verir)

# Hangi Alanlarda Kullanılır?

Görüntü işleme / Bilgisayarlı görü (Computer Vision): Nesne-arkaplan ayrımı, kontur (contour) bulma öncesi ön işlem

OCR (metin tanıma): Taranmış belgelerdeki yazıyı arkaplandan ayırmak için

Tıbbi görüntüleme: MR/röntgen görüntülerinde tümör, doku gibi bölgelerin segmentasyonu

Endüstriyel kalite kontrol: Kusur tespiti, parça sayımı

Robotik/otonom sistemler: Şerit takibi, engel tespiti gibi basit segmentasyon işlemlerinde (senin Husky projene benzer senaryolarda YOLO öncesi ön işleme adımı olarak da kullanılabilir)

Belge tarama ve arşivleme: Siyah-beyaz belge dönüşümleri

Parmak izi / biyometrik analiz: Desenlerin netleştirilmesi