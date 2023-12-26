from flask import Flask, request, render_template_string, send_from_directory
from pathlib import Path

app = Flask(__name__)
UPLOAD_FOLDER = Path('./files')
PUBLIC_FOLDER = Path('./public')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PUBLIC_FOLDER'] = PUBLIC_FOLDER

# 確保上傳目錄和公開目錄存在
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
PUBLIC_FOLDER.mkdir(parents=True, exist_ok=True)

@app.route('/list_files')
def list_files():
    files = [f.name for f in PUBLIC_FOLDER.iterdir() if f.is_file()]
    return render_template_string('''
        <!doctype html>
        <title>檔案列表</title>
        <h1>可下載的檔案</h1>
        <ul>
            {% for file in files %}
                <li><a href="{{ url_for('download_file', filename=file) }}">{{ file }}</a></li>
            {% endfor %}
        </ul>
        <a href="/">返回上傳頁面</a>
    ''', files=files)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['PUBLIC_FOLDER'], filename)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist('file')
        upload_statuses = []

        for file in files:
            if file.filename:
                file.save(UPLOAD_FOLDER / file.filename)
                upload_statuses.append(f'檔案 "{file.filename}" 上傳成功')
            else:
                upload_statuses.append('未選擇檔案或檔案名稱為空')

        return render_template_string('''
            <!doctype html>
            <title>上傳結果</title>
            <h1>上傳結果</h1>
            {% for status in upload_statuses %}
                <p>{{ status }}</p>
            {% endfor %}
            <a href="/">返回上傳頁面</a>
        ''', upload_statuses=upload_statuses)

    return '''
    <!doctype html>
    <title>上傳新檔案</title>
    <h1>上傳新檔案</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file multiple>
      <input type=submit value=上傳>
    </form>
    <a href="/list_files">瀏覽可下載檔案</a>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
