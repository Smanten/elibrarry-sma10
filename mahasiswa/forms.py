from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from sim.models import Tpetugas
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed



class petugas_F(FlaskForm):
    nama = StringField('Nama', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    kon_pass = PasswordField('Konfirmasi Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrasi')

    #cek email
    def validate_email(self, email):
        cekemail=Tpetugas.query.filter_by(email=email.data).first()
        if cekemail:
            raise ValidationError('Email Sudah Terdaftar, Gunakan Email Yang Lain')


class loginpetugas_F(FlaskForm):
    email= StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class editpetugas_F(FlaskForm):
    nama = StringField('Nama', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    kon_pass = PasswordField('Konfirmasi Password', validators=[DataRequired(), EqualTo('password')])
    foto= FileField('Ubah Foto Profil', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Ubah Data')

    #cek email
    def validate_email(self, email):
        if email.data != current_user.email:
            cekemail=Tpetugas.query.filter_by(email=email.data).first()
            if cekemail:
                raise ValidationError('Email Sudah Terdaftar, Gunakan Email Yang Lain')

class pj_F(FlaskForm):
    nama = StringField('Nama', validators=[DataRequired()])
    nohp = StringField('No HP', validators=[DataRequired(), Length(min=10, max=15)])
    kategori = SelectField(u'Kelas', choices=[('sepuluh','10'), ('sebelas','11'), ('duabelas','12')],  validators=[DataRequired()])
    kategori2 = SelectField(u'Jurusan', choices=[('Ipa','IPA'), ('Ips','IPS')],  validators=[DataRequired()])
    alamat = TextAreaField('Alamat', validators=[DataRequired()])
    judul_buku = StringField('Judul Buku', validators=[DataRequired()])
    jumlahbuku = StringField ('Jumlah Buku', validators=[DataRequired()])
    penerbit = StringField('Penerbit', validators=[DataRequired()])
    nama_petugas = StringField ('Nama Petugas', validators=[DataRequired()])
    submit = SubmitField('Kirim')
    

class editpj_F(FlaskForm):
    nama = StringField('Nama', validators=[DataRequired()])
    nohp = StringField('No HP', validators=[DataRequired(), Length(min=10, max=15)])
    kategori = SelectField(u'Kelas', choices=[('sepuluh','10'), ('sebelas','11'), ('duabelas','12')],  validators=[DataRequired()])
    kategori2 = SelectField(u'Jurusan', choices=[('Ipa','IPA'), ('Ips','IPS')],  validators=[DataRequired()])
    alamat = TextAreaField('Alamat', validators=[DataRequired()])
    judul_buku = StringField('Judul Buku', validators=[DataRequired()])
    jumlahbuku = StringField ('Jumlah Buku', validators=[DataRequired()])    
    penerbit = StringField('Penerbit', validators=[DataRequired()])
    nama_petugas = StringField ('Nama Petugas', validators=[DataRequired()])
    submit = SubmitField('Ubah')

class BasicForm(FlaskForm):
    ids = StringField("Search",validators=[DataRequired()])
    submit = SubmitField("Search")