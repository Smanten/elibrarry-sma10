from datetime import datetime
from sim import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(petugas_id):
    return Tpetugas.query.get(int(petugas_id))


class Tpetugas(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    foto = db.Column(db.String(30), nullable=False, default='default.jpg')
    pjs = db.relationship('Tpj', backref='petugas',lazy=True)

    def __repr__(self):
        return f"Tpetugas('{self.nama}','{self.email}','{self.password}','{self.foto}')"


class Tpj(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(300), nullable=False)
    nohp = db.Column(db.String(12), nullable=False)
    kategori = db.Column(db.String(50), nullable=False)
    kategori2 = db.Column(db.String(50), nullable=False)
    judul_buku = db.Column(db.String(100), nullable=False)
    jumlahbuku= db.Column(db.String(10), nullable=False)
    alamat = db.Column(db.String(300), nullable=False)
    tgl_post = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    penerbit = db.Column(db.String(300), nullable=False)
    nama_petugas = db.Column(db.String(300), nullable=False)
    petugas_id = db.Column(db.Integer, db.ForeignKey('tpetugas.id'), nullable=False)

    def __repr__(self):
        return f"Tpj('{self.nama}','{self.nohp}','{self.kategori}','{self.kategori2}','{self.judul_buku}','{self.jumlahbuku}','{self.alamat}','{self.tgl_post}','{self.penerbit}','{self.nama_petugas}')"