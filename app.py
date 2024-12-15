# app.py
from flask import Flask, render_template, request
from cf_calculator import calculate_cf

app = Flask(__name__)

penyakit = {
    'P1': 'Anemia',
    'P2': 'Kwashiorkor',
    'P3': 'Marasmus',
    'P4': 'Stunting'
}

gejala_penyakit = {
    'P1': ['G01', 'G02', 'G03', 'G04', 'G05', 'G06'],
    'P2': ['G01', 'G07', 'G08', 'G09', 'G10', 'G11', 'G12', 'G13', 'G14', 'G15'],
    'P3': ['G03', 'G04', 'G05', 'G06', 'G15', 'G16', 'G17', 'G18'],
    'P4': ['G13', 'G15', 'G06', 'G19', 'G20', 'G21']
}

gejala = {
    'G01': 'Merasa kelelahan yang berat dan berlebihan',
    'G02': 'Mengalami pusing yang terus-menerus',
    'G03': 'Mengalami perubahan warna kulit yang pucat dan menguning',
    'G04': 'Mengalami detak jantung yang tidak teratur',
    'G05': 'Memiliki rasa dingin pada tangan dan kaki',
    'G06': 'Mengalami nyeri pada dada',
    'G07': 'Memiliki kulit kering dan bersisik',
    'G08': 'Memiliki rambut yang terlihat kusam dan kering',
    'G09': 'Memiliki perut yang buncit',
    'G10': 'Mengalami hilangnya massa otot',
    'G11': 'Memiliki pembengkakan dibawah kulit (edema)',
    'G12': 'Mengalami perubahan mood yang sering',
    'G13': 'Susah menambah berat dan tinggi badan',
    'G14': 'Mengalami kondisi gigi mudah tanggal atau copot',
    'G15': 'Mengalami masalah perhambatan pada pertumbuhan',
    'G16': 'Mengalami diare kronis',
    'G17': 'Memiliki infeksi saluran pernapasan',
    'G18': 'Sering merasa sangat lapar',
    'G19': 'Memiliki kemampuan fokus dan memori yang kurang baik',
    'G20': 'Cenderung lebih pendiam dan tidak melakukan kontak mata dengan orang disekitarnya',
    'G21': 'Berat badan lebih ringan untuk anak seusianya'
}

cf_pakar = {
    'P1': {'G01': 0.8, 'G02': 0.6, 'G03': 0.8, 'G04': 1, 'G05': 0.4, 'G06': 0.6},
    'P2': {'G01': 0.8, 'G07': 0.6, 'G08': 0.4, 'G09': 0.6, 'G10': 0.4, 'G11': 0.8, 'G12': 0.4, 'G13': 0.8, 'G14': 0.4, 'G15': 0.8},
    'P3': {'G03': 0.8, 'G04': 1, 'G05': 0.4, 'G06': 0.6, 'G15': 0.8, 'G16': 1, 'G17': 0.8, 'G18': 0.6},
    'P4': {'G13': 0.8, 'G15': 0.8, 'G06':0.6, 'G19': 0.8, 'G20': 0.8, 'G21': 0.8}
}

@app.route('/')
def index():
    return render_template('index.html', gejala=gejala)

@app.route('/diagnosis', methods=['POST'])
def diagnosis():
    gejala_terpilih = request.form.getlist('gejala')
    cf_user = {g: float(request.form[g]) for g in gejala_terpilih}

    hasil_diagnosis = {}
    for kode_penyakit, daftar_gejala in gejala_penyakit.items():
        cf_values = [cf_user[g] * cf_pakar[kode_penyakit][g] for g in daftar_gejala if g in cf_user]
        cf_diagnosis = calculate_cf(cf_values) if cf_values else 0
        hasil_diagnosis[penyakit[kode_penyakit]] = cf_diagnosis

    hasil_diagnosis = sorted(hasil_diagnosis.items(), key=lambda x: x[1], reverse=True)
    return render_template('result.html', hasil_diagnosis=hasil_diagnosis)

if __name__ == '__main__':
    app.run(debug=True)