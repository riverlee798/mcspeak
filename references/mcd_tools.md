# mcd_tools.md — mcspeak 用到的 mcd-mcp 工具手册

> 只收录本 Skill 真正会用到的 13 个工具。其余（商城、派对、抽奖、外送地址）不在范围内。
> 所有结论来自 2026-10-24 对门店 `3350020` 的实测（见 `samples/`）。**工具描述里的枚举和字段说明有错，以实测为准。**

## 0. 全局约定

| 项目 | 约定 |
|---|---|
| 成功判定 | 信封 `data`/`success`+`code`：`success===true && code===200` 才算成功，**不要只看 `message`** |
| 场景口径 | 只做**到店自取**：`beType=1`、`orderType=1`、**不传 beCode** |
| 取餐方式 | `takeWayCode` 只有 `eat-in`（堂食）与 `take-in-store`（外带）两种，取自 `calculate-price` 的 `data.takeWayList[].code` |
| 金额单位 | `calculate-price` = **分（整数）**；`create-order` / `query-order` = **元（字符串）**，如 `"33.5"` |
| productCode | **字符串**（4/6/10 位混排，如 `"1600"`、`"521952"`、`"9900014838"`），禁止转 int |
| 中文 | 所有字段值、错误文案、`itemName` 都是中文，**必须过一层本地化**才能给访客看 |

---

## 1. now-time-info

取服务端时间。**所有日期/时段判断的唯一时间源**，不要用访客手机的时区。

- 参数：无
- 返回：`data.timestamp`(ms)、`data.datetime`(ISO)、`data.formatted`(yyyy-MM-dd HH:mm:ss)、`data.date`、`data.year/month/day`、`data.dayOfWeek`(SATURDAY)、`data.timezone`(GMT+08:00)、`data.offset`、`data.utc`

---

## 2. query-nearby-stores

查到店可点餐门店。

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `beType` | integer | ✅ | 只传 `1`（到店自取）。`5` 是得来速，本 Skill 不用 |
| `searchType` | integer | ✅ | `2`=按位置搜（需 city+keyword）；`1`=收藏门店 |
| `city` | string | 条件 | `searchType=2` 必填，如 `济南市` |
| `keyword` | string | 条件 | `searchType=2` 必填，如 `山东大学中心校区` |

返回 `data[]`：`storeCode`、`storeName`、`address`、`distance`(米)、`businessStatus`、`businessStartTime/EndTime`、`reservation`、`reservationTimeOptions[]`、`longitude`/`latitude`（**恒 0.0**）、`beCode`（beType=1 时不存在）

**坑**
- **`searchType=1`（收藏门店）字段残缺**：没有 `businessStatus/businessStartTime/businessEndTime`，`distance` 恒 `0`。**只能用来显示店名和 storeCode，不能判断是否营业、不能排序。**
- 经纬度恒 `0.0` → 不能做地图、不能本地算最近距离，只能用接口给的 `distance`。
- `storeName` 含换行/全角括号，展示前要清洗。
- 预约时段是整串中文（`夜市(17:14至21:45)，宵夜(22:14至23:31)`），要原样展示，`today=true` 标当天。

---

## 3. query-meals

查门店菜单（**两层结构**）。

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `storeCode` | string | ✅ | 纯数字 |
| `orderType` | integer | ✅ | 传 `1` |
| `beType` | integer | ✅ | 传 `1`（到店自取时不传 beCode） |
| `beCode` | string | ❌ | 到店自取**不要传** |
| `reservationDate` | string | ❌ | 仅预约下单时传，`yyyy-MM-dd HH:mm` |

返回：
```
data.categories[].name              分类名（含 \n，需清洗）
data.categories[].meals[].code      商品码
data.categories[].meals[].tags[]    "套餐"/"单品"/"100%纯牛肉"/"麦香鱼系列"/"麦金卡" 等营销标签
data.meals{code}.name / .image
data.meals{code}.currentPrice       现价【元字符串】"33.5"
data.meals{code}.originalPrice      划线价【元字符串】
data.meals{code}.discountType       null / 随单购麦金卡优惠 / 促销优惠
data.meals{code}.canWithOrder       是否可随单购
data.meals{code}.withOrder{membershipCode, specId}
data.frequent{code, tags}           常点（可能为空）
```

**坑**
- 同一商品会在多个分类出现（实测 99 条目 / **93 个唯一商品**）→ 按分类渲染、按 code 去重。
- 价格是元字符串，不是数字，也不是分。
- 单个响应约 9 KB → **必须按 storeCode+orderType+beType 缓存**（建议 10–15 分钟）。
- 本接口**没有任何配料/过敏原/热量/辣度/清真字段** → 见 `menu_tags.md`（人工标注）。

---

## 4. query-meal-detail

查单个餐品的套餐组成 + 特调项。**下单前必须查，否则不知道能不能改。**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `storeCode` | string | ✅ | |
| `orderType` | integer | ✅ | `1` |
| `beType` | integer | ✅ | `1` |
| `code` | string | ✅ | 商品码 |
| `beCode` | string | ❌ | 到店自取不传 |
| `reservationDate` | string | ❌ | 仅预约 |

返回：
```
data.supportModify : boolean
data.rounds[]                       套餐轮次；【单品为空数组】
  .id .name .minQuantity .maxQuantity .quantity
  .choices[]
    .code .name .quantity .maxQuantity .isDefault(1/0)
    .diffPrice("+ ¥1.5" 字符串)
    .supportModify
    .modification{ items[] }        该选项自己的特调组
data.modification{ items[] }        单品的特调组
  items[]: .maxValues .minValues
    .values[]: .code .name .price(分) .maxQuantity .minQuantity
              .selectedQuantity .selectedKey .unselectedKey(可能没有)
```

**坑（全部踩过）**
- **单品的特调挂在 `data.modification`，套餐子项的特调挂在 `rounds[].choices[].modification`** —— 两套路径都要处理。例：麦香鱼 `rounds=[]` 但 `supportModify=true`。
- `choices[].maxQuantity = -1` 表示"不限"，不是"不能选"。
- 每个商品都要查一次详情（93 个商品 = 93 次调用）→ **先筛 3–5 个候选再查**，并缓存。

---

## 5. list-nutrition-foods

查营养数据。

- 参数：无
- 返回：`data` 是**一个多行 CSV 字符串**（不是数组！）：
  ```
  [160]{productName,nutritionDescription,energyKj,energyKcal,protein,fat,carbohydrate,sodium,calcium}:
    猪柳麦满分,null,1288,308,16,16,24,781,213
  ```

**坑**
- 首行是"条数 + 表头"，要跳过；每行按逗号 split，共 9 列。
- **没有任何 productCode / id，只能按名称匹配**；实测 93 个商品里**仅 18 个能精确命中**，套餐全部无数据，且存在重名（`小杯玉米杯`、`纯牛奶（盒装）`各 2 条）。
- 匹配不到就**不要显示热量**，绝不估算。

---

## 6. available-coupons

查「麦麦省」当前可领券列表。参数：无。返回：券名称、图片、状态、促销标签（**无 couponId**）。

## 7. auto-bind-coupons

一键领取所有可领券。参数：无。
返回是**渲染文本**（不是 JSON），形如：
```
11.9元麦辣鸡腿堡
  couponId：C0FFEE0000000000C0FFEE0000000000
  couponCode：MCD000000000000000
立即领取：https://m.mcd.cn/...
```

**坑**：返回里**没有适用商品、没有有效期**；它是纯文本，需要正则抽 `couponId` / `couponCode`；「立即领取」链接要给访客点（领取动作本身不在 MCP 内完成，视场景而定）。

## 8. query-my-coupons

查卡包里的券（**不校验门店/渠道可用性**）。

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `page` | string | ❌ | 默认 1，最多 5 页 |
| `pageSize` | string | ❌ | 默认 200，最大 200 |

**坑**：返回**不含 `couponId` / `couponCode`**（只有券名、优惠、有效期、渠道标签）→ 要和 `auto-bind-coupons` 的结果**按券名 join** 才能拿到 code。有效期是文本，能解释"为什么门店侧不可用"。

## 9. query-store-coupons

查「指定门店 + 订单类型」可用券（**下单前唯一可信的可用性判断**）。

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `storeCode` | string | ✅ | 纯数字 |
| `orderType` | integer | ✅ | `1` |
| `beType` | integer | ✅ | `1` |
| `beCode` | string | ❌ | 到店自取不传 |
| `reservationDate` | string | ❌ | 仅预约；**传 null 会报 schema 错**，非预约场景干脆别传 |

返回 `data[]`：`title`、`couponId`、`couponCode`（**一个 couponId 可对应多个 code**）、`tradeDateTime`、`products[].productName`、`products[].productCode`

**坑**：可能返回**空数组**（券存在但未到生效日/不适用本店），实测 10-24 查询、券 10-26 才生效 → `[]`。空数组是"当前不可用"，不是"没有券"。

---

## 10. calculate-price

计价（**下单前必须调用**，且是拿 `takeWayCode` 的唯一来源）。

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `storeCode` | string | ✅ | |
| `orderType` | integer | ✅ | `1` |
| `beType` | integer | ✅ | `1` |
| `beCode` | string | ❌ | 到店自取不传 |
| `items` | array | ✅ | 见下 |
| `reservationDate` | string | ❌ | 仅预约 |
| `needTableware` | boolean | ❌ | 外送才有意义 |
| `gmServiceCode` | string | ❌ | 团餐，不用 |

`items[]`：
```jsonc
{
  "productCode": "9900005456",
  "quantity": 1,
  "couponId": "C0FFEE0000000000C0FFEE0000000000",       // 券挂在这一行上，与 couponCode 成对
  "couponCode": "MCD680...",
  "modification": { "values": [{ "code": "100136", "key": "0-1", "quantity": 1 }] },
  "roundList": [               // 套餐才用
    { "round": "1", "comboItemList": [{ "code": "1440", "quantity": 1,
        "modification": { "values": [ ... ] } }] }
  ]
}
```

返回（单位**分**）：`productOriginalPrice`、`productPrice`、`originalPrice`、`discount`、`price`、`productList[]{productCode,productName,quantity,originalSubtotal,subtotal}`、`takeWayList[]{code,title,subtitle}`、条件出现：`deliveryPrice/packingPrice/tablewarePrice/enjoyed/enjoyable/mealAssistanceList`

**坑**
- 到店自取时 `deliveryPrice/packingPrice/tablewarePrice/enjoyed/enjoyable` **可能整块缺失**，不要假设存在。
- **特调是否生效，价格上看不出来**（可去项都是 0 元）→ 只能靠下单后 `query-order` 的 `comboItemList` 核对。
- `round` 实测传 `"1"/"2"/"3"`（轮次 id 字符串）可被接受。

---

## 11. create-order

创建订单（**产生真实订单，必须先获用户确认**）。

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `storeCode` | string | ✅ | |
| `orderType` | integer | ✅ | `1` |
| `beType` | integer | ✅ | `1` |
| `takeWayCode` | string | ✅* | `orderType=1` 必传，取 `eat-in` / `take-in-store` |
| `items` | array | ✅ | 结构同 `calculate-price` |
| `beCode` | string | ❌ | 到店自取不传 |
| `addressId` | string | ❌ | 仅外送 |
| `remark` | string | ❌ | **仅外送**（≤50 字），到店自取传了也无意义 |
| `needTableware` | boolean | ❌ | 外送 |
| `reservationDate` | string | ❌ | 仅预约 |

返回（**外层多一层 `orderDetail`**）：
```
data.orderId                       订单号
data.payId                         支付单号
data.payH5Url                      支付链接（只有这里才有！）
data.orderDetail.orderId
data.orderDetail.orderStatus       状态文字，如 "待支付"
data.orderDetail.status            状态码，实测待支付 = "10"
data.orderDetail.storeName / storeAddress
data.orderDetail.orderProductList[].productName / productImage / quantity
                                   / price(元) / comboItemList[]{itemName, itemQuantity}
data.orderDetail.totalAmount / realTotalAmount / totalDiscountAmount  （元字符串）
data.orderDetail.couponList[]{couponName, discountAmount}
data.orderDetail.createTime
data.orderDetail.expirePayTime     ★ 付款时限（实测 = createTime + 15 分钟）
data.orderDetail.pickupCode        ★ 取餐码，**未支付时为空字符串**
data.orderDetail.lockerCode / lockerQrCode   取餐柜（未见返回）
data.orderDetail.takeWay           取餐方式文字，如 "外带"
data.orderDetail.needTableware
data.orderDetail.deliveryInfo{...} 仅外送
data.orderDetail.remark
```

**坑**
- **`payH5Url` 只在 create-order 出现，`query-order` 拿不到** → 创建后必须立刻把订单号/支付链接/时限存下来。
- `pickupCode` 付款前是 `""`，**付款卡在前、取餐卡在后**。
- 金额变**元字符串**（`"33.5"`），与计价接口的**分**不是一回事。

---

## 12. query-order

查订单详情 / 支付状态 / 取餐码。

- 参数：`orderId` string ✅
- 返回：**平铺结构**（没有 `orderDetail` 外层），字段与 `orderDetail` 基本一致，但**没有 `payH5Url`，也没有 `payId` 以外的支付信息**（`payId` 仍在）

**坑**
- `status` 码与工具文档对不上：实测验到 `status="10"` + `orderStatus="待支付"`，而文档写 "10=配餐中-餐厅确认配餐中"。**以实测为准**，见 `order_status_map.md`。
- `create-order` 与 `query-order` 两种形状都要能解析（写一个 `normalizeOrder()`）。

## 13. cancel-order

取消订单（非商城）。

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `orderId` | string | ✅ | |
| `cancelReasonCode` | string | ✅ | `1` 改主意、`2` 重复下单、`3` 点错、`4` 地址/电话错、`5` 时间错、`-1` 其它 |

**坑**：已过期/已完成的订单取消会失败；错误文案是中文口语，要本地化。

---

# 8 条硬结论（写代码前必须读）

## ① modification 的 key 必须**按组类型**解释

| 组类型 | 判定方式 | key 语义 | 怎么传 |
|---|---|---|---|
| **开关组** | `values[]` 里**有 `unselectedKey`** | `selectedKey`=保留、`unselectedKey`=去掉 | **组内所有项都必须传**，选中的用 selectedKey、未选中的用 unselectedKey |
| **单选组** | **没有 `unselectedKey`**，且 `minValues=1 && maxValues=1` | 每个 key 就是**一个选项**，按选项名匹配 | **只传选中的那一个** |

实测冰量（code 恒为 `200002`，4 个选项 code 相同，只能靠 key 区分）：

| 选项 | key |
|---|---|
| 标准 | `0-1` |
| **去冰** | **`0-0`** |
| 多冰 | `0-2` |
| 少冰 | `1-1` |

> ⚠️ **同一个字符串 `0-0` 在两类组里含义相反**：开关组里是"去掉"，单选组（冰量）里是"去冰"这个选项。**绝不能写一个全局的 key→含义映射表**，必须带上组类型一起判断。

同理「加浓缩」是单选组：`不加=0-0`、`加=0-1`（加价 500 分）。

## ② `pickupCode` 付款前是空字符串
取餐码只有付款成功后用 `query-order` 才有值。**付款前无法生成取餐卡**，只能生成"柜台点餐卡"。

## ③ 支付链接与付款时限
`payH5Url`（`https://m.mcd.cn/mcp/scanToPay?orderId=...`）**只在 `create-order` 返回**，创建后要立即保存。
时限看 `data.orderDetail.expirePayTime`，实测 = 创建后 **15 分钟**；App 提示「超时未支付订单将被取消」。

## ④ 金额单位两套
`calculate-price` → **分（整数）**；`create-order` / `query-order` → **元（字符串）**。展示前统一成 `¥xx.xx`，内部统一存分。

## ⑤ 订单状态以实测为准
工具文档的 `status` 枚举不可信（实测 `10` = 待支付，文档写配餐中）。**同时存 `orderStatus` 文字和 `status` 码**，UI 用文字、逻辑用码。App 显示的状态文字与 `orderStatus` **一致**。详见 `order_status_map.md`。

## ⑥ 两种订单结构
`create-order` 的结果在 `data.orderDetail` 里；`query-order` 是 `data` 平铺。写 `normalizeOrder(resp)` 统一。

## ⑦ 双语卡片从**我们自己的入参**生成，不解析 `itemName`
卡片内容 = 下单时的 `items` 参数 + `menu_tags.md` 的英文名/描述。
`itemName`（如 `麦辣鸡腿汉堡 切块生菜(不要)`、`可乐中杯 冰(去冰)`）**只用来核对定制是否生效**：出现 `(不要)` / `(去冰)` 就说明 key 传对了。它是拼好的中文串，做翻译源不可靠。

## ⑧ 券的失败是整单失败
券挂在 `items[i].couponId + couponCode` 上；一张无效 → 整个 `calculate-price` 失败（实测 `code=600012`「此卡券不在使用日期内，请在有效期内来使用哦！」），**不会自动降级为无券价格**。
→ 策略：`auto-bind-coupons`（领）→ `query-store-coupons`（确认本店可用）→ 按券名/商品匹配到具体 item → 逐张试算，**失败就摘掉该券重算**，并把原因用访客母语说明。

---

# 踩坑清单（速查）

| # | 坑 | 应对 |
|---|---|---|
| 1 | `searchType=1` 无营业时间、distance=0 | 只用来显示店名 |
| 2 | 经纬度恒 0.0 | 不做地图/本地距离计算 |
| 3 | 菜单 99 条目 vs 93 商品 | 按 code 去重 |
| 4 | 价格元字符串 vs 计价分 | 统一存分 |
| 5 | `query-meals` 9 KB/次 | 缓存 10–15 min |
| 6 | 单品特调在 `data.modification`，套餐在 `choices[].modification` | 两条路径都写 |
| 7 | `maxQuantity=-1` = 不限 | 不要当"不可选" |
| 8 | 营养表是 CSV 字符串、无 code、18/93 命中 | 匹配不到就不显示 |
| 9 | `query-store-coupons` 可能返回 `[]`（券未生效） | 当作"不可用"，不是"没有券" |
| 10 | 券无效 → 整单 600012 | 摘券重算 + 母语解释 |
| 11 | `reservationDate: null` 会触发 schema 校验失败 | 非预约场景不传该键 |
| 12 | `payH5Url` 只在 create-order | 下单后立即落库 |
| 13 | `pickupCode` 付款前为空 | 付款后再出取餐卡 |
| 14 | `status` 码文档不可信 | 用实测映射表 |
| 15 | `orderStatus`/`itemName`/错误文案全中文 | 过本地化层 |
| 16 | 特调不影响价格 | 用 `comboItemList` 核对 |
