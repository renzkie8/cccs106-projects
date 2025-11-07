import flet as ft
import mysql.connector
from db_connection import connect_db

def main(page: ft.Page):
    # --- Page setup ---
    page.title = "User Login"
    page.window_height = 350
    page.window_width = 400
    page.bgcolor = ft.Colors.AMBER_ACCENT

    try:
        page.window_center()
        page.window_frameless = True
    except:
        pass

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- UI controls ---
    title = ft.Text("User Login", size=20, weight=ft.FontWeight.BOLD, font_family="Arial")

    username = ft.TextField(
        label="User name",
        hint_text="Enter your user name",
        helper_text="This is your unique identifier",
        width=300,
        autofocus=True,
        icon=ft.Icons.PERSON,
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT,
    )

    password = ft.TextField(
        label="Password",
        hint_text="Enter your password",
        helper_text="This is your secret key",
        width=300,
        password=True,
        can_reveal_password=True,
        icon=ft.Icons.LOCK,
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT,
    )

    # --- Helper to close dialogs ---
    def close_dialog(dialog):
        dialog.open = False
        page.update()

    # --- Define dialogs once ---
    success_dialog = ft.AlertDialog(
        title=ft.Row([ft.Icon(name=ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN), ft.Text("Login Successful")]),
        content=ft.Text("", text_align=ft.TextAlign.CENTER),
        actions=[ft.TextButton("OK", on_click=lambda e: close_dialog(success_dialog))]
    )

    failure_dialog = ft.AlertDialog(
        title=ft.Row([ft.Icon(name=ft.Icons.ERROR, color=ft.Colors.RED), ft.Text("Login Failed")]),
        content=ft.Text("Invalid username or password", text_align=ft.TextAlign.CENTER),
        actions=[ft.TextButton("OK", on_click=lambda e: close_dialog(failure_dialog))]
    )

    invalid_input_dialog = ft.AlertDialog(
        title=ft.Row([ft.Icon(name=ft.Icons.INFO, color=ft.Colors.BLUE), ft.Text("Input Error")]),
        content=ft.Text("Please enter username and password", text_align=ft.TextAlign.CENTER),
        actions=[ft.TextButton("OK", on_click=lambda e: close_dialog(invalid_input_dialog))]
    )

    database_error_dialog = ft.AlertDialog(
        title=ft.Text("Database Error"),
        content=ft.Text("An error occurred while connecting to the database", text_align=ft.TextAlign.CENTER),
        actions=[ft.TextButton("OK", on_click=lambda e: close_dialog(database_error_dialog))]
    )

    # Register dialogs in overlay
    page.overlay.extend([success_dialog, failure_dialog, invalid_input_dialog, database_error_dialog])

    # --- Login logic ---
    def login_click(e):
        print("Login button clicked!")  # DEBUG

        if not username.value or not password.value:
            invalid_input_dialog.open = True
            page.update()
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM users WHERE username=%s AND password=%s",
                (username.value, password.value)
            )
            result = cursor.fetchone()
            cursor.close()
            conn.close()

            print("Query result:", result)  # DEBUG

            if result:
                success_dialog.content = ft.Text(f"Welcome, {username.value}!", text_align=ft.TextAlign.CENTER)
                success_dialog.open = True
            else:
                failure_dialog.open = True

            page.update()

        except mysql.connector.Error as err:
            print("Database error:", err)  # DEBUG
            database_error_dialog.open = True
            page.update()

    # --- Layout ---
    login_btn = ft.ElevatedButton(
        text="Login",
        icon=ft.Icons.LOGIN,
        width=100,
        on_click=login_click,
    )

    page.add(
        ft.Column(
            [
                title,
                username,
                password,
                login_btn,
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(target=main)
