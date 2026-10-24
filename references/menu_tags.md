# menu_tags.md — 全量菜单人工标注（93 个商品）

> ⚠️ **这是按"商品名称 + 套餐组成 + 可去掉配料"做的人工标注，不是官方配料表，也不是官方过敏原信息。**
> 麦当劳中国通过 mcd-mcp 提供的菜单/详情接口里**没有配料、没有过敏原、没有清真标识、没有辣度字段**（见 `mcd_tools.md`）。
> 一切以门店实时菜单和包装标识为准；**表里没有的新品一律视为"不确定"**，不得推断。
>
> 数据源：`samples/04-query-meals-store3350020.json`（2026-10-24，门店 3350020，93 个唯一商品）
> 「可去掉的配料」只对**已实测 detail 的商品**有值，其余写「未探测」——需要用 `query-meal-detail` 补。
> 英文名是通行叫法，**非官方译名**，上线前需人工校准。

## 读表说明

| 列 | 取值 |
|---|---|
| 肉类 | 鸡 / 牛 / 猪 / 鱼 / 虾 / 无肉 / 混合 / 非食品 / **不确定** |
| 含猪肉 | 含 / 不含 / **不确定**（套餐里只要有一样含猪肉，整份标"含"） |
| 辣度 | 0 不辣 · 1 微辣或不确定 · 2 辣 · 3 很辣 |
| 可去掉的配料 | 来自 `modification`，格式「物料名(默认带/可去)」；「未探测」= 还没调 detail |

---

## 人气热卖（6）

| 官方中文名 | productCode | 拼音 | 英文名 | 肉类 | 含猪肉 | 辣度 | 英文感官描述 | 可去掉的配料 |
|---|---|---|---|---|---|---|---|---|
| 枫糖风味厚松饼猪柳蛋堡三件套 | 9900014838 | fēng táng fēng wèi hòu sōng bǐng zhū liǔ dàn bǎo sān jiàn tào | McGriddles Sausage Egg & Cheese Meal | 猪 | 含 | 0 | Sweet maple griddle cakes hugging a savoury pork patty, egg and cheese, with fries and a drink. | 未探测 |
| 龙焰鸡腿堡三件套 | 9900016073 | lóng yàn jī tuǐ bǎo sān jiàn tào | Dragon Flame Chicken Burger Meal | 鸡 | 不含 | 3 | Crispy chicken under a smoky chilli-butter glaze that builds real heat. | 未探测 |
| 龙焰鸡腿堡 | 521952 | lóng yàn jī tuǐ bǎo | Dragon Flame Chicken Burger | 鸡 | 不含 | 3 | Crunchy chicken fillet with a Korean-style chilli-butter sauce — the hottest thing on the menu. | 未探测 |
| 全明星双人分享餐八件套 | 9900011056 | quán míng xīng shuāng rén fēn xiǎng cān bā jiàn tào | All-Star Share Meal for Two (8 pcs) | 混合 | 不确定 | 1 | A bit of everything for two — burgers, chicken, fries and drinks in one tray. | 未探测 |
| 麦麦周末双人餐 | 9900015151 | mài mài zhōu mò shuāng rén cān | Weekend Meal for Two | 混合 | 不确定 | 1 | A generous two-person spread built for sharing on a lazy weekend. | 未探测 |
| 精选单人餐三件套 | 9900004064 | jīng xuǎn dān rén cān sān jiàn tào | Classic Solo Meal (3 pcs) | 不确定 | 不确定 | 1 | A safe one-person set: one burger, one side, one drink. Composition varies — confirm at the counter. | 未探测 |

## 小食拼盘 / 多人餐（3）

| 官方中文名 | productCode | 拼音 | 英文名 | 肉类 | 含猪肉 | 辣度 | 英文感官描述 | 可去掉的配料 |
|---|---|---|---|---|---|---|---|---|
| BFF四宫格小食盘 | 9900015730 | BFF sì gōng gé xiǎo shí pán | BFF Snack Platter (4 sections) | 混合 | 不确定 | 1 | Four little compartments of finger food — made for picking and passing around. | 未探测 |
| 堡堡随心拼（7件任选） | 9900004066 | bǎo bǎo suí xīn pīn | Build-Your-Own Burger Box (7 pcs) | 混合 | 不确定 | 1 | Seven pieces you choose yourself — a build-your-own box for a group. | 未探测 |
| BFF四宫格小食盘双人餐 | 9900005321 | BFF sì gōng gé xiǎo shí pán shuāng rén cān | BFF Snack Platter Meal for Two | 混合 | 不确定 | 1 | The four-section snack platter plus drinks, sized for two. | 未探测 |

## 精选单人餐（5）

| 官方中文名 | productCode | 拼音 | 英文名 | 肉类 | 含猪肉 | 辣度 | 英文感官描述 | 可去掉的配料 |
|---|---|---|---|---|---|---|---|---|
| 枫糖风味厚松饼猪柳蛋堡三件套 | 9900014837 | fēng táng fēng wèi hòu sōng bǐng zhū liǔ dàn bǎo sān jiàn tào | McGriddles Sausage Egg & Cheese Meal | 猪 | 含 | 0 | Sweet maple griddle cakes, savoury pork, egg and cheese — a breakfast staple. | 未探测 |
| 枫糖风味厚松饼猪柳堡三件套 | 9900014974 | fēng táng fēng wèi hòu sōng bǐng zhū liǔ bǎo sān jiàn tào | McGriddles Sausage Meal | 猪 | 含 | 0 | Maple-sweet griddle cakes with a juicy pork patty — no egg, just pork. | 未探测 |
| 人气超值四件套随心选 | 9900004236 | rén qì chāo zhí sì jiàn tào suí xīn xuǎn | Popular Value Meal (4 pcs, your pick) | 混合 | 不确定 | 1 | Four items you pick yourself at a flat price — mix burger, side and drink. | 未探测 |
| 鱼牛汉堡四件套随心选 | 9900010110 | yú niú hàn bǎo sì jiàn tào suí xīn xuǎn | Fish & Beef Meal (4 pcs, your pick) | 混合 | 不含 | 1 | Choose between fish and beef for your main, plus side and drink. | 未探测 |
| 安格斯厚牛堡四件套随心选 | 9900006957 | ān gé sī hòu niú bǎo sì jiàn tào suí xīn xuǎn | Angus Beef Meal (4 pcs, your pick) | 牛 | 不含 | 0 | A thick Angus patty with your choice of toppings, plus side and drink. | 未探测 |

## 鸡肉汉堡 / 卷（10）

| 官方中文名 | productCode | 拼音 | 英文名 | 肉类 | 含猪肉 | 辣度 | 英文感官描述 | 可去掉的配料 |
|---|---|---|---|---|---|---|---|---|
| 龙焰鸡腿堡四件套 | 9900016309 | lóng yàn jī tuǐ bǎo sì jiàn tào | Dragon Flame Chicken Burger Meal (4 pcs) | 鸡 | 不含 | 3 | The chilli-butter chicken burger, upsized to four items. | 未探测 |
| 麦辣鸡腿堡四件套 | 9900000891 | mài là jī tuǐ bǎo sì jiàn tào | McSpicy Chicken Burger Meal (4 pcs) | 鸡 | 不含 | 2 | China's classic spicy chicken burger with fries and a drink. | 未探测 |
| 板烧鸡腿堡四件套 | 9900000890 | bǎn shāo jī tuǐ bǎo sì jiàn tào | Grilled Chicken Burger Meal (4 pcs) | 鸡 | 不含 | 0 | A juicy grilled chicken thigh with a teriyaki-style glaze — not spicy. | 未探测 |
| 板烧鸡腿堡三件套 | 9900005462 | bǎn shāo jī tuǐ bǎo sān jiàn tào | Grilled Chicken Burger Meal (3 pcs) | 鸡 | 不含 | 0 | Grilled chicken thigh, sweet-savoury glaze, fries and a drink. | 未探测 |
| 麦辣鸡腿汉堡三件套 | 9900005456 | mài là jī tuǐ hàn bǎo sān jiàn tào | McSpicy Chicken Burger Meal (3 pcs) | 鸡 | 不含 | 2 | Crispy spicy chicken fillet with lettuce and mayo-style sauce, fries and a drink. | 麦香鸡酱(默认带)、切块生菜(默认带，可去) |
| 麦香鸡套餐 | 9900005453 | mài xiāng jī tào cān | McChicken Meal | 鸡 | 不含 | 0 | Mild chicken patty with shredded lettuce and mayo — the gentle option. | 未探测 |
| 麦辣鸡腿汉堡 | 1440 | mài là jī tuǐ hàn bǎo | McSpicy Chicken Burger | 鸡 | 不含 | 2 | Crunchy chicken fillet with a peppery kick and cool shredded lettuce. | 麦香鸡酱(默认带)、切块生菜(默认带，可去) |
| 板烧鸡腿堡 | 1406 | bǎn shāo jī tuǐ bǎo | Grilled Chicken Burger | 鸡 | 不含 | 0 | Grilled thigh meat, glossy sweet glaze, soft bun — savoury, not spicy. | 未探测 |
| 麦香鸡 | 1450 | mài xiāng jī | McChicken | 鸡 | 不含 | 0 | The plain, mild chicken burger — soft patty, lettuce, mayo. | 未探测 |
| 鸡肉堡单品精选 | 9900008746 | jī ròu bǎo dān pǐn jīng xuǎn | Chicken Burger Picks | 鸡 | 不确定 | 1 | A rotating pick of chicken burgers — ask which one is included today. | 未探测 |

## 随心配 1+1（1）

| 官方中文名 | productCode | 拼音 | 英文名 | 肉类 | 含猪肉 | 辣度 | 英文感官描述 | 可去掉的配料 |
|---|---|---|---|---|---|---|---|---|
| 精选超值随心配 | 9900015568 | jīng xuǎn chāo zhí suí xīn pèi | Mix & Match 1+1 | 不确定 | 不确定 | 1 | Pick any two small items for one low price — the cheapest way to try things. | 未探测 |

## 大堡口福单人餐（1）

| 官方中文名 | productCode | 拼音 | 英文名 | 肉类 | 含猪肉 | 辣度 | 英文感官描述 | 可去掉的配料 |
|---|---|---|---|---|---|---|---|---|
| 大堡口福三件套 | 9900015602 | dà bǎo kǒu fú sān jiàn tào | Big Burger Value Meal (3 pcs) | 不确定 | 不确定 | 1 | A big-bite burger set at a value price — burger type varies by store. | 未探测 |

## 巨无霸 / 牛 / 鱼 / 肉堡（22）

| 官方中文名 | productCode | 拼音 | 英文名 | 肉类 | 含猪肉 | 辣度 | 英文感官描述 | 可去掉的配料 |
|---|---|---|---|---|---|---|---|---|
| 枫糖风味厚松饼猪柳蛋堡四件套 | 9900016301 | fēng táng fēng wèi hòu sōng bǐng zhū liǔ dàn bǎo sì jiàn tào | McGriddles Sausage Egg & Cheese Meal (4 pcs) | 猪 | 含 | 0 | Maple griddle cakes, pork patty, egg and cheese — the full breakfast set. | 未探测 |
| 巨无霸四件套 | 9900000888 | jù wú bà sì jiàn tào | Big Mac Meal (4 pcs) | 牛 | 不含 | 0 | The two-patty icon with Big Mac sauce, plus fries, drink and a side. | 未探测 |
| 不素之霸双层牛堡四件套 | 9900000886 | bù sù zhī bà shuāng céng niú bǎo sì jiàn tào | Double Beef Burger Meal (4 pcs) | 牛 | 不含 | 0 | Two beef patties, no vegetables, straight-up meat and cheese. | 未探测 |
| 培根蔬萃双层牛堡四件套 | 9900000885 | péi gēn shū cuì shuāng céng niú bǎo sì jiàn tào | Bacon Veggie Double Beef Meal (4 pcs) | 牛 | 含 | 0 | Double beef with bacon and crisp vegetables — smoky and savoury. | 未探测 |
| 双层深海鳕鱼堡四件套 | 9900000893 | shuāng céng shēn hǎi xuě yú bǎo sì jiàn tào | Double Filet-O-Fish Meal (4 pcs) | 鱼 | 不含 | 0 | Two flaky white-fish patties with tartar sauce and cheese. | 未探测 |
| 不素之霸双层牛堡三件套 | 9900005411 | bù sù zhī bà shuāng céng niú bǎo sān jiàn tào | Double Beef Burger Meal (3 pcs) | 牛 | 不含 | 0 | Pure double beef and cheese, fries, drink — no greens in sight. | 未探测 |
| 巨无霸三件套 | 9900005466 | jù wú bà sān jiàn tào | Big Mac Meal (3 pcs) | 牛 | 不含 | 0 | Two beef patties, Big Mac sauce, pickles, onion and lettuce, with fries and a drink. | 巨无霸酱、吉士、生菜、酸黄瓜、洋葱粒（全部默认带，均可去） |
| 培根蔬萃双层牛堡三件套 | 9900005468 | péi gēn shū cuì shuāng céng niú bǎo sān jiàn tào | Bacon Veggie Double Beef Meal (3 pcs) | 牛 | 含 | 0 | Smoky bacon over double beef with crunchy vegetables. | 未探测 |
| 双层深海鳕鱼堡三件套 | 9900005413 | shuāng céng shēn hǎi xuě yú bǎo sān jiàn tào | Double Filet-O-Fish Meal (3 pcs) | 鱼 | 不含 | 0 | Two fish patties, tartar sauce, cheese — mild and creamy. | 未探测 |
| 麦香鱼套餐 | 9900005460 | mài xiāng yú tào cān | Filet-O-Fish Meal | 鱼 | 不含 | 0 | Steamed-bun fish sandwich with tartar sauce and cheese, fries and a drink. | 未探测 |
| 双层吉士汉堡套餐 | 9900005464 | shuāng céng jí shì hàn bǎo tào cān | Double Cheeseburger Meal | 牛 | 不含 | 0 | Two beef patties, two slices of cheese, pickles and ketchup. | 未探测 |
| 吉士汉堡包套餐 | 9900005449 | jí shì hàn bǎo bāo tào cān | Cheeseburger Meal | 牛 | 不含 | 0 | The simplest beef burger: one patty, one cheese slice, pickles, ketchup. | 未探测 |
| 枫糖风味厚松饼猪柳蛋堡 | 521730 | fēng táng fēng wèi hòu sōng bǐng zhū liǔ dàn bǎo | McGriddles Sausage Egg & Cheese | 猪 | 含 | 0 | Sweet maple griddle cakes with pork sausage, egg and melted cheese. | 吉士（默认带，可去） |
| 枫糖风味厚松饼猪柳堡 | 521731 | fēng táng fēng wèi hòu sōng bǐng zhū liǔ bǎo | McGriddles Sausage | 猪 | 含 | 0 | Maple griddle cakes and a pork patty — sweet on the outside, savoury inside. | 未探测 |
| 巨无霸 | 1100 | jù wú bà | Big Mac | 牛 | 不含 | 0 | Two beef patties, three bun layers, Big Mac sauce, pickles, onion, lettuce. | 巨无霸酱、吉士、生菜、酸黄瓜、洋葱粒（全部默认带，均可去） |
| 双层深海鳕鱼堡 | 9900003586 | shuāng céng shēn hǎi xuě yú bǎo | Double Filet-O-Fish | 鱼 | 不含 | 0 | Two soft white-fish patties with tangy tartar sauce. | 未探测 |
| 麦香鱼 | 1600 | mài xiāng yú | Filet-O-Fish | 鱼 | 不含 | 0 | A steamed bun, one crisp fish patty, tartar sauce and half a slice of cheese. | 麦香鱼酱(默认带)、吉士(默认带，均可去) |
| 不素之霸双层牛堡 | 4648 | bù sù zhī bà shuāng céng niú bǎo | Double Beef Burger | 牛 | 不含 | 0 | Double beef, double cheese, no lettuce — pure savoury weight. | 未探测 |
| 培根蔬萃双层牛堡 | 1106 | péi gēn shū cuì shuāng céng niú bǎo | Bacon Veggie Double Beef Burger | 牛 | 含 | 0 | Bacon strips over two beef patties with crunchy veg and sauce. | 未探测 |
| 双层吉士汉堡 | 1120 | shuāng céng jí shì hàn bǎo | Double Cheeseburger | 牛 | 不含 | 0 | Two patties, two cheese slices, pickles and ketchup — a classic stack. | 未探测 |
| 高达吉士双牛堡 | 521316 | gāo dá jí shì shuāng niú bǎo | Gouda Double Beef Burger | 牛 | 不含 | 0 | Two beef patties under nutty melted Gouda — richer than a standard cheeseburger. | 未探测 |
| 牛肉堡单品精选 | 9900008747 | niú ròu bǎo dān pǐn jīng xuǎn | Beef Burger Picks | 牛 | 不确定 | 1 | A rotating beef-burger pick — ask which one is included today. | 未探测 |

## 安格斯 MAX 厚牛堡（6）

| 官方中文名 | productCode | 拼音 | 英文名 | 肉类 | 含猪肉 | 辣度 | 英文感官描述 | 可去掉的配料 |
|---|---|---|---|---|---|---|---|---|
| 培根安格斯厚牛堡四件套 | 9900000881 | péi gēn ān gé sī hòu niú bǎo sì jiàn tào | Bacon Angus Burger Meal (4 pcs) | 牛 | 含 | 0 | A thick Angus patty with bacon, plus side and drink. | 未探测 |
| 芝士安格斯厚牛堡四件套 | 9900000882 | zhī shì ān gé sī hòu niú bǎo sì jiàn tào | Cheese Angus Burger Meal (4 pcs) | 牛 | 不含 | 0 | Thick Angus beef blanketed in melted cheese, fries and a drink. | 未探测 |
| 培根安格斯厚牛堡三件套 | 9900005428 | péi gēn ān gé sī hòu niú bǎo sān jiàn tào | Bacon Angus Burger Meal (3 pcs) | 牛 | 含 | 0 | Angus beef with smoky bacon — the heaviest burger on the menu. | 未探测 |
| 芝士安格斯厚牛堡三件套 | 9900005430 | zhī shì ān gé sī hòu niú bǎo sān jiàn tào | Cheese Angus Burger Meal (3 pcs) | 牛 | 不含 | 0 | Angus beef and cheese, fries and a drink — rich and filling. | 未探测 |
| 培根安格斯厚牛堡 | 511781 | péi gēn ān gé sī hòu niú bǎo | Bacon Angus Burger | 牛 | 含 | 0 | A thick, coarse-ground Angus patty topped with bacon. | 未探测 |
| 芝士安格斯厚牛堡 | 511782 | zhī shì ān gé sī hòu niú bǎo | Cheese Angus Burger | 牛 | 不含 | 0 | Coarse-ground Angus beef with a thick layer of melted cheese. | 未探测 |

## 炸鸡（6）

| 官方中文名 | productCode | 拼音 | 英文名 | 肉类 | 含猪肉 | 辣度 | 英文感官描述 | 可去掉的配料 |
|---|---|---|---|---|---|---|---|---|
| 麦辣鸡翅4块套餐 | 9900005451 | mài là jī chì sì kuài tào cān | McWings Meal (4 pcs) | 鸡 | 不含 | 2 | Four peppery fried wings with fries and a drink. | 未探测 |
| 麦乐鸡套餐 | 9900004835 | mài lè jī tào cān | Chicken McNuggets Meal | 鸡 | 不含 | 0 | Bite-size breaded chicken with a dipping sauce, fries and a drink. | 未探测 |
| 麦辣鸡翅 | 1700 | mài là jī chì | McWings (2 pcs) | 鸡 | 不含 | 2 | Fried wings dusted with a peppery spice mix — mild but noticeable. | 未探测 |
| 麦乐鸡 | 1401 | mài lè jī | Chicken McNuggets | 鸡 | 不含 | 0 | Golden nuggets, crisp outside, soft white meat inside. | 未探测 |
| 那么大鸡排（椒盐风味） | 521156 | nà me dà jī pái | Big Chicken Fillet (Salt & Pepper) | 鸡 | 不含 | 0 | A palm-sized slab of chicken with a salt-and-pepper crust. | 未探测 |
| 麦麦脆汁鸡1块 | 9900005432 | mài mài cuì zhī jī | Crispy Juicy Chicken (1 pc) | 鸡 | 不含 | 0 | One piece of crunchy fried chicken that stays juicy inside. | 未探测 |

## 开心乐园（2）

| 官方中文名 | productCode | 拼音 | 英文名 | 肉类 | 含猪肉 | 辣度 | 英文感官描述 | 可去掉的配料 |
|---|---|---|---|---|---|---|---|---|
| 汉堡开心乐园餐 | 9900016057 | hàn bǎo kāi xīn lè yuán cān | Happy Meal (Burger) | 牛 | 不含 | 0 | A kids' set with a small burger, side, drink and a toy. | 未探测 |
| 鱼排堡开心乐园餐 | 9900016058 | yú pái bǎo kāi xīn lè yuán cān | Happy Meal (Fish) | 鱼 | 不含 | 0 | A kids' set with a small fish burger, side, drink and a toy. | 未探测 |

## 小食 / 甜品 / 其它（11）

| 官方中文名 | productCode | 拼音 | 英文名 | 肉类 | 含猪肉 | 辣度 | 英文感官描述 | 可去掉的配料 |
|---|---|---|---|---|---|---|---|---|
| 灰焰圆筒 | 521951 | huī yàn yuán tǒng | Ash-Grey Cone | 无肉 | 不含 | 0 | A soft-serve cone in a striking charcoal-grey swirl. | 未探测 |
| “葱不求人”按摩捶痒痒挠 | 521914 | cōng bù qiú rén | Novelty Back Scratcher | **非食品** | 不适用 | 不适用 | **Not food** — a novelty back scratcher sold as merch. Do not order for eating. | — |
| 泷愿成真麦旋风——大米风味 | 521917 | lóng yuàn chéng zhēn mài xuán fēng | Rice-Flavour McFlurry | 无肉 | 不含 | 0 | Creamy soft-serve swirled with a toasty rice-flavour crunch. | 未探测 |
| 脆薯饼 | 521741 | cuì shǔ bǐng | Hash Brown | 无肉 | 不含 | 0 | A flat golden patty of shredded potato, crisp outside and soft within. | 未探测 |
| 薯条 | 4810 | shǔ tiáo | Fries (Medium) | 无肉 | 不含 | 0 | Golden shoestring fries, lightly salted. | 未探测 |
| 脆脆薯条 | 514782 | cuì cuì shǔ tiáo | Crinkle-Cut Fries | 无肉 | 不含 | 0 | Ridged, extra-crisp fries with more surface for crunch. | 未探测 |
| 玉米杯 | 4437 | yù mǐ bēi | Corn Cup | 无肉 | 不含 | 0 | Sweet kernels of corn in a cup — the mildest side on the menu. | 未探测 |
| 经典麦旋风 | 9900008754 | jīng diǎn mài xuán fēng | McFlurry (Oreo / Strawberry) | 无肉 | 不含 | 0 | Thick vanilla soft-serve folded with cookie crumbs or strawberry sauce. | 无可去项（只能二选一口味：奥利奥/草莓） |
| 新地 | 9900008745 | xīn dì | Sundae | 无肉 | 不含 | 0 | Cold soft-serve under a glossy fruit or chocolate topping. | 未探测 |
| 圆筒冰淇淋 | 515837 | yuán tǒng bīng qí lín | Soft Serve Cone | 无肉 | 不含 | 0 | Plain vanilla soft-serve in a crisp cone — the cheapest cold treat. | 未探测 |
| 派 | 9900008752 | pài | Pie | 无肉 | 不确定 | 0 | A flaky fried pastry with a warm fruit filling; flavour rotates. | 未探测 |

## 麦咖啡™（10）

| 官方中文名 | productCode | 拼音 | 英文名 | 肉类 | 含猪肉 | 辣度 | 英文感官描述 | 可去掉的配料 |
|---|---|---|---|---|---|---|---|---|
| 麦咖啡™美式 | 507411 | mài kā fēi měi shì | McCafé Americano | 无肉 | 不含 | 0 | Clean, bitter espresso lengthened with hot or iced water. | 加浓缩(不加/加 ¥5)、冰量(标准/去冰/多冰/少冰) |
| 麦咖啡™奶铁 | 507409 | mài kā fēi nǎi tiě | McCafé Latte | 无肉 | 不含 | 0 | Espresso rounded out with plenty of steamed milk. | 加浓缩、冰量 |
| 燕麦奶铁 | 510479 | yàn mài nǎi tiě | Oat Latte | 无肉 | 不含 | 0 | Espresso with oat drink instead of dairy — lighter, slightly nutty. | 未探测 |
| 卡布奇诺 | 507387 | kǎ bù qí nuò | Cappuccino | 无肉 | 不含 | 0 | Espresso under a thick cap of airy milk foam. | 未探测 |
| 奶铁雪冰 | 520361 | nǎi tiě xuě bīng | Latte Frappé | 无肉 | 不含 | 0 | Blended iced latte, thick and slushy — closer to a dessert than a coffee. | 未探测 |
| 咖啡阿芙佳朵 | 514851 | kā fēi ā fú jiā duǒ | Coffee Affogato | 无肉 | 不含 | 0 | Hot espresso poured over cold ice cream — sweet and bitter at once. | 未探测 |
| 鲜萃咖啡 | 520689 | xiān cuì kā fēi | Fresh Brewed Coffee | 无肉 | 不含 | 0 | Filter coffee, mellow and easy to drink black. | 奶油球、白砂糖（默认带，均可去） |
| 浓缩咖啡 | 507389 | nóng suō kā fēi | Espresso | 无肉 | 不含 | 0 | One short, intense shot — the strongest coffee here. | 未探测 |
| 牛奶 | 507394 | niú nǎi | Milk | 无肉 | 不含 | 0 | Plain cold or hot milk, no coffee. | 未探测 |
| 燕麦奶 | 510488 | yàn mài nǎi | Oat Milk | 无肉 | 不含 | 0 | Plant-based oat drink, dairy-free by ingredient (shared equipment still possible). | 未探测 |

## 500 大卡套餐（3）

| 官方中文名 | productCode | 拼音 | 英文名 | 肉类 | 含猪肉 | 辣度 | 英文感官描述 | 可去掉的配料 |
|---|---|---|---|---|---|---|---|---|
| 酥脆无双套餐 | 9900011126 | sū cuì wú shuāng tào cān | Crispy Combo (~500 kcal) | 不确定 | 不确定 | 1 | A lighter combo put together to stay around 500 kcal — contents vary. | 未探测 |
| “辣”么快乐套餐 | 9900011123 | là me kuài lè tào cān | Spicy Happy Combo | 不确定 | 不确定 | 3 | Built around something spicy — expect noticeable heat. | 未探测 |
| 牛气满满套餐 | 9900009245 | niú qì mǎn mǎn tào cān | Beefy Combo | 牛 | 不确定 | 1 | A beef-forward combo; exact build varies by store. | 未探测 |

## 饮品（7）

| 官方中文名 | productCode | 拼音 | 英文名 | 肉类 | 含猪肉 | 辣度 | 英文感官描述 | 可去掉的配料 |
|---|---|---|---|---|---|---|---|---|
| 可乐 | 9900008751 | kě lè | Coca-Cola | 无肉 | 不含 | 0 | Cold, fizzy and sweet — the default drink with any meal. | 冰量(标准/去冰/多冰/少冰) |
| 怡泉+C | 515520 | yí quán jiā xī | Schweppes Lemon | 无肉 | 不含 | 0 | Sparkling lemon soda, tart and sharp rather than sweet. | 冰量 |
| 【美汁源】“黄金橙橙” | 2430 | huáng jīn chéng chéng | Minute Maid Orange | 无肉 | 不含 | 0 | Orange juice drink, sweet with a little acidity. | 冰量 |
| 阳光柠檬红茶 | 515280 | yáng guāng níng méng hóng chá | Lemon Iced Tea | 无肉 | 不含 | 0 | Sweet black tea with lemon — the usual choice if you don't want soda. | 冰量 |
| 阳光橙麦炫酷 | 6352 | yáng guāng chéng mài xuàn kù | Orange McFloat | 无肉 | 不含 | 0 | Orange soda with soft-serve ice cream floating on top. | 未探测 |
| 100% 苹果汁（盒装） | 6362 | píng guǒ zhī | 100% Apple Juice (box) | 无肉 | 不含 | 0 | Pure apple juice in a carton — no bubbles, not too sweet. | 未探测 |
| 锡兰红茶 | 3505 | xī lán hóng chá | Ceylon Black Tea | 无肉 | 不含 | 0 | Plain hot black tea, served without milk or sugar. | 未探测 |

---

# 衍生清单（供 diet_rules.md 直接引用）

## 含猪肉（**清真一律排除，不提供"去掉猪肉"**）
`9900014838` `9900014837` `9900014974` `9900016301` `521730` `521731`（猪柳）
`9900000885` `9900005468` `1106` `9900000881` `9900005428` `511781`（培根）

> 猪柳 = pork sausage；培根 = bacon；火腿 = ham。**这三类词一出现就是含猪肉。**

## 辣度 ≥2（不辣需求要避开）
| 辣度 3（很辣） | 辣度 2（辣） |
|---|---|
| `521952` `9900016073` `9900016309` 龙焰系列<br>`9900011123` “辣”么快乐套餐 | `1440` `9900005456` `9900000891` 麦辣鸡腿系列<br>`1700` `9900005451` 麦辣鸡翅 |

> 注意区分：**麦辣（mài là）辣**、**麦香鸡（mài xiāng jī）不辣**、**板烧不辣**。中文只差一个字，英文名必须写清 `Spicy` / 不写。

## 无肉（鱼、素食、甜品、饮料、小食）
**鱼**：`1600` `9900003586` `9900005460` `9900005413` `9900000893` `9900016058`
**奶/甜品**：`515837` `9900008745` `9900008754` `521951` `521917` `9900008752`(馅料不确定)
**小食**：`4810` `514782` `4437` `521741`
**饮品/咖啡**：`9900008751` `515520` `2430` `515280` `6352` `6362` `3505` `507411` `507409` `510479` `507387` `520361` `514851` `520689` `507389` `507394` `510488`

## 非食品（绝对不能推荐）
`521914` “葱不求人”按摩捶痒痒挠 —— 这是周边商品，在菜单里混着卖。

# 缺口

1. **88 个商品还没探测 `modification`** → 「可去掉的配料」大多为「未探测」。需要批量补 `query-meal-detail`（建议只补高频单品：`1406` 板烧、`1450` 麦香鸡、`1120` 双吉、`9900003586` 双层鳕鱼、`1401` 麦乐鸡、`1700` 麦辣鸡翅）。
2. 套餐类（三件套/四件套/随心选）的**具体组合随门店和时段变化**，本表按名称推断，属"不确定"。
3. 英文名非官方译名，需与麦当劳官方英文菜单校准。
4. 辣度是按名称标注，不是官方数据。
