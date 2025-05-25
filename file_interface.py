import os
import json
import base64
from glob import glob


class FileInterface:
    def __init__(self):
        os.makedirs('files', exist_ok=True)
        os.chdir('files/')

    def list(self,params=[]):
        try:
            filelist = glob('*.*')
            print("File list found:", filelist)
            return dict(status='OK',data=filelist)
        except Exception as e:
            print("Error in list:", e)
            return dict(status='ERROR',data=str(e))


    def get(self,params=[]):
        try:
            filename = params[0]
            if (filename == ''):
                return None
            fp = open(f"{filename}",'rb')
            isifile = base64.b64encode(fp.read()).decode()
            return dict(status='OK',data_namafile=filename,data_file=isifile)
        except Exception as e:
            return dict(status='ERROR',data=str(e))

    def upload(self, params=[]):
        try:
            filename = params[0]
            data_base64 = params[1]
            with open(filename, 'wb') as f:
                f.write(base64.b64decode(data_base64))
            return dict(status='OK', data=f'{filename} berhasil diupload')
        except Exception as e:
            return dict(status='ERROR', data=str(e))

    def delete(self, params=[]):
        try:
            filename = params[0]
            if os.path.exists(filename):
                os.remove(filename)
                return dict(status='OK', data=f'{filename} berhasil dihapus')
            else:
                return dict(status='ERROR', data='File tidak ditemukan')
        except Exception as e:
            return dict(status='ERROR', data=str(e))



if __name__ == '__main__':
    f = FileInterface()
    
    print("=== LIST ===")
    print(f.list())

    filename = input("Masukkan nama file yang ingin diambil (GET): ")
    print(f.get([filename]))

    # Upload file dari nama bebas
    file_to_upload = input("Masukkan nama file lokal yang ingin di-upload: ")
    upload_as = input("Simpan di server sebagai nama file: ")
    with open(file_to_upload, "rb") as testfile:
        encoded = base64.b64encode(testfile.read()).decode()
    print(f.upload([upload_as, encoded]))

    # Delete file dengan nama bebas
    to_delete = input("Masukkan nama file yang ingin dihapus dari server: ")
    print(f.delete([to_delete]))
