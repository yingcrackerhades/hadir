try:
    import argparse
    import importlib
    import socket
    import requests
    import sys,os
    from prettytable import PrettyTable
except ImportError as error:
    print("\n[!] Error on import", error)
    print("[!]Please install module using pip\n")


logo = ('''
  _               _ _      
 | |             | (_)     
 | |__   __ _  __| |_ _ __ 
 | '_ \ / _` |/ _` | | '__|
 | | | | (_| | (_| | | |   
 |_| |_|\__,_|\__,_|_|_|(hades dirsearch)                
''')

# Cek koneksi internet
def connect():
  try:
    # Kirim permintaan ke Google
    socket.create_connection(("www.google.com", 80))
    return True
  except OSError:
    pass
  return False

# Cek apakah tersambung ke internet
if not connect():
  print("[!]Tidak tersambung ke internet, periksa jaringan anda!!!")
  sys.exit(1)

# Fungsi untuk mencari file dan directory sesuai wordlist
def search(url, wordlist):
  with open(wordlist, 'r') as f:
  # Baca file wordlist
    lines = f.readlines()

  # Inisialisasi tabel
  table = PrettyTable()
  table.field_names = ['Path', 'Status Code', 'Description']

  # Iterasi melalui setiap baris dalam wordlist
  for line in lines:
    # Buang karakter baris baru di akhir baris
    path = line.rstrip()
    # Buat URL lengkap dengan menggabungkan URL target dengan path
    full_url = 'http://' + url + '/' + path
    # Kirim permintaan HTTP GET ke URL lengkap
    try:
      response = requests.get(full_url)
    except requests.exceptions.RequestException as e:
      # Jika terjadi exception, tambahkan entri ke tabel dengan status code 0
      table.add_row([path, 0, str(e)])
      continue

    # Jika status code bukan 404, tambahkan entri ke tabel
    if response.status_code != 404:
      table.add_row([path, response.status_code, response.reason])

  # Tampilkan tabel
  print(table)

# Parsing argument command line
parser = argparse.ArgumentParser(description='hadir is a dirsearch tool', formatter_class=argparse.RawTextHelpFormatter, epilog='Contoh penggunaan: python hadir.py -u example.com -w wordlist.txt')
parser.add_argument('-u', '--url', help='URL target')
parser.add_argument('-w', '--wordlist', help='Wordlist file')
args = parser.parse_args()

# Cek apakah URL dan wordlist kosong
if args.url is None or args.wordlist is None:
  parser.print_help()
  sys.exit(1)

#cek file wordlist
if not os.path.exists(args.wordlist):
  print(f'[!]Wordlist {args.wordlist} tidak ditemukan')
  sys.exit(1)

# Jalankan fungsi search
try:
  connect()
  print(logo)
  print('\n[!]Scanning Please waiting...')
  search(args.url, args.wordlist)
except KeyboardInterrupt:
  print('\nExiting program...')
  sys.exit(0)
