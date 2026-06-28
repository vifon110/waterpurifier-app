# 小米净水器 无陈水控制 App

将 `set_no_stale_water.py` 打包为安卓 APK。

## 功能

- 零陈水模式（节水）
- 增强零陈水模式（水质优先）
- 关闭无陈水
- 查看当前状态
- 米家账号二维码扫码登录

## 构建方法

### 方法 1: 在安卓手机上用 Termux 构建（推荐）

1. 将 `waterpurifier_app/` 整个文件夹传到手机（通过微信/QQ/USB等）

2. 在 Termux 中执行：

```bash
# 复制到 Termux 目录
cp -r /sdcard/Download/waterpurifier_app ~/

# 运行构建脚本
cd ~/waterpurifier_app
bash build_on_android.sh
```

3. 构建完成后 APK 在 `~/waterpurifier_app/bin/` 下
4. 点击安装即可

> ⏱ 首次构建会下载 Android SDK/NDK，约需 30-60 分钟
> 💡 建议插电亮屏、WiFi 稳定时构建

### 方法 2: 在 Linux PC 上构建

```bash
# 安装依赖
sudo apt install python3-pip git openjdk-17-jdk
pip install buildozer cython

# 构建
cd waterpurifier_app/
buildozer android debug

# APK 在 bin/ 目录下
```

### 方法 3: 用 Google Colab 在线构建

把 `waterpurifier_app/` 上传到 Google Drive，然后用 Colab 笔记本运行 Buildozer。

## 安装说明

APK 安装后：
1. 打开 App
2. 点击「登录」→ 用米家APP扫码 → 首次只需一次
3. 点击对应按钮切换模式
4. 下次使用直接打开即可

## 原始脚本

控制逻辑与 `set_no_stale_water.py` 相同，使用米家云 API：
- 设备: 小米净水器2 Pro
- Service #2 (water-purifier) → Property #4 (no-old-water-mode)
- SIID=2, PIID=4
