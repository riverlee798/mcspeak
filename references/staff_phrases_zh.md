# staff_phrases_zh.md — 给店员看的中文模板

> 用法：全部是**给店员看的中文**，第一人称、温暖礼貌、不带命令口气。
> 每句配一个 `key`，Skill 里按 key 取句，**不要现场翻译**（避免翻车）。
> 卡片上中文用大字（≥20pt），英文小字辅助；阿拉伯语等从右往左的语言另起一列右对齐。

## 使用原则

1. 一次只显示 **2–4 句**，多了店员会不想看。
2. 每句前面加一个 emoji 或符号做视觉锚点（🍔 💳 🥤），方便手指着说。
3. 结尾常用「不行也没关系～」「麻烦您了」，软化请求。
4. 不要用「请给我」「必须」「快点」这类生硬祈使句。
5. 涉及金额时写「参考价格」，最终以收银为准。

---

## A. 开场与点餐

| key | 中文（给店员看） | 英文对照 |
|---|---|---|
| `staff.hello` | 您好！我不太会中文，麻烦您帮我点一下餐，谢谢您～ | Hello! My Chinese isn't good — could you help me order? Thank you! |
| `staff.no_kiosk` | 我不太会用自助点餐机，也不太会扫码点餐，能麻烦您直接在柜台帮我点吗？ | I can't use the self-service kiosk or scan-to-order. Could you take my order here at the counter? |
| `staff.list_intro` | 我想点这些，麻烦您看一下： | I'd like these, please: |
| `staff.list_follow` | 如果方便的话，可以帮我确认一下还有没有这几样吗？不行也没关系～ | If it's easy, could you check whether these are available? No worries if not. |
| `staff.soft_request` | 如果方便的话……不行也没关系～ | If it's convenient… no worries at all if not. |
| `staff.point_menu` | 麻烦您帮我指一下菜单上这个，谢谢～ | Could you point to this on the menu for me? Thank you. |

## B. 饮食限制

| key | 中文（给店员看） | 英文对照 |
|---|---|---|
| `staff.no_pork` | 我不吃猪肉，请问这个里面有猪肉、培根或者火腿吗？ | I don't eat pork. Does this contain pork, bacon or ham? |
| `staff.no_beef` | 我不吃牛肉，请问这个里面有牛肉吗？ | I don't eat beef. Does this contain beef? |
| `staff.vegetarian` | 我吃素，请问这个里面有肉吗？ | I'm vegetarian. Does this contain any meat? |
| `staff.allergy` | 我对 **{过敏原}** 过敏，请问这个里面有 **{过敏原}** 吗？ | I'm allergic to **{allergen}**. Does this contain **{allergen}**? |
| `staff.allergy_serious` | 我过敏比较严重，麻烦您帮我确认一下，谢谢您！ | My allergy is serious — could you double-check for me? Thank you! |
| `staff.no_spicy` | 我不能吃辣，这个辣吗？可以做不辣的吗？ | I can't eat spicy food. Is this spicy? Can it be made not spicy? |
| `staff.shared_fryer` | 请问薯条和炸鸡是用同一个油锅吗？ | Are the fries fried in the same oil as the chicken? |

## C. 堂食 / 外带

| key | 中文（给店员看） | 英文对照 |
|---|---|---|
| `staff.dine_in` | 我在这里吃，**堂食**，谢谢～ | I'll eat here — **dine in**, please. |
| `staff.takeaway` | 我**带走**，谢谢～ | **Takeaway**, please. |
| `staff.no_bag` | 不用袋子，谢谢～ | No bag needed, thank you. |

## D. 付款

| key | 中文（给店员看） | 英文对照 |
|---|---|---|
| `staff.wechat` | 我用微信付款，麻烦您扫我，谢谢～ | I'll pay by WeChat — please scan my code. |
| `staff.alipay` | 我用支付宝付款，麻烦您扫我，谢谢～ | I'll pay by Alipay — please scan my code. |
| `staff.cash` | 我可以付现金吗？ | Can I pay in cash? |
| `staff.card` | 可以刷境外银行卡吗？ | Can I pay with a foreign bank card? |
| `staff.price_note` | 参考价格是 **¥{金额}**，最终以收银为准，谢谢～ | Reference price is **¥{amount}**; the till is final. Thank you. |
| `staff.receipt` | 麻烦给我一张小票，谢谢～ | Could I have a receipt, please? |

## E. 取餐与核对

| key | 中文（给店员看） | 英文对照 |
|---|---|---|
| `staff.pickup_code` | 这是我的取餐码：**{取餐码}**，麻烦您帮我取一下，谢谢～ | Here's my pickup code: **{code}**. Could you get my order? Thank you. |
| `staff.wait_number` | 请问是在这里等叫号吗？ | Should I wait here for my number to be called? |
| `staff.missing_item` | 不好意思，我的餐好像少了一样，麻烦您帮我看看，谢谢～ | Sorry, I think one item is missing — could you check? Thank you. |
| `staff.not_mine` | 不好意思，这个好像不是我点的，麻烦您帮我确认一下，谢谢～ | Sorry, I don't think this is mine — could you check? Thank you. |
| `staff.cold_food` | 这个好像凉了，可以帮我换一份吗？不行也没关系～ | This seems cold — could it be replaced? No worries if not. |
| `staff.wrong_drink` | 我点的是 **{饮料}**，拿到的是别的，麻烦您帮我换一下～ | I ordered **{drink}** but got something else — could you swap it? |

## F. 附加物品

| key | 中文（给店员看） | 英文对照 |
|---|---|---|
| `staff.tissue` | 麻烦给我几张纸巾，谢谢～ | Could I have some napkins? |
| `staff.straw` | 麻烦给我一根吸管，谢谢～ | Could I have a straw? |
| `staff.ketchup` | 麻烦给我两包番茄酱，谢谢～ | Could I have two ketchup packets? |
| `staff.water` | 麻烦给我一杯温水，谢谢～ | Could I have a cup of warm water? |
| `staff.spoon` | 麻烦给我一把勺子，谢谢～ | Could I have a spoon? |
| `staff.highchair` | 请问有儿童座椅吗？ | Do you have a high chair? |
| `staff.toilet` | 请问洗手间在哪里？ | Where is the restroom? |
| `staff.wifi` | 请问 Wi-Fi 密码是多少？ | What's the Wi-Fi password? |

## G. 沟通兜底（最重要）

| key | 中文（给店员看） | 英文对照 |
|---|---|---|
| `staff.type_instead` | 我听不懂中文，麻烦您把想说的话打在我手机上，谢谢您～ | I don't understand Chinese — could you type what you want to say on my phone? Thank you. |
| `staff.slow_down` | 麻烦您说慢一点，谢谢～ | Could you speak a little slower, please? |
| `staff.photo_menu` | 我可以拍一下菜单吗？ | May I take a photo of the menu? |
| `staff.thanks` | 太感谢您了，麻烦您了！ | Thank you so much for your help! |
| `staff.bye` | 谢谢，祝您一天愉快～ | Thank you — have a nice day! |

## H. 打车 / 给司机看

| key | 中文（给店员看） | 英文对照 |
|---|---|---|
| `staff.taxi_hello` | 师傅您好，麻烦送我到这里，谢谢！ | Hello driver — please take me to this address, thank you! |
| `staff.taxi_show` | 就是下面这个地址，麻烦您看一下，谢谢～ | Here is the address — please take a look. Thank you! |
| `staff.ask_metro` | 请问最近的地铁站怎么走？ | Excuse me, how do I get to the nearest metro station? |
| `staff.ask_bus` | 请问最近的公交站在哪里？ | Excuse me, where is the nearest bus stop? |

> **地址必须照抄门店查询返回的原文**（含号数后缀、括号、楼层），一个字都不能省、不能简写。
>
> **地铁 / 公交只给「问句」，不给站名**：mcd-mcp 没有任何交通数据，编一个站名比不说更糟。
> 站名让地图 App 现查（高德搜「地铁站」/「公交站」），或者拿上面这两句问店员。

---

# 店员常问的问题 → 可选回答

> 这是 mcspeak 的"预判"能力：店员大概率会说这几句中文，把**他可能说的话**和**我方可选的中文回答**都准备好，访客手指一下就行。

| # | 店员可能说（中文原文） | 含义 | 我方回答（给店员看） |
|---|---|---|---|
| 1 | 「请去自助机点餐」/「扫码点餐」 | 让访客去自助机或扫码 | 「我不太会用自助机，麻烦您帮我在柜台点好吗？谢谢～」 |
| 2 | 「堂食还是外带？」 | 在这里吃还是带走 | 「堂食，谢谢～」／「外带，谢谢～」 |
| 3 | 「要加大的吗？」/「加 3 元可以升级大杯」 | 促销升级 | 「不用了，谢谢～」／「好的，麻烦升级大杯，谢谢～」 |
| 4 | 「要不要加一份小食？」/「加 5 元换购」 | 追加销售 | 「不用了，谢谢～」／「好的，加一份，谢谢～」 |
| 5 | 「是会员吗？」/「有优惠券吗？」 | 问会员/券 | 「不是会员，谢谢～」／「我用这个券，麻烦您看一下～」 |
| 6 | 「怎么付款？」/「微信还是支付宝？」 | 支付方式 | 「微信，谢谢～」／「支付宝，谢谢～」／「现金可以吗？」 |
| 7 | 「还要别的吗？」 | 是否加购 | 「就这些，谢谢～」／「再加一个 **{商品}**，谢谢～」 |
| 8 | 「请稍等一下」/「马上就好」 | 等待 | 「好的，谢谢～」 |
| 9 | 「请到旁边等叫号」/「{号码}号请取餐」 | 叫号取餐 | 「好的，谢谢～」（把取餐码指给他看） |
| 10 | 「这个卖完了」/「这个没有了」 | 售罄 | 「那麻烦换一个 **{替代品}**，可以吗？」 |
| 11 | 「这个要等 10 分钟」 | 出餐慢 | 「没问题，我等一下，谢谢～」／「那换一个快一点的，谢谢～」 |
| 12 | 「一共 {金额} 元」 | 报价 | 「好的，这是 **¥{金额}** 对吗？」 |
| 13 | 「需要袋子吗？」 | 是否要打包袋 | 「要一个，谢谢～」／「不用，谢谢～」 |
| 14 | 「餐具需要吗？」 | 餐具 | 「不用餐具，谢谢～」／「麻烦给一下餐具，谢谢～」 |
| 15 | 「不好意思，听不懂」 | 沟通失败 | 「没关系，我打字给您看～」（切换成 `staff.type_instead`） |

---

## 卡片排版建议

```
┌────────────────────────────────────┐
│  🙏 我不太会中文，麻烦您帮我点餐     │   ← staff.hello（最大字号）
│                                    │
│  🍔 麦辣鸡腿汉堡（不要生菜）      x1 │   ← 商品中文名 + 定制
│  🍟 中薯条                        x1 │
│  🥤 可乐中杯（去冰）              x1 │
│                                    │
│  🍽 堂食（在这里吃）                │   ← staff.dine_in（加粗）
│  💳 微信支付                        │
│                                    │
│  参考价格 ¥33.50（以收银为准）      │   ← staff.price_note
└────────────────────────────────────┘
```

**取餐卡**额外一行大字：`取餐码 1234` + `staff.pickup_code`。
**过敏用户**：把 `staff.allergy` 放在**最顶部红框**，优先于一切。
