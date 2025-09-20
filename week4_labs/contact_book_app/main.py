# main.py
import flet as ft
from database import init_db
from app_logic import display_contacts, add_contact, search_contacts


def main(page: ft.Page):
    page.title = "Contact Book"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_width = 400
    page.window_height = 600
    page.bgcolor = ft.Colors.WHITE
    page.theme_mode = ft.ThemeMode.LIGHT
    page.animate = ft.Animation(800, "ease")  

    db_conn = init_db()

    name_input = ft.TextField(label="👤 Name", width=350)
    phone_input = ft.TextField(label="📞 Phone", width=350)
    email_input = ft.TextField(label="✉️ Email", width=350)

    inputs = (name_input, phone_input, email_input)

    contacts_list_view = ft.ListView(expand=True, spacing=10, auto_scroll=True)

    add_button = ft.ElevatedButton(
        text="➕ Add Contact",
        on_click=lambda e: add_contact(page, inputs, contacts_list_view, db_conn)
    )

    # Search bar
    search_input = ft.TextField(
        label="🔍 Search contacts",
        width=350,
        on_change=lambda e: search_contacts(page, e, contacts_list_view, db_conn)
    )

    #added dark/light theme
    def toggle_theme(e):
        page.theme_mode = (
            ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        )
        theme_switch.label = "🌞 Light" if page.theme_mode == ft.ThemeMode.LIGHT else "🌙 Dark"
        page.bgcolor = ft.Colors.WHITE if page.theme_mode == ft.ThemeMode.LIGHT else ft.Colors.BLACK
        page.update()

    theme_switch = ft.Switch(
        label="🌞 Light",  # default when the app is run its always light mode
        on_change=toggle_theme
    )

    # Layout
    page.add(
        ft.ListView(
            expand=True,
            spacing=5,
            controls=[
                ft.Text("Enter Contact Details:", size=20, weight=ft.FontWeight.BOLD),
                name_input,
                phone_input,
                email_input,
                add_button,
                ft.Divider(),
                search_input,
                theme_switch,
                ft.Text("Contacts:", size=20, weight=ft.FontWeight.BOLD),
                contacts_list_view,
            ]
        )
    )

    display_contacts(page, contacts_list_view, db_conn)


if __name__ == "__main__":
    ft.app(target=main)
