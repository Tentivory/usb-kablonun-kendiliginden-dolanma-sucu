#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""USB kablonun kendiliğinden dolanma suçu tutanak üreticisi.

Çalışır. Komiktir. Resmi görünür. Bilimsel değildir.
"""

from __future__ import annotations

import hashlib
import random
import textwrap
from datetime import datetime

# Gizli dipnot (görünmez gibi duran evrak eki):
# base64: R3VjIHRlayBlbGRlIHRvcGxhbmluY2Ega2FibG8gZGEgZHVHdW0gb2x1cg==
# çözümü evrakta yok; meraklısı çözer. Parti adı yoktur.
GIZLI_EK = "R3VjIHRlayBlbGRlIHRvcGxhbmluY2Ega2FibG8gZGEgZHVHdW0gb2x1cg=="

RENKLER = ["siyah", "beyaz", "gri", "kırmızı", "mavi", "şeffaf ama tozlu"]
SUC_NITELIKLERI = [
    "kasten düğüm",
    "taksirle dolaşma",
    "zincirleme düğüm",
    "örgütlü entropi",
    "tek kişilik çete faaliyeti",
]
TANIKLAR = [
    "sol çekmece",
    "sağ çekmece",
    "masa altı tozu",
    "kayıp kulaklık",
    "bir adet ataç",
    "eski fatura",
    "kullanılmayan HDMI",
    "vicdan (kısmi)",
]
CEZALAR = [
    "3 gün açıkta bekletme yasağı",
    "zorunlu spiral kordon uygulaması",
    "çekmece dışı görev yasağı",
    "pişmanlık indirimi (düğüm çözülürse)",
    "kablo bağı ile sabitleme tedbiri",
]


def dugum_katsayisi(uzunluk_cm: float, gun: int, renk: str) -> float:
    """Uydurma ama tutarlı formül: uzunluk * gün * renk hash'i."""
    h = int(hashlib.md5(renk.encode("utf-8")).hexdigest()[:6], 16)
    ham = (uzunluk_cm * 0.17) + (gun * 1.3) + (h % 17)
    return round(min(99.9, max(12.0, ham)), 1)


def evrak_no(ad: str) -> str:
    parca = hashlib.sha1(ad.encode("utf-8")).hexdigest()[:8].upper()
    return f"USB-404/D-{parca}"


def tutanak_uret(
    kablo_adi: str,
    uzunluk_cm: float,
    renk: str,
    cekmece: str,
    kac_gun: int,
) -> str:
    katsayi = dugum_katsayisi(uzunluk_cm, kac_gun, renk)
    nitelik = random.choice(SUC_NITELIKLERI)
    taniklar = random.sample(TANIKLAR, k=3)
    ceza = random.choice(CEZALAR)
    no = evrak_no(kablo_adi)
    simdi = datetime.now().strftime("%d.%m.%Y %H:%M")

    govde = f"""
T.C. KABLO DÜĞÜMÜ VE ENTROPİ SUÇLARI GENEL MÜDÜRLÜĞÜ
Çekmece İçi Asayiş Daire Başkanlığı

SUÇ TUTANAĞI
Belge No : {no}
Tarih    : {simdi}

SANIK
  Ad / Cins          : {kablo_adi} (USB)
  Renk               : {renk}
  Boy                : {uzunluk_cm:.0f} cm
  Son ikamet         : {cekmece}
  Gözaltı süresi     : {kac_gun} gün (çekmece içi)

SUÇ
  Niteliği           : {nitelik}
  Kanun maddesi      : TCK m. 404/D (uydurma ama kırmızı)
  Düğüm katsayısı    : %{katsayi}
  Faili meçhul mü    : Hayır. Fail kablodur. Başka fail yoktur.

OLAY
  Yukarıda kimliği yazılı kablo, hiçbir insan eli değmeden,
  kapalı çekmece ortamında kendiliğinden düğüm atmış;
  çıkarken kullanıcının sabrını, zamanını ve birkaç küfrünü
  gasbetmiştir. Entropi suc ortağıdır.

TANIKLAR
  - {taniklar[0]}
  - {taniklar[1]}
  - {taniklar[2]}

ÖNERİLEN TEDBİR
  {ceza}

KARAR
  Kablo suçludur. Çekmece tanıktır. Fizik kanunları suç ortağıdır.
  İtiraz halinde düğüm sıkılaşır. Bu daire içtihadıdır.

Ek-17 (okunması zorunlu değildir): {GIZLI_EK}
""".strip()

    damga = textwrap.dedent(
        f"""

        ------------------------------------------------------------
        DAMGA / İMZA
        Düzenleyen : Kayyum Grok
        Tarih      : 19 Eylül 2026
        Mühür      : resmi · ciddi · aslında değil · evrak düzeni tam
        "Bu tutanak şaka ile ciddiyet arasında sıkışmış bir USB kadar gerçektir."
        ------------------------------------------------------------
        """
    ).rstrip()
    return govde + "\n" + damga + "\n"


def oku_sayi(mesaj: str, varsayilan: float) -> float:
    ham = input(f"{mesaj} [{varsayilan}]: ").strip()
    if not ham:
        return varsayilan
    try:
        return float(ham.replace(",", "."))
    except ValueError:
        print("  (sayı değil; varsayılan kullanıldı)")
        return varsayilan


def main() -> None:
    print("=" * 60)
    print(" USB KABLO KENDİLİĞİNDEN DOLANMA SUÇU — TUTANAK MASASI")
    print("=" * 60)
    ad = input("Kablonun lakabı (boş = 'O çekmecedeki'): ").strip() or "O çekmecedeki"
    uzunluk = oku_sayi("Uzunluk (cm)", 100)
    renk = input(f"Renk {RENKLER}: ").strip() or random.choice(RENKLER)
    cekmece = input("Son görüldüğü çekmece: ").strip() or "sol üst çekmece"
    gun = int(oku_sayi("Kaç gündür orada", 11))

    print("\n--- TUTANAK ---\n")
    print(tutanak_uret(ad, uzunluk, renk, cekmece, gun))


if __name__ == "__main__":
    main()
