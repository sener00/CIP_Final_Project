import math
import random
import pygame

# ====================== AYARLAR ======================
GENISLIK = 900
YUKSEKLIK = 600
FPS = 60
UST_BANT = 70               # üstteki yazı alanının yüksekliği (piksel)

BEKLEME_SURESI = 300        # tuşlar arası bekleme (ms)

MAKS_SEKIL = 400            # ekranda aynı anda en fazla bu kadar şekil
SEKIL_CARPANI = 1           # basılan rakam × bu sayı kadar şekil eklenir
TIKLAMA_SEKIL_ADEDI = 10    # sol tıkta aynı anda eklenecek şekil sayısı
GERI_SAYIM_SURESI = 3       # çıkıştan önceki geri sayım (saniye)

ARKA_PLAN = (20, 20, 30)

pygame.init()
ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Rastgele Şekil Aracı")
saat = pygame.time.Clock()
yazi_tipi = pygame.font.SysFont("arial", 18)
buyuk_yazi = pygame.font.SysFont("arial", 180, bold=True)
orta_yazi = pygame.font.SysFont("arial", 32)

# Geri sayım sırasında ekranı karartmak için yarı saydam bir katman
karartma = pygame.Surface((GENISLIK, YUKSEKLIK), pygame.SRCALPHA)
karartma.fill((0, 0, 0, 170))


# ====================== YARDIMCI FONKSİYONLAR ======================
def rastgele_renk():
    return (random.randint(60, 255), random.randint(60, 255), random.randint(60, 255))


def koyulastir(renk, oran=0.5):
    return tuple(int(c * oran) for c in renk)


def acilar(n):
    """0 ile 2π arasında eşit aralıklı n açı üretir."""
    return [2 * math.pi * i / n for i in range(n)]


def dondur(noktalar, cx, cy, aci):
    """(0,0) merkezli noktaları aci kadar döndürür ve (cx, cy) merkezine taşır."""
    c, s = math.cos(aci), math.sin(aci)
    return [(cx + px * c - py * s, cy + px * s + py * c) for px, py in noktalar]


def duzgun_kose(yaricaplar):
    """Her köşe için verilen yarıçapa göre (0,0) etrafında noktalar üretir."""
    n = len(yaricaplar)
    return [(r * math.cos(a), r * math.sin(a)) for r, a in zip(yaricaplar, acilar(n))]


# ====================== ŞEKİL ÜRETİCİLERİ ======================
# Her fonksiyon (cx, cy, b, renk, kal, aci) alır ve "öğe" listesi döndürür.
# Öğe = (tip, renk, kalınlık, veri)   tip: "daire", "poligon" veya "cizgi"
# cx, cy = merkez | b = boyut | kal = 0 ise içi dolu | aci = dönüş açısı

def s_daire(cx, cy, b, renk, kal, aci):
    return [("daire", renk, kal, ((cx, cy), b))]


def s_elips(cx, cy, b, renk, kal, aci):
    w, h = b * random.uniform(1.1, 1.6), b * random.uniform(0.5, 0.9)
    nok = [(w * math.cos(t), h * math.sin(t)) for t in acilar(40)]
    return [("poligon", renk, kal, dondur(nok, cx, cy, aci))]


def s_dikdortgen(cx, cy, b, renk, kal, aci):
    w, h = b * random.uniform(0.8, 1.5), b * random.uniform(0.5, 1.2)
    nok = [(-w, -h), (w, -h), (w, h), (-w, h)]
    return [("poligon", renk, kal, dondur(nok, cx, cy, aci))]


def s_ucgen(cx, cy, b, renk, kal, aci):
    return [("poligon", renk, kal, dondur(duzgun_kose([b] * 3), cx, cy, aci))]


def s_cokgen(cx, cy, b, renk, kal, aci):
    nok = duzgun_kose([b] * random.randint(5, 8))
    return [("poligon", renk, kal, dondur(nok, cx, cy, aci))]


def s_yildiz(cx, cy, b, renk, kal, aci):
    uc = random.randint(5, 8)
    ic = random.uniform(0.35, 0.55)
    nok = duzgun_kose([b if i % 2 == 0 else b * ic for i in range(uc * 2)])
    return [("poligon", renk, kal, dondur(nok, cx, cy, aci))]


def s_elmas(cx, cy, b, renk, kal, aci):
    nok = [(0, -b * 1.3), (b * 0.7, 0), (0, b * 1.3), (-b * 0.7, 0)]
    return [("poligon", renk, kal, dondur(nok, cx, cy, aci))]


def s_arti(cx, cy, b, renk, kal, aci):
    t = b * 0.35
    nok = [(-t, -b), (t, -b), (t, -t), (b, -t), (b, t), (t, t),
           (t, b), (-t, b), (-t, t), (-b, t), (-b, -t), (-t, -t)]
    return [("poligon", renk, kal, dondur(nok, cx, cy, aci))]


def s_ok(cx, cy, b, renk, kal, aci):
    nok = [(-b, -b * 0.3), (0, -b * 0.3), (0, -b * 0.7), (b, 0),
           (0, b * 0.7), (0, b * 0.3), (-b, b * 0.3)]
    return [("poligon", renk, kal, dondur(nok, cx, cy, aci))]


def s_kalp(cx, cy, b, renk, kal, aci):
    nok = []
    for t in acilar(50):
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        nok.append((x * b / 14, y * b / 14))
    return [("poligon", renk, kal, dondur(nok, cx, cy, aci))]


def s_cicek(cx, cy, b, renk, kal, aci):
    yaprak = random.randint(4, 9)
    nok = [(b * (0.4 + 0.6 * abs(math.cos(yaprak * t / 2))) * math.cos(t),
            b * (0.4 + 0.6 * abs(math.cos(yaprak * t / 2))) * math.sin(t))
           for t in acilar(90)]
    return [("poligon", renk, kal, dondur(nok, cx, cy, aci)),
            ("daire", koyulastir(renk, 0.4), 0, ((cx, cy), b * 0.18))]


def s_blob(cx, cy, b, renk, kal, aci):
    """Yumuşak, amorf (belirsiz biçimli) şekil."""
    harmonikler = [(h, random.uniform(0.05, 0.2), random.uniform(0, 2 * math.pi))
                   for h in (2, 3, 4)]
    nok = []
    for t in acilar(60):
        r = b * (1 + sum(a * math.sin(h * t + f) for h, a, f in harmonikler))
        nok.append((r * math.cos(t), r * math.sin(t)))
    return [("poligon", renk, kal, dondur(nok, cx, cy, aci))]


def s_duzensiz(cx, cy, b, renk, kal, aci):
    """Köşeli, kırık amorf şekil."""
    nok = duzgun_kose([random.uniform(0.4, 1.0) * b for _ in range(random.randint(7, 12))])
    return [("poligon", renk, kal, dondur(nok, cx, cy, aci))]


def s_pasta(cx, cy, b, renk, kal, aci):
    aci_aralik = random.uniform(1.5, 5.0)
    nok = [(0, 0)] + [(b * math.cos(aci_aralik * i / 20), b * math.sin(aci_aralik * i / 20))
                      for i in range(21)]
    return [("poligon", renk, kal, dondur(nok, cx, cy, aci))]


def s_halka(cx, cy, b, renk, kal, aci):
    return [("daire", rastgele_renk() if i else renk, 4, ((cx, cy), b * oran))
            for i, oran in enumerate((1.0, 0.65, 0.3))]


def s_hedef(cx, cy, b, renk, kal, aci):
    return [("daire", renk if i % 2 == 0 else koyulastir(renk), 0, ((cx, cy), b * oran))
            for i, oran in enumerate((1.0, 0.75, 0.5, 0.25))]


def s_bulut(cx, cy, b, renk, kal, aci):
    return [("daire", renk, 0, ((cx + random.uniform(-b * 0.8, b * 0.8),
                                 cy + random.uniform(-b * 0.4, b * 0.4)),
                                b * random.uniform(0.35, 0.6)))
            for _ in range(random.randint(4, 6))]


def s_gunes(cx, cy, b, renk, kal, aci):
    kalinlik = random.randint(2, 5)
    ogeler = [("daire", renk, 0, ((cx, cy), b * 0.5))]
    for t in acilar(12):
        p1 = (cx + b * 0.7 * math.cos(t), cy + b * 0.7 * math.sin(t))
        p2 = (cx + b * 1.2 * math.cos(t), cy + b * 1.2 * math.sin(t))
        ogeler.append(("cizgi", renk, kalinlik, [p1, p2]))
    return ogeler


def s_carpi(cx, cy, b, renk, kal, aci):
    kalinlik = random.randint(3, 6)
    return [("cizgi", renk, kalinlik, dondur([(-b, -b), (b, b)], cx, cy, aci)),
            ("cizgi", renk, kalinlik, dondur([(-b, b), (b, -b)], cx, cy, aci))]


def s_spiral(cx, cy, b, renk, kal, aci):
    nok = []
    for i in range(80):
        t = 5 * math.pi * i / 79
        r = b * t / (5 * math.pi)
        nok.append((r * math.cos(t), r * math.sin(t)))
    return [("cizgi", renk, random.randint(2, 4), dondur(nok, cx, cy, aci))]


def s_zikzak(cx, cy, b, renk, kal, aci):
    nok = [(-b + 2 * b * i / 8, b * 0.4 * (1 if i % 2 == 0 else -1)) for i in range(9)]
    return [("cizgi", renk, random.randint(3, 6), dondur(nok, cx, cy, aci))]


def s_dalga(cx, cy, b, renk, kal, aci):
    nok = []
    for i in range(40):
        t = i / 39
        nok.append(((-1.3 + 2.6 * t) * b, 0.4 * b * math.sin(t * 4 * math.pi)))
    return [("cizgi", renk, random.randint(3, 6), dondur(nok, cx, cy, aci))]


SEKIL_URETICILERI = {
    "daire": s_daire, "elips": s_elips, "dikdortgen": s_dikdortgen,
    "ucgen": s_ucgen, "cokgen": s_cokgen, "yildiz": s_yildiz,
    "elmas": s_elmas, "arti": s_arti, "ok": s_ok, "kalp": s_kalp,
    "cicek": s_cicek, "blob": s_blob, "duzensiz": s_duzensiz,
    "pasta": s_pasta, "halka": s_halka, "hedef": s_hedef,
    "bulut": s_bulut, "gunes": s_gunes, "carpi": s_carpi,
    "spiral": s_spiral, "zikzak": s_zikzak, "dalga": s_dalga,
}

# Tür isimlerinin listesi (bir kez hazırlanır)
SEKIL_TURLERI = list(SEKIL_URETICILERI.keys())


def rastgele_sekil_olustur(konum=None):
    """Rastgele özelliklere sahip bir şekil üretir.
    konum verilirse (tıklama gibi) şekil o noktanın çevresine yerleşir."""
    tur = random.choice(SEKIL_TURLERI)
    b = random.randint(18, 65)
    pay = int(b * 1.7)

    if konum is None:
        cx = random.randint(pay, GENISLIK - pay)
        cy = random.randint(UST_BANT + pay, YUKSEKLIK - pay)
    """ else:
        cx = konum[0] + random.randint(-300, 300)              mouse tıklandığında şekilleri imleç çevresine yakın oluşturur
        cy = konum[1] + random.randint(-300, 300)
        cx = max(pay, min(GENISLIK - pay, cx))
        cy = max(UST_BANT + pay, min(YUKSEKLIK - pay, cy)) """

    renk = rastgele_renk()
    kal = random.choice([0, 0, 0, 3])          # 0 = içi dolu, 3 = sadece çerçeve
    aci = random.uniform(0, 2 * math.pi)

    return {"tur": tur, "ogeler": SEKIL_URETICILERI[tur](cx, cy, b, renk, kal, aci)}


def sekli_ciz(sekil):
    for tip, renk, kal, veri in sekil["ogeler"]:
        if tip == "daire":
            merkez, yaricap = veri
            pygame.draw.circle(ekran, renk, (int(merkez[0]), int(merkez[1])),
                               max(1, int(yaricap)), kal)
        elif tip == "poligon":
            pygame.draw.polygon(ekran, renk, veri, kal)
        elif tip == "cizgi":
            pygame.draw.lines(ekran, renk, False, veri, kal)


def sekil_ekle(sekiller, adet, konum=None):
    for _ in range(adet):
        sekiller.append(rastgele_sekil_olustur(konum))
    while len(sekiller) > MAKS_SEKIL:
        sekiller.pop(0)                         # en eski şekilleri sil


# ====================== PROGRAM DURUMU ======================
sekiller = []
son_giris_zamani = -BEKLEME_SURESI
uyari_bitis_zamani = 0
kapaniyor = False
kapanis_baslangic = 0



def giris_isle(simdi, adet):
    """Klavye ve fare için ortak giriş kontrolü.
    Bekleme süresi dolduysa şekil ekler, dolmadıysa uyarı gösterir."""
    global son_giris_zamani, uyari_bitis_zamani

    if simdi - son_giris_zamani >= BEKLEME_SURESI:
        sekil_ekle(sekiller, adet)
        son_giris_zamani = simdi
    else:
        uyari_bitis_zamani = simdi + 1000    # uyarıyı 1 sn göster


# ====================== ANA DÖNGÜ ======================
calisiyor = True
while calisiyor:
    simdi = pygame.time.get_ticks()

    # 1) OLAYLAR
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calisiyor = False

        elif olay.type == pygame.KEYDOWN:
            if olay.key == pygame.K_SPACE and not kapaniyor:
                kapaniyor = True
                kapanis_baslangic = simdi
            elif not kapaniyor and pygame.K_1 <= olay.key <= pygame.K_9:
                giris_isle(simdi, (olay.key - pygame.K_0) * SEKIL_CARPANI)

        elif olay.type == pygame.MOUSEBUTTONDOWN and olay.button == 1 and not kapaniyor:
            giris_isle(simdi, TIKLAMA_SEKIL_ADEDI)

    # 2) ÇİZİM
    ekran.fill(ARKA_PLAN)
    for sekil in sekiller:
        sekli_ciz(sekil)

    # Üst bant (şekiller yazının altında kalmasın)
    pygame.draw.rect(ekran, ARKA_PLAN, (0, 0, GENISLIK, UST_BANT))
    talimat = yazi_tipi.render(
        "1-9: şekil ekle (tuşlar arası 0.3 sn bekleme)  |  Sol tık: çoklu şekil  |  Boşluk: çıkış",
        True, (230, 230, 230))
    ekran.blit(talimat, (15, 8))

    kalan = BEKLEME_SURESI - (simdi - son_giris_zamani)
    if simdi < uyari_bitis_zamani:
        durum = yazi_tipi.render("Çok hızlısın! Tuşlar arasında 0.3 saniye beklemelisin.",
                                 True, (255, 90, 90))
    elif kalan > 0:
        durum = yazi_tipi.render(f"Bekleyin: {kalan / 1000:.1f} sn", True, (255, 200, 80))
    else:
        durum = yazi_tipi.render("Hazır! Bir tuşa basabilirsin", True, (120, 255, 120))
    ekran.blit(durum, (15, 38))

    sayac = yazi_tipi.render(f"Şekil sayısı: {len(sekiller)}", True, (160, 160, 200))
    ekran.blit(sayac, (GENISLIK - sayac.get_width() - 15, 38))

    # 3) KAPANIŞ GERİ SAYIMI
    if kapaniyor:
        gecen = simdi - kapanis_baslangic
        if gecen >= GERI_SAYIM_SURESI * 1000:
            calisiyor = False
        else:
            ekran.blit(karartma, (0, 0))
            sayi = GERI_SAYIM_SURESI - gecen // 1000
            sayi_yuzey = buyuk_yazi.render(str(sayi), True, (255, 255, 255))
            ekran.blit(sayi_yuzey, sayi_yuzey.get_rect(center=(GENISLIK // 2, YUKSEKLIK // 2 - 20)))
            mesaj = orta_yazi.render("Program kapanıyor...", True, (255, 200, 80))
            ekran.blit(mesaj, mesaj.get_rect(center=(GENISLIK // 2, YUKSEKLIK // 2 + 110)))

    pygame.display.flip()
    saat.tick(FPS)

pygame.quit()