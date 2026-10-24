#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mcspeak · render_card.py —— 把订单数据填进 HTML 模板，生成双语卡片（一格一事、双语同格）。

用法：
  python scripts/render_card.py --type counter --lang ru --out examples/ru/counter_card.html --demo
  python scripts/render_card.py --type payment --lang ja --out examples/ja/payment_notice.html --demo
  python scripts/render_card.py --type pickup  --lang ar --out examples/ar/pickup_card.html --pickup-code 00000 --demo

约定（与 references/ 对齐）：
  1. 给店员看的**中文**全部来自 references/staff_phrases_zh.md（含"店员常问"表的问答），脚本不新写中文句。
  2. 状态与 App 词汇来自 references/order_status_map.md。
  3. 订单数据来自 references/samples/17-create-order.json（真实下单返回）。
  4. 定制文案由**下单参数**生成自然中文（"不要切块生菜""可乐去冰"），只出现一次，不用 App 的 "冰(去冰)" 写法。
  5. 全部字符串清除 markdown 标记（** * `），模板只渲染 HTML。
  6. 卡片文案覆盖 en / ru / ja / ar；其他语言回退英文（聊天层仍按 locale_style.md 覆盖 8 语）。
"""

import argparse
import json
import os
import re
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(ROOT, "references")
TPL = os.path.join(ROOT, "templates")
DEFAULT_SAMPLE = os.path.join(REF, "samples", "17-create-order.json")

# ---------------------------------------------------------------- 解析参考文件

def parse_phrases():
    path = os.path.join(REF, "staff_phrases_zh.md")
    out = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"^\|\s*`(staff\.[a-z_]+)`\s*\|\s*([^|]+?)\s*\|", line)
            if m:
                out[m.group(1).replace("staff.", "")] = m.group(2).strip()
    return out


def parse_staff_q():
    """返回 [(问题中文, [答案中文...]), ...]，全部来自「店员常问」表。"""
    path = os.path.join(REF, "staff_phrases_zh.md")
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not re.match(r"^\|\s*\d+\s*\|", line):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 4:
                continue
            q = cells[1].replace("「", "").replace("」", "")
            q = re.split(r"[／/]", q)[0].strip()
            ans = [v.strip().strip("「」 ") for v in re.split(r"[／/]", cells[3]) if v.strip()]
            ans = [a for a in ans if "{" not in a and "`" not in a]
            rows.append((q, ans))
    return rows


def parse_app_vocab():
    path = os.path.join(REF, "order_status_map.md")
    text = open(path, encoding="utf-8").read()
    sec = text.split("## 2. 麦当劳 App 界面词汇对照表")[-1].split("### 各状态的英文对照")[0]
    out = []
    for line in sec.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 4 and cells[0] not in ("中文原文", "") and not set(cells[0]) <= {"-"}:
            out.append({"zh": cells[0], "en": cells[1]})
    return out


PHRASES = parse_phrases()
STAFF_Q = parse_staff_q()
APP_VOCAB = parse_app_vocab()
ZH_DINE = next((v["zh"] for v in APP_VOCAB if v["en"].lower().startswith("dining")), "就餐方式")
ZH_PICKUP = next((v["zh"] for v in APP_VOCAB if v["zh"] == "取餐码"), "取餐码")

# ---------------------------------------------------------------- 订单

NON_FOOD = ("麦金卡", "月卡", "会员卡", "礼券", "券包")

PINYIN = {"麦辣鸡腿汉堡三件套": "mài là jī tuǐ hàn bǎo sān jiàn tào",
          "麦辣鸡腿汉堡": "mài là jī tuǐ hàn bǎo", "中薯条": "zhōng shǔ tiáo",
          "可乐中杯": "kě lè zhōng bēi"}


def load_order(path, pickup_code=None):
    raw = json.load(open(path, encoding="utf-8"))
    data = raw.get("raw_response", raw).get("data", raw.get("data", raw))
    od = data.get("orderDetail", data)
    items = []
    for p in od.get("orderProductList", []):
        name = p.get("productName", "")
        if any(k in name for k in NON_FOOD):
            continue
        combos = []
        for c in p.get("comboItemList", []):
            cname = c.get("itemName", "")
            m = re.match(r"^(.*?)\s+([^\s]+\([^)]*\))$", cname)
            combos.append({"zh": m.group(1).strip() if m else cname,
                           "custom": m.group(2).strip() if m else ""})
        items.append({"zh": name, "qty": p.get("quantity", 1), "combos": combos})
    money = lambda v: "%.2f" % float(v or 0)
    exp = od.get("expirePayTime", "")
    return {"store_zh": od.get("storeName", ""), "items": items,
            "paid": money(od.get("realTotalAmount")), "list": money(od.get("totalAmount")),
            "saved": money(od.get("totalDiscountAmount")),
            "coupons": [c.get("couponName", "") for c in od.get("couponList", [])],
            "takeaway_zh": od.get("takeWay", "外带"),
            "pickupCode": pickup_code or "", "deadline": exp[11:16] if len(exp) >= 16 else "--:--",
            "payUrl": data.get("payH5Url", "")}


def natural_custom(base, custom):
    """把 App 的 '切块生菜(不要)' / '冰(去冰)' 变成自然中文。"""
    if custom.endswith("(不要)"):
        return "不要" + custom[:-4]
    if custom.endswith("(去冰)"):
        return re.sub(r"(中杯|大杯|小杯)$", "", base) + "去冰"
    return re.sub(r"[()（）]", "", custom)


# ---------------------------------------------------------------- 词条（en/ru/ja/ar）

L = {
 "en": dict(howto="Hello, this is my order — please read the Chinese in each row.",
            howtoBack="Show this screen to the staff; whatever row they point at, look at that row.",
            speak="Read the Chinese aloud", back="Back", locked="The pickup code appears only after payment.",
            payNow="Pay now", priceLabel="Reference price", priceNote="The till price is final.",
            saved="You saved", coupons="Coupons", stale="This card is over 30 minutes old — please check the order again.",
            sampleTag="SAMPLE", sampleNote="Sample data, not a real order.",
            dine="Dine in", takeaway="Takeaway", wechat="WeChat Pay", alipay="Alipay",
            q=["Use the kiosk to order", "Dine in or takeaway?", "Would you like to upsize?",
               "Are you a member? Any coupons?", "How will you pay?", "Anything else?",
               "Please wait for your number"],
            say=["Some napkins, please", "Two ketchup packets, please",
                 "One item is missing — could you check?", "I don't think this is mine",
                 "Thank you so much!"],
            steps=["Open the McDonald's app and find your order",
                   "When it shows 请取餐, go to the pickup counter",
                   "Show this card — the staff will read the number"],
            pos=["1st from left", "middle", "right, yellow"], status={"待支付": "Awaiting payment"},
            staffLine="Here is my order — pickup code is"),
 "ru": dict(howto="Здравствуйте, это мой заказ — прочитайте китайский текст в каждой строке.",
            howtoBack="Покажите экран сотруднику; на какую строку он покажет — ту и смотрите.",
            speak="Прочитать по-китайски", back="Назад", locked="Номер появится только после оплаты.",
            payNow="Оплатить", priceLabel="Ориентировочно", priceNote="Итоговую цену определяет касса.",
            saved="Вы сэкономили", coupons="Купоны", stale="Карточке больше 30 минут — проверьте заказ заново.",
            sampleTag="ПРИМЕР", sampleNote="Пример данных, не реальный заказ.",
            dine="В зале", takeaway="С собой", wechat="WeChat Pay", alipay="Alipay",
            q=["Заказывайте в терминале", "Здесь или с собой?", "Увеличить порцию?",
               "Вы участник программы? Есть купоны?", "Как будете платить?", "Что-то ещё?",
               "Подождите, пока назовут номер"],
            say=["Дайте, пожалуйста, салфетки", "Два пакетика кетчупа, пожалуйста",
                 "Кажется, одного блюда не хватает", "Кажется, это не мой заказ",
                 "Большое спасибо!"],
            steps=["Откройте приложение McDonald's и найдите заказ",
                   "Когда появится 请取餐, подойдите к стойке выдачи",
                   "Покажите эту карточку — номер прочитает сотрудник"],
            pos=["1-я слева", "по центру", "справа, жёлтая"], status={"待支付": "Ожидает оплаты"},
            staffLine="Вот мой заказ, номер получения"),
 "ja": dict(howto="こんにちは。これが注文です。各枠の中国語をお読みください。",
            howtoBack="画面を店員に見せてください。店員が指した枠を、あなたも見てください。",
            speak="中国語を読み上げる", back="戻る", locked="受け取り番号はお支払い後に表示されます。",
            payNow="支払う", priceLabel="参考価格", priceNote="最終価格はレジで確定します。",
            saved="お得になった金額", coupons="クーポン", stale="このカードは30分以上前のものです。注文を確認し直してください。",
            sampleTag="サンプル", sampleNote="サンプルデータです。実際の注文ではありません。",
            dine="店内", takeaway="持ち帰り", wechat="WeChat Pay", alipay="Alipay",
            q=["セルフレジで注文してください", "店内ですか、持ち帰りですか？", "サイズを大きくしますか？",
               "会員ですか？クーポンはありますか？", "お支払い方法は？", "ほかにご注文は？",
               "番号が呼ばれるまでお待ちください"],
            say=["紙ナプキンをください", "ケチャップを2つください",
                 "商品が1つ足りないようです", "これは私の注文ではないようです",
                 "ありがとうございました！"],
            steps=["マクドナルドアプリで注文を開く", "「请取餐」が出たら受け取りカウンターへ",
                   "このカードを見せる（番号は店員が読みます）"],
            pos=["左から1番目", "真ん中", "右・黄色"], status={"待支付": "お支払い待ち"},
            staffLine="注文はこちらです。受け取り番号は"),
 "ar": dict(howto="مرحبًا، هذا طلبي — يرجى قراءة النص الصيني في كل صف.",
            howtoBack="اعرض الشاشة على الموظف؛ أي صف يشير إليه، انظر إليه.",
            speak="قراءة النص الصيني", back="رجوع", locked="يظهر رقم الاستلام بعد الدفع فقط.",
            payNow="ادفع الآن", priceLabel="السعر التقريبي", priceNote="السعر النهائي في الكاشير.",
            saved="وفّرت", coupons="القسائم", stale="عمر البطاقة أكثر من 30 دقيقة — تحقّق من الطلب مجددًا.",
            sampleTag="نموذج", sampleNote="بيانات تجريبية وليست طلبًا حقيقيًا.",
            dine="داخل المطعم", takeaway="طلب خارجي", wechat="WeChat Pay", alipay="Alipay",
            q=["اطلب من الجهاز الذاتي", "داخل المطعم أم خارجي؟", "هل تريد حجمًا أكبر؟",
               "هل أنت عضو؟ لديك قسائم؟", "كيف ستدفع؟", "هل تريد شيئًا آخر؟",
               "يرجى الانتظار حتى يُنادى رقمك"],
            say=["أريد مناديل، لو سمحت", "أريد كيسين كاتشاب، لو سمحت",
                 "يبدو أن أحد الأصناف ناقص", "يبدو أن هذا ليس طلبي",
                 "شكرًا جزيلًا!"],
            steps=["افتح تطبيق ماكدونالدز واطلب الطلب", "عند ظهور 请取餐 توجّه إلى كاونتر الاستلام",
                   "اعرض هذه البطاقة — سيقرأ الموظف الرقم"],
            pos=["الأول من اليسار", "الوسط", "اليمين، أصفر"], status={"待支付": "بانتظار الدفع"},
            staffLine="هذا طلبي، رقم الاستلام"),
}

# 补充词条
_EXTRA = {
    "en": dict(pickupLabel="PICKUP CODE", payBefore="Pay before"),
    "ru": dict(pickupLabel="НОМЕР ПОЛУЧЕНИЯ", payBefore="Оплатите до"),
    "ja": dict(pickupLabel="受け取り番号", payBefore="お支払い期限"),
    "ar": dict(pickupLabel="رقم الاستلام", payBefore="يرجى الدفع قبل"),
}
for _k, _v in _EXTRA.items():
    L[_k].update(_v)

# 分区标题的用户语言部分（中文部分在模板里固定）
_EXTRA2 = {
    "en": dict(secOrder="my order", secFacts="how and pay", secDlg="tap a row, then show the screen",
               secStaffAsk="staff may ask", secCustSay="I want to say", secStatus="order status",
               secApp="in the app", secSteps="how to collect", secPay="how to pay"),
    "ru": dict(secOrder="мой заказ", secFacts="как и оплата", secDlg="нажмите строку и покажите экран",
               secStaffAsk="персонал может спросить", secCustSay="я хочу сказать", secStatus="статус заказа",
               secApp="в приложении", secSteps="как получить", secPay="как оплатить"),
    "ja": dict(secOrder="注文", secFacts="食事と支払い", secDlg="行をタップして画面を見せる",
               secStaffAsk="店員が聞くこと", secCustSay="伝えたいこと", secStatus="注文の状態",
               secApp="アプリの表示", secSteps="受け取り方", secPay="支払い方法"),
    "ar": dict(secOrder="طلبي", secFacts="الطعام والدفع", secDlg="اضغط صفًا ثم اعرض الشاشة",
               secStaffAsk="قد يسأل الموظف", secCustSay="أريد أن أقول", secStatus="حالة الطلب",
               secApp="في التطبيق", secSteps="طريقة الاستلام", secPay="طريقة الدفع"),
}
for _k, _v in _EXTRA2.items():
    L[_k].update(_v)

# 付款：首选 App，链接备用
_EXTRA3 = {
    "en": dict(payInApp="pay in the app",
               tapYellow="Tap the yellow “去支付” at the bottom right of the app.",
               payLink="Backup: payment link"),
    "ru": dict(payInApp="оплата в приложении",
               tapYellow="Нажмите жёлтую кнопку «去支付» справа внизу в приложении.",
               payLink="Запасной вариант: ссылка"),
    "ja": dict(payInApp="アプリで支払う",
               tapYellow="アプリ右下の黄色い「去支付」を押してください。",
               payLink="予備：支払いリンク"),
    "ar": dict(payInApp="الدفع في التطبيق",
               tapYellow="اضغط الزر الأصفر «去支付» أسفل يمين التطبيق.",
               payLink="بديل: رابط الدفع"),
}
for _k, _v in _EXTRA3.items():
    L[_k].update(_v)

# 中文定制 → 各语言（由 natural_custom 生成的中文做 key）
CUSTOM_LOC = {
    "不要切块生菜": {"en": "no shredded lettuce", "ru": "без салата", "ja": "レタス抜き", "ar": "بدون خس"},
    "可乐去冰": {"en": "Coke, no ice", "ru": "кола без льда", "ja": "コーラ氷なし", "ar": "كولا بدون ثلج"},
}
# 中文答案 → 各语言
ANS_LOC = {
    "我不太会用自助机，麻烦您帮我在柜台点好吗？谢谢～":
        {"en": "I can't use the kiosk — could you take my order here, please?",
         "ru": "Я не умею пользоваться терминалом — оформите, пожалуйста, здесь.",
         "ja": "セルフレジが苦手です。カウンターで注文してもらえますか？",
         "ar": "لا أستطيع استخدام الجهاز — هل يمكنك تسجيل طلبي هنا؟"},
    "堂食，谢谢～": {"en": "Dine in, please", "ru": "В зале, пожалуйста", "ja": "店内で", "ar": "داخل المطعم"},
    "外带，谢谢～": {"en": "Takeaway, please", "ru": "С собой, пожалуйста", "ja": "持ち帰りで", "ar": "طلب خارجي"},
    "不用了，谢谢～": {"en": "No, thank you", "ru": "Нет, спасибо", "ja": "大丈夫です", "ar": "لا، شكرًا"},
    "好的，麻烦升级大杯，谢谢～": {"en": "Yes, please upsize", "ru": "Да, побольше, пожалуйста",
                            "ja": "はい、大きくしてください", "ar": "نعم، حجم أكبر"},
    "不是会员，谢谢～": {"en": "Not a member, thanks", "ru": "Не участник, спасибо",
                     "ja": "会員ではありません", "ar": "لست عضوًا"},
    "我用这个券，麻烦您看一下～": {"en": "I'd like to use this coupon", "ru": "Хочу использовать этот купон",
                          "ja": "このクーポンを使いたいです", "ar": "أريد استخدام هذه القسيمة"},
    "微信，谢谢～": {"en": "WeChat Pay, please", "ru": "WeChat Pay, пожалуйста", "ja": "WeChat Pay で", "ar": "WeChat Pay"},
    "支付宝，谢谢～": {"en": "Alipay, please", "ru": "Alipay, пожалуйста", "ja": "Alipay で", "ar": "Alipay"},
    "现金可以吗？": {"en": "Can I pay cash?", "ru": "Можно наличными?", "ja": "現金でもいいですか？", "ar": "هل يمكن الدفع نقدًا؟"},
    "就这些，谢谢～": {"en": "That's all, thanks", "ru": "Это всё, спасибо", "ja": "以上です", "ar": "هذا كل شيء"},
    "好的，谢谢～": {"en": "Sure, thanks", "ru": "Хорошо, спасибо", "ja": "はい、ありがとうございます", "ar": "حسنًا، شكرًا"},
}

Q_LOC = {
    "请去自助机点餐": {"en": "Please order at the kiosk", "ru": "Заказывайте в терминале",
                 "ja": "セルフレジで注文してください", "ar": "اطلب من الجهاز الذاتي"},
    "堂食还是外带？": {"en": "Dine in or takeaway?", "ru": "Здесь или с собой?", "ja": "店内ですか、持ち帰りですか？",
                 "ar": "داخل المطعم أم خارجي؟"},
    "要加大的吗？": {"en": "Would you like to upsize?", "ru": "Увеличить порцию?", "ja": "サイズを大きくしますか？",
                "ar": "هل تريد حجمًا أكبر؟"},
    "是会员吗？": {"en": "Are you a member? Any coupons?", "ru": "Вы участник? Есть купоны?",
              "ja": "会員ですか？クーポンは？", "ar": "هل أنت عضو؟ لديك قسائم؟"},
    "怎么付款？": {"en": "How will you pay?", "ru": "Как будете платить?", "ja": "お支払い方法は？", "ar": "كيف ستدفع؟"},
    "还要别的吗？": {"en": "Anything else?", "ru": "Что-то ещё?", "ja": "ほかにご注文は？", "ar": "هل تريد شيئًا آخر؟"},
    "请到旁边等叫号": {"en": "Please wait for your number", "ru": "Подождите, назовут номер",
                "ja": "番号が呼ばれるまでお待ちください", "ar": "يرجى الانتظار حتى يُنادى رقمك"},
    "请稍等一下": {"en": "One moment, please", "ru": "Минутку, пожалуйста", "ja": "少々お待ちください",
              "ar": "لحظة من فضلك"},
    "这个卖完了": {"en": "This one is sold out", "ru": "Это закончилось", "ja": "これは売り切れです",
             "ar": "هذا الصنف نفد"},
    "这个要等 10 分钟": {"en": "This takes 10 minutes", "ru": "Это будет через 10 минут",
                  "ja": "これは10分かかります", "ar": "هذا يحتاج 10 دقائق"},
    "需要袋子吗？": {"en": "Do you need a bag?", "ru": "Нужен пакет?", "ja": "袋は必要ですか？", "ar": "هل تريد كيسًا؟"},
    "餐具需要吗？": {"en": "Do you need cutlery?", "ru": "Нужны приборы?", "ja": "カトラリーは必要ですか？",
               "ar": "هل تريد أدوات؟"},
    "不好意思，听不懂": {"en": "Sorry, I don't understand", "ru": "Извините, не понимаю",
                 "ja": "すみません、わかりません", "ar": "عذرًا، لا أفهم"},
}

SAY_KEYS = ["tissue", "ketchup", "missing_item", "not_mine", "thanks"]
STATUS_ORDER = ["待支付", "配餐中", "请取餐", "订单已完成", "订单已取消"]

# ---------------------------------------------------------------- 组装

def strip_md(s):
    if isinstance(s, dict):
        return {k: strip_md(v) for k, v in s.items()}
    if isinstance(s, list):
        return [strip_md(v) for v in s]
    if isinstance(s, str):
        return s.replace("**", "").replace("*", "").replace("`", "")
    return s


def build(kind, lang, order, sample=False):
    lang = lang if lang in L else "en"
    t = L[lang]
    names = {"麦辣鸡腿汉堡三件套": {"en": "McSpicy Chicken Burger Meal", "ru": "Набор с острым куриным бургером",
                              "ja": "マックスパイシーチキンバーガーセット", "ar": "وجبة برغر الدجاج الحار"},
             "麦辣鸡腿汉堡": {"en": "McSpicy Chicken Burger", "ru": "Острый куриный бургер",
                          "ja": "マックスパイシーチキンバーガー", "ar": "برغر الدجاج الحار"},
             "中薯条": {"en": "Medium fries", "ru": "Картофель фри (сред.)", "ja": "ポテト（M）", "ar": "بطاطس (وسط)"},
             "可乐中杯": {"en": "Coca-Cola (M)", "ru": "Кола (сред.)", "ja": "コーラ（M）", "ar": "كولا (وسط)"}}
    num = "①②③④⑤⑥⑦⑧⑨"

    items, combos_zh_all, combos_loc_all, customs = [], [], [], []
    for i, it in enumerate(order["items"]):
        cz = [c["zh"] for c in it["combos"]]
        cl = [names.get(c["zh"], {}).get(lang, c["zh"]) for c in it["combos"]]
        my_customs = []
        for c in it["combos"]:
            if c.get("custom"):
                zh = natural_custom(c["zh"], c["custom"])
                loc = CUSTOM_LOC.get(zh, {}).get(lang, c["custom"])
                my_customs.append({"zh": zh, "local": loc})
                customs.append({"zh": zh, "local": loc})
        items.append({"n": num[i] if i < len(num) else str(i + 1),
                      "zh": it["zh"], "local": names.get(it["zh"], {}).get(lang, it["zh"]),
                      "qty": it["qty"], "combosZh": "＋".join(cz), "combosLocal": " · ".join(cl),
                      "customs": my_customs})

    take_zh = order["takeaway_zh"]
    facts = [{"icon": "🍽️" if take_zh == "堂食" else "🛍️", "zh": take_zh,
              "local": t["dine"] if take_zh == "堂食" else t["takeaway"]},
             {"icon": "💳", "zh": "微信支付", "local": t["wechat"]}]

    # 店员想问（中文来自「店员常问」表；答案同样来自该表，配本地语言）
    qa = []
    for qz, answers in STAFF_Q:
        ql = Q_LOC.get(qz, {}).get(lang)
        if not ql:
            continue
        ans = []
        for az in answers:
            al = ANS_LOC.get(az, {}).get(lang)
            if al:
                ans.append({"zh": az, "local": al})
        if ans:
            qa.append({"q": {"zh": qz, "local": ql}, "answers": ans[:3]})
    qa = qa[:7]

    say = []
    for k, zh_slot in zip(SAY_KEYS, t["say"]):
        if PHRASES.get(k):
            say.append({"zh": PHRASES[k], "local": zh_slot})

    app_vocab = []
    for zh, style, pos in [("取消订单", "outline", t["pos"][0]),
                           ("联系客服", "outline", t["pos"][1]),
                           ("去支付", "yellow", t["pos"][2])]:
        row = next((v for v in APP_VOCAB if v["zh"] == zh), None)
        if row:
            loc = {"en": {"取消订单": "Cancel order", "联系客服": "Contact us", "去支付": "Pay now"},
                   "ru": {"取消订单": "Отменить", "联系客服": "Поддержка", "去支付": "Оплатить"},
                   "ja": {"取消订单": "キャンセル", "联系客服": "お問い合わせ", "去支付": "支払う"},
                   "ar": {"取消订单": "إلغاء", "联系客服": "الدعم", "去支付": "ادفع"}}[lang][zh]
            app_vocab.append({"zh": zh, "local": loc, "style": style, "pos": pos})

    status_rows = [
        {"zh": "待支付", "local": {"en": "Awaiting payment", "ru": "Ожидает оплаты", "ja": "お支払い待ち", "ar": "بانتظار الدفع"}[lang],
         "action": "", "hot": False},
        {"zh": "配餐中", "local": {"en": "Preparing", "ru": "Готовится", "ja": "準備中", "ar": "قيد التحضير"}[lang],
         "action": "", "hot": False},
        {"zh": "请取餐", "local": {"en": "Ready — collect now", "ru": "Готово — заберите", "ja": "できあがり", "ar": "جاهز — استلم"}[lang],
         "action": "", "hot": True},
        {"zh": "订单已完成", "local": {"en": "Completed", "ru": "Выполнен", "ja": "完了", "ar": "مكتمل"}[lang],
         "action": "", "hot": False},
    ]

    data = {
        "kind": kind, "lang": lang, "dir": "rtl" if lang == "ar" else "ltr",
        "generatedAt": datetime.now().strftime("%Y-%m-%d %H:%M"), "isSample": bool(sample),
        "store": {"zh": order["store_zh"], "pinyin": "Mài dāng láo Jǐ nán Shān dà lù (Chéng dà gāo kē) cān tīng",
                  "local": "McDonald's Shanda Road"},
        "howto": {"zh": "您好，这是我要点的餐，请看每一格的中文。", "local": t["howtoBack"]},
        "items": items, "facts": facts,
        "price": {"zhLabel": "参考价格", "amount": "¥" + order["list"],
                  "local": t["priceLabel"] + " ¥" + order["list"],
                  "note": t["priceNote"],
                  "saved": (t["saved"] + " ¥" + order["saved"]) if order["saved"] not in ("0.00", "0") else "",
                  "coupons": (t["coupons"] + ": " + " · ".join(order["coupons"])) if order["coupons"] else ""},
        "status": {"zh": "待支付", "local": t["status"]["待支付"]},
        "appStatus": {"zh": "待支付", "local": t["status"]["待支付"]},
        "deadline": {"hhmm": order["deadline"],
                     "zh": "请在 " + order["deadline"] + " 前付款",
                     "local": t["payBefore"] + " " + order["deadline"]},
        "pickup": {"code": order["pickupCode"], "zh": ZH_PICKUP, "local": t["pickupLabel"]},
        "payUrl": order["payUrl"], "paySteps": [],
        "steps": [{"zh": s, "local": L[lang]["steps"][i]} for i, s in enumerate(
                  ["打开麦当劳 App 订单页", "看到「请取餐」就去取餐台", "把这张卡给店员看"])],
        "appVocab": app_vocab, "statusRows": status_rows,
        "qaStaff": qa, "sayCustomer": say,
        "sec": {"order": t["secOrder"], "facts": t["secFacts"], "dlg": t["secDlg"],
                "staffAsk": t["secStaffAsk"], "custSay": t["secCustSay"],
                "status": t["secStatus"], "app": t["secApp"], "steps": t["secSteps"], "pay": t["secPay"]},
        "staffLine": {"zh": "您好！我在手机上点好了，取餐码是 {code}，谢谢！", "local": t["staffLine"]},
        "ui": {"speak": t["speak"], "back": t["back"], "stale": t["stale"], "sampleTag": t["sampleTag"],
               "sampleNote": t["sampleNote"], "locked": t["locked"], "payNow": t["payNow"],
               "payInApp": t["payInApp"], "tapYellow": t["tapYellow"], "payLink": t["payLink"],
               "noSpeech": "—"},
        "zhui": {"back": "返回"},
    }

    # 付款卡：首选 App，链接备用
    data["paySteps"] = [
        {"zh": "打开麦当劳 App，在我的订单里点右下角黄色的「去支付」",
         "local": {"en": "Open the McDonald's app → your order → tap the yellow “去支付” at the bottom right",
                   "ru": "Откройте приложение McDonald's → заказ → жёлтая кнопка «去支付» справа внизу",
                   "ja": "マクドナルドアプリ → 注文 → 右下の黄色い「去支付」を押す",
                   "ar": "افتح تطبيق ماكدونالدز → الطلب → اضغط الزر الأصفر «去支付» أسفل اليمين"}[lang]},
        {"zh": "付款成功后回到对话里告诉我",
         "local": {"en": "Tell me once you've paid", "ru": "Напишите мне после оплаты",
                   "ja": "支払ったら教えてください", "ar": "أخبرني بعد الدفع"}[lang]},
    ]
    return strip_md(data)


# ---------------------------------------------------------------- 地图卡（S15 导航）

MAP_EXTRA = {
    "en": dict(mHowto="I'm going to this McDonald's. Show the big Chinese block to the driver.",
               mHowToGo="how to get there", mQr="scan to open the map", mTaxi="show the driver",
               mSpeak="Read the address aloud", mAddr="Shanda Rd 146-6 (Chengda Gaoke), 1st floor",
               mStore="McDonald's Shanda Road",
               mTencentNote="backup map", mGoogleNote="may be offset inside China",
               mQrCap="Open the map for this restaurant",
               mTaxiLocal="Show this screen to the taxi driver. The Chinese address is above."),
    "ru": dict(mHowto="Мне нужно в этот McDonald's. Покажите большой китайский блок водителю.",
               mHowToGo="как добраться", mQr="сканируйте, чтобы открыть карту", mTaxi="покажите водителю",
               mSpeak="Прочитать адрес", mAddr="Шаньда-роуд 146-6 (Чэнда Гаокэ), 1 этаж",
               mStore="Макдональдс на Шаньда-роуд",
               mTencentNote="резервная карта", mGoogleNote="внутри Китая возможен сдвиг",
               mQrCap="Открыть карту этого ресторана",
               mTaxiLocal="Покажите этот экран водителю такси. Китайский адрес — выше."),
    "ja": dict(mHowto="このマクドナルドに行きます。大きな中国語の部分を運転手に見せてください。",
               mHowToGo="行き方", mQr="スキャンして地図を開く", mTaxi="運転手に見せる",
               mSpeak="住所を読み上げる", mAddr="山大路146-6号（成大高科）1階",
               mStore="マクドナルド山大路店",
               mTencentNote="予備の地図", mGoogleNote="中国国内では位置がずれる場合があります",
               mQrCap="この店の地図を開く",
               mTaxiLocal="この画面をタクシーの運転手に見せてください。中国語の住所は上にあります。"),
    "ar": dict(mHowto="أريد الذهاب إلى هذا المطعم. اعرض المربع الصيني الكبير على السائق.",
               mHowToGo="كيف أصل", mQr="امسح لفتح الخريطة", mTaxi="اعرض على السائق",
               mSpeak="اقرأ العنوان", mAddr="طريق شاندا 146-6 (تشنغدا غاوكِه)، الطابق الأول",
               mStore="ماكدونالدز شارع شاندا",
               mTencentNote="خريطة بديلة", mGoogleNote="قد يكون هناك انحراف داخل الصين",
               mQrCap="افتح خريطة هذا الفرع",
               mTaxiLocal="اعرض هذه الشاشة على سائق التاكسي. العنوان الصيني في الأعلى."),
}
for _k, _v in MAP_EXTRA.items():
    L[_k].update(_v)


def load_store(path, code="3350020"):
    raw = json.load(open(path, encoding="utf-8"))
    data = raw.get("raw_response", raw).get("data", raw)
    arr = data if isinstance(data, list) else data.get("data", [])
    for s in arr:
        if s.get("storeCode") == code:
            return s
    return arr[0]


def build_map(lang, store, sample=False):
    from urllib.parse import quote
    lang = lang if lang in L else "en"
    t = L[lang]
    name = store.get("storeName", "")
    addr = store.get("address", "")
    lat = float(store.get("latitude") or 0)
    lng = float(store.get("longitude") or 0)
    has_coord = abs(lat) > 1e-4 and abs(lng) > 1e-4
    city = "济南" if "济南" in name else ""
    kw = quote((name + " " + city).strip())

    if has_coord:
        amap = "https://uri.amap.com/marker?position=%.6f,%.6f&name=%s" % (lng, lat, quote(name))
    else:
        amap = "https://uri.amap.com/search?keyword=%s&city=%s" % (kw, quote(city))
    tencent = "https://apis.map.qq.com/uri/v1/search?keyword=%s&referer=mcspeak" % kw
    google = "https://www.google.com/maps/search/?api=1&query=%s" % quote((addr + " " + city).strip())

    qr_uri = None
    try:
        import segno
        q = segno.make(amap, error="m")
        u = q.svg_data_uri(scale=1, border=2, dark="#0B0B0B", light="#FFFFFF")
        qr_uri = u if len(u) < 12000 else None
    except Exception:
        qr_uri = None

    data = {
        "kind": "map", "lang": lang, "dir": "rtl" if lang == "ar" else "ltr",
        "generatedAt": datetime.now().strftime("%Y-%m-%d %H:%M"), "isSample": bool(sample),
        "howto": {"zh": "您好，我要去这家麦当劳，麻烦您看一下地址。", "local": t["mHowto"]},
        "store": {"nameZh": name, "addressZh": addr,
                  "local": t["mStore"], "addressLocal": t["mAddr"]},
        "coords": ({"lat": "%.6f" % lat, "lng": "%.6f" % lng,
                    "local": "From the store lookup (mcd-mcp)"} if has_coord else None),
        "links": [
            {"nameZh": "高德地图（推荐）", "nameLocal": "Amap (recommended)", "url": amap,
             "primary": True, "noteZh": "", "noteLocal": ""},
            {"nameZh": "腾讯地图", "nameLocal": "Tencent Maps", "url": tencent, "primary": False,
             "noteZh": "备选", "noteLocal": t["mTencentNote"]},
            {"nameZh": "谷歌地图", "nameLocal": "Google Maps", "url": google, "primary": False,
             "noteZh": "国内可能有偏移，仅作参考", "noteLocal": t["mGoogleNote"]},
        ],
        "qr": ({"dataUri": qr_uri, "capZh": "扫码打开高德地图", "capLocal": t["mQrCap"]} if qr_uri else None),
        "taxi": {"hello": PHRASES.get("taxi_hello", "师傅您好，麻烦送我到这里，谢谢！"),
                 "addressZh": addr, "nameZh": name, "local": t["mTaxiLocal"]},
        "sec": {"howToGo": t["mHowToGo"], "qr": t["mQr"], "taxi": t["mTaxi"]},
        "ui": {"speak": t["mSpeak"], "stale": t["stale"], "sampleNote": t["sampleNote"],
               "back": t["back"], "noSpeech": "—"},
        "zhui": {"back": "返回"},
    }
    return strip_md(data)


def render(kind, lang, out, sample_path=DEFAULT_SAMPLE, pickup_code=None, sample=False,
           store_code="3350020", store_sample=None):
    if kind == "map":
        sp = store_sample or os.path.join(REF, "samples", "02-query-nearby-stores-nearby.json")
        data = build_map(lang, load_store(sp, store_code), sample)
        tpl = os.path.join(TPL, "map_card.html")
    else:
        tpl = os.path.join(TPL, "counter_card.html" if kind == "counter" else
                           ("payment_notice.html" if kind == "payment" else "pickup_card.html"))
        order = load_order(sample_path, pickup_code)
        if kind == "payment":
            order["pickupCode"] = ""
        data = build(kind, lang, order, sample)
    html = open(tpl, encoding="utf-8").read().replace("/*__DATA__*/", json.dumps(data, ensure_ascii=False, indent=1))
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    open(out, "w", encoding="utf-8").write(html)
    return out


def try_png(html_path):
    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        return None
    png = os.path.splitext(html_path)[0] + ".png"
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 900, "height": 1400}, device_scale_factor=2)
        pg.goto("file://" + os.path.abspath(html_path))
        pg.wait_for_timeout(500)
        pg.screenshot(path=png, full_page=True)
        b.close()
    return png


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--type", default="counter", choices=["counter", "pickup", "payment", "map"])
    ap.add_argument("--lang", default="en")
    ap.add_argument("--out", required=True)
    ap.add_argument("--sample", dest="sample_path", default=DEFAULT_SAMPLE)
    ap.add_argument("--pickup-code", default="")
    ap.add_argument("--store-code", default="3350020")
    ap.add_argument("--store-sample", default=None)
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--png", action="store_true")
    a = ap.parse_args()
    print("HTML ->", render(a.type, a.lang, a.out, a.sample_path, a.pickup_code, a.demo,
                            a.store_code, a.store_sample))
    if a.png:
        print("PNG  ->", try_png(a.out) or "skipped (playwright not installed)")


if __name__ == "__main__":
    main()
