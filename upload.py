# 安装所需的库
# pip install flask

from flask import Flask, request, send_from_directory, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'

# 确保上传文件夹存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    # 移除了文件类型检查，允许所有文件
    return True

@app.route('/')
def index():
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

def get_date_time_folder():
    # 获取当前日期和时间
    now = datetime.now()
    date_time_str = now.strftime("%Y-%m-%d-%H-%M-%S")
    # 创建以日期和时间为名称的文件夹路径
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], date_time_str)
    # 如果文件夹不存在，则创建它
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path

@app.route('/', methods=['POST'])
def upload_file():
    print(request.files)  # Log uploaded files
    if 'file' not in request.files:
        print("No 'file' in request.files")
        return redirect(request.url)
    file = request.files['file']
    print(f"Uploaded file: {file.filename}")
    if file.filename == '':
        print("Empty filename")
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = file.filename
        date_time_folder = get_date_time_folder()
        file.save(os.path.join(date_time_folder, filename))
        return f'File {filename} uploaded successfully'
    else:
        print("Invalid file type")
        return 'Invalid file type'


@app.route('/uploads/<date_time>/<filename>')
def uploaded_file(date_time, filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], date_time), filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)