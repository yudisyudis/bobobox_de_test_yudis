# BOBOBOX DATA ENGINEERING TEST
## YUDISTHIRA IRIANA PUTRA

Seluruh soal yang diberikan dalam test kali ini sudah dirangkum dalam satu struktur folder docker container, sehingga bisa dijalankan dengan perintah 
```
docker compose up --build
```
Soal A, mengenai python coding challenge solusinya ada di file [A_python_solution.py](./docker/script/A_python_solution.py)
Soal B, mengenai query SQL challenge solusinya ada di file [B_querySQL_solution.py](./docker/script/B_querySQL_solution.py)
Soal C, mengenai Data Analysis challenge solusinya ada di file [C_dataAnalysis_solution.py](./docker/script/C_dataAnalysis_solution.py)

dalam project ini, telah disediakan 2 buah sample data yang digunakan untuk Python challenge dan Data Analysis challenge yang saya masukkan di folder [Data](./docker/data). Sementara untuk SQL challenge tidak disediakan data, hanya schema database, sehingga saya mengenerate data sendiri sesuai dengan skema dan skenario soal, yang konfigurasi generate nya saya tampung di folder [Database](./docker/database), di mana di bagian tersebut ada schema table dan insert data table dari keempat table yang diinstruksikan.

seluruh output dari solusi yang telah dijalankan dapat ditemui di folder [Output](./docker/output), satu file hasil solusi python challenge, 2 file hasil query challenge, dan beberapa gambar dan summary dari Data analysis challenge. Sementara untuk soal D terkait database design saya buatkan file DDL-nya.

File dalam bentuk format .ipynb hasil dari eksperimen yang saya lakukan untuk project ini saya tampung juga dalam folder [Jupyter](./docker/jupyter) in case diperlukan.

Demikian hasil pengerjaan project test Data Engineering Bobobox oleh saya, semoga dapat dinilai optimal.
