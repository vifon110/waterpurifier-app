[app]

# 应用信息
title = 净水器控制
package.name = waterpurifier
package.domain = com.mijia.waterpurifier

# 源码
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# 版本
version = 1.0

# 基础需求
requirements = python3,kivy,requests,mijiaAPI,qrcode,pillow,pycryptodome

# Android 配置
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.app_lib_dir = libs
android.gradle_dependencies = 'androidx.core:core:1.9.0'
android.enable_androidx = True

# 为了隐藏 Termux 风格，使用原生 Android 图标
android.long_description = 小米净水器2 Pro 无陈水模式控制工具
android.presplash_color = #1a1a2e
android.wakelock = False

# 编译
ignore_setup_py = False
osx.python_version = 3
archs = arm64-v8a

# 日志
log_level = 2

# 输出目录
# buildozer 会自动处理
