from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
import json

class ProductDB:
    def __init__(self):
        self.filename = "products.json"
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.products = json.load(f)
        except:
            self.products = {
                "4601234567890": {"name": "Молоко", "location": "Холодильник, полка 2"},
                "4609876543210": {"name": "Хлеб", "location": "Стеллаж А, полка 3"},
            }
    def save(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.products, f, ensure_ascii=False, indent=2)
    def get(self, b):
        return self.products.get(b)
    def add(self, b, n, l):
        self.products[b] = {"name": n, "location": l}
        self.save()

class BarcodeApp(App):
    def build(self):
        self.db = ProductDB()
        tabs = TabbedPanel(do_default_tab=False)
        
        t1 = TabbedPanelItem(text="🔍 Поиск")
        l1 = BoxLayout(orientation='vertical', spacing=10, padding=15)
        l1.add_widget(Label(text="📦 Barcode Locator", font_size=26, size_hint_y=0.15))
        self.inp = TextInput(hint_text="Штрихкод", font_size=20, size_hint_y=0.12, multiline=False)
        l1.add_widget(self.inp)
        b = Button(text="🔍 Найти", size_hint_y=0.12, background_color=(0.2,0.6,1,1))
        b.bind(on_press=self.search)
        l1.add_widget(b)
        self.res = Label(text="Введите штрихкод", font_size=18, size_hint_y=0.5, halign='center')
        l1.add_widget(self.res)
        t1.content = l1
        tabs.add_widget(t1)
        
        t2 = TabbedPanelItem(text="✏️ База")
        l2 = BoxLayout(orientation='vertical', spacing=10, padding=15)
        self.list_lbl = Label(text="", font_size=14, size_hint_y=0.8, halign='left', valign='top', markup=True)
        l2.add_widget(self.list_lbl)
        b2 = Button(text="🔄 Обновить", size_hint_y=0.1)
        b2.bind(on_press=self.refresh)
        l2.add_widget(b2)
        t2.content = l2
        tabs.add_widget(t2)
        
        self.refresh(None)
        return tabs
    
    def search(self, i):
        b = self.inp.text.strip()
        p = self.db.get(b)
        if p:
            self.res.text = f"✅ {p['name']}\n\n📍 {p['location']}"
            self.res.color = (0,0.6,0,1)
        else:
            self.res.text = f"❌ Не найдено: {b}"
            self.res.color = (1,0,0,1)
    
    def refresh(self, i):
        t = ""
        for bc, d in self.db.products.items():
            t += f"[b]{d['name']}[/b]\n📌 {bc}\n📍 {d['location']}\n\n"
        self.list_lbl.text = t or "База пуста"

BarcodeApp().run()
