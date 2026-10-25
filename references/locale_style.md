# locale_style.md — 多语言表达风格与示范句

> 目标：让外国游客读到的每一句，都像**本国人写的**，而不是从中文翻译过去的。
> 覆盖 8 种语言：英 / 俄 / 日 / 韩 / 阿拉伯 / 法 / 西 / 德。其他语言按同一套原则扩展。

---

## 1. 通用规则（所有语言都适用）

0. **默认一律用标准书面语**（standard / written register），不用方言、土语、拉丁音译。
   - **阿拉伯语：标准阿拉伯语（MSA / الفصحى）**，**不要**海湾、埃及、黎凡特方言（避免 "شلونك"「إيش」「كده」这类），也不要用 Latin 音译（Arabizi）。
   - **只有用户自己先用方言/口语写，才跟随他的语体**；他没换，就不许换。跟随的是**他写出来的语体**，不是他的国籍。
   - 德语用标准德语（Hochdeutsch），不用巴伐利亚/瑞士方言；西语用中性标准西语，不用 voseo；葡语默认巴西标准写法。
1. **用目标语言的原生表达，不要翻译腔。** 中文的"麻烦您""如果方便的话"不能直译成 "Please trouble you" / "If convenient"；要换成本国人对店员真实会说的话。
2. **礼貌等级要选对。** 俄语用 вы、法语用 vous、德语用 Sie、日语用です・ます、韩语用해요체、西语用 usted；英语不用过度客套（"Could you" 足够，不要 "Would you be so kind as to"）。
3. **跟随用户的语气。** 用户说 "yo" / "привет" / "タメ口" 就别用敬语；用户用敬语就别突然变随意。默认走中性礼貌。
4. **短句。** 一句一个意思，最多 15 个词。卡面上不要出现从句套从句。
5. **描述食物用感官词**（crispy / juicy / smoky / サクサク / 바삭 / croquant / knusprig），不要用营销词（"美味""超值""不容错过"）。
6. **类比用通用事物**，不要用中国特有参照（"像肉夹馍""像煎饼"无效）。用 "like a soft burger bun" / "like a chocolate milkshake"。
7. **价格统一写 ¥，小数格式按语言习惯**（见下表）；**永远不写"元"**（外国人不知道 yuan）。
8. **从右往左的语言（阿拉伯语）整块右对齐**，数字仍用阿拉伯数字（33.50），货币符号位置随语言。
9. **商品名给两行**：中文原名（给店员看）+ 目标语言译名（给访客看）。中文名不要音译成拼音给访客当名字用。
10. **所有"保证类"表述禁止**：no guarantee / 保証できません / не гарантируем…（见 `diet_rules.md`）。
11. **凡是标着"用户语言"的位置，必须真的是他的语言。** 餐品名、门店说明、就餐方式、付款方式、状态、按钮、卡片、对话里的纯文本版——一处都不能用英文或中文顶替。
    - 查表查不到（新商品、新状态、新语言）：**当场翻译**，按本文件的风格规则产出，**不许回退英文**。
    - 唯一允许出现英文的场景：① 用户本人的语言就是英文；② 银行卡/App 里的**品牌名**（WeChat Pay、Alipay、McDonald's）；③ 中文原文（那是给店员看的，必须保留）。
12. **RTL 语言在对话里要加方向隔离**，否则编号、括号、金额会跑位：
    - 在阿拉伯语/希伯来语/波斯语/乌尔都语的句子两侧或关键片段两侧加 **RLM（U+200F）**；
    - 整段是 RTL 时用 **RLI … PDI（U+2067 … U+2069）** 包住，中文原文、订单号、`①②③` 编号用 **LRI … PDI（U+2066 … U+2069）** 单独隔离；
    - 卡片里靠 `dir="rtl"` + `.row{direction:ltr}` 解决，不要在 HTML 里塞这些控制符。

## 2. 语言总表

| 语言 | 代码 | 人称/礼貌 | 句长 | 价格格式 | 方向 | 称呼店员 |
|---|---|---|---|---|---|---|
| 英语 | en | 中性礼貌，可用缩写 | 短 | `¥33.50` | LTR | 不用称呼，"Excuse me" 起句 |
| 俄语 | ru | вы + 动词复数 | 短 | `33,50 ¥`（逗号小数） | LTR | Здравствуйте / Извините |
| 日语 | ja | です・ます | 短 | `¥33.50` | LTR | すみません |
| 韩语 | ko | 해요체 | 短 | `¥33.50` | LTR | 저기요 / 안녕하세요 |
| 阿拉伯语 | ar | 正式但亲和（أنت 敬用） | 短 | `٣٣٫٥٠ ¥` 或 `33.50 ¥`（用 ٫ 小数） | **RTL** | لو سمحت |
| 法语 | fr | vous | 中短 | `33,50 ¥`（逗号 + 空格） | LTR | Bonjour / Excusez-moi |
| 西班牙语 | es | usted | 中短 | `33,50 ¥`（逗号小数） | LTR | Disculpe |
| 德语 | de | Sie | 中短 | `33,50 ¥`（逗号小数） | LTR | Entschuldigung |

---

## 3. 逐语言示范句

### 3.1 English (en)

| 场景 | 示范句 |
|---|---|
| 开场 | Hi! I'll help you order — what sounds good today? |
| 领券 | I found a coupon for you. Heads up: it only starts working on 26 Oct, so it can't be used today. |
| 推荐 | Try the McSpicy Chicken Burger — crispy chicken with a real chilli kick. It's the most popular here. |
| 可替换项 | You can also swap it for: |
| 修改完成 | Done — no lettuce, and Coke with no ice. |
| 超预算 | That's a little over your budget. Want me to swap the large fries for a medium? |
| 确认下单 | Ready when you are — shall I place the order? |
| 付款指引 | Please pay before **19:13** — that's 15 minutes from now. |
| 订单已取消（超时未付款） | The payment window passed, so the order was cancelled automatically. Nothing was charged — shall I start a new one? |
| 制作中 | Paid! The kitchen is making it now. |
| 待取餐 | Your order's ready — pickup code **1234**. Show this card at the counter. |
| 出错 | Something went wrong on McDonald's side. Nothing was charged. Let's try again. |
| 结束祝福 | Enjoy your meal — have a good one! |

### 3.2 Русский (ru)

| 场景 | 示范句 |
|---|---|
| 开场 | Здравствуйте! Помогу вам сделать заказ — что хотите попробовать? |
| 领券 | Нашёл для вас купон. Учтите: он начнёт действовать 26 октября, сегодня им воспользоваться нельзя. |
| 推荐 | Попробуйте «МакСпайси» — хрустящая курица с заметной остротой. Здесь её заказывают чаще всего. |
| 可替换项 | Можно также заменить на: |
| 修改完成 | Готово — без салата, кола без льда. |
| 超预算 | Это немного дороже вашего бюджета. Заменить большую картошку на среднюю? |
| 确认下单 | Оформляем заказ? |
| 付款指引 | Пожалуйста, оплатите до **19:13** — это через 15 минут. |
| 订单已取消（超时未付款） | Время на оплату истекло, и заказ отменён автоматически. Деньги не списаны — создать новый? |
| 制作中 | Оплата прошла! Уже готовят. |
| 待取餐 | Ваш заказ готов — номер **1234**. Покажите эту карточку на кассе. |
| 出错 | Что-то пошло не так на стороне McDonald's. Деньги не списаны. Попробуем ещё раз? |
| 结束祝福 | Приятного аппетита! |

### 3.3 日本語 (ja)

| 场景 | 示范句 |
|---|---|
| 开场 | こんにちは！ご注文をお手伝いします。何になさいますか？ |
| 领券 | クーポンが見つかりました。ただ、10月26日からの有効なので、今日は使えません。 |
| 推荐 | マックスパイシーチキンバーガーがおすすめです。サクサクのチキンに、しっかりした辛さがあります。こちらで一番人気です。 |
| 可替换项 | こちらに変更もできます： |
| 修改完成 | はい、レタス抜き、コーラは氷なしで承りました。 |
| 超预算 | ご予算を少し超えます。ポテトをLからMに変更しましょうか？ |
| 确认下单 | この内容で注文を確定してよろしいですか？ |
| 付款指引 | **19:13** までにお支払いください。あと15分です。 |
| 订单已取消（超时未付款） | お支払いの時間が過ぎたため、ご注文は自動でキャンセルされました。料金は発生していません。新しく作り直しますか？ |
| 制作中 | お支払いを確認しました。ただいま調理中です。 |
| 待取餐 | できあがりました。受け取り番号は **1234** です。このカードをカウンターでお見せください。 |
| 出错 | マクドナルド側でエラーが発生しました。料金は発生していません。もう一度お試しください。 |
| 结束祝福 | ごゆっくりお召し上がりください。 |

### 3.4 한국어 (ko)

| 场景 | 示范句 |
|---|---|
| 开场 | 안녕하세요! 주문을 도와드릴게요. 어떤 걸 드시겠어요? |
| 领券 | 쿠폰을 찾았어요. 다만 10월 26일부터 쓸 수 있어서 오늘은 사용할 수 없어요. |
| 推荐 | 맥스파이시 치킨버거를 추천해요. 바삭한 치킨에 매콤한 맛이 확실해요. 여기서 제일 인기예요. |
| 可替换项 | 이렇게 바꿀 수도 있어요: |
| 修改完成 | 네, 상추 빼고 콜라 얼음 없이로 담았어요. |
| 超预算 | 예산보다 조금 넘어요. 감자튀김을 라지에서 미디엄으로 바꿀까요? |
| 确认下单 | 이대로 주문 넣을까요? |
| 付款指引 | **19:13**까지 결제해 주세요. 지금부터 15분이에요. |
| 订单已取消（超时未付款） | 결제 시간이 지나서 주문이 자동으로 취소됐어요. 결제는 안 됐어요. 새로 주문할까요? |
| 制作中 | 결제 완료됐어요. 지금 만드는 중이에요. |
| 待取餐 | 준비됐어요. 픽업 번호는 **1234**예요. 이 카드를 카운터에 보여 주세요. |
| 出错 | 맥도날드 쪽에서 문제가 생겼어요. 결제는 안 됐어요. 다시 해 볼까요? |
| 结束祝福 | 맛있게 드세요! |

### 3.5 العربية (ar) — 整块右对齐

| 场景 | 示范句 |
|---|---|
| 开场 | مرحبًا! سأساعدك في الطلب — ماذا تحب أن تجرب؟ |
| 领券 | وجدت لك قسيمة. لكنها تبدأ في 26 أكتوبر، فلا يمكن استخدامها اليوم. |
| 推荐 | أنصحك ببرغر ماك سبايسي — دجاج مقرمش مع حرارة واضحة، وهو الأكثر طلبًا هنا. |
| 可替换项 | يمكنك أيضًا استبداله بـ: |
| 修改完成 | تم — بدون خس، وكولا بدون ثلج. |
| 超预算 | السعر أعلى قليلًا من ميزانيتك. هل أستبدل البطاطس الكبيرة بالوسطى؟ |
| 确认下单 | هل أؤكد الطلب؟ |
| 付款指引 | يرجى الدفع قبل **19:13** — أي بعد 15 دقيقة. |
| 订单已取消（超时未付款） | انتهى وقت الدفع، فأُلغي الطلب تلقائيًا. لم يُخصم أي مبلغ — هل أبدأ طلبًا جديدًا؟ |
| 制作中 | تم الدفع! جارٍ تحضير الطلب الآن. |
| 待取餐 | طلبك جاهز — رقم الاستلام **1234**. اعرض هذه البطاقة على الكاشير. |
| 出错 | حدث خطأ من جانب ماكدونالدز. لم يُخصم أي مبلغ. لنحاول مرة أخرى. |
| 结束祝福 | بالهناء والشفاء! |

### 3.6 Français (fr)

| 场景 | 示范句 |
|---|---|
| 开场 | Bonjour ! Je vous aide à commander — qu'est-ce qui vous ferait plaisir ? |
| 领券 | J'ai trouvé un coupon pour vous. Attention : il ne prend effet que le 26 octobre, il n'est donc pas utilisable aujourd'hui. |
| 推荐 | Essayez le McSpicy — poulet croustillant et bien relevé. C'est le plus commandé ici. |
| 可替换项 | Vous pouvez aussi le remplacer par : |
| 修改完成 | C'est noté — sans salade, et Coca sans glaçons. |
| 超预算 | C'est un peu au-dessus de votre budget. Je remplace les grandes frites par des moyennes ? |
| 确认下单 | Je valide la commande ? |
| 付款指引 | Merci de payer avant **19 h 13** — dans 15 minutes. |
| 订单已取消（超时未付款） | Le délai de paiement est dépassé, la commande a donc été annulée automatiquement. Rien n'a été débité — j'en crée une nouvelle ? |
| 制作中 | Paiement reçu ! La cuisine prépare votre commande. |
| 待取餐 | Votre commande est prête — numéro **1234**. Montrez cette carte au comptoir. |
| 出错 | Une erreur est survenue côté McDonald's. Rien n'a été débité. On réessaie ? |
| 结束祝福 | Bon appétit ! |

### 3.7 Español (es)

| 场景 | 示范句 |
|---|---|
| 开场 | ¡Hola! Le ayudo a pedir — ¿qué le apetece hoy? |
| 领券 | Encontré un cupón para usted. Ojo: empieza a valer el 26 de octubre, así que hoy no se puede usar. |
| 推荐 | Le recomiendo la McSpicy: pollo crujiente con un picante de verdad. Es la más pedida aquí. |
| 可替换项 | También puede cambiarlo por: |
| 修改完成 | Listo: sin lechuga y la Coca-Cola sin hielo. |
| 超预算 | Se pasa un poco de su presupuesto. ¿Cambio las papas grandes por medianas? |
| 确认下单 | ¿Confirmo el pedido? |
| 付款指引 | Pague antes de las **19:13** — faltan 15 minutos. |
| 订单已取消（超时未付款） | Se acabó el plazo de pago, así que el pedido se canceló automáticamente. No se cobró nada. ¿Lo creo de nuevo? |
| 制作中 | ¡Pago recibido! Ya lo están preparando. |
| 待取餐 | Su pedido está listo: número **1234**. Muestre esta tarjeta en el mostrador. |
| 出错 | Hubo un error del lado de McDonald's. No se cobró nada. ¿Lo intentamos otra vez? |
| 结束祝福 | ¡Que lo disfrute! |

### 3.8 Deutsch (de)

| 场景 | 示范句 |
|---|---|
| 开场 | Hallo! Ich helfe Ihnen bei der Bestellung — worauf haben Sie Lust? |
| 领券 | Ich habe einen Coupon für Sie. Achtung: Er gilt erst ab 26. Oktober, heute lässt er sich nicht einlösen. |
| 推荐 | Probieren Sie den McSpicy — knuspriges Hähnchen mit deutlicher Schärfe. Der läuft hier am besten. |
| 可替换项 | Sie können ihn auch tauschen gegen: |
| 修改完成 | Erledigt — ohne Salat, Cola ohne Eis. |
| 超预算 | Das liegt etwas über Ihrem Budget. Soll ich die großen Pommes gegen mittlere tauschen? |
| 确认下单 | Soll ich die Bestellung abschicken? |
| 付款指引 | Bitte zahlen Sie bis **19:13** — in 15 Minuten. |
| 订单已取消（超时未付款） | Die Zahlungsfrist ist abgelaufen, daher wurde die Bestellung automatisch storniert. Es wurde nichts belastet. Soll ich eine neue anlegen? |
| 制作中 | Zahlung eingegangen! Die Küche bereitet Ihre Bestellung zu. |
| 待取餐 | Ihre Bestellung ist fertig — Abholnummer **1234**. Zeigen Sie diese Karte am Counter. |
| 出错 | Auf McDonald's-Seite ist ein Fehler aufgetreten. Es wurde nichts belastet. Noch einmal versuchen? |
| 结束祝福 | Guten Appetit! |

---

## 4. 接口中文报错 → 各语言友好说法

> 接口（尤其 `calculate-price` / `create-order` / `cancel-order`）会把**中文口语**直接抛回来，例如 `600012`「此卡券不在使用日期内，请在有效期内来使用哦！」。
> **绝不能把中文原文给访客。** 先按场景归类，再用下表。

| 场景 | 中文原文（示例） | 我们内部的判定 |
|---|---|---|
| 券不在使用期 | 此卡券不在使用日期内，请在有效期内来使用哦！ | `code=600012` 或文案含「不在使用日期」 |
| 售罄 | 该商品已售完 / 暂时缺货 | 文案含「售完」「缺货」「下架」 |
| 门店不可用 | 当前门店暫不支持 / 门店休息中 | 文案含「门店」「不支持」「休息」「打烊」 |
| 超时 | 请求超时 / 系统繁忙 | 文案含「超时」「繁忙」「网络」 |
| 订单已取消（超时未付款） | 订单已取消 / 订单已关闭 | 文案含「已取消」「已关闭」，或 `expirePayTime` 已过 |

| 语言 | 券不在使用期 | 售罄 | 门店不可用 | 超时 | 订单已取消（超时未付款） |
|---|---|---|---|---|---|
| en | This coupon isn't valid yet — it starts on **{date}**. I'll price it without the coupon. | That item just sold out. Want me to swap it? | This store isn't taking orders right now. Try another branch? | McDonald's system is slow to respond. Let's retry in a moment. | The payment window passed, so the order was cancelled automatically. Nothing was charged — want to start a new one? |
| ru | Этот купон ещё не действует — с **{date}**. Пересчитаю без него. | Это блюдо только что закончилось. Заменить? | Ресторан сейчас не принимает заказы. Попробовать другой? | Система McDonald's не отвечает. Попробуем через минуту. | Время на оплату истекло, заказ отменён автоматически. Деньги не списаны — создать новый? |
| ja | このクーポンはまだ使えません（**{date}**から有効）。クーポンなしで計算しますね。 | ただいま売り切れました。別のものに変更しますか？ | この店舗は現在注文を受け付けていません。別の店舗にしますか？ | マクドナルドのシステムが応答していません。少ししてから再度お試しください。 | お支払いの時間が過ぎたため、ご注文は自動でキャンセルされました。料金は発生していません。新しく作り直しますか？ |
| ko | 이 쿠폰은 아직 사용할 수 없어요 (**{date}**부터). 쿠폰 없이 계산할게요. | 방금 품절됐어요. 다른 걸로 바꿀까요? | 이 매장은 지금 주문을 받지 않아요. 다른 매장으로 갈까요? | 맥도날드 시스템 응답이 느려요. 잠시 후 다시 시도할게요. | 결제 시간이 지나서 주문이 자동으로 취소됐어요. 결제는 안 됐어요. 새로 주문할까요? |
| ar | هذه القسيمة غير فعّالة بعد — تبدأ في **{date}**. سأحسب بدونها. | هذا الصنف نفد للتو. هل أستبدله؟ | هذا الفرع لا يستقبل طلبات الآن. هل نجرّب فرعًا آخر؟ | نظام ماكدونالدز لا يستجيب. لنحاول بعد قليل. | انتهى وقت الدفع، فأُلغي الطلب تلقائيًا. لم يُخصم أي مبلغ — هل أبدأ طلبًا جديدًا؟ |
| fr | Ce coupon n'est pas encore valable — à partir du **{date}**. Je recalcule sans lui. | Cet article vient d'être épuisé. Je le remplace ? | Ce restaurant ne prend pas de commandes pour le moment. Un autre point de vente ? | Le système McDonald's ne répond pas. On réessaie dans un instant. | Le délai de paiement est dépassé, la commande a donc été annulée automatiquement. Rien n'a été débité — j'en crée une nouvelle ? |
| es | Este cupón aún no es válido — empieza el **{date}**. Calculo sin él. | Ese producto se acaba de agotar. ¿Lo cambio? | Este local no acepta pedidos ahora. ¿Probamos otro? | El sistema de McDonald's no responde. Reintentemos en un momento. | Se acabó el plazo de pago, así que el pedido se canceló automáticamente. No se cobró nada. ¿Lo creo de nuevo? |
| de | Dieser Coupon gilt noch nicht — erst ab **{date}**. Ich rechne ohne ihn. | Der Artikel ist gerade ausverkauft. Soll ich ihn tauschen? | Diese Filiale nimmt gerade keine Bestellungen an. Andere Filiale? | Das McDonald's-System antwortet nicht. Gleich noch einmal versuchen. | Die Zahlungsfrist ist abgelaufen, daher wurde die Bestellung automatisch storniert. Es wurde nichts belastet. Soll ich eine neue anlegen? |

**实现要求**：建一张 `errorMap: { code?, keyword[] } → { scene, i18nKey }`，先按 `code` 命中，再按中文关键词兜底，**最后一定要有 `unknown` 兜底句**（不要把原文透出）：
- en: `Something went wrong on McDonald's side. Nothing was charged. Want to try again?`
- 其余语言同理，见上表"出错"行。

---

## 5. 排版与可读性

| 项目 | 要求 |
|---|---|
| 字号 | 中文（给店员）≥ 20pt；目标语言 ≥ 16pt；数字 ≥ 22pt |
| 行宽 | 每行 ≤ 22 个汉字 / ≤ 40 个拉丁字符 |
| 强调 | 堂食/外带、取餐码、过敏声明用加粗或色块 |
| RTL | 阿拉伯语整块 `dir="rtl"`，标点镜像，数字保持 LTR 不翻转 |
| 双语 | 中文在上（给店员看），目标语言在下（给访客看），不要混排成一行 |
| 禁用 | 拼音当译名、emoji 当动词、全大写长句（德语尤其不要全大写） |
