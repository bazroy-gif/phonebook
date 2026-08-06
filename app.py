إليك الكود كاملاً بعد تصحيح خطأ حقل البحث (`e.control.value`) ليعمل بدون أي أخطاء:

```python
import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ربط قاعدة بيانات Firebase الخاصة بك
DATABASE_URL = "https://phonebook-44782-default-rtdb.firebaseio.com/contacts"

# قائمة الأسماء والهويات والأرقام التي أرسلتها لضمان وجودها وتحديثها
initial_contacts = [
    {"name": "صباح التنوري", "id": "30930", "phone": "4984236"},
    {"name": "أرملة فرج الريس", "id": "22536", "phone": "3659349"},
    {"name": "سهى صليبا", "id": "11529", "phone": "4983282"},
    {"name": "اميل العقل", "id": "22549", "phone": "4983282"},
    {"name": "جرجس معادي + وديعة أبي شيل", "id": "22705", "phone": "70160848"},
    {"name": "اميلي الراعي", "id": "30912", "phone": "3550415"},
    {"name": "كفى منصور", "id": "11551", "phone": "71770045"},
    {"name": "أنطوان أبي حيدر (ليلى ابي فرح)", "id": "7819", "phone": "71921202"},
    {"name": "سمير حموي + زوجته", "id": "15010", "phone": "3521613"},
    {"name": "ميشال ضو", "id": "22548", "phone": "3521613"},
    {"name": "جرجس الريس + أوديت الجميل", "id": "22527", "phone": "3940709"},
    {"name": "نجيب الجميل أرمل ليلى كرم", "id": "7279", "phone": "3465244"},
    {"name": "صباح غانم", "id": "30931", "phone": "4985766"},
    {"name": "سلوى صفير", "id": "30927", "phone": "3434729"},
    {"name": "فيرا الراعي", "id": "22594", "phone": "3357420"},
    {"name": "كريمة الحلو", "id": "22592", "phone": "3126514"},
    {"name": "لبيبة حبيقة (أرملة اميل حبيقة)", "id": "22533", "phone": "71897837"},
    {"name": "كلود أبو خليل", "id": "7306", "phone": ""},
    {"name": "لورانس كرم (أرملة فؤاد كرم)", "id": "22704", "phone": ""},
    {"name": "روكز الحاج + تريز الحاج", "id": "23152", "phone": "71355156"},
    {"name": "جورج الخوري حنا + بديعة", "id": "22703", "phone": "3740591"},
    {"name": "نهاد أيوب", "id": "11800", "phone": ""},
    {"name": "فوزي أيوب", "id": "4107", "phone": ""},
    {"name": "مارون الخراط", "id": "22541", "phone": "3809801"},
    {"name": "ليلى نصار", "id": "11631", "phone": "70514676"},
    {"name": "هولندا السبعلي", "id": "30152", "phone": "3646552"},
    {"name": "جانيت السبعلي", "id": "11498", "phone": "3646552"},
    {"name": "سمعان نصار", "id": "23156", "phone": "70474618"},
    {"name": "لودي جرداق ( أرملة أنطوان سماحة)", "id": "3757", "phone": "3290602"},
    {"name": "مريم السبعلي", "id": "30946", "phone": "3874947"},
    {"name": "كلير روحانا", "id": "30937", "phone": "76510843"},
    {"name": "جورجيت ( أرملة شفيق رياشي)", "id": "37056", "phone": "70450399"},
    {"name": "ندى رياشي ( أرملة لطف الله سماحة)", "id": "22538", "phone": "70450399"},
    {"name": "برناديت الريس", "id": "30082", "phone": "3737821"},
    {"name": "أديبة أبو أنطون", "id": "30205", "phone": "4981564"},
    {"name": "يوسف أبي شبل", "id": "4110", "phone": "3728258"},
    {"name": "نوال الجميل", "id": "30146", "phone": "71812378"},
    {"name": "ماري سابا", "id": "30944", "phone": "71148081"},
    {"name": "ميشال بشير", "id": "23296", "phone": "3657694"},
    {"name": "نورا جرجي مشقة أرملة الياس الحايك", "id": "354", "phone": ""},
    {"name": "ليلى بطرس الزايد", "id": "492", "phone": ""},
    {"name": "أديب الزايد", "id": "525", "phone": ""},
    {"name": "ميشال الجلخ", "id": "3753", "phone": "71941230"},
    {"name": "نجاح سماحة أرملة ميشال قاصوف", "id": "3861", "phone": "03-244026"},
    {"name": "ليلى اللحام أرملة ميشال خنيصر", "id": "3883", "phone": ""},
    {"name": "يوسف الراعي كريم", "id": "4050", "phone": "03-393949"},
    {"name": "ميلاد صليبا", "id": "22530", "phone": ""},
    {"name": "ميوس حبيقة أرملة مهدي حبيقة", "id": "4126", "phone": ""},
    {"name": "عايدة برصونا أرملة يوسف ماضي", "id": "4200", "phone": ""},
    {"name": "جورجيت كفوري (أرملة جميل الحلو)", "id": "4217", "phone": ""},
    {"name": "ايلان الراعي أرملة عبدو أبو ضوموط", "id": "4549", "phone": ""},
    {"name": "سيدة الشدياق أرملة أنطون مرعي", "id": "4576", "phone": "79115118"},
    {"name": "سميرة أبو صعب", "id": "7131", "phone": "3286104"},
    {"name": "مي كعدي", "id": "7214", "phone": ""},
    {"name": "ماري كرم", "id": "7297", "phone": ""},
    {"name": "نجاة صليبا", "id": "7321", "phone": ""},
    {"name": "سامية صليبا", "id": "7822", "phone": "71445743"},
    {"name": "منتهى الريس", "id": "11216", "phone": ""},
    {"name": "هيلين خوري", "id": "11385", "phone": ""},
    {"name": "جانيت السبعلي", "id": "11498", "phone": ""},
    {"name": "جوزفين صليبا", "id": "11532", "phone": ""},
    {"name": "تقلا أبو خليل", "id": "11657", "phone": ""},
    {"name": "انعام السبعلي وزوجها بدر السبعلي", "id": "11804", "phone": "71242972"},
    {"name": "ماري الشدياق", "id": "11819", "phone": "70-718440"},
    {"name": "سميرة الريس", "id": "12571", "phone": ""},
    {"name": "تريز الريس أرملة فرج الريس", "id": "22526", "phone": ""},
    {"name": "سارة أبي شبل أرملة سعد الريس", "id": "22535", "phone": ""},
    {"name": "جوزفين أبو خليل أرملة يوسف الحاج", "id": "22537", "phone": ""},
    {"name": "سعدى الجميل أرملة يوسف الشدياق", "id": "22544", "phone": "03-608498"},
    {"name": "روكز قرطباوي أرمل نظيرة كرم", "id": "22597", "phone": "70018451"},
    {"name": "حنة بعينو", "id": "3881", "phone": "3146646"},
    {"name": "مينيرفا أبو داغر", "id": "30947", "phone": "70467330"},
    {"name": "جورج سماحة", "id": "23146", "phone": "4270671"},
    {"name": "هنريات مقدسي", "id": "30952", "phone": "71028035"},
    {"name": "أرملة جميل الحلو (جورجيت كفوري)", "id": "4217", "phone": "3944382"},
    {"name": "ايلين خوري", "id": "11216", "phone": "3445969"},
    {"name": "عزيزة الريس", "id": "30934", "phone": "81330759"},
    {"name": "نوال سلامة", "id": "30105", "phone": "71432227"},
    {"name": "ملحم أبو أنطون و جورجيت الجميل", "id": "22723", "phone": "71152354"},
    {"name": "سامية أبو نعمة", "id": "2552", "phone": "3853879"},
    {"name": "سامية كركي", "id": "30142", "phone": "71662375"},
    {"name": "حنا القاصوف", "id": "22547", "phone": "3095070"},
    {"name": "مريم السبعلي", "id": "30209", "phone": "3961896"},
    {"name": "عادل سرور", "id": "22668", "phone": "3276894"},
    {"name": "انعام سرور", "id": "30913", "phone": "3276894"},
    {"name": "ابراهيم حنا", "id": "22698", "phone": "70730093"},
    {"name": "طانيوس الحاج", "id": "23161", "phone": "70899515"},
    {"name": "أنطون أبي شبل", "id": "22663", "phone": "4982428"},
    {"name": "فاديا قربان", "id": "4565", "phone": "71514490"},
    {"name": "وردة الجلخ أرملة جورج سابا", "id": "30015", "phone": "70926029"},
    {"name": "جورج عيد", "id": "23148", "phone": "3525064"},
    {"name": "جوزيف عيد", "id": "23150", "phone": "3525064"},
    {"name": "تريز غصن", "id": "30093", "phone": "3436697"},
    {"name": "أرملة جرجي الجلخ ( جانيت)", "id": "22603", "phone": "3660977"},
    {"name": "ايلين الراعي أرملة عبدو أبو ضوموط", "id": "4549", "phone": "3863427"},
    {"name": "اسحاق كرم", "id": "22721", "phone": "3190150"},
    {"name": "نوال الخوري", "id": "7211", "phone": "3079268"},
    {"name": "ماري بطرس كرم", "id": "7297", "phone": "04981026"},
    {"name": "عواطف كرم أرملة موريس أبو حيدر", "id": "3737", "phone": ""},
    {"name": "سيدة الصياح", "id": "30923", "phone": "76188256"},
    {"name": "سارة الصياح", "id": "30085", "phone": "76672137"},
    {"name": "يوسف الصياح", "id": "4003", "phone": "70391311"},
    {"name": "ليليان صليبا", "id": "30976", "phone": "76055837"},
    {"name": "جانيت السبعلي أرملة حنا السبعلي", "id": "22543", "phone": "70106097"},
    {"name": "حفيظة السبعلي", "id": "6799", "phone": "70106097"},
    {"name": "لودي الجميل (أرملة بديع أسعد)", "id": "3939", "phone": "70461730"},
    {"name": "ساسين كرم", "id": "22596", "phone": "4288486"},
    {"name": "ملحم ابراهيم المر", "id": "22528", "phone": "3208475"},
    {"name": "جانيت نبهان أرملة جرجي الجلخ", "id": "22603", "phone": ""},
    {"name": "جوزيف الرميلي", "id": "22607", "phone": ""},
    {"name": "أنطوان أبو شبل", "id": "22663", "phone": ""},
    {"name": "جرجي الريس و شمس الريس", "id": "22695", "phone": "03-132585"},
    {"name": "طانيوس صقر و تريز ضو", "id": "22701", "phone": "81099065"},
    {"name": "عزيزة بو كرم أرملة جميل كرم", "id": "22720", "phone": ""},
    {"name": "قزحيا بو كرم و حنة الراعي", "id": "22721", "phone": "03-190150"},
    {"name": "حنة أبي كرم أرملة ساسين التنوري", "id": "22722", "phone": ""},
    {"name": "جوزيف سماحة وتريز المعلوف", "id": "22726", "phone": "03-532012"},
    {"name": "بشارة الراعي و سمسم السبعلي", "id": "22729", "phone": ""},
    {"name": "افدوك حبيقة أرملة يوسف الحاج", "id": "22732", "phone": ""},
    {"name": "مريم مظلوم أرملة يوسف الياس", "id": "23066", "phone": ""},
    {"name": "مارسيل عبود أرملة أنيس صليبا", "id": "23136", "phone": ""},
    {"name": "بشير السبعلي", "id": "23138", "phone": "70944375"},
    {"name": "جرجس سماحة", "id": "23146", "phone": ""},
    {"name": "جان كعدي", "id": "23151", "phone": ""},
    {"name": "ندى حريق أرملة رشاد أبي فرح", "id": "23154", "phone": ""},
    {"name": "يوسف توفيق الراعي وفيروز سماحة", "id": "23173", "phone": ""},
    {"name": "مخايل قربان وانتصار صليبا", "id": "23241", "phone": "76561186"},
    {"name": "فايز سماحة أرملة منتهى ابراهيم", "id": "30072", "phone": ""},
    {"name": "ملكة الراعي", "id": "30100", "phone": "70282427"},
    {"name": "ايفيت الريف", "id": "30914", "phone": ""},
    {"name": "دليلة المر", "id": "30921", "phone": ""},
    {"name": "روز المر", "id": "30922", "phone": ""},
    {"name": "سعدى كرم", "id": "30926", "phone": "3786728"},
    {"name": "سمية عبد الأحد", "id": "30928", "phone": "70944375"},
    {"name": "هدى السبعلي", "id": "30954", "phone": "76978736"},
    {"name": "وداد السبعلي", "id": "30955", "phone": "3750167"},
    {"name": "وردة المر", "id": "30957", "phone": "76599886"},
    {"name": "حنة السبعلي", "id": "7196", "phone": "4985893"},
    {"name": "الماظ رياشي", "id": "30910", "phone": "71987638"},
    {"name": "نعوة الريس", "id": "30977", "phone": "03-429961"},
]

def main(page: ft.Page):
    page.title = "Cloud Phonebook Directory"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.scroll = ft.ScrollMode.AUTO
    page.rtl = False  # اتجاه إنجليزي من اليسار لليمين
    page.window_width = 450
    page.window_height = 700

    id_field = ft.TextField(label="ID Number (Serial)", border=ft.InputBorder.OUTLINE)
    name_field = ft.TextField(label="Person Name", border=ft.InputBorder.OUTLINE)
    address_field = ft.TextField(label="Address (Optional)", border=ft.InputBorder.OUTLINE)
    
    # تم تصحيح هنا واستخدام e.control.value بدلاً من e.value
    search_field = ft.TextField(
        label="Search by Name or ID...", 
        border=ft.InputBorder.OUTLINE, 
        on_change=lambda e: filter_contacts(e.control.value)
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
            else:
                all_contacts_cache = []
                for item in initial_contacts:
                    c_id = str(item["id"]).strip()
                    c_data = {
                        "id": c_id,
                        "name": item["name"],
                        "address": "",
                        "phones": [item["phone"]] if item["phone"] else []
                    }
                    requests.put(f"{DATABASE_URL}/{c_id}.json", data=json.dumps(c_data), verify=False)
                    all_contacts_cache.append(c_data)

            try:
                all_contacts_cache.sort(key=lambda x: int(str(x.get("id", 0)).strip()))
            except:
                all_contacts_cache.sort(key=lambda x: str(x.get("id", "")).strip())
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
                phones_list = c.get("phones", [])
                phones_str = " | ".join(p for p in phones_list if p) if phones_list else "No Phone Number"
                card = ft.Card(
                    content=ft.Container(
                        padding=12,
                        content=ft.Column([
                            ft.Row([
                                ft.Text(f"Name: {c.get('name')}", weight=ft.FontWeight.BOLD, size=16),
                                ft.Text(f"ID: {c.get('id')}", weight=ft.FontWeight.BOLD),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Text(f"Address: {c.get('address', 'N/A')}"),
                            ft.Text(f"Phones: {phones_str}"),
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
    ft.app(target=main, port=port, host="0.0.0.0")

```
