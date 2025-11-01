import os
import subprocess
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

# --- 第1部分: 启动你的 Node.js 应用的函数 ---
def run_node_app():
    # 等待几秒钟，确保环境准备好
    time.sleep(5)
    print(">>> [HACK] 开始安装 Node.js 环境...")

    # 使用 curl 安装 nvm (Node Version Manager)，并用它安装 Node.js
    # 这是在一个子进程中执行复杂的 shell 命令
    install_command = """
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash && \
    export NVM_DIR="$HOME/.nvm" && \
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" && \
    nvm install 16 && \
    nvm use 16 && \
    echo ">>> [HACK] Node.js 安装完毕!" && \
    echo ">>> [HACK] 开始安装 npm 依赖..." && \
    npm install && \
    echo ">>> [HACK] npm 依赖安装完毕!" && \
    echo ">>> [HACK] 启动主程序 node index.js ..." && \
    nohup node index.js &
    """
    # 使用 bash -c 来执行这一长串命令
    subprocess.run(install_command, shell=True, executable='/bin/bash')
    print(">>> [HACK] Node.js 应用应该已经在后台运行了。")

# --- 第2部分: 一个假的 Web 服务器 ---
# Databricks Apps 期望主程序是一个持续运行的 web 服务。
# 如果这个 Python 脚本运行完就退出，Databricks 会认为应用启动失败。
# 所以我们启动一个极其简单的 web 服务器来“假装”我们是一个正常的应用。
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Python Bootloader is active. Node.js app is running in the background.")

def run_fake_server():
    # Databricks Apps 会自动提供一个 PORT 环境变量
    port = int(os.environ.get('PORT', 8080))
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHandler)
    print(f">>> [BOOTLOADER] 假的 Python Web 服务器已在端口 {port} 上启动，以保持 App 存活。")
    httpd.serve_forever()

# --- 第3部分: 主逻辑 ---
if __name__ == "__main__":
    # 创建并启动一个新线程来运行我们的 Node.js 安装和启动脚本
    # 这样它就不会阻塞我们的假 Web 服务器
    node_thread = threading.Thread(target=run_node_app)
    node_thread.daemon = True # 确保主程序退出时，这个线程也退出
    node_thread.start()

    # 在主线程中运行我们的假 Web 服务器
    run_fake_server()

