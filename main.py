from flask import Flask, request, redirect, url_for, send_from_directory, render_template
import os

app = Flask(__name__)

# Configuración
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return '''
    <h1>Gestión de Archivos</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <label for="file">Subir archivo:</label>
        <input type="file" name="file" id="file">
        <button type="submit">Subir</button>
    </form>
    <a href="/files">Ver Archivos</a>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No se encontró el archivo", 400
    file = request.files['file']
    if file.filename == '':
        return "No se seleccionó ningún archivo", 400
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return redirect(url_for('home'))

@app.route('/files')
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    if not files:
        return "No hay archivos disponibles"
    return '''
    <h1>Archivos disponibles</h1>
    <ul>
        {}
    </ul>
    <a href="/">Volver</a>
    '''.format(''.join(f'<li><a href="/download/{file}">{file}</a></li>' for file in files))

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")