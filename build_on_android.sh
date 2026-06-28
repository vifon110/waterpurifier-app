#!/data/data/com.termux/files/usr/bin/bash
# ===============================================================
# 小米净水器控制 - Termux APK 构建脚本
# 用法: bash build_on_android.sh
# ===============================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}========================================"
echo -e "  小米净水器控制 - APK 构建脚本"
echo -e "========================================${NC}"

# 检查是否在 Termux 环境
if [ ! -d "/data/data/com.termux" ]; then
    echo -e "${RED}[ERROR] 请在 Termux 中运行此脚本${NC}"
    exit 1
fi

# 1. 安装依赖
echo -e "${YELLOW}[1/7]${NC} 安装 Termux 依赖包..."
pkg install -y python python-pip git openjdk-17 wget which unzip

# 2. 安装 Python 依赖
echo -e "${YELLOW}[2/7]${NC} 安装 Python 构建工具..."
pip install --upgrade pip -q
pip install buildozer cython==0.29.37 -q

# 3. 设置项目目录
PROJECT_DIR="$HOME/waterpurifier_app"
echo -e "${YELLOW}[3/7]${NC} 项目目录: $PROJECT_DIR"

if [ ! -d "$PROJECT_DIR" ]; then
    mkdir -p "$PROJECT_DIR"
fi

# 4. 如果当前目录有源码文件，复制过来
CURRENT_DIR="$(pwd)"
if [ -f "$CURRENT_DIR/main.py" ]; then
    echo -e "${YELLOW}[4/7]${NC} 从当前目录复制源码..."
    cp -r "$CURRENT_DIR"/* "$PROJECT_DIR/"
else
    echo -e "${YELLOW}[4/7]${NC} 检查项目文件..."
    if [ ! -f "$PROJECT_DIR/main.py" ]; then
        echo -e "${RED}[ERROR] 未找到源码文件，请先下载项目 zip 并解压到 $PROJECT_DIR${NC}"
        exit 1
    fi
fi

cd "$PROJECT_DIR"

# 5. 检查/生成 buildozer.spec
echo -e "${YELLOW}[5/7]${NC} 检查 buildozer.spec..."
if [ ! -f "buildozer.spec" ]; then
    echo "  生成 buildozer.spec..."
    buildozer init
fi

# 6. 预先下载 Android SDK/NDK（避免构建时网络问题）
echo -e "${YELLOW}[6/7]${NC} 检查 Android SDK/NDK..."
export ANDROID_HOME="$HOME/.buildozer/android/platform/android-sdk"
export ANDROIDNDK="$HOME/.buildozer/android/platform/android-ndk-r25b"

if [ ! -d "$ANDROID_HOME" ]; then
    echo "  首次构建需要下载 Android SDK (~500MB)，请耐心等待..."
    echo "  建议连接 WiFi 并保持充电"
fi

# 7. 开始构建
echo ""
echo -e "${GREEN}========================================"
echo -e "  开始构建 APK"
echo -e "  预计时间: 首次 30-60 分钟，后续 5-10 分钟"
echo -e "  请保持 Termux 前台运行、手机充电"
echo -e "========================================${NC}"
echo ""

buildozer -v android debug

# 8. 完成
echo ""
echo -e "${GREEN}========================================"
echo -e "  构建完成！"
echo -e "========================================${NC}"
echo -e "APK 位置: ${YELLOW}$PROJECT_DIR/bin/*.apk${NC}"
echo ""
echo "安装方法:"
echo "  1. 在手机文件管理器中找到 bin/ 目录"
echo "  2. 点击 .apk 文件安装"
echo "  3. 如提示'禁止安装未知来源应用'，请在设置中允许"
echo ""
echo "使用方法:"
echo "  1. 打开 APP"
echo "  2. 首次使用点击'登录米家账号'"
echo "  3. 扫码登录后即可控制净水器"
