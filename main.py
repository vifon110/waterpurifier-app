# -*- coding: utf-8 -*-
"""
小米净水器控制 App - Kivy 安卓客户端
"""
import sys
import os
import io

# Kivy 初始化（必须在任何其他 kivy import 之前）
os.environ["KIVY_ORIENTATION"] = "portrait"

from kivy.config import Config
Config.set("graphics", "resizable", False)
Config.set("graphics", "width", "360")
Config.set("graphics", "height", "640")

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image as KivyImage
from kivy.uix.modalview import ModalView
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.text import LabelBase
from kivy.metrics import dp

from PIL import Image as PILImage

# 核心控制模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import mijia


# ==================================================================
# 颜色主题
# ==================================================================

COLORS = {
    "bg_dark":       "#1a1a2e",
    "bg_card":       "#16213e",
    "accent":        "#0f9b8e",
    "accent_light":  "#2dd4bf",
    "text_white":    "#e0e0e0",
    "text_dim":      "#8892b0",
    "success":       "#4ade80",
    "warning":       "#fbbf24",
    "error":         "#f87171",
    "btn_bg":        "#1e3a5f",
    "btn_pressed":   "#254e7a",
}


# ==================================================================
# 主界面
# ==================================================================

class WaterPurifierApp(App):
    def build(self):
        self.title = "小米净水器"
        self._qr_modal = None
        return MainLayout()

    def on_start(self):
        # 设置 UI 回调
        mijia.set_callbacks({
            "on_log": self._on_log,
            "on_login_qr": self._on_login_qr,
            "on_login_done": self._on_login_done,
            "on_status": self._on_status,
            "on_error": self._on_error,
        })
        # 启动时检查登录状态
        Clock.schedule_once(lambda dt: self._check_login(), 0.5)

    def _check_login(self):
        root = self.root
        if mijia.check_auth():
            root.ids.log_area.text = "[已登录，点击查询/操作按钮]\n"
            Clock.schedule_once(lambda dt: mijia.refresh_status(), 0.3)
        else:
            root.ids.log_area.text = "[未登录，请先扫码登录]\n"

    # ---- UI 回调（由后台线程通过 Clock 调度到主线程） ----

    def _on_log(self, msg):
        Clock.schedule_once(lambda dt: self._append_log(msg))

    def _append_log(self, msg):
        root = self.root
        log = root.ids.log_area
        log.text += msg + "\n"
        # 自动滚动到底部
        root.ids.scroll_area.scroll_y = 0

    def _on_login_qr(self, pil_img):
        Clock.schedule_once(lambda dt: self._show_qr(pil_img))

    def _show_qr(self, pil_img):
        # 将 PIL Image 转为 Kivy Texture
        pil_img = pil_img.convert("RGBA")
        data = pil_img.tobytes()
        tex = Texture.create(size=pil_img.size, colorfmt="rgba")
        tex.blit_buffer(data, colorfmt="rgba", bufferfmt="ubyte")

        # 创建模态窗口显示二维码
        modal = ModalView(size_hint=(0.7, 0.5), background_color=[0,0,0,0.85])
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        qr_widget = KivyImage(texture=tex, size_hint=(1, 0.8), allow_stretch=True)
        hint = Label(
            text="用米家APP扫码登录",
            color=COLORS["text_white"],
            font_size=16,
            size_hint=(1, 0.1),
        )
        cancel_btn = Button(
            text="取消",
            size_hint=(1, 0.1),
            background_color=[0.6, 0.2, 0.2, 1],
            color=[1,1,1,1],
        )
        cancel_btn.bind(on_press=lambda x: (modal.dismiss(), mijia.qr_login.__self__ if False else None))
        # 取消按钮绑定
        def on_cancel(btn):
            modal.dismiss()
        cancel_btn.bind(on_press=on_cancel)

        layout.add_widget(qr_widget)
        layout.add_widget(hint)
        layout.add_widget(cancel_btn)
        modal.add_widget(layout)
        self._qr_modal = modal
        modal.open()

    def _on_login_done(self, success):
        Clock.schedule_once(lambda dt: self._login_result(success))

    def _login_result(self, success):
        if self._qr_modal:
            self._qr_modal.dismiss()
            self._qr_modal = None
        if success:
            self._append_log("[OK] 登录成功!\n")
            mijia.refresh_status()
        else:
            self._append_log("[WARN] 登录失败或取消\n")

    def _on_status(self, name):
        Clock.schedule_once(lambda dt: self._update_status(name))

    def _update_status(self, name):
        self.root.ids.status_label.text = f"当前: {name}"

    def _on_error(self, msg):
        Clock.schedule_once(lambda dt: self._append_log(f"[ERROR] {msg}\n"))

    # ---- 按钮事件 ----

    def btn_login(self):
        self._append_log("正在获取二维码...\n")
        mijia.start_login()

    def btn_refresh(self):
        self._append_log("查询中...\n")
        mijia.refresh_status()

    def btn_zero(self):
        self._append_log("设置: 零陈水模式...\n")
        mijia.set_water_mode("zero")

    def btn_enhanced(self):
        self._append_log("设置: 增强零陈水模式...\n")
        mijia.set_water_mode("enhanced")

    def btn_off(self):
        self._append_log("设置: 关闭...\n")
        mijia.set_water_mode("off")

    def btn_clear_log(self):
        self.root.ids.log_area.text = ""
        self.root.ids.scroll_area.scroll_y = 1

    def btn_relogin(self):
        mijia.clear_auth()
        self._append_log("已清除登录信息，请重新登录\n")


# ==================================================================
# 主布局（KV 字符串内联，减少文件依赖）
# ==================================================================

KV = """
BoxLayout:
    orientation: "vertical"
    canvas.before:
        Color:
            rgba: 0.1, 0.1, 0.18, 1
        Rectangle:
            pos: self.pos
            size: self.size

    # 顶部标题栏
    BoxLayout:
        size_hint_y: 0.08
        padding: [15, 5]
        canvas.before:
            Color:
                rgba: 0.06, 0.06, 0.12, 1
            Rectangle:
                pos: self.pos
                size: self.size
        Label:
            text: "小米净水器 · 无陈水控制"
            font_size: 17
            bold: True
            color: 0.88, 0.92, 0.96, 1

    # 状态栏
    BoxLayout:
        size_hint_y: 0.06
        padding: [15, 2]
        id: status_bar
        Label:
            id: status_label
            text: "当前: -"
            font_size: 14
            color: 0.53, 0.57, 0.69, 1
            halign: "left"

    # 模式按钮区
    GridLayout:
        size_hint_y: 0.28
        cols: 2
        spacing: 10
        padding: [15, 10]

        Button:
            text: "零陈水"
            font_size: 15
            bold: True
            background_color: 0.06, 0.61, 0.56, 1
            background_normal: ""
            color: 1, 1, 1, 1
            on_press: app.btn_zero()

        Button:
            text: "增强零陈水"
            font_size: 15
            bold: True
            background_color: 0.22, 0.52, 0.78, 1
            background_normal: ""
            color: 1, 1, 1, 1
            on_press: app.btn_enhanced()

        Button:
            text: "关闭"
            font_size: 15
            bold: True
            background_color: 0.5, 0.5, 0.5, 1
            background_normal: ""
            color: 1, 1, 1, 1
            on_press: app.btn_off()

        Button:
            text: "查看状态"
            font_size: 15
            bold: True
            background_color: 0.12, 0.24, 0.4, 1
            background_normal: ""
            color: 1, 1, 1, 1
            on_press: app.btn_refresh()

    # 底部操作按钮
    BoxLayout:
        size_hint_y: 0.07
        spacing: 8
        padding: [15, 4]

        Button:
            text: "登录"
            font_size: 14
            bold: True
            background_color: 0.06, 0.61, 0.56, 1
            background_normal: ""
            color: 1, 1, 1, 1
            on_press: app.btn_login()

        Button:
            text: "重新登录"
            font_size: 13
            background_color: 0.6, 0.3, 0.1, 1
            background_normal: ""
            color: 1, 1, 1, 1
            on_press: app.btn_relogin()

        Button:
            text: "清日志"
            font_size: 13
            background_color: 0.2, 0.2, 0.3, 1
            background_normal: ""
            color: 1, 1, 1, 1
            on_press: app.btn_clear_log()

    # 日志输出区
    BoxLayout:
        orientation: "vertical"
        size_hint_y: 0.51
        padding: [15, 5]
        Label:
            text: "运行日志"
            font_size: 12
            color: 0.53, 0.57, 0.69, 1
            size_hint_y: 0.06
            halign: "left"
        ScrollView:
            id: scroll_area
            do_scroll_x: False
            Label:
                id: log_area
                text: ""
                font_size: 11
                color: 0.8, 0.85, 0.9, 1
                text_size: self.width - 20, None
                size_hint_y: None
                height: max(self.minimum_height, scroll_area.height)
                valign: "bottom"
"""


class MainLayout(BoxLayout):
    pass


# ==================================================================
# 入口
# ==================================================================

if __name__ == "__main__":
    from kivy.lang import Builder
    Builder.load_string(KV)
    WaterPurifierApp().run()
