
from kivy.config import Config
from kivy.utils import get_color_from_hex as hex_color
# Set window size to mobile dimensions BEFORE importing kivy
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', False)

from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.button import MDFabButton
from kivy.metrics import dp
from kivy.utils import get_color_from_hex as hex_colors
from kivy.storage.jsonstore import JsonStore
from datetime import datetime
import uuid

from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView


class TodoScreen(MDScreen):
    def on_kv_post(self, base_widget):
        self.store = JsonStore("todos.json")
        todos = []

        for key in self.store.keys():
            data = self.store.get(key)
            completed = data.get('completed', False)
            timestamp = data.get('timestamp', "")
            text = data.get('text', "")
            todos.append((timestamp, completed, text))

        # Sort by timestamp (latest first)
        todos.sort(reverse=True)

        for timestamp, completed, todo_text in todos:
            self.add_list_item(todo_text, completed=completed)

    def text_length(self, textfield):
        if len(textfield.text) > 65:
            textfield.text = textfield.text[:65]

    def toggle_todo(self, instance, text):
        for key in list(self.store.keys()):
            if self.store.get(key)['text'] == text:
                self.store.put(key, text=text, timestamp=self.store.get(key)['timestamp'], completed=instance.active)

    def delete_todo(self, instance, todo_text):
        # Find and delete the matching todos based on the text
        for key in list(self.store.keys()):
            if self.store.get(key)['text'] == todo_text:
                self.store.delete(key)
                break

        # Now remove the widget from the UI
        self.ids.todo_list.remove_widget(instance.parent.parent)

    def add_todo(self):
        new_text = self.ids.todo_item.text
        if not new_text.strip():
            return  # Don't add empty todos

        key = str(uuid.uuid4())  # Generate a fast unique ID
        timestamp = datetime.now().isoformat()
        completed = False

        # Save to JSON
        self.store.put(key, text=new_text, timestamp=timestamp, completed=completed)

        # Add to the top visually
        self.add_list_item(new_text, insert_top=True)

        # Clear input
        self.ids.todo_item.text = ""
        Clock.schedule_once(lambda dt: setattr(self.ids.scroll_view, 'scroll_y', 1), 0.05)

    def add_list_item(self, text, insert_top=False, completed=False):

        box = MDBoxLayout(
            radius=[dp(15)],
            orientation="horizontal",
            size_hint_y=None,
            size_hint_x=1,
            height=dp(60),
            padding=dp(10),
            spacing=dp(10),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            md_bg_color=hex_color("#ffffff"),

        )

        layout = MDRelativeLayout(pos_hint={"center_x": 0.5, "center_y": 0.5})

        checkbox = MDCheckbox(
            size_hint=(None, None),
            size=("48dp", "48dp"),
            pos_hint={"left": 1, "center_y": 0.5},
            color_active=hex_color('#39aacc'),
            color_inactive=hex_color('#39aacc'),
            active=completed,
            on_release=lambda instance: self.toggle_todo(instance, text)
        )

        label = MDLabel(
            adaptive_size=False,  # Disable adaptive_size to prevent font size from changing
            size_hint_x=1,
            text_size=(self.width, None),  # Adjust text_size considering the left padding
            padding=(dp(60), dp(5)),  # Left padding of 60, no vertical padding
            halign="left",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            text=text,
            font_style="Title",
            role="small",
            theme_text_color="Custom",
            text_color=hex_color('#687179'),
            bold=True,
        )

        delete_btn = MDFabButton(
            icon="trash-can",
            style="small",
            pos_hint={"right": 1},
            theme_text_color="Custom",
            text_color=hex_color('#ffffff'),
            theme_bg_color="Custom",
            md_bg_color=hex_color('#e40f0f'),
            on_release=lambda instance: self.delete_todo(instance, text)
        )

        layout.add_widget(checkbox)
        layout.add_widget(label)
        layout.add_widget(delete_btn)
        box.add_widget(layout)

        todo_list = self.ids.todo_list

        if insert_top:
            todo_list.add_widget(box)
            todo_list.children = todo_list.children[::-1]  # Insert at top!
        else:
            todo_list.add_widget(box)  # Normal append at bottom

    def reload_all_todos(self):
        self.ids.todo_list.clear_widgets()
        self.ids.todo_list.height = 0  # Reset the height

        todos = []

        for key in self.store.keys():
            data = self.store.get(key)
            completed = data.get('completed', False)
            timestamp = data.get('timestamp', "")
            text = data.get('text', "")
            todos.append((timestamp, completed, text))

        todos.sort(key=lambda x: x[0], reverse=True)

        for timestamp, completed, todo_text in todos:
            self.add_list_item(todo_text, completed=completed)

    from kivy.clock import Clock

    def search_todos(self, search_widget):
        search_text = search_widget.text.lower().strip()

        todo_list = self.ids.todo_list
        todo_list.clear_widgets()
        todo_list.height = 0

        if not search_text:
            Clock.schedule_once(lambda dt: self.reload_all_todos(), 0.05)
            return

        for key in self.store.keys():
            data = self.store.get(key)
            text = data.get('text', '')
            completed = data.get('completed', False)

            if search_text in text.lower():
                self.add_list_item(text, completed=completed)
        # Scroll to top AFTER search items are added
        Clock.schedule_once(lambda dt: setattr(self.ids.scroll_view, 'scroll_y', 1), 0.05)

class MyApp(MDApp):
    def build(self):

        kv = Builder.load_file('todo.kv')
        return kv



if __name__ == "__main__":
    MyApp().run()
