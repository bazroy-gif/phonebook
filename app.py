import flet as ft
import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ربط قاعدة بيانات Firebase الخاصة بك
DATABASE_URL = "https://phonebook-44782-default-rtdb.firebaseio.com/contacts"

def main(page: ft.Page):
    page.title = "Cloud Phonebook Directory"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.scroll = ft.ScrollMode.AUTO
    page.rtl = False  # تم تحويل الاتجاه إلى الإنجليزية (من اليسار لليمين)
    page.window_width = 450
    page.window_height = 700

    id_field = ft.TextField(label="ID Number (Serial)", border=ft.InputBorder.OUTLINE)
    name_field = ft.TextField(label="Person Name", border=ft.InputBorder.OUTLINE)
    address_field = ft.TextField(label="Address (Optional)", border=ft.InputBorder.OUTLINE)
    
    search_field = ft.TextField(
        label="Search by Name or ID...", 
        border=ft.InputBorder.OUTLINE, 
        on_change=lambda e: filter_contacts(e.value)
    )

    phones_column = ft.Column()
    phone_fields = []
    
    all_contacts_cache = []
    results_column = ft.Column(scroll=ft.ScrollMode.AUTO, height=260)

    def show_message(text_msg):
        snack = ft.SnackBar(content=ft.Text(text_msg))
        page.overlay.append(snack)
        snack.open = True
        page.update()

    def add_phone_field(e=None):
        phone_input = ft.TextField(
            label=f"Phone Number {len(phone_fields) + 1}",
            keyboard_type=ft.KeyboardType.PHONE,
            border=ft.InputBorder.OUTLINE
        )
        phone_fields.append(phone_input)
        phones_column.controls.append(phone_input)
        page.update()

    add_phone_field()

    def fetch_contacts():
        nonlocal all_contacts_cache
        try:
            response = requests.get(f"{DATABASE_URL}.json", verify=False)
            if response.status_code == 200 and response.json():
                data = response.json()
                all_contacts_cache = [{"key": k, **v} for k, v in data.items()]
                
                # ترتيب الأرقام تصاعدياً حسب الـ ID
                try:
                    all_contacts_cache.sort(key=lambda x: int(str(x.get("id", 0)).strip()))
                except:
                    all_contacts_cache.sort(key=lambda x: str(x.get("id", "")).strip())
            else:
                all_contacts_cache = []
        except Exception as ex:
            print("Connection Error:", ex)
            all_contacts_cache = []
        
        display_contacts(all_contacts_cache)

    def display_contacts(contacts):
        results_column.controls.clear()
        if not contacts:
            results_column.controls.append(ft.Text("No records found in the cloud directory."))
        else:
            for c in contacts:
                phones_str = " | ".join(c.get("phones", []))
                card = ft.Card(
                    content=ft.Container(
                        padding=12,
                        content=ft.Column([
                            ft.Row([
                                ft.Text(f"Name: {c.get('name')}", weight=ft.FontWeight.BOLD, size=16),
                                ft.Text(f"ID: {c.get('id')}", weight=ft.FontWeight.BOLD),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Text(f"Address: {c.get('address', 'N/A')}"),
                            ft.Text(f"Phones: {phones_str if phones_str else 'No Phone Number'}"),
                        ])
                    )
                )
                results_column.controls.append(card)
        page.update()

    def filter_contacts(query):
        query = query.lower().strip()
        if not query:
            display_contacts(all_contacts_cache)
            return
        
        filtered = [
            c for c in all_contacts_cache 
            if query in str(c.get('id', '')).lower() or query in c.get('name', '').lower()
        ]
        display_contacts(filtered)

    def save_contact(e):
        if not id_field.value or not name_field.value:
            show_message("Please enter both ID and Name at least!")
            return

        all_phones = [p.value for p in phone_fields if p.value]

        new_contact = {
            "id": id_field.value.strip(),
            "name": name_field.value.strip(),
            "address": address_field.value.strip() if address_field.value else "",
            "phones": all_phones
        }

        contact_id = id_field.value.strip()
        url = f"{DATABASE_URL}/{contact_id}.json"

        try:
            response = requests.put(url, data=json.dumps(new_contact), verify=False)
            if response.status_code == 200:
                show_message("Saved and updated in the cloud successfully!")
                id_field.value = ""
                name_field.value = ""
                address_field.value = ""
                phone_fields.clear()
                phones_column.controls.clear()
                add_phone_field()
                fetch_contacts()
            else:
                show_message("Failed to save in the cloud!")
        except Exception as ex:
            show_message(f"Error: {ex}")

    page.add(
        ft.Text("📖 Shared Cloud Phonebook", size=18, weight=ft.FontWeight.BOLD),
        search_field,
        ft.Divider(),
        id_field,
        name_field,
        address_field,
        ft.Text("Phone Numbers:", weight=ft.FontWeight.BOLD),
        phones_column,
        ft.TextButton(content=ft.Text("[+] Add Another Phone Number"), on_click=add_phone_field),
        ft.ElevatedButton(content=ft.Text("Save or Update in Directory"), on_click=save_contact),
        ft.Divider(),
        ft.Text("📋 Contacts List (Sorted by ID):", weight=ft.FontWeight.BOLD),
        results_column
    )

    fetch_contacts()

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    ft.app(target=main, view=ft.WEB_BROWSER, port=port, host="0.0.0.0")
