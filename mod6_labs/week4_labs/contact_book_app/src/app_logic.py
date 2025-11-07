import flet as ft 
from database import update_contact_db, delete_contact_db, add_contact_db, get_all_contacts_db

def display_contacts(page, contacts_list_view, db_conn, contacts=None):
    """Fetches and displays all contacts in the ListView."""
    contacts_list_view.controls.clear()

    # If no contacts were passed (normal load), fetch from DB
    if contacts is None:
        contacts = get_all_contacts_db(db_conn)

    if not contacts:
        contacts_list_view.controls.append(
            ft.Text("No contacts found.", italic=True, color="gray")
        )
    else:
        for contact in contacts:
            contact_id, name, phone, email = contact

            contact_card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(name, size=18, weight=ft.FontWeight.BOLD),
                            ft.Row([ft.Icon(ft.Icons.PHONE, size=16), ft.Text(phone)], spacing=6),
                            ft.Row([ft.Icon(ft.Icons.EMAIL, size=16), ft.Text(email)], spacing=6),
                            ft.Row(
                                [
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,
                                        tooltip="Edit",
                                        on_click=lambda e, c=contact: open_edit_dialog(page, c, db_conn, contacts_list_view)
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE,
                                        tooltip="Delete",
                                        on_click=lambda e, cid=contact_id: delete_contact(page, cid, db_conn, contacts_list_view)
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ]
                    ),
                    padding=10,
                ),
                elevation=3,
                margin=5,
                shape=ft.RoundedRectangleBorder(radius=12),
            )

            contacts_list_view.controls.append(contact_card)

    page.update()



def search_contacts(page, e, contacts_list_view, db_conn):
    """Filters contacts based on search input."""
    search_term = e.control.value.strip().lower()
    contacts = get_all_contacts_db(db_conn)
    if search_term:
        # can search by name, phone, or email
        filtered_contacts = [
            c for c in contacts
            if search_term in c[1].lower()  # name
            or search_term in c[2].lower()  # phone
            or search_term in c[3].lower()  # email
        ]
    else:
        filtered_contacts = contacts  # if search bar is empty, show all, if search name prio name etc.
    # for example if search @gmail all @gmail appear while @my will not 
    display_contacts(page, contacts_list_view, db_conn, filtered_contacts)



def add_contact(page, inputs, contacts_list_view, db_conn): 
    """Adds a new contact and refreshes the list.""" 
    name_input, phone_input, email_input = inputs 
    if not name_input.value.strip(): # Input validation preventing users from adding empty contact
        name_input.error_text = "Name cannot be empty" 
        page.update()
        return
    # continue with adding contact
    add_contact_db(db_conn, name_input.value, phone_input.value, email_input.value) 

    for field in inputs: 
        field.value = "" 
 
    display_contacts(page, contacts_list_view, db_conn) 
    page.update() 

def delete_contact(page, contact_id, db_conn, contacts_list_view): 
    """Deletes a contact after confirmation and refreshes the list.""" 

    def yes_action(e): # ask the user for action click input if yes
        try:
            delete_contact_db(db_conn, contact_id)
            # show quick feedback
            page.snack_bar = ft.SnackBar(ft.Text("Contact deleted"))
            page.snack_bar.open = True
            display_contacts(page, contacts_list_view, db_conn)
        except Exception as exc:
            # if something goes wrong, show message in snackbar and the console
            page.snack_bar = ft.SnackBar(ft.Text(f"Delete failed: {exc}"))
            page.snack_bar.open = True
            print("delete error:", exc)
        finally:
            dialog.open = False
            page.update()

    def no_action(e): # ask the user for action click input if no
        dialog.open = False
        page.update()

    dialog = ft.AlertDialog( # this dialog added feature prevents the user or the admin to prevent accidental deletion,.
        title=ft.Text("Confirm Delete"),
        content=ft.Text("Are you sure you want to delete this contact?"),
        actions=[
            ft.TextButton("Yes", on_click=yes_action),
            ft.TextButton("No", on_click=no_action),
        ],
    )

    page.open(dialog)


def open_edit_dialog(page, contact, db_conn, contacts_list_view): 
    """Opens a dialog to edit a contact's details.""" 
    contact_id, name, phone, email = contact 
 
    edit_name = ft.TextField(label="Name", value=name) 
    edit_phone = ft.TextField(label="Phone", value=phone) 
    edit_email = ft.TextField(label="Email", value=email)

    def save_and_close(e): 
        update_contact_db(db_conn, contact_id, edit_name.value, edit_phone.value, 
edit_email.value) 
        dialog.open = False 
        page.update() 
        display_contacts(page, contacts_list_view, db_conn) 
 
    dialog = ft.AlertDialog( 
        modal=True, 
        title=ft.Text("Edit Contact"), 
        content=ft.Column([edit_name, edit_phone, edit_email]), 
        actions=[ 
            ft.TextButton("Cancel", on_click=lambda e: setattr(dialog, 'open', False) 
or page.update()), 
            ft.TextButton("Save", on_click=save_and_close), 
        ], 
    ) 
 
    page.open(dialog)

