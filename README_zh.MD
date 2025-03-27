# WeChat OCR API Docker

一个基于 Docker 的 REST API 服务，使用微信 OCR 引擎实现文字识别功能。

## 项目概述
本项目将优秀的 wechat-ocr 项目封装为简易的 REST API 服务，支持通过 Docker 快速部署。通过微信强大的 OCR 能力，实现对图像中的文字进行识别。

## ⚠️ 重要声明
本项目为开源学习交流项目，严禁用于商业用途。用户因不当使用本项目造成的任何后果需自行承担全部责任。​
**Copyright Disclaimer:** 本项目仅为现有开源项目的容器化封装。若您认为本仓库侵犯了您的版权或知识产权，请立即联系仓库所有者，我们将在第一时间删除仓库。我们尊重知识产权，无意侵犯任何权利。

## 致谢

本项目基于 swigger 的 wechat-ocr 项目开发。感谢他们对微信 OCR 功能的逆向工程实现，为本项目奠定了重要基础。

## 快速开始

### Docker 部署
```bash
# 拉取镜像
docker pull bimiracle/ocr

# 运行容器
docker run -d -p 5000:5000 --name ocr bimiracle/ocr
```
### API 使用说明

向 /ocr 端点发送 POST 请求，携带 base64 编码的图像数据：

```bash
curl -X POST http://localhost:5000/ocr \
  -H "Content-Type: application/json" \
  -d '{"image": "BASE64_ENCODED_IMAGE_DATA"}'
```

示例（无需包含 data:image/gif;base64, 前缀）：

```bash
curl -X POST http://localhost:5000/ocr \
  -H "Content-Type: application/json" \
  -d '{"image": "R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=="}'
```

#### 响应示例

```json
{
  "errcode": 0,
  "height": 72,
  "width": 410,
  "imgpath": "temp/5726fe7b-25d6-43a6-a50d-35b5f668fbb6.png",
  "ocr_response": [
    {
      "bottom": 1683.3515625,
      "left": 473.9742431640625,
      "rate": 0.9614794850349426,
      "right": 1999.8101806640625,
      "text": "SPRING",
      "top": 1490.0010986328125
    }
  ]
}
```

### Python 客户端示例

以下 Python 客户端示例演示如何调用 OCR API：

```python
import requests
import base64
import os

def ocr_recognize(image_path=None, image_url=None, api_url="http://localhost:5000/ocr"):
    """
    发送图像到 OCR API 服务并获取识别结果
    必须提供 image_path 或 image_url 参数之一
    """
    # 获取图像数据
    if image_path:
        if not os.path.exists(image_path):
            print(f"错误：本地图像未找到: {image_path}")
            return
        with open(image_path, "rb") as image_file:
            img_data = image_file.read()
    elif image_url:
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            img_data = response.content
        except Exception as e:
            print(f"图像下载失败: {str(e)}")
            return
    else:
        print("请提供 image_path 或 image_url 参数")
        return

    # 转换为 base64 编码
    base64_image = base64.b64encode(img_data).decode('utf-8')
    
    # 发送 API 请求
    try:
        response = requests.post(api_url, json={"image": base64_image})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"API 请求失败: {str(e)}")
        return None

# 使用示例
if __name__ == "__main__":
    # 本地文件示例
    result = ocr_recognize(image_path="ocrtest.png")
    if result:
        print(result)
    
    # 网络图片示例（取消注释使用）
    # result = ocr_recognize(image_url="https://example.com/image.png")
```

## 项目结构

- `main.py`: Flask API 服务主程序
- `opt/wechat/wxocr`: 微信 OCR 二进制文件
- `opt/wechat/`: 微信运行时依赖文件

## 技术细节

本服务使用 Flask 框架提供 REST API 接口，处理流程如下：

1. 接收 base64 编码的图像数据并解码
2. 创建临时图像文件
3. 通过 wcocr Python 绑定调用微信 OCR 引擎
4. 返回 JSON 格式的识别结果
5. 自动清理临时文件

## 已知限制

- 当前仅支持 PNG 格式（可按需扩展）
- 依赖微信 OCR 二进制文件（可能随微信更新而变更）

## 许可协议

本项目基于 MIT 许可证发布，附加以下条款：

1.仓库所有者不对本软件的任何使用承担法律责任
2.使用、复制、修改或分发本软件即表示您同意：任何使用行为均为使用者个人行为，需自行承担全部责任
3.使用者需自行承担使用本仓库及其内容的风险
4.仓库所有者不承担因使用本软件产生的任何法律后果

## 贡献指南

欢迎提交 Pull Request 参与项目改进！