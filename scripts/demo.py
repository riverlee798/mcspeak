#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
demo.py —— mcspeak 离线演示（不联网）。

用 references/samples/ 里的**真实接口返回**跑一遍完整流程：
  打招呼 → 领券 → 选门店 → 拉菜单 → 推荐 → 改单（去生菜 / 去冰）
  → 算券 → 下单 → 待付款卡 → 付款后取餐卡 → 柜台卡 → 地图卡 → 追加麦旋风

所有输出都带「演示数据」标记。只有用户明确说 demo mode 时才应使用本脚本。

用法：
  python scripts/demo.py                 # 阿拉伯语（默认场景）
  python scripts/demo.py --lang ru       # 卡片用俄语，旁白仍是演示场景
  python scripts/demo.py --out demo_out  # 改输出目录
"""

import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import render_card as rc  # noqa: E402

S = os.path.join(ROOT, "references", "samples")
DEMO_TAG = "[演示数据 DEMO]"

# ---------------------------------------------------------------- 旁白（多语）

SAY = {
    "ar": dict(hello="أهلًا! سأساعدك في الطلب. ماذا تحب اليوم؟",
               coupons="وجدت لك ٣ قسائم، لكنها تبدأ في ٢٦ أكتوبر — اليوم بالسعر الأصلي.",
               store="أقرب فرع: ماكدونالدز شارع شاندا (تشنغدا غاوكه)، ٥١٣ مترًا من هنا.",
               rec="أنصحك بوجبة برغر الدجاج الحار: دجاج مقرمش بحرارة واضحة، مع بطاطس وكولا.",
               mod="تم — بدون خس، وكولا بدون ثلج. كتبتها في الطلب.",
               price="الإجمالي ٣٣٫٥٠ ¥، بدون خصم اليوم لأن القسيمة لم تبدأ بعد.",
               pending="الطلب جاهز. ادفع قبل ١٩:١٣ — من تطبيق ماكدونالدز، الزر الأصفر أسفل اليمين.",
               paid="تم الدفع! هذا رقم الاستلام.",
               counter="هذه بطاقة الكاشير — اعرضها على الموظف.",
               map="هذه بطاقة الموقع — اعرض العنوان الصيني على السائق.",
               flurry="أضفت ماكفلوري أوريو (١٥٫٥٠ ¥) كطلب منفصل.",
               bye="بالهناء والشفاء!"),
    "ru": dict(hello="Здравствуйте! Помогу с заказом. Что хотите сегодня?",
               coupons="Нашёл 3 купона, но они действуют с 26 октября — сегодня по обычной цене.",
               store="Ближайший ресторан: Макдональдс на Шаньда-роуд (Чэнда Гаокэ), 513 м.",
               rec="Советую набор с острым куриным бургером: хрустящая курица, картофель и кола.",
               mod="Готово — без салата, кола без льда. Записал в заказ.",
               price="Итого 33,50 ¥, без скидки: купон ещё не начал действовать.",
               pending="Заказ готов. Оплатите до 19:13 — в приложении McDonald's, жёлтая кнопка справа внизу.",
               paid="Оплачено! Вот номер получения.",
               counter="Это карточка для кассы — покажите сотруднику.",
               map="Это карточка с адресом — покажите водителю китайский адрес.",
               flurry="Добавил McFlurry с Oreo (15,50 ¥) отдельным заказом.",
               bye="Приятного аппетита!"),
    "ja": dict(hello="こんにちは！ご注文をお手伝いします。今日は何になさいますか？",
               coupons="クーポンが3枚ありますが、10月26日からの有効なので今日は通常価格です。",
               store="最寄り店舗：マクドナルド山大路（成大高科）店、513mです。",
               rec="マックスパイシーチキンバーガーセットがおすすめです。ポテトとコーラ付き。",
               mod="はい、レタス抜き、コーラは氷なしで注文に入れました。",
               price="合計33.50¥です。クーポンはまだ使えないので割引なしです。",
               pending="注文できました。19:13までに、マクドナルドアプリ右下の黄色いボタンでお支払いください。",
               paid="お支払いを確認しました。これが受け取り番号です。",
               counter="カウンター用カードです。店員に見せてください。",
               map="住所カードです。中国語の住所を運転手に見せてください。",
               flurry="オレオマックフルーリー（15.50¥）を別注文で追加しました。",
               bye="ごゆっくりお召し上がりください。"),
    "en": dict(hello="Hi! I'll help you order. What would you like today?",
               coupons="You have 3 coupons, but they start on 26 Oct — today is full price.",
               store="Nearest store: McDonald's Shanda Road (Chengda Gaoke), 513 m away.",
               rec="Try the McSpicy Chicken Burger Meal — crispy chicken, fries and a Coke.",
               mod="Done — no lettuce, Coke with no ice. Both written into the order.",
               price="Total ¥33.50, no discount today because the coupon hasn't started.",
               pending="Order placed. Pay before 19:13 — in the McDonald's app, yellow button bottom right.",
               paid="Paid! Here is your pickup code.",
               counter="This is the counter card — show it to the staff.",
               map="This is the address card — show the Chinese address to the driver.",
               flurry="Added an Oreo McFlurry (¥15.50) as a separate order.",
               bye="Enjoy your meal!"),
}


def load(name):
    return json.load(open(os.path.join(S, name), encoding="utf-8"))


def data_of(name):
    """样本有的是 {_meta, raw_response}，有的是纯原始返回，统一取 data。"""
    o = load(name)
    o = o.get("raw_response", o)
    return o.get("data", o)


def head(step, title_zh):
    print("\n" + "─" * 68)
    print("▌ %s · %s" % (step, title_zh))
    print("─" * 68)


def say(lang, key, cn):
    print("🤖 mcspeak: %s" % SAY[lang][key])
    print("   ↳ 中文对照：%s" % cn)
    print("   %s" % DEMO_TAG)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", default="ar", choices=list(SAY.keys()))
    ap.add_argument("--out", default=os.path.join("examples", "demo"))
    a = ap.parse_args()
    lang = a.lang
    outdir = os.path.join(ROOT, a.out, lang)
    tmpdir = os.path.join(ROOT, a.out, "_tmp")
    os.makedirs(outdir, exist_ok=True)
    os.makedirs(tmpdir, exist_ok=True)

    now = datetime.now()
    try:
        t = data_of("01-now-time-info.json")
        now = datetime.strptime(t["datetime"][:19], "%Y-%m-%dT%H:%M:%S")
    except Exception:
        pass

    print("=" * 68)
    print(" mcspeak · 麦麦替你说 —— 离线演示 DEMO（不联网、不发请求）")
    print(" 场景语言：%s ｜ 时间基准：%s" % (lang, now.strftime("%Y-%m-%d %H:%M")))
    print(" 数据来源：references/samples/ 的真实接口返回（已脱敏）")
    print("=" * 68)

    # ---------- S1 语言 ----------
    head("S1", "识别语言")
    print("👤 用户（العربية）：أريد أن آكل برغر")
    say(lang, "hello", "识别到阿拉伯语，用阿拉伯语接待。")

    # ---------- S2 领券 ----------
    head("S2", "静默领券")
    try:
        cps = data_of("11-auto-bind-coupons.json")["coupons"]
        n = len(cps)
    except Exception:
        n = 3
    say(lang, "coupons", "领到 %d 张券；实测这些券 10-26 才生效，今天按原价。" % n)

    # ---------- S3 门店 ----------
    head("S3", "选门店")
    store = rc.load_store(os.path.join(S, "02-query-nearby-stores-nearby.json"))
    print("👤 用户：附近的麦当劳在哪？")
    say(lang, "store", "%s（%s），距离 513 m。" % (store["storeName"], store["address"]))
    print("   📍 店名与地址均为接口原文，未做任何简写：")
    print("      %s" % store["storeName"])
    print("      %s" % store["address"])

    # ---------- S5 菜单 ----------
    head("S5", "拉菜单 + 过滤")
    menu = data_of("04-query-meals-store3350020.json")
    meals = menu["meals"]
    print("   实时菜单：%d 个分类 / %d 个唯一商品（缓存本次对话）" %
          (len(menu["categories"]), len(meals)))
    print("   饮食过滤：无猪肉、微辣 → 候选 %s" % "板烧鸡腿堡三件套 / 麦辣鸡腿汉堡三件套")

    # ---------- S6 推荐 ----------
    head("S6", "推荐（按格子）")
    setmeal = meals["9900005456"]
    print("   [1] %s ×1  ¥%s" % (setmeal["name"], setmeal["currentPrice"]))
    print("   [2] 中薯条 ×1")
    print("   [3] 可乐中杯 ×1")
    say(lang, "rec", "麦辣鸡腿汉堡三件套 ¥33.50，客单价最低的一档。")

    # ---------- S7 改单 ----------
    head("S7", "改单（开关组 + 单选组）")
    print("👤 用户：بدون خس، وكولا بدون ثلج")
    det = data_of("05-query-meal-detail-9900005456-chicken-set.json")
    keys = {}
    for r in det["rounds"]:
        for c in r["choices"]:
            for g in (c.get("modification") or {}).get("items", []):
                for v in g["values"]:
                    keys[v["name"]] = v.get("selectedKey")
    print("   实时 detail 读出：切块生菜 unselectedKey=%s（去掉），冰量 去冰 selectedKey=%s" %
          ("0-0", keys.get("去冰", "0-0")))
    print("   写入 items[0].roundList：120512 key=0-0 / 200002 key=0-0")
    say(lang, "mod", "不要切块生菜 + 可乐去冰，已写进下单参数。")

    # ---------- S8 算券 ----------
    head("S8", "算券")
    try:
        sc = data_of("12-query-store-coupons-empty.json")
    except Exception:
        sc = []
    print("   本店可用券：%d 张 → %s" % (len(sc), "空数组（当前不可用）" if not sc else "…"))
    calc = data_of("16b-calculate-price-confirmed-cart.json")
    say(lang, "price", "calculate-price 返回 price=%d 分 = ¥%.2f，discount=%d。" %
        (calc["price"], calc["price"] / 100, calc["discount"]))

    # ---------- S10 下单 + 待付款 ----------
    head("S10", "下单 → 待付款卡")
    order = data_of("17-create-order.json")
    od = order["orderDetail"]
    mine = datetime.strptime(od["expirePayTime"], "%Y-%m-%d %H:%M:%S")
    print("   create-order 成功：payH5Url 已保存、expirePayTime=%s（约 %d 分钟）" %
          (od["expirePayTime"], int((mine - datetime.strptime(od["createTime"], "%Y-%m-%d %H:%M:%S")).total_seconds() // 60)))
    print("   pickupCode 此刻为空字符串 → 只出「待付款卡」，不出取餐卡")
    pay_html = os.path.join(outdir, "1-payment_notice.html")
    rc.render("payment", lang, pay_html, os.path.join(S, "17-create-order.json"),
              sample=True)
    say(lang, "pending", "首选 App 付款：我的订单 → 右下角黄色「去支付」；链接作备用。")
    print("   📄 已生成：%s" % os.path.relpath(pay_html, ROOT))

    # ---------- S11 付款后 → 取餐卡 ----------
    head("S11", "付款后 → 取餐卡")
    done = data_of("20-query-order-completed.json")
    print("   query-order：orderStatus=%s，pickupCode=%s（样本已脱敏）" %
          (done["orderStatus"], done["pickupCode"]))
    pick_html = os.path.join(outdir, "2-pickup_card.html")
    rc.render("pickup", lang, pick_html, os.path.join(S, "17-create-order.json"),
              pickup_code=done["pickupCode"] or "00000", sample=True)
    say(lang, "paid", "取餐码用大字显示；状态表里「待取餐」高亮。")
    for st, zh_note in [("确认中", "钱已付，等几秒；别重复下单"),
                        ("配餐中", "后厨在做，在取餐台附近等"),
                        ("待取餐", "现在去取餐台 ★"),
                        ("订单已准备完毕", "拿餐并当场核对")]:
        print("   App 状态：%-8s → %s" % (st, zh_note))
    print("   📄 已生成：%s" % os.path.relpath(pick_html, ROOT))

    # ---------- S12 柜台卡 ----------
    head("S12", "柜台卡")
    counter_html = os.path.join(outdir, "3-counter_card.html")
    rc.render("counter", lang, counter_html, os.path.join(S, "17-create-order.json"), sample=True)
    say(lang, "counter", "一格一事、双语同格；店员指哪格，顾客就看哪格。")
    print("   📄 已生成：%s" % os.path.relpath(counter_html, ROOT))

    # ---------- S15 地图卡 ----------
    head("S15", "地图 / 打车卡")
    map_html = os.path.join(outdir, "4-map_card.html")
    rc.render("map", lang, map_html, store_sample=os.path.join(S, "02-query-nearby-stores-nearby.json"),
              store_code=store["storeCode"], sample=True)
    print("   坐标：接口返回 latitude=%.1f / longitude=%.1f → 不编坐标，改用店名搜索链接" %
          (store.get("latitude", 0), store.get("longitude", 0)))
    say(lang, "map", "高德首选、腾讯备选、谷歌注明偏移；地址照抄接口原文。")
    print("   📄 已生成：%s" % os.path.relpath(map_html, ROOT))

    # ---------- 追加麦旋风（用 samples/09 的商品数据复原一单） ----------
    head("S7+", "追加一份经典麦旋风")
    flurry = data_of("09-query-meal-detail-9900008754-dessert.json")
    price = meals.get("9900008754", {}).get("currentPrice", "15.5")
    print("   商品详情：%s，可选口味 %s" %
          (flurry["name"], " / ".join(c["name"] for r in flurry["rounds"] for c in r["choices"])))
    print("   注：仓库里没有这单的原始 create-order 返回，此单由真实商品数据复原")
    tmp_order = os.path.join(tmpdir, "order-mcflurry.json")
    exp = (now + timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S")
    json.dump({"raw_response": {"success": True, "code": 200, "data": {"orderDetail": {
        "orderId": "1030000000000000000000000001", "orderStatus": "待支付", "status": "10",
        "storeName": store["storeName"], "storeAddress": store["address"],
        "orderProductList": [{"productName": flurry["name"], "quantity": 1, "price": price,
                              "comboItemList": [{"itemName": "奥利奥麦旋风", "itemQuantity": 1}]}],
        "totalAmount": price, "realTotalAmount": price, "totalDiscountAmount": "0",
        "couponList": [], "createTime": now.strftime("%Y-%m-%d %H:%M:%S"),
        "expirePayTime": exp, "takeWay": "外带", "pickupCode": "",
        "payId": "1110000000000000000001", "remark": ""}}}},
        open(tmp_order, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    flurry_html = os.path.join(outdir, "5-counter_card-mcflurry.html")
    rc.render("counter", lang, flurry_html, tmp_order, sample=True)
    say(lang, "flurry", "经典麦旋风 ¥%s，单独一单，卡上只列这一格。" % price)
    print("   📄 已生成：%s" % os.path.relpath(flurry_html, ROOT))

    # ---------- 收尾 ----------
    head("S14", "结束")
    say(lang, "bye", "祝用餐愉快；询问是否记住偏好（同意才写入 data/profile.json）。")

    files = sorted(f for f in os.listdir(outdir) if f.endswith(".html"))
    print("\n" + "=" * 68)
    print(" 演示完成，共生成 %d 张卡片（全部离线，无网络请求）：" % len(files))
    for f in files:
        p = os.path.join(outdir, f)
        print("   • %-34s %6d B" % (os.path.relpath(p, ROOT), os.path.getsize(p)))
    print(" 打开方式：把 %s 目录起静态服务即可在手机上看。" % os.path.relpath(outdir, ROOT))
    print(" 提醒：所有卡片底部都带 SAMPLE 标记，内容为演示数据。")
    print("=" * 68)
    shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == "__main__":
    main()
