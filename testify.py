import os
import glob
from flask import Flask, render_template, request, send_file

# Configure Application
app = Flask(__name__)

global filename
global ftype

@app.route("/")
def home():
    # Delete old files
    filelist = glob.glob('uploads/*')
    for f in filelist:
        os.remove(f)
    filelist = glob.glob('downloads/*')
    for f in filelist:
        os.remove(f)
    return render_template("home.html")

# Set the file uploads directory (relative path)
app.config["FILE_UPLOADS"] = os.path.join("uploads")

@app.route("/compress", methods=["GET", "POST"])
def compress():
    if request.method == "GET":
        return render_template("compress.html", check=0)

    else:
        up_file = request.files["file"]

        if len(up_file.filename) > 0:
            global filename
            global ftype
            filename = up_file.filename
            print(up_file.filename)
            up_file.save(os.path.join(app.config["FILE_UPLOADS"], filename))
            os.system('c.exe uploads\\{}'.format(filename))
            filename = filename[:filename.index(".",1)]
            ftype = "-compressed.bin"
            while True:
                if os.path.exists(os.path.join('uploads', '{}-compressed.bin'.format(filename))):
                    os.system('move uploads\\{}-compressed.bin downloads\\'.format(filename))
                    break

            return render_template("compress.html", check=1)

        else:
            print("ERROR")
            return render_template("compress.html", check=-1)

@app.route("/decompress", methods=["GET", "POST"])
def decompress():
    if request.method == "GET":
        return render_template("decompress.html", check=0)

    else:
        up_file = request.files["file"]

        if len(up_file.filename) > 0:
            global filename
            global ftype
            filename = up_file.filename
            print(up_file.filename)
            up_file.save(os.path.join(app.config["FILE_UPLOADS"], filename))
            os.system('d.exe uploads\\{}'.format(filename))
            f = open(os.path.join('uploads', filename), 'rb')
            ftype = "-decompressed." + (f.read(int(f.read(1)))).decode("utf-8")
            filename = filename[:filename.rfind("-")]

            print(filename)

            while True:
                if os.path.exists(os.path.join('uploads', '{}-decompressed.txt'.format(filename))):
                    os.system('move uploads\\{}-decompressed.txt downloads\\'.format(filename))
                    break

            return render_template("decompress.html", check=1)

        else:
            print("ERROR")
            return render_template("decompress.html", check=-1)

@app.route("/download")
def download_file():
    global filename
    global ftype
    path = os.path.join("downloads", filename + ftype)
    return send_file(path, as_attachment=True)

# Restart application whenever changes are made
if __name__ == "__main__":
    app.run(debug=True)
