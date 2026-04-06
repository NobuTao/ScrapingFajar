import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin # Untuk merapikan link yang tidak lengkap

def scrape_semua_elemen(url):
    # 1. Penyamaran (User-Agent)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        print(f"Memproses: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"Gagal! Status code: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        # 2. Ekstraksi Berbagai Jenis Elemen
        
        # Ambil Judul Utama (H1)
        judul_utama = soup.find('h1').get_text(strip=True) if soup.find('h1') else "N/A"

        # Ambil semua Sub-judul (H2 dan H3)
        sub_judul = [h.get_text(strip=True) for h in soup.find_all(['h2', 'h3'])]

        # Ambil semua Paragraf (P)
        paragraf = [p.get_text(strip=True) for p in soup.find_all('p') if len(p.get_text(strip=True)) > 0]

        # Ambil semua Link (A) - Kita ambil teks link dan URL-nya
        links = []
        for a in soup.find_all('a', href=True):
            link_data = {
                'teks': a.get_text(strip=True),
                'url': urljoin(url, a['href']) # Mengubah link relatif jadi link lengkap
            }
            if link_data['teks']: # Hanya ambil yang ada teksnya agar rapi
                links.append(link_data)

        # Ambil semua Gambar (IMG)
        gambar = []
        for img in soup.find_all('img', src=True):
            img_url = urljoin(url, img['src'])
            alt_text = img.get('alt', 'Tidak ada deskripsi')
            gambar.append({'src': img_url, 'alt': alt_text})

        # 3. Gabungkan semua ke dalam satu struktur Data
        hasil_akhir = {
            'metadata': {
                'url_sumber': url,
                'total_paragraf': len(paragraf),
                'total_link': len(links),
                'total_gambar': len(gambar)
            },
            'konten': {
                'judul_h1': judul_utama,
                'sub_judul': sub_judul,
                'isi_paragraf': paragraf,
                'daftar_link': links,
                'daftar_gambar': gambar
            }
        }

        # 4. Simpan ke JSON
        nama_file = 'data_scraping_fajar.json'
        with open(nama_file, 'w', encoding='utf-8') as f:
            json.dump(hasil_akhir, f, ensure_ascii=False, indent=4)

        print(f"--- SELESAI ---")
        print(f"Data berhasil disimpan di: {nama_file}")

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

# Jalankan fungsi dengan URL targetmu
if __name__ == "__main__":
    target = 'https://gudangssl.id/blog/cara-membuat-blog-di-blogger/'
    scrape_semua_elemen(target)