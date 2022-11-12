from flask import Flask, render_template, redirect, request, url_for, Blueprint, flash, request
from sim.mahasiswa.forms import petugas_F, loginpetugas_F, editpetugas_F, pj_F, editpj_F, BasicForm
from sim.models import Tpetugas, Tpj
from sim import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL
import os
import secrets
from sim import app
from PIL import Image


rpetugas = Blueprint('rpetugas', __name__)

@rpetugas.route("/")
def home():
    return render_template("home.html")

@rpetugas.route("/about")
def about():
    return render_template("about.html")

@rpetugas.route("/home2")
def home2():
    return render_template("home2.html")

@rpetugas.route("/data_petugas", methods=['GET', 'POST'])
def data_petugas():
    form = petugas_F()
    if form.validate_on_submit():
        pass_hash=bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        add_petugas = Tpetugas(nama=form.nama.data, email=form.email.data, password=pass_hash)
        db.session.add(add_petugas)
        db.session.commit()
        flash(f'Akun- {form.nama.data} berhasil daftar', 'info')
        return redirect(url_for('rpetugas.login_petugas'))
    return render_template("data-petugas.html", form=form)


@rpetugas.route("/login_petugas", methods=['GET', 'POST'])
def login_petugas():
    if current_user.is_authenticated:
        return redirect(url_for('rpetugas.home'))
    form = loginpetugas_F()
    if form.validate_on_submit():
        cekemail= Tpetugas.query.filter_by(email=form.email.data).first()
        if cekemail and bcrypt.check_password_hash(cekemail.password, form.password.data):
            login_user(cekemail)
            flash('Selamat Datang Kembali', 'warning')
            return redirect(url_for('rpetugas.akunpetugas'))
        else:
            flash('Login Gagal, Periksa NPM dan Password kembali!', 'danger')
    return render_template("login_petugas.html", form=form)


@rpetugas.route("/akunpetugas")
@login_required
def akunpetugas():
    return render_template('akunpetugas.html')


@rpetugas.route("/logout_petugas")
def logout_petugas():
    logout_user()
    return redirect(url_for('rpetugas.home'))

@rpetugas.route("/pemberitahuan")
@login_required
def pemberitahuan():
    #return redirect(url_for('rpetugas.pemberitahuan'))
    dt_pj=Tpj.query.all()
    return render_template('pemberitahuan.html', dt_pj=dt_pj)


#simpan foto
def simpan_foto(form_foto):
    random_hex= secrets.token_hex(8)
    f_name, f_ext= os.path.splitext(form_foto.filename)
    foto_fn=random_hex + f_ext
    foto_path= os.path.join(app.root_path, 'sim/static/foto', foto_fn)
    ubah_size=(300,300)
    j=Image.open(form_foto)
    j.thumbnail(ubah_size)
    j.save(foto_path)
    #form_foto.save(foto_path)
    return foto_fn

@rpetugas.route("/edit_petugas", methods=['GET', 'POST'])
@login_required
def edit_petugas():
    form=editpetugas_F()
    if form.validate_on_submit():
        if form.foto.data:
            file_foto=simpan_foto(form.foto.data)
            current_user.foto = file_foto
        pass_hash=bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        current_user.nama=form.nama.data
        current_user.email=form.email.data
        current_user.password=pass_hash
        db.session.commit()
        flash('Data Berhasil di Ubah','warning')
        return redirect(url_for('rpetugas.edit_petugas'))
    elif request.method=="GET":
        form.nama.data=current_user.nama
        form.email.data=current_user.email

    return render_template("edit_petugas.html", form=form )


@rpetugas.route("/pj", methods=['GET', 'POST'])
@login_required
def pj():
    dt_pj=Tpj.query.filter_by(petugas_id=current_user.id)
    form=pj_F()
    if form.validate_on_submit():
        #tambah data pengaduan
        add_pj=Tpj(nama=form.nama.data, nohp=form.nohp.data, kategori=form.kategori.data, kategori2=form.kategori2.data, alamat=form.alamat.data, judul_buku=form.judul_buku.data,
        jumlahbuku=form.jumlahbuku.data,penerbit=form.penerbit.data,nama_petugas=form.nama_petugas.data, petugas=current_user)
        db.session.add(add_pj)
        db.session.commit()
        flash('Data Berhasil di Tambahkan','warning')
        return redirect(url_for('rpetugas.pj'))
    return render_template('peminjaman.html', form=form, dt_pj=dt_pj)


@rpetugas.route("/pj/<int:ed_id>/update", methods=['GET', 'POST'])
@login_required
def update_pj(ed_id):
    form=editpj_F()
    dt_pj=Tpj.query.get_or_404(ed_id)
    if request.method=="GET":
        form.nama.data=dt_pj.nama
        form.nohp.data=dt_pj.nohp
        form.kategori.data=dt_pj.kategori
        form.kategori2.data=dt_pj.kategori2
        form.alamat.data=dt_pj.alamat
        form.judul_buku.data=dt_pj.judul_buku
        form.jumlahbuku.data=dt_pj.jumlahbuku
        form.penerbit.data=dt_pj.penerbit
        form.nama_petugas.data=dt_pj.nama_petugas

    elif form.validate_on_submit():
        dt_pj.nama= form.nama.data
        dt_pj.nohp=form.nohp.data
        dt_pj.kategori=form.kategori.data
        dt_pj.kategori2=form.kategori2.data
        dt_pj.alamat=form.alamat.data
        dt_pj.judul_buku=form.judul_buku.data
        dt_pj.jumlahbuku=form.jumlahbuku.data
        dt_pj.penerbit=form.penerbit.data
        dt_pj.nama_petugas=form.nama_petugas.data
        db.session.commit()
        flash('Data Berhasil di Ubah', 'warning')
        return redirect(url_for('rpetugas.pj'))
    return render_template('edit_peminjaman.html', form=form)

@rpetugas.route("/delete/<id>", methods=['GET', 'POST'])
@login_required
def hapus_pj(id):
    h_pj=Tpj.query.get(id)
    db.session.delete(h_pj)
    db.session.commit()
    flash('Data Berhasil di Hapus', 'warning')
    return redirect(url_for('rpetugas.pemberitahuan'))


@rpetugas.route("/pj/<int:ed_id>/detail_pj", methods=['GET', 'POST'])
@login_required
def detail_pj(ed_id):
    dt_pj=Tpj.query.get_or_404(ed_id)
    return render_template('detail_pj.html', dt_pj=dt_pj)

@rpetugas.route("/pj/<int:ed_id>/search_pj", methods=['GET', 'POST'])
@login_required
def search_pj(ed_id):
    form = BasicForm()
    dt_pj=Tpj.query.get_or_404(ed_id)
    if request.method=="GET":
        return redirect(url_for('rpetugas.pj'))
    return render_template('pemberitahuan.html', dt_pj=dt_pj)