import asyncio
import threading
import telebot
from telebot import types
from telebot.types import LabeledPrice
import json
import os
import time
import random
import sys
import datetime
from telethon import TelegramClient, functions, errors


# ⚙️ НАЛАШТУВАННЯ (SYSTEM CONFIG)

API_ID = api_id
API_HASH = 'api_hash'
BOT_TOKEN = "Ur_api"

DB_FILE = "titanium_final.json"
SESSION_NAME = "titanium_session"
ADMIN_KEY = "/login_admin_secret_88"

# 🌍 МОВИ ТА ТЕКСТИ (UA & EN)

TEXTS = {
    'ua': {
        'welcome_msg': (
            "👋 **Привіт, {name}!**\n"
            "Я створений, щоб зекономити твій час та ресурси. "
            "Більше не потрібно годинами моніторити маркет вручну — я роблю це за тебе 24/7.\n\n"
            "💎 **МОЇ ПЕРЕВАГИ:**\n"
            "• **Швидкість:** Сканую лімітки швидше за людське око.\n"
            "• **Ефективність:** Автоматично фільтрую 'сміття'.\n"
            "• **Точність:** Сповіщаю миттєво.\n\n"
            "🚀 **ПОЧНИ ПРЯМО ЗАРАЗ:**\n"
            "Тисни /help для додаткової інформації або кнопку Меню."
        ),
        'help_body': (
            "📚 **ДОВІДНИК КОМАНД**\n\n"
            "🔍 **ПОШУК:**\n"
            "🔹 `/add [Назва] [Ціна]`\n"
            "   *Приклад:* `/add Snoop 500`\n"
            "🔹 `/add [Назва] : [Фільтр] : [Мін] : [Макс]`\n\n"
            "📊 **ІНФО:**\n"
            "🔹 `/analyze [Назва]` — Аналіз ціни\n"
            "🔹 `/profile` — Профіль\n"
            "🔹 `/donate` — Підтримати\n\n"
            "⚙️ **СИСТЕМА:**\n"
            "🔸 `/list` — Список завдань\n"
            "🔸 `/del [N]` — Видалити\n"
            "🔸 `/clear` — Очистити\n"
            "🔸 `/status` — Статус\n"
            "🔸 `/run` | `/stop` — Старт/Стоп"
        ),
        'admin_menu': (
            "👑 **АДМІН-ПАНЕЛЬ:**\n"
            "📨 `/reply [ID] [Текст]` — Відповісти\n"
            "🕵️ `/spy` — Шпигун\n"
            "🏹 `/hunter` — Hunter Mode\n"
            "💰 `/hprice [ціна]` — Ліміт Hunter (Зараз: {hprice})\n"
            "📢 `/broadcast [Текст]` — Розсилка\n"
            "💾 `/db` — Скачати базу\n"
            "🚫 `/ban` | ✅ `/unban`"
        ),
        'status_report': (
            "📊 **СТАТУС СИСТЕМИ**\n\n"
            "🟢 Сканер: **{state}**\n"
            "🎯 Ваші цілі: **{count}**\n"
            "📚 Каталог: **{cat}** шт.\n"
            "🏹 Hunter Mode: **{hunter}** (<{hprice})\n"
            "⏱ Uptime: **{uptime}**"
        ),
        'analyze_report': (
            "📊 **АНАЛІЗ РИНКУ: {name}**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "📉 **Floor Price:** {floor} Stars\n"
            "📈 **Average Price:** {avg} Stars\n"
            "📦 **Обсяг:** {vol} шт.\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "💡 *Дані з Telegram Market*"
        ),
        'profile_card': (
            "👤 **ТВІЙ ПРОФІЛЬ**\n\n"
            "🆔 ID: `{uid_val}`\n"
            "📅 Реєстрація: **{joined}**\n"
            "🔰 Статус: **{status}**\n"
            "🎯 Завдань: **{tasks}**\n"
            "💰 Донати: **{donated} Stars**"
        ),
        'donate_prompt': "👇 **Напиши суму донату (числом):**\nНаприклад: 50, 100",
        'donate_thanks': "💖 **Дякую!** Твої зірки отримано.",
        'task_added': "✅ **Ціль додано!**\n📦 {name} < {price}\n🆔 Каталог ID: {gid}",
        'task_not_found': "⚠️ **Не знайдено!** Я не бачу '{name}' у каталозі.\nПеревірте назву (спробуйте англійською).",
        'list_header': "**🎯 ВАШІ ЗАВДАННЯ:**\n\n",
        'list_empty': "📭 Список порожній.",
        'match_single': "🔥 **ЗНАЙДЕНО!**\n🎁 Gift: **{name}**\n💎 Price: **{price} Stars**\n👇 **КУПИТИ ЗАРАЗ:**\n{link}",
        'match_batch': "🔥 **МАСОВИЙ ДРОП ({count} шт)!**\n\n{items}",
        'admin_login': "👑 **АДМІН-ПАНЕЛЬ АКТИВНА.**",
        'support_sent': "✅ **Надіслано адміну.**",
        'reply_received': "📩 **ВІДПОВІДЬ ВІД ПІДТРИМКИ:**\n\n{text}",
        'banned': "⛔️ Доступ заборонено."
    },
    'en': {
        'welcome_msg': (
            "👋 **Hi, {name}!**\n"
            "I am created to save your time and resources. "
            "No need to monitor manually — I do it for you 24/7.\n\n"
            "💎 **MY ADVANTAGES:**\n"
            "• **Speed:** I scan limited gifts faster than the human eye.\n"
            "• **Efficiency:** Auto-filter junk.\n"
            "• **Accuracy:** Instant notifications.\n\n"
            "🚀 **START NOW:**\n"
            "Press /help or use the menu."
        ),
        'help_body': (
            "📚 **COMMAND MANUAL**\n\n"
            "🔍 **SEARCH:**\n"
            "🔹 `/add [Name] [Price]`\n"
            "   *Ex:* `/add Snoop 500`\n"
            "🔹 `/add [Name] : [Filter] : [Min] : [Max]`\n\n"
            "📊 **INFO:**\n"
            "🔹 `/analyze [Name]` — Market Analysis\n"
            "🔹 `/profile` — My Stats\n"
            "🔹 `/donate` — Support Dev\n\n"
            "⚙️ **SYSTEM:**\n"
            "🔸 `/list` — Active tasks\n"
            "🔸 `/del [N]` — Delete task\n"
            "🔸 `/clear` — Clear all\n"
            "🔸 `/status` — System Status\n"
            "🔸 `/run` | `/stop` — Start/Stop"
        ),
        'admin_menu': "👑 **ADMIN PANEL:**\n/reply, /spy, /hunter, /hprice, /broadcast, /db, /ban",
        'status_report': "📊 **STATUS**\n🟢 Scanner: **{state}**\n🎯 Tasks: **{count}**\n📚 Catalog: **{cat}** items\n🏹 Hunter: **{hunter}** (<{hprice})\n⏱ Uptime: **{uptime}**",
        'analyze_report': "📊 **MARKET: {name}**\n━━━━━━━━━━\n📉 **Floor:** {floor} Stars\n📈 **Avg:** {avg} Stars\n📦 **Vol:** {vol} items",
        'profile_card': "👤 **PROFILE**\n\n🆔 ID: `{uid_val}`\n📅 Joined: **{joined}**\n🔰 Status: **{status}**\n🎯 Tasks: **{tasks}**\n💰 Donated: **{donated} Stars**",
        'donate_prompt': "👇 **Enter amount (number):**\nExample: 50, 100",
        'donate_thanks': "💖 **Thank you!** Stars received.",
        'task_added': "✅ **Added:** {name} < {price}\n🆔 Catalog ID: {gid}",
        'task_not_found': "⚠️ **Not Found!** '{name}' is not in catalog.",
        'list_header': "**🎯 TARGETS:**\n\n",
        'list_empty': "📭 Empty list.",
        'match_single': "🔥 **MATCH FOUND!**\n🎁 Gift: **{name}**\n💎 Price: **{price} Stars**\n👇 **BUY NOW:**\n{link}",
        'match_batch': "🔥 **BATCH ({count} items)!**\n\n{items}",
        'admin_login': "👑 **ADMIN ACCESS GRANTED.**",
        'support_sent': "✅ **Sent to admin.**",
        'reply_received': "📩 **SUPPORT REPLY:**\n\n{text}",
        'banned': "⛔️ Banned."
    }
}

# ==============================================================================
# 🧩 VARIABLES & CONFIG
# ==============================================================================
users_db = {}       
user_meta = {}      
user_settings = {}  
config = {
    "admin_id": None, 
    "banned_users": [], 
    "hunter_mode": True, 
    "hunter_max_price": 250, 
    "is_running": True, 
    "start_time": time.time()
}
seen_items = {}     
catalog_map = {}    
unique_gift_ids = [] 
user_states = {}    

bot = telebot.TeleBot(BOT_TOKEN)
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
loop = asyncio.new_event_loop()

# --- 💾 DATABASE ---
def load_database():
    global users_db, user_settings, config, user_meta
    print("📂 Loading Database...", end="")
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                users_db = {int(k): v for k, v in data.get("users", {}).items()}
                user_settings = {int(k): v for k, v in data.get("settings", {}).items()}
                user_meta = {int(k): v for k, v in data.get("meta", {}).items()}
                config.update(data.get("config", {}))
                config['start_time'] = time.time()
            print(" ✅ OK.")
        except: print(" ⚠️ New DB.")
    else: print(" ⚠️ New DB.")

def save_database():
    try:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump({"users": users_db, "settings": user_settings, "meta": user_meta, "config": config}, f, indent=4)
    except: pass

load_database()

# --- HELPERS (NO CONFLICTS) ---
def tx(chat_id, key, **kwargs):
    lang = user_settings.get(chat_id, {}).get('lang', 'ua')
    # Fallback logic: Try EN, if missing -> UA
    if lang == 'en':
        text = TEXTS['en'].get(key, TEXTS['ua'].get(key, ""))
    else:
        text = TEXTS['ua'].get(key, "")
    return text.format(**kwargs) if kwargs else text

def smart_clean(name):
    # Old reliable logic
    return str(name).strip().lower()

def get_price_fixed(item):
    if getattr(item, 'resale_ton_only', False): return None 
    if hasattr(item, 'stars') and item.stars: return item.stars
    if hasattr(item, 'def_price') and hasattr(item.def_price, 'amount'): return item.def_price.amount
    return None

def check_attributes(item, filter_text):
    if not filter_text: return True
    found = []
    if hasattr(item, 'attributes') and item.attributes:
        for a in item.attributes:
            if hasattr(a, 'name'): found.append(str(a.name).lower())
            if hasattr(a, 'string_value'): found.append(str(a.string_value).lower())
    return filter_text in " ".join(found)

def register_user(uid):
    if uid not in user_meta: user_meta[uid] = {'joined': time.time(), 'donated': 0}; save_database()
    elif 'donated' not in user_meta[uid]: user_meta[uid]['donated'] = 0; save_database()

def is_admin(uid): return uid == config.get('admin_id')
def is_banned(uid): return uid in config.get('banned_users', [])

# --- CONSOLE (GARNA RAMKA) ---
def print_dashboard():
    os.system('cls' if os.name == 'nt' else 'clear')
    run_status = "RUNNING" if config['is_running'] else "PAUSED"
    hunter = "ON" if config['hunter_mode'] else "OFF"
    active_users = len(users_db)
    
    print("\033[96m")
    print("╔══════════════════════════════════════════╗")
    print("║        TITANIUM v26 | RESTORED           ║")
    print("╠══════════════════════════════════════════╣")
    print(f"║ Status:      {run_status.ljust(20)}║")
    print(f"║ Hunter:      {hunter.ljust(20)}║")
    print(f"║ Hunter Max:  {str(config['hunter_max_price']).ljust(20)}║")
    print(f"║ Active Users:{str(active_users).ljust(20)}║")
    print(f"║ Catalog:     {str(len(catalog_map)).ljust(20)}║")
    print("╚══════════════════════════════════════════╝")
    print("\033[0m")
    print("\nLogs:")

# ==============================================================================
# 🤖 COMMANDS
# ==============================================================================

@bot.message_handler(commands=['start', 'lang'])
def cmd_start(m):
    register_user(m.chat.id)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🇺🇦 Українська", callback_data='lang_ua'),
               types.InlineKeyboardButton("🇬🇧 English", callback_data='lang_en'))
    bot.send_message(m.chat.id, "🌐 **Language / Мова:**", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def callback_language(call):
    uid = call.message.chat.id
    lang = call.data.split('_')[1]
    
    if uid not in user_settings: user_settings[uid] = {}
    user_settings[uid]['lang'] = lang
    save_database()
    
    bot.delete_message(uid, call.message.message_id)
    welcome_text = tx(uid, 'welcome_msg', name=call.from_user.first_name)
    bot.send_message(uid, welcome_text, parse_mode="Markdown", reply_markup=main_menu_markup(uid))

def main_menu_markup(uid):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("/analyze", "/list")
    markup.row("/profile", "/donate")
    markup.row("/help", "/status")
    return markup

@bot.message_handler(commands=['help'])
def cmd_help(m): bot.reply_to(m, tx(m.chat.id, 'help_body'), parse_mode="Markdown")

# --- SEARCH / ADD ---
@bot.message_handler(commands=['add'])
def cmd_add(m):
    uid = m.chat.id
    text = m.text[5:].strip()
    if not text: return bot.reply_to(m, "ℹ️ `/add Name Price`", parse_mode="Markdown")
    
    try:
        if ':' in text:
            parts = [p.strip() for p in text.split(':')]
            name, flt, min_p, max_p = parts[0], parts[1].lower(), int(parts[2]), int(parts[3])
        else:
            parts = text.rsplit(' ', 1)
            name, price = parts[0].strip(), int(parts[1])
            flt, min_p, max_p = None, 0, price

        # Old logic: Find by key or value
        target_key = smart_clean(name)
        gid = catalog_map.get(target_key)
        
        if not gid:
             for k, v in catalog_map.items():
                 if target_key in k or k in target_key: # Loose match
                     gid = v; target_key = k; break

        if gid:
            if uid not in users_db: users_db[uid] = []
            users_db[uid].insert(0, {"target": target_key, "original_name": name, "price": max_p, "min_price": min_p, "filter": flt})
            save_database()
            bot.reply_to(m, tx(uid, 'task_added', name=name, price=max_p, gid=gid), parse_mode="Markdown")
        else:
            bot.reply_to(m, tx(uid, 'task_not_found', name=name), parse_mode="Markdown")

    except: bot.reply_to(m, "⚠️ Format error.", parse_mode="Markdown")

# --- LIST ---
@bot.message_handler(commands=['list'])
def cmd_list(m):
    uid = m.chat.id
    tasks = users_db.get(uid, [])
    if not tasks: return bot.reply_to(m, tx(uid, 'list_empty'))
    
    msg_text = tx(uid, 'list_header')
    for i, task_item in enumerate(tasks): 
        msg_text += f"**{i+1}. {task_item['original_name']}** (< {task_item['price']})\n"
    
    bot.reply_to(m, msg_text, parse_mode="Markdown")

@bot.message_handler(commands=['del'])
def cmd_del(m):
    try:
        idx = int(m.text.split()[1]) - 1
        users_db[m.chat.id].pop(idx); save_database(); bot.reply_to(m, "🗑")
    except: pass

@bot.message_handler(commands=['clear'])
def cmd_clear(m): users_db[m.chat.id]=[]; save_database(); bot.reply_to(m, "🗑")

# --- ADMIN ---
@bot.message_handler(commands=[ADMIN_KEY.replace('/', '')])
def admin_log(m): config['admin_id']=m.chat.id; save_database(); bot.reply_to(m, tx(m.chat.id, 'admin_login'), parse_mode="Markdown")

@bot.message_handler(commands=['admin'])
def admin_men(m):
    if is_admin(m.chat.id): bot.reply_to(m, tx(m.chat.id, 'admin_menu', hprice=config['hunter_max_price']), parse_mode="Markdown")

@bot.message_handler(commands=['hunter'])
def admin_hunt(m):
    if is_admin(m.chat.id): config['hunter_mode'] = not config['hunter_mode']; save_database(); bot.reply_to(m, f"🏹 Hunter: {config['hunter_mode']}")

@bot.message_handler(commands=['hprice'])
def admin_hp(m):
    if is_admin(m.chat.id): config['hunter_max_price'] = int(m.text.split()[1]); save_database(); bot.reply_to(m, "Updated.")

@bot.message_handler(commands=['broadcast'])
def admin_bc(m):
    if is_admin(m.chat.id):
        for u in users_db: 
            try: bot.send_message(u, f"📢 **SYSTEM:**\n{m.text[10:]}", parse_mode="Markdown") 
            except: pass

@bot.message_handler(commands=['spy'])
def admin_spy(m):
    if is_admin(m.chat.id):
        r = "🕵️ SPY:\n"
        for u, tasks_list in users_db.items(): 
            r += f"{u}: {len(tasks_list)} tasks\n"
        bot.send_message(m.chat.id, r)

@bot.message_handler(commands=['reply'])
def cmd_reply(m):
    if not is_admin(m.chat.id): return
    try:
        _, tid, txt = m.text.split(maxsplit=2)
        bot.send_message(int(tid), tx(int(tid), 'reply_received', text=txt), parse_mode="Markdown")
        bot.reply_to(m, "✅ Sent.")
    except: pass

@bot.message_handler(commands=['support'])
def cmd_sup(m): user_states[m.chat.id]="sup"; bot.reply_to(m, "✍️ Write msg:")
@bot.message_handler(func=lambda m: user_states.get(m.chat.id)=="sup")
def h_sup(m):
    if config['admin_id']: bot.send_message(config['admin_id'], f"📩 SUP ({m.chat.id}):\n{m.text}\n👉 `/reply {m.chat.id} ...`", parse_mode="Markdown")
    bot.reply_to(m, tx(m.chat.id, 'support_sent')); user_states[m.chat.id]=None

@bot.message_handler(commands=['status'])
def cmd_stat(m):
    uid = m.chat.id
    s = "ON" if config['is_running'] else "PAUSED"
    h = "ON" if config['hunter_mode'] else "OFF"
    sec = int(time.time()-config['start_time'])
    bot.reply_to(m, tx(uid, 'status_report', state=s, count=len(users_db.get(uid,[])), cat=len(catalog_map), hunter=h, hprice=config['hunter_max_price'], uptime=str(datetime.timedelta(seconds=sec))), parse_mode="Markdown")

@bot.message_handler(commands=['analyze'])
def cmd_analyze(m):
    threading.Thread(target=lambda: asyncio.run_coroutine_threadsafe(do_analyze(m), loop)).start()

async def do_analyze(m):
    try:
        name = smart_clean(m.text.split(maxsplit=1)[1])
        gid = catalog_map.get(name)
        
        # OLD LOGIC for analyze search
        if not gid: 
             for k, v in catalog_map.items():
                 if name in k: gid = v; name = k; break
        
        if not gid: return bot.reply_to(m, "❌ Not found.")
        
        bot.send_chat_action(m.chat.id, 'typing')
        res = await client(functions.payments.GetResaleStarGiftsRequest(gift_id=gid, sort_by_price=True, limit=20, offset=''))
        prices = [get_price_fixed(i) for i in res.gifts if get_price_fixed(i)]
        
        if prices:
            msg = tx(m.chat.id, 'analyze_report', name=name.upper(), floor=min(prices), avg=int(sum(prices)/len(prices)), vol=len(prices))
            bot.reply_to(m, msg, parse_mode="Markdown")
        else: bot.reply_to(m, "📭 Empty.")
    except: pass

@bot.message_handler(commands=['profile'])
def cmd_profile(m):
    uid = m.chat.id; register_user(uid)
    meta = user_meta[uid]
    j = datetime.datetime.fromtimestamp(meta['joined']).strftime('%Y-%m-%d')
    s = "ADMIN" if is_admin(uid) else "User"
    bot.reply_to(m, tx(uid, 'profile_card', uid_val=uid, joined=j, status=s, tasks=len(users_db.get(uid,[])), donated=meta['donated']), parse_mode="Markdown")

@bot.message_handler(commands=['donate'])
def cmd_donate(m): user_states[m.chat.id]="donate"; bot.reply_to(m, tx(m.chat.id, 'donate_prompt'))

@bot.message_handler(func=lambda m: user_states.get(m.chat.id)=="donate")
def h_donate(m):
    try:
        amt = int(m.text)
        bot.send_invoice(m.chat.id, "Support", "Donation", "d", "", "XTR", [LabeledPrice("G", amt)])
        user_states[m.chat.id] = None
    except: pass

@bot.pre_checkout_query_handler(func=lambda q: True)
def pc(q): bot.answer_pre_checkout_query(q.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def pay(m):
    register_user(m.chat.id)
    user_meta[m.chat.id]['donated'] += m.successful_payment.total_amount
    save_database()
    bot.reply_to(m, tx(m.chat.id, 'donate_thanks'))

@bot.message_handler(commands=['run'])
def r(m): config['is_running']=True; save_database(); bot.reply_to(m, "▶️"); print_dashboard()
@bot.message_handler(commands=['stop'])
def s(m): config['is_running']=False; save_database(); bot.reply_to(m, "⏸"); print_dashboard()

# ==============================================================================
# 🕵️ SCANNER
# ==============================================================================
async def safe_api(coro):
    try: return await coro
    except: return None

async def scanner_engine():
    global unique_gift_ids, loop
    print("🚀 Loading Catalog...")
    await client.start()
    
    try:
        raw = await safe_api(client(functions.payments.GetStarGiftsRequest(hash=0)))
        if raw:
            for g in raw.gifts:
                # LOAD BOTH TITLE AND SLUG (Best compatibility)
                if hasattr(g, 'title'): catalog_map[smart_clean(g.title)] = g.id
                if hasattr(g, 'slug'): catalog_map[smart_clean(g.slug)] = g.id
                if getattr(g, 'limited', False): unique_gift_ids.append(g.id)
            print(f"✅ Catalog Loaded: {len(catalog_map)} keys.")
    except: pass
    
    print_dashboard()
    h_idx = 0

    while True:
        if not config['is_running']: await asyncio.sleep(2); continue
        
        if users_db:
            for uid, tasks in list(users_db.items()):
                for task in tasks:
                    sys.stdout.write(f"\r🔎 Scanning: {task['original_name']}...   ")
                    sys.stdout.flush()
                    
                    gid = catalog_map.get(task['target'])
                    if not gid: continue 
                    
                    await asyncio.sleep(random.uniform(0.6, 1.2))
                    try:
                        res = await client(functions.payments.GetResaleStarGiftsRequest(gift_id=gid, sort_by_price=True, limit=30, offset=''))
                        batch = []
                        for item in res.gifts:
                            p = get_price_fixed(item)
                            if p and task['min_price'] <= p <= task['price']:
                                if task['filter'] and not check_attributes(item, task['filter']): continue
                                s, n = getattr(item, 'slug', 'gift'), getattr(item, 'num', 0)
                                key = f"{uid}_{s}_{n}_{p}"
                                if key not in seen_items:
                                    batch.append({'name': f"{s} #{n}", 'price': p, 'link': f"https://t.me/nft/{s}-{n}"})
                                    seen_items[key] = True
                        if batch:
                            if len(batch) > 5:
                                txt = "\n".join([f"🔹 [{i['name']}]({i['link']}) — {i['price']}" for i in batch[:10]])
                                bot.send_message(uid, tx(uid, 'match_batch', count=len(batch), items=txt), parse_mode="Markdown", disable_web_page_preview=True)
                            else:
                                for i in batch:
                                    bot.send_message(uid, tx(uid, 'match_single', name=i['name'], price=i['price'], link=i['link']), parse_mode="Markdown")
                    except: pass

        if config['hunter_mode'] and unique_gift_ids:
            try:
                gid = unique_gift_ids[h_idx]
                res = await client(functions.payments.GetResaleStarGiftsRequest(gift_id=gid, sort_by_price=True, limit=5, offset=''))
                for item in res.gifts:
                    p = get_price_fixed(item)
                    if p and p <= config['hunter_max_price']:
                        s, n = getattr(item, 'slug', 'gift'), getattr(item, 'num', 0)
                        key = f"hunt_{s}_{n}_{p}"
                        if key not in seen_items and config['admin_id']:
                            bot.send_message(config['admin_id'], f"🏹 **HUNTER:** {s} #{n} - {p}\n🔗 https://t.me/nft/{s}-{n}")
                            seen_items[key] = True
            except: pass
            h_idx = (h_idx + 1) % len(unique_gift_ids)
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.set_event_loop(loop)
    threading.Thread(target=bot.infinity_polling).start()

    loop.run_until_complete(scanner_engine())
