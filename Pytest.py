import os
import pytest
from unittest.mock import MagicMock
from demo_modul5 import create_pesanan, update_pesanan, delete_pesanan, read_pesanan, load_document, save_document, FILENAME

@pytest.fixture
def mock_load_document(mocker):
    # Mocking load_document agar tidak memerlukan file .docx nyata
    return mocker.patch('demo_modul5.load_document', return_value=MagicMock())

@pytest.fixture
def mock_save_document(mocker):
    # Mocking save_document agar tidak menulis ke file fisik
    return mocker.patch('demo_modul5.save_document')

def test_create_pesanan(mock_load_document, mock_save_document):
    # Mock document
    mock_doc = mock_load_document.return_value
    mock_paragraph = MagicMock()
    mock_doc.add_paragraph.return_value = mock_paragraph

    # Test data
    nama = "John Doe"
    makanan = "Pizza"
    jumlah = "2"
    gambar = "pizza.jpg"

    # Panggil fungsi create_pesanan
    create_pesanan(nama, makanan, jumlah, gambar)

    # Verifikasi bahwa fungsi add_paragraph dipanggil dan text ditambahkan
    mock_doc.add_paragraph.assert_called()
    mock_paragraph.add_run.assert_any_call(f"Nama Pelanggan: {nama}\n")
    mock_paragraph.add_run.assert_any_call(f"Makanan: {makanan}\n")
    mock_paragraph.add_run.assert_any_call(f"Jumlah: {jumlah}\n")
    mock_paragraph.add_run.assert_any_call(f"Image Path: {gambar}\n")
    mock_save_document.assert_called_with(mock_doc)

def test_update_pesanan(mock_load_document, mock_save_document):
    # Mock document dan paragraf
    mock_doc = mock_load_document.return_value
    mock_paragraph = MagicMock()
    mock_doc.paragraphs = [mock_paragraph]

    nama = "John Doe"
    status_baru = "selesai"

    # Menyiapkan paragraf dengan status sebelumnya
    mock_paragraph.text = "Nama Pelanggan: John Doe\nStatus: diproses"

    # Panggil fungsi update_pesanan
    update_pesanan(nama, status_baru)

    # Verifikasi bahwa teks status telah diperbarui
    mock_paragraph.clear.assert_called()
    mock_paragraph.add_run.assert_any_call("Nama Pelanggan: John Doe\nStatus: selesai")

    # Verifikasi save_document dipanggil
    mock_save_document.assert_called_with(mock_doc)

def test_delete_pesanan(mock_load_document, mock_save_document):
    # Mock document dan paragraf
    mock_doc = mock_load_document.return_value
    mock_paragraph = MagicMock()
    mock_doc.paragraphs = [mock_paragraph]

    nama = "John Doe"

    # Menyiapkan paragraf dengan status batal
    mock_paragraph.text = "Nama Pelanggan: John Doe\nStatus: batal"

    # Panggil fungsi delete_pesanan
    delete_pesanan(nama)

    # Verifikasi paragraf dihapus
    mock_paragraph.clear.assert_called()

    # Verifikasi save_document dipanggil
    mock_save_document.assert_called_with(mock_doc)

def test_read_pesanan(mock_load_document, monkeypatch):
    # Mock document dan paragraf
    mock_doc = mock_load_document.return_value
    mock_paragraph1 = MagicMock()
    mock_paragraph1.text = "Pesanan 1"
    mock_paragraph2 = MagicMock()
    mock_paragraph2.text = "Pesanan 2"
    
    mock_doc.paragraphs = [mock_paragraph1, mock_paragraph2]

    # Simpan teks asli yang diharapkan
    expected_output = "Pesanan 1\nPesanan 2\n"

    # Patch fungsi print untuk memverifikasi output
    mock_print = MagicMock()
    monkeypatch.setattr("builtins.print", mock_print)

    # Panggil fungsi read_pesanan
    read_pesanan()

    # Verifikasi bahwa print dipanggil dengan teks yang benar
    mock_print.assert_any_call("Pesanan 1")
    mock_print.assert_any_call("Pesanan 2")

if __name__ == "__main__":
    pytest.main()
