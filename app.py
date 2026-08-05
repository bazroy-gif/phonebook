import flet as ft
import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# تم ربط قاعدة بيانات Firebase الخاصة بك بنجاح
DATABASE_URL = "https://phonebook-44782-default-rtdb.firebaseio.com/contacts"

def main(page: ft.Page):
    page.title = "دليل الهواتف السحابي"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.scroll = ft.ScrollMode.AUTO
    page.rtl = True
    page.window_width = 450
    page.window_height = 700

    id_field = ft.TextField(label="رقم الـ ID (الرقم التسلسلي)", border=ft.InputBorder.OUTLINE)
    name_field = ft.TextField(label="اسم الشخص", border=ft.InputBorder.OUTLINE)
    address_field = ft.TextField(label="العنوان (اختياري)", border=ft.InputBorder.OUTLINE)
    
    search_field = ft.TextField(
        label="ابحث هنا بالاسم أو برقم الـ ID...", 
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
            label=f"رقم الهاتف {len(phone_fields) + 1}",
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
                
                # ترتيب الأرقام تصاعدياً حسب الـ ID من الأصغر للأكبر
                try:
                    all_contacts_cache.sort(key=lambda x: int(str(x.get("id", 0)).strip()))
                except:
                    all_contacts_cache.sort(key=lambda x: str(x.get("id", "")).strip())
            else:
                all_contacts_cache = []
        except Exception as ex:
            print("خطأ في الاتصال:", ex)
            all_contacts_cache = []
        
        display_contacts(all_contacts_cache)

    def display_contacts(contacts):
        results_column.controls.clear()
        if not contacts:
            results_column.controls.append(ft.Text("لا توجد نتائج مسجلة في الدفتر السحابي."))
        else:
            for c in contacts:
                phones_str = " | ".join(c.get("phones", []))
                card = ft.Card(
                    content=ft.Container(
                        padding=12,
                        content=ft.Column([
                            ft.Row([
                                ft.Text(f"الاسم: {c.get('name')}", weight=ft.FontWeight.BOLD, size=16),
                                ft.Text(f"ID: {c.get('id')}", weight=ft.FontWeight.BOLD),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Text(f"العنوان: {c.get('address', 'غير متوفر')}"),
                            ft.Text(f"الأرقام: {phones_str}"),
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
            show_message("الرجاء إدخال رقم الـ (ID) واسم الشخص على الأقل!")
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
                show_message("تم الحفظ والتحديث في السحابة بنجاح!")
                id_field.value = ""
                name_field.value = ""
                address_field.value = ""
                phone_fields.clear()
                phones_column.controls.clear()
                add_phone_field()
                fetch_contacts()
            else:
                show_message("فشل الحفظ في السحابة!")
        except Exception as ex:
            show_message(f"خطأ: {ex}")

    page.add(
        ft.Text("📖 دفتر الهواتف السحابي المشترك", size=18, weight=ft.FontWeight.BOLD),
        search_field,
        ft.Divider(),
        id_field,
        name_field,
        address_field,
        ft.Text("أرقام الهواتف:", weight=ft.FontWeight.BOLD),
        phones_column,
        ft.TextButton(content=ft.Text("[+] إضافة رقم هاتف آخر"), on_click=add_phone_field),
        ft.ElevatedButton(content=ft.Text("حفظ أو تعديل في الدفتر"), on_click=save_contact),
        ft.Divider(),
        ft.Text("📋 قائمة الأرقام (مرتبة حسب الـ ID):", weight=ft.FontWeight.BOLD),
        results_column
    )

    fetch_contacts()

ft.app(target=main)