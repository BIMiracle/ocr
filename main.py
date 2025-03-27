from flask import Flask, request, jsonify, send_from_directory, Response
import os
import wcocr
import uuid
import base64
from mimetypes import guess_type

app = Flask(__name__,
           static_folder=os.environ.get('FLASK_STATIC_FOLDER'),
           static_url_path='')

wcocr.init("/app/wx/opt/wechat/wxocr", "/app/wx/opt/wechat")

def get_compressed_path(path):
    gzip_path = f"{path}.gz"
    if os.path.exists(os.path.join(app.static_folder, gzip_path)):
        return gzip_path
    return path

@app.route('/')
def index():
    return handle_static('index.html')

def handle_static(path):
    # 优先检查Gzip版本
    gzip_path = get_compressed_path(path)
    actual_path = gzip_path if gzip_path != path else path
    
    # 设置正确的MIME类型
    mimetype = guess_type(path)[0] or 'text/plain'
    
    # 创建响应对象
    response = send_from_directory(app.static_folder, actual_path)
    
    # 添加Gzip头
    if actual_path.endswith('.gz'):
        response.headers['Content-Encoding'] = 'gzip'
        # 移除.gz后缀的Content-Type
        original_type = guess_type(path)[0] or 'text/plain'
        response.headers['Content-Type'] = original_type
    
    # 设置缓存头（可选）
    response.headers['Cache-Control'] = 'public, max-age=31536000'
    
    return response

# OCR接口保持不变
@app.route('/ocr', methods=['POST'])
def ocr():
    try:
        image_data = request.json.get('image')
        if not image_data:
            return jsonify({'error': 'No image data provided'}), 400

        temp_dir = 'temp'
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        filename = os.path.join(temp_dir, f"{uuid.uuid4()}.png")
        try:
            image_bytes = base64.b64decode(image_data)
            with open(filename, 'wb') as f:
                f.write(image_bytes)

            result = wcocr.ocr(filename)
            return jsonify({'result': result})

        finally:
            if os.path.exists(filename):
                os.remove(filename)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)