# mcspeak 数据探测报告（第 1 步 · 只读）

> 项目：**mcspeak（麦麦替你说）**
> 目标：帮不会中文的外国人在中国麦当劳点餐 —— 母语推荐 / 改单 / 自动领券算最省 / 谨慎处理清真与过敏限制 / 输出双语柜台点餐卡或取餐卡
> 探测时间：2026-10-24 17:22–17:25（GMT+8，周六）
> 探测门店：`3350020` 麦当劳济南山大路(成大高科)餐厅（距山东大学中心校区 513 m，营业 05:00–23:45）
> 场景口径：到店自取 `orderType=1` / `beType=1`，**不传 beCode**
> 只读约束：全程未调用 `create-order`、`cancel-order`、`mall-create-order`、`party-order-create`、`draw-lottery`；`auto-bind-coupons` 已调用（会写入用户券包，属允许范围）
> 原始样本：`references/samples/`（16 个 JSON，已脱敏）

---

## 0. 一句话结论

| # | 结论 | 置信度 |
|---|---|---|
| 1 | **MCP 里没有配料表、没有过敏原、没有清真标识**。唯一接近"成分"的是改造项（可去掉吉士/生菜/酸黄瓜/洋葱粒/酱），它只能做"减项"，不能证明"不含"。 | 高（5 个样本 + 全量字段结构交叉验证） |
| 2 | **券确实挂在 `items[]` 的每一个商品上**（`couponId` + `couponCode`），且服务端逐券强校验，无效券直接整单报错 `600012`，不会静默忽略。 | 高（实测报错） |
| 3 | **到店场景 `takeWayList` 只有 2 项**：`eat-in`（堂食 / 店内用餐）与 `take-in-store`（外带 / 店内自提）。**取餐方式由这个 code 决定，不是由门店决定。** | 高（实测） |

---

## 1. 第 1 步：当前时间（`now-time-info`）

**返回**：`timestamp`（毫秒）、`datetime`、`formatted`、`date`、`year/month/day`、`dayOfWeek`、`timezone`(GMT+08:00)、`offset`、`utc`，外层是统一信封 `{success, code, message, datetime, traceId, data}`。

**结论**
- 服务端时间是**唯一可信时间源**，返回 `2026-10-24 17:22:11`，`dayOfWeek=SATURDAY`。
- 统一信封是后面所有错误处理的基础：**判定成功要同时看 `success` 与 `code`**，`code=200` 才继续。

**对开发的影响**
- 套餐/早餐卡的时段（如早餐卡优惠、早午餐切换）必须用服务端时间判断，不能用访客手机时区。
- `reservationDate`（预约）格式是 `yyyy-MM-dd HH:mm`，要由服务端时间推导，不能自己拼。

---

## 2. 第 2 步：门店（`query-nearby-stores`）

### 2.1 `searchType=2`（按位置搜索，city=济南市，keyword=山东大学中心校区）

返回 5 家门店，字段完整：

| storeCode | 门店 | 距离 | 营业 | 支持预约 |
|---|---|---|---|---|
| **3350020** | 麦当劳济南山大路(成大高科)餐厅 | **513 m** | 05:00–23:45 | ✅ |
| 3350307 | 麦当劳济南印象城IS餐厅 | 821 m | 00:00–23:59 | ✅ |
| 3350257 | 麦当劳济南花园路IS餐厅 | 1031 m | 06:00–23:00 | ✅ |
| 3350069 | 麦当劳济南山大路(华强广场)餐厅 | 1057 m | 06:00–23:55 | ✅ |
| 3350285 | 麦当劳济南鑫苑鑫中心餐厅 | 2508 m | 07:00–23:59 | ✅ |

**选定：`3350020`**（最近 513 m 且营业中）。`beCode` **不存在** —— 到店自取场景本来就没有 beCode，后续所有调用都不传。

### 2.2 `searchType=1`（收藏门店）

返回 **1 家**（就是 `3350020`），但**字段是残缺版**：

| 字段 | searchType=2 | searchType=1 |
|---|---|---|
| `businessStatus` / `businessStartTime` / `businessEndTime` | 有 | **无** |
| `distance` | 真实米数 | **恒为 0** |
| `reservation` / `reservationTimeOptions` | 有 | 有 |
| `longitude` / `latitude` | 全为 `0.0` | 全为 `0.0` |

**对开发的影响**
1. 收藏门店可以"一键复购"，但**不能用来判断是否营业**，也不能拿 `distance` 排序 → mcspeak 首页应有"上次那家 / 附近门店"两条路径，且收藏路径要补一次 `searchType=2` 校验或直接查菜单看是否可售。
2. `longitude/latitude` 恒 `0.0` → **不能做地图、不能做"最近门店"本地计算**，只能用接口给的 `distance`（且仅 `searchType=2` 有）。
3. 预约时段以字符串形式返回，例如 `夜市(17:14至21:45)，宵夜(22:14至23:31)`，`today=true` 标记当天 —— 要原样展示给访客，不能只取一半（工具描述明确警告）。

---

## 3. 第 3 步：菜单（`query-meals`）

### 3.1 规模

| 指标 | 数值 |
|---|---|
| 分类数 | **14** |
| 分类内条目数（含跨分类重复） | **99** |
| 去重后商品数（= `meals` 映射表条数） | **93** |
| 分类引用与映射表缺失/孤立 | 0 / 0（一致） |
| `canWithOrder=true`（随单购麦金卡优惠） | 16 |
| `discountType` | `随单购麦金卡优惠` 16、`促销优惠` 3、无 74 |

分类名（含换行符，需 `replace('\n','')`）：人气热卖、小食拼盘/多人餐、精选单人餐、鸡肉汉堡/卷、随心配1+1、大堡口福单人餐、巨无霸/牛鱼肉堡、安格斯MAX厚牛堡、炸鸡、开心乐园、小食甜品/其他、麦咖啡™、500大卡套餐、饮品。

### 3.2 字段结构（关键：两层结构）

```
data.categories[]           ← 只给 code + tags（+ 分类名，含 \n）
  .name
  .meals[].code
  .meals[].tags[]           ← "套餐"/"单品"/"100%纯牛肉"/"麦香鱼系列"/"麦金卡" 等营销标签
data.meals{code}            ← 真正的详情映射表
  .name  .image
  .currentPrice  .originalPrice   ← ⚠️ 都是【字符串】"33.5"，不是数字
  .discountType                    ← null / 随单购麦金卡优惠 / 促销优惠
  .canWithOrder                    ← 是否可随单购
  .withOrder{membershipCode, specId}  ← 实际只返回这两个（schema 里写的 cardId/cardType 没返回）
data.frequent{code, tags}   ← 常点（本次返回为空）
```

### 3.3 结论
- **菜单里没有任何配料、原料、过敏原、热量、辣度、清真字段**。只有名字、图、价、营销标签。
- 商品 ID 是**字符串**（`"1600"` 四位、`"521952"` 六位、`"9900014838"` 十位混排），**不要当 int 处理**（会丢前导位或精度）。
- 分类里同一商品会重复出现（99 vs 93），**渲染按分类走、去重按 code 走**。
- 价格要 `parseFloat`，并且注意"划线价"与"现价"并存：`currentPrice` 是实付价、`originalPrice` 是原价。

### 3.4 对开发的影响
- 推荐引擎的可用特征只有：**分类归属、名称、价格、营销标签、是否随单购**。想按"口味/辣度/热量/肉种"推荐，必须**自建静态知识库**（本轮已确认接口不给）。
- `query-meals` 一次返回 ~9 KB / 93 商品，**必须缓存**（按 storeCode + orderType + beType + 时间段），否则每轮对话都拉一次很浪费。

---

## 4. 第 4 步：餐品详情（`query-meal-detail`，5 个样本）

### 4.1 样本选择

| 类型 | 商品 | code | 结构 |
|---|---|---|---|
| 鸡肉汉堡套餐 | 麦辣鸡腿汉堡三件套 | `9900005456` | 3 个 round |
| 牛肉汉堡套餐 | 巨无霸三件套 | `9900005466` | 3 个 round |
| 麦香鱼（单品） | 麦香鱼 | `1600` | `rounds=[]`，modification 挂在 data 层 |
| 含猪肉 | 枫糖风味厚松饼猪柳蛋堡 | `521730` | `rounds=[]` |
| 甜品 | 经典麦旋风 | `9900008754` | 1 个 round（口味二选一） |

### 4.2 结构（三层）

```
data.supportModify : boolean            ← 单品是否可特调
data.rounds[]                           ← 套餐的"轮次"，单品为空数组
  .id .name .minQuantity .maxQuantity .quantity
  .choices[]
    .code .name .quantity .maxQuantity
    .isDefault(1/0) .diffPrice("+ ¥1.5" 字符串)
    .supportModify : boolean
    .modification{ items[] }            ← 该选项自己的特调组
data.modification{ items[] }            ← 单品的特调组
  items[]:
    .maxValues .minValues               ← 该组最多/最少改几项
    .values[]:
      .code        ← 特调物料码（同一组内可能重复，如冰量 4 项都是 200002）
      .name        ← 吉士 / 生菜 / 酸黄瓜 / 洋葱粒 / 巨无霸酱 / 麦香鸡酱 / 麦香鱼酱 / 奶油球 / 白砂糖
      .price       ← 加价（分），如加浓缩 8008 = 500（+¥5）
      .selectedQuantity / .maxQuantity / .minQuantity
      .selectedKey / .unselectedKey     ← 关键：下单要传的 key
```

### 4.3 `selectedKey` / `unselectedKey` 到底是什么

这是本轮最有价值的发现之一 —— **它是"要不要这个配料"的开关**：

| 场景 | key 形态 | 含义 |
|---|---|---|
| 巨无霸：巨无霸酱/吉士/生菜/酸黄瓜/洋葱粒 | `selectedKey="0-1"` / `unselectedKey="0-0"` | `0-1` = 保留，`0-0` = 去掉。**组内所有项都必须传**，选中的用 selectedKey、未选中的用 unselectedKey |
| 可乐冰量：标准/去冰/多冰/少冰 | 依次 `0-1` / `0-0` / `0-2` / `1-1`，**4 项 code 全是 `200002`** | 单选组，用 key 区分取值，**不能靠 code 区分** |
| 咖啡加浓缩：不加/加 | `0-0` / `0-1`（加价 500 分） | 加价项，price≠0 |
| 鲜萃咖啡：奶油球 / 白砂糖 | 各有 selected/unselected | 可独立勾选 |

> 工具自带的两条硬规则（必须落到代码里）：
> 1. 含 `unselectedKey` 的组，**组内所有项都要传**（选中的用 selectedKey、未选中的用 unselectedKey），少传会算错或报错。
> 2. `minValues=1 && maxValues=1 && values.length==1` → 该项**必选**，不能给用户"不要"的选项。

### 4.4 重点问题：有没有配料 / 原料 / 过敏原字段？

**没有。逐字段核对结果：**

| 想找的字段 | 是否存在 | 实际情况 |
|---|---|---|
| `ingredients` / 配料表 | ❌ | 全响应无此概念 |
| `allergen` / 过敏原 | ❌ | 全响应无此概念 |
| `nutrition` / 热量 | ❌ | 详情接口不给（只有另一个独立的 `list-nutrition-foods`，见第 5 步） |
| `isHalal` / 清真标识 | ❌ | 完全没有 |
| `spicyLevel` / 辣度 | ❌ | 只有名字里带"辣"（麦辣） |
| 可去掉的物料名 | ✅ | `modification.values[].name`，例如 **吉士、生菜、酸黄瓜、洋葱粒、巨无霸酱、麦香鸡酱、麦香鱼酱、切块生菜、奶油球、白砂糖** |

**注意两个坑：**
- **麦香鱼**：`data.rounds = []` 但 `supportModify=true`，特调在 `data.modification` 上；而**套餐**的特调挂在 `rounds[].choices[].modification`。**两套路径都要处理**，否则麦香鱼类单品会"看起来不能改"。
- **猪柳蛋堡**：`modification` 里**只有"吉士"能去掉**，猪肉本体不可去 → 对清真/素食用户只能"不推荐"，不能"改造"。

### 4.5 对开发的影响（最关键）
- mcspeak 想做"清真/过敏安全"，**MCP 数据无法支撑自动判定**，必须换成**保守产品策略**（见第 7 节）。
- 但 `modification` 足以支撑"点餐卡的个性化备注"：访客说 no pickles / no onions / no mayo，可以真实落到订单参数上，而不是只写在纸上。这是 mcspeak 相对"翻译卡片"的核心壁垒。
- 每个商品都要单独调一次详情才知道能不能改 → **不能预先全量拉 93 个商品的详情**（93 次调用）。策略：先按菜单层筛 3–5 个候选，再按需查详情。

---

## 5. 第 5 步：营养成分（`list-nutrition-foods`）

### 5.1 返回格式（重要：不是 JSON 数组）

```
data = "[160]{productName,nutritionDescription,energyKj,energyKcal,protein,fat,carbohydrate,sodium,calcium}:\n  猪柳麦满分,null,1288,308,16,16,24,781,213\n  ..."
```

- `data` 是**一个字符串**，首行是表头 + 条数，之后每行 CSV。
- 9 个字段：名称、营养描述、能量 kJ、能量 kcal、蛋白质 g、脂肪 g、碳水 g、钠 mg、钙 mg。
- 共 **160 条**，其中 `小杯玉米杯`、`纯牛奶（盒装）` **重名**（各出现 2 次）。

### 5.2 能不能和 `query-meals` 的 productCode 对上？

**不能 —— 完全没有任何 code / id，只能按名称匹配，而且匹配率很低：**

| 指标 | 数值 |
|---|---|
| 营养条目 | 160 |
| 本店商品 | 93 |
| 名称**精确**命中 | **18 / 93（19%）** |
| 未命中 | 75 个 |

未命中的典型原因（都是"看起来该有"但实际没有）：
- **套餐全部没有**：`巨无霸三件套`、`麦香鱼套餐`、`板烧鸡腿堡三件套`…… 营养表只有单品。
- **命名不一致**：`那么大鸡排（椒盐风味）` vs 营养表 `那么大鸡排`；`麦咖啡™美式` vs `冰美式中杯`；`新地` vs `朱古力新地/草莓新地`。
- **营养表里有本店没卖/别的渠道商品**：`雪碧`、`yeyeyeye奶冻款`、`柠檬拉明顿`、`皮蛋鸡肉粥`（早餐/下市品）。

### 5.3 对开发的影响
- 想显示"这顿多少卡"，只能做**单品级、名称模糊匹配**，并且必须处理"匹配不上就坦白说没有"。
- 建议建一张手工映射表 `productCode → 营养名`（先覆盖 18 个精确命中 + 高频单品），匹配不到就不显示热量 —— **绝不能猜**（热量猜错对外国游客是误导）。
- 附带的可用信号：营养表里的**名称本身**能反推部分成分（`猪柳`、`培根`、`牛肉`、`鳕鱼`、`鸡肉`、`牛奶`、`燕麦奶`、`豆浆`），可以做"肉种/奶源"的**弱判断**，但仍不足以判定清真/过敏。

---

## 6. 第 6 步：优惠券

### 6.1 `auto-bind-coupons`（一键领券）

返回**渲染文本**（非 JSON），共领到 3 张：

| 券名 | couponId | couponCode |
|---|---|---|
| 11.9元麦辣鸡腿堡 | `B34E5EC6710BEEECEC8B25C742D3F119` | `MCD000000000000000` |
| 19.9元王牌炸鸡任选2 | `A03BC156F97B8937213963D7632F3338` | `MCD000000000000000` |
| 免费脆薯饼 | `0D94B7923332F58026539DB8CCA81275` | `MCD000000000000000` |

⚠️ 这里**没有**适用商品、没有有效期、没有门槛 —— 拿不到"这张券能买什么"。

### 6.2 `query-store-coupons`（同门店 orderType=1 beType=1）

**返回 `data: []` 空数组**，连续调 2 次都一样。但券明明刚领到。

原因在 `query-my-coupons` 里找到了：

| 券名 | 优惠 | 有效期 | 标签 |
|---|---|---|---|
| 11.9元麦辣鸡腿堡 | ¥11.9（用券价） | **2026-10-26 10:30** – 2026-10-30 23:59（周一至周五 10:30-23:59） | 到店专用、外送专用 |
| 19.9元王牌炸鸡任选2 | ¥19.9（用券价） | **2026-10-26 10:30** – 2026-10-30 23:59（周一至周五 10:30-23:59） | 到店专用、外送专用 |

**今天是 10-24，券从 10-26 才生效** → 门店侧判定"当前不可用" → 返回空数组。工具自报"共 2 张可用"（第 3 张 `免费脆薯饼` 未列出，说明已被时间/状态过滤）。

### 6.3 券的元数据在两个接口之间是断的

| 想拿的字段 | auto-bind | query-store-coupons | query-my-coupons |
|---|---|---|---|
| 券名 | ✅ | ✅ `title` | ✅ |
| couponId | ✅ | ✅ | ❌ |
| couponCode | ✅ | ✅ | ❌ |
| 有效期 | ❌ | ✅ `tradeDateTime` | ✅（文本） |
| 适用商品 | ❌ | ✅ `products[].productName/productCode` | ❌ |

→ **必须做 join**：`auto-bind`/`query-my-coupons` 给 id+name，`query-store-coupons` 给 name+products。用 `title` 作为 join key（脆弱，但当前唯一可用）。

### 6.4 券的其它语义（来自 `query-store-coupons` 自带说明）
- **同一 couponId 可对应多个 couponCode**（多张同款券），展示要按 couponId 分组，否则会重复列一堆。
- 返回的是"当前门店 + 当前订单类型"可用券，已经过门店/渠道/配送方式校验 —— 与 `query-my-coupons`（"我有什么券"，不校验）是两个口径。

---

## 7. 第 7 步：计价（`calculate-price`）

### 7.1 不带券（巨无霸三件套 × 1）

```json
{"productOriginalPrice":3700,"productPrice":3700,"originalPrice":3700,"discount":0,"price":3700,
 "productList":[{"productCode":"9900005466","productName":"巨无霸三件套","quantity":1,
                 "originalSubtotal":3700,"subtotal":3700}],
 "takeWayList":[{"code":"eat-in","title":"堂食","subtitle":"店内用餐"},
                {"code":"take-in-store","title":"外带","subtitle":"店内自提"}]}
```

- **全部金额单位 = 分**（3700 → ¥37.00），与 `query-meals` 的元字符串（`"37"`）**不是同一单位**，务必分层转换。
- 本次未返回 `deliveryPrice / packingPrice / tablewarePrice / enjoyed / enjoyable / mealAssistanceList` —— 到店自取场景不适用，**这些字段是条件出现的，不能假设必有**。

### 7.2 带券（把 11.9 元麦辣鸡腿堡券挂在巨无霸三件套的 item 上）

```json
{"success":false,"code":600012,"message":"此卡券不在使用日期内，请在有效期内来使用哦！"}
```

**三个结论：**
1. **券是按商品挂在 `items[]` 上的** —— 每个 item 自己带 `couponId` + `couponCode`，一张券作用于一个商品行。
2. 服务端**强校验**：有效期不符 → **整单失败**（不是忽略券继续算）。
3. 错误信息是**中文口语**（"请在有效期内来使用哦！"）。mcspeak 必须自带**错误码 → 多语**映射，不能把中文抛给访客。

### 7.3 附加实验：把"去掉吉士 / 去掉洋葱粒"传进 `roundList`

入参：`items[0].roundList = [{round:"1", comboItemList:[{code:"1100", modification:{values:[…吉士 key=0-0…]}}]}, {round:"2",…}, {round:"3",…}]`

结果：**没报错，价格仍 3700**。因为本单所有特调加价都是 0，**无法通过价格差判断特调是否真的生效** → 需要在真正下单后从订单详情核对。本阶段禁调 `create-order`，**留为待验证缺口**（见第 10 节）。

### 7.4 取餐方式 `takeWayList`（重点问题 3）

到店自取（`beType=1, orderType=1`）返回 **2 项**，对应"堂食"与"外带"：

| code | title | subtitle | 含义 | 对点餐卡的意义 |
|---|---|---|---|---|
| `eat-in` | 堂食 | 店内用餐 | 在店里吃 | 卡片要印「堂食 / Dine-in」→ 店员不会给打包盒 |
| `take-in-store` | 外带 | 店内自提 | 在店里点、拿走吃 | 卡片要印「外带 / Takeaway」→ 店员会给袋子和餐具 |

- 下单必须带 `takeWayCode`，**否则订单缺少取餐方式**。
- 这是外国游客最高频的歧义点（"here or to go?"），mcspeak 必须在**下单前就问**，并写进双语卡。
- 得来速（`beType=5`）与外送（`orderType=2`）的 `takeWayList` 本轮未探测（不在范围内）。

---

## 8. 第 8 步：样本落盘

`~/mcspeak/references/samples/`，16 个文件：

| 文件 | 内容 |
|---|---|
| `00-index.md` | 索引与脱敏说明 |
| `01-now-time-info.json` | 服务端时间 + 统一信封 |
| `02-query-nearby-stores-nearby.json` | 5 家门店（searchType=2）+ 选定理由 |
| `03-query-nearby-stores-favorite.json` | 收藏门店（searchType=1，字段残缺对照） |
| `04-query-meals-store3350020.json` | 14 分类 / 93 商品全量菜单 |
| `05-…-9900005456-chicken-set.json` | 麦辣鸡腿堡三件套（3 rounds） |
| `06-…-9900005466-beef-set.json` | 巨无霸三件套（3 rounds，5 个可去配料） |
| `07-…-1600-fish.json` | 麦香鱼（rounds=[] + data.modification） |
| `08-…-521730-pork.json` | 猪柳蛋堡（只有吉士可去） |
| `09-…-9900008754-dessert.json` | 经典麦旋风（口味二选一，不可特调） |
| `10-list-nutrition-foods.json` | 160 条营养 CSV（字符串格式） |
| `11-auto-bind-coupons.json` | 领券 3 张（id+code） |
| `12-query-store-coupons-empty.json` | 门店可用券为空 + 有数据时的字段说明 |
| `13-query-my-coupons.json` | 券包 2 张 + 有效期（解释空数组原因） |
| `14-calculate-price-no-coupon.json` | 不带券计价 + takeWayList |
| `15-calculate-price-with-coupon-error.json` | 带券 → 600012 |
| `16-calculate-price-with-modification.json` | 附加：带 roundList/特调计价 |

**脱敏**：本轮所有响应都不含访客个人信息（无手机号、无地址、无联系人）。门店地址属公开营业信息，保留到门牌级；如后续接 `delivery-query-addresses` / `delivery-create-address`，必须对 `address`、`addressDetail`、`contactName`、`phone` 做掩码后再落盘。

---

## 9. 三个必答问题（结论版）

### Q1：配料信息能不能支持清真（halal）和过敏（allergen）过滤？

**结论：不能，一条都不能自动判定。** 必须改成"保守白名单 + 显式免责"的产品策略。

| 维度 | 接口是否有数据 | 能做的最多是什么 | 绝对不能做什么 |
|---|---|---|---|
| 清真 | ❌ 无 halal 字段、无门店清真标识、无认证信息 | 用**商品名 + 可去配料**做"不含猪肉/培根/猪柳"的**白名单**（如巨无霸、麦香鱼、板烧鸡腿堡、薯条、玉米杯、可乐）；能明确识别的高风险词：**猪柳、培根、火腿**（`521730`、`521731`、`1106`、`511781`、`9900014838`…） | ❌ 不能说"这是 halal" / "清真认证"；❌ 不能承诺"无猪肉交叉污染"（共用炸锅、共用操作台） |
| 过敏原 | ❌ 无 allergen 字段（无麸质/奶/蛋/花生/坚果/大豆/鱼/贝类/芝麻） | 用菜名做**风险提示**：麦香鱼=鱼+麸质+奶；汉堡=麸质+奶(吉士)+蛋(酱)；麦旋风/新地=奶；派=麸质 | ❌ 不能输出"本餐不含坚果/不含麸质"；❌ 不能给过敏用户"安全"背书 |
| 素食 | ❌ 无素食标识 | 按名字识别肉类，给出"可能含肉"清单（连薯条都要提示共用炸油） | ❌ 不能判定"纯素" |
| 热量 | ⚠️ 有，但只覆盖 19% 的商品且只能按名匹配 | 显示**单品**热量，匹配不到就不显示 | ❌ 不能给套餐编一个总热量 |

**落到产品上的三条铁律**
1. **不认证，只提示**：卡片和对话里出现"halal-friendly / 不含 X"这类断言前，必须过一遍"我们的数据只能证明什么"。
2. **风险前置，不藏在二级页**：访客一说清真/过敏，先给**风险声明**，再给推荐。
3. **把"可去掉的配料"当成唯一可执行动作**：`no cheese / no pickles / no onions / no sauce` 是真能落单的；"这个不含猪肉"是不能落单的。

### Q2：券是不是按商品挂在 `items` 上？

**是。** 具体语义：

```
items: [
  { productCode: "9900005466", quantity: 1,
    couponId:   "C0FFEE0000000000C0FFEE0000000000",   ← 挂在这一个商品行上
    couponCode: "MCD000000000000000" }
]
```

- 券是**商品级**而非订单级；`couponId` 与 `couponCode` **要成对传**（只传一个不行）。
- 服务端**逐券强校验**：不在有效期 → 整个 `calculate-price` 失败（`600012`），**不会自动降级为无券价格**。→ 聊天流程里必须先 `query-store-coupons` 确认可用，再挂券；挂了要能优雅回滚重算。
- 一张券通常对应一个商品行；"一单多件、各挂各的券"是可行形态；"一张券抵多件"未验证。
- `query-store-coupons` 的 `products[]` 说明**一张券可适用多个商品**（要自己挑一个匹配的商品行去挂）。

### Q3：`takeWayList` 有哪些取餐方式？分别对应堂食还是外带？

**到店自取场景只有两个，且就是"堂食 vs 外带"：**

| code | title / subtitle | 堂食 or 外带 |
|---|---|---|
| `eat-in` | 堂食 / 店内用餐 | **堂食**（在店吃） |
| `take-in-store` | 外带 / 店内自提 | **外带**（在店点、拿走） |

- 必须把 code 传给 `create-order` 的 `takeWayCode`。
- 对 mcspeak：这是**双语点餐卡的必填项**，也是"店员能否听懂"的关键 —— 卡片上用大字标 `堂食 DINE-IN` / `外带 TAKEAWAY`。
- 得来速（DT）与外送的取餐方式清单本轮未取（未在探测范围）。

---

## 10. 未验证 / 缺口清单（下一轮要补）

| # | 缺口 | 为什么重要 | 建议动作 |
|---|---|---|---|
| 1 | `create-order` 的返回结构（**取餐号**、支付链接、订单号） | 双语取餐卡的"取餐号"字段没它做不出来 | 下一轮允许下单时，用最低价单品试一单并 `query-order` 核对 |
| 2 | 特调（去吉士/去洋葱）是否**真的**落到订单 | 这是 mcspeak 的核心卖点，不能只"不报错" | 同上：下单后读订单详情，确认 modification 回显 |
| 3 | 有效券的**真实优惠金额**与叠加规则 | 现在只验证了失败路径，没验证 `discount` 如何变 | 换一张当天有效的券复测 |
| 4 | 外送 / 得来速的 `takeWayList` | 若支持送餐到酒店，卡片形态不同 | `delivery-query-*` + `beType=5` 探测 |
| 5 | 过敏原 / 清真信息的**外部数据源** | 接口永远不会有 | 用麦当劳官方营养/过敏原页面 + 门店清真名单，人工维护成静态表 |
| 6 | 官方英文商品名 | 直译会闹笑话（"麦辣鸡腿汉堡" ≠ "Spicy Chicken Burger" 的官方叫法） | 建 `中→英` 官方名词典（Big Mac / McSpicy / Filet-O-Fish / McWings / McFlurry / McGriddles…） |
| 7 | 门店是否清真、是否有英文服务 | 无接口字段 | 人工标注 + 卡片兜底（指图 + 数字） |

---

## 11. 对 mcspeak 架构的直接影响（可直接照做）

1. **数据层**：写一个 `mcd-client` 薄封装，统一处理
   - 信封判定（`success && code===200`）
   - 价格单位归一（菜单=元字符串 / 计价=分）
   - 错误码表（`600012 → "优惠券不在有效期 / Coupon not valid on this date"` + 建议动作）
   - 菜单按 `storeCode+orderType+beType` 缓存（TTL 建议 10–15 分钟）
2. **商品模型**：`Product(code, nameZh, nameEn, price, tags, category, canWithOrder, withOrder)`；**不要**把 `category` 当唯一归属（一物多分类）。
3. **详情按需加载**：先筛 3–5 个候选，再 `query-meal-detail`，缓存 `modification` 结果（同一商品结构稳定）。
4. **券流程**（严格顺序，防止整单失败）：
   `auto-bind-coupons`（领）→ `query-store-coupons`（确认本店本场景可用）→ 用 `title` join 拿 `couponId/couponCode` → 只在**匹配到商品行**时挂券 → `calculate-price` 失败则**摘券重算**并把失败原因译成访客母语。
5. **必问三件事**（进店前决定订单形态）：**在这里吃还是带走**（→ `eat-in` / `take-in-store`）、**饮食限制**（清真 / 过敏 / 素食 / 不吃牛肉…）、**预算**。
6. **双语卡字段**（柜台卡 / 取餐卡共用一套模板）：
   门店名 + storeCode / 堂食·外带（双语大字）/ 商品中英名 + 数量 + 单价 / 已选特调（`no pickles` 等，双语）/ 饮食声明（"No pork, please confirm" 而非 "Halal"）/ 合计（¥ + 分单位换算）/ 取餐号（待补）/ 二维码或订单号（待补）。
7. **不做的事**：不做"清真认证"背书、不做过敏"安全"承诺、不给套餐编热量、不猜 `productCode` 与营养表的对应。

---

_本报告基于 2026-10-24 单次、单门店、到店自取的只读探测。菜单与券随时效变化，`references/samples/` 里的原始返回是唯一事实来源。_
