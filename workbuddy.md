# mcspeak 开发对话记录

> 由 WorkBuddy 会话记录导出（`14860ecc-fb21-412e-a49d-389c137d7bc5.jsonl`），只保留对话正文：
> 已剔除工具调用、工具返回、思考过程与系统提示；订单号、支付链接、取餐码等已脱敏。

## 👤 用户

列出 mcd-mcp 的所有工具，每个工具写明名称、作用、参数（名称/类型/是否必填）和返回字段，整理成 markdown 表格

---

## 🤖 mcspeak

已拉取 mcd-mcp（麦当劳中国）全部 **35 个** 工具的实际 schema，按业务链路分成 5 组。参数列中 `*` 表示必填。

## 一、门店 / 地址 / 餐品（9）

| 工具 | 作用 | 参数（名称: 类型） | 返回字段 |
|---|---|---|---|
| `query-nearby-stores` | 到店场景查可点餐门店（到店自取 / 得来速） | `beType: integer*`（1 到店自取、5 得来速）、`searchType: integer*`（1 收藏门店、2 按位置搜索）、`city: string`（searchType=2 必填）、`keyword: string`（searchType=2 必填） | 门店列表：`storeCode`、`beCode`（仅 beType=5）、`reservation`、`reservationTimeOptions`、`today` |
| `delivery-query-addresses` | 外送场景查用户配送地址列表 | 无 | 地址列表（含 `addressId`，供后续查可配送门店） |
| `delivery-create-address` | 新增配送地址 | `address: string*`、`addressDetail: string*`、`city: string*`、`contactName: string*`、`phone: string*`（11 位）、`gender: string` | 未声明ᐟ（后续流程需 `addressId`，故响应应含地址 ID） |
| `delivery-query-stores` | 按地址 ID 查可配送门店 | `addressId: string*`、`beType: integer*`（2 麦乐送、6 团餐） | 门店列表：`storeCode`、`beCode` 等 |
| `query-meals` | 查门店餐品列表（含随单购） | `storeCode: string*`、`orderType: integer*`（1 到店、2 外送）、`beType: integer*`（1/2/5/6）、`beCode: string`（得来速/外送/团餐必传）、`reservationDate: string`（yyyy-MM-dd HH:mm） | 餐品列表：`productCode`、价格、随单购信息等 |
| `query-meal-detail` | 查单个餐品详情、套餐组成与特调项 | `storeCode: string*`、`orderType: integer*`、`beType: integer*`、`code: string*`（餐品编码）、`beCode: string`、`reservationDate: string` | `data.supportModify`、`choices[]`（`name`、`isDefault`、`choice.supportModify`）、`modification`（`selectedKey`/`unselectedKey`、特调 code、数量） |
| `query-meal-assistance` | 企业团餐查门店可用助餐服务（仅 beType=6） | `storeCode: string*`、`beCode: string`、`beType: integer`（固定 6）、`orderType: integer`、`reservationDate: string` | 助餐服务列表（含 `gmServiceCode`，供计价/下单） |
| `query-promotions` | 团餐场景查门店有效促销规则（满减/满折） | `storeCode: string*`、`orderType: integer*`（固定 2）、`beType: integer*`（固定 6）、`beCode: string`（团餐必传）、`reservationDate: string` | `promotionId`、`promotionType`（31 满额减、33 订单折扣）、`ruleCategory`（30 满折、40 满减）、`beTypes`、`startTime`、`endTime`、`gmServiceCode`、`products[]`（`type`、`productCode`）、`ruleDetail` |
| `list-nutrition-foods` | 查餐品营养成分（热量、蛋白质等） | 无 | 能量、蛋白质、脂肪、碳水化合物、钠、钙等营养字段 |

## 二、计价与订单（5）

| 工具 | 作用 | 参数（名称: 类型） | 返回字段 |
|---|---|---|---|
| `calculate-price` | 计算含优惠的总价（下单前必须调用） | `storeCode: string*`、`orderType: integer*`（1/2）、`beType: integer*`（1/2/5/6）、`beCode: string`（得来速/外送/团餐必传）、`reservationDate: string`、`gmServiceCode: string`（团餐助餐码）、`needTableware: boolean`、`items: array*`（`productCode: string*`、`quantity: integer*`、`couponId: string`、`couponCode: string`、`modification: object{values[]{code,key,quantity}}`、`roundList: array{round, comboItemList[]{code,quantity,modification}}`）、`withOrder: object{cardId,cardType,membershipCode,membershipSpecId}` | **价格字段（单位：分）**、`data.takeWayList[].code`（取餐方式码，下单用） |
| `create-order` | 创建麦当劳订单（到店 / 外送） | `storeCode: string*`、`orderType: integer*`、`beType: integer*`、`beCode: string`（条件必传）、`addressId: string`（orderType=2 必填）、`takeWayCode: string`（orderType=1 必填，来自 takeWayList）、`gmServiceCode: string`（团餐必填）、`items: array`（结构同上）、`withOrder: object`、`needTableware: boolean`、`remark: string`（≤50 字，仅外送）、`reservationDate: string` | 未声明ᐟ（引导话术含“支付链接”，响应应含订单号与支付链接） |
| `query-order` | 查订单详情 / 支付状态 / 配送进度 | `orderId: string*` | 未声明ᐟ |
| `order-list` | 查历史订单（非商城订单） | 无 | 未声明ᐟ（订单列表） |
| `cancel-order` | 取消非商城订单 | `orderId: string*`、`cancelReasonCode: string*`（1 改主意、2 重复下单、3 点错、4 地址/电话错、5 时间错、-1 其它） | 未声明ᐟ |

## 三、优惠券与营销（7）

| 工具 | 作用 | 参数（名称: 类型） | 返回字段 |
|---|---|---|---|
| `available-coupons` | 查「麦麦省」当前可领券列表 | 无 | 券名称、图片、状态、促销标签 |
| `auto-bind-coupons` | 一键自动领取所有可领券（无需 couponId） | 无 | 未声明ᐟ（领券结果） |
| `query-my-coupons` | 查卡包内已有券（不校验门店/订单可用性） | `page: string`（默认 1，最多 5 页）、`pageSize: string`（默认 200，最大 200） | 券资产列表（券信息与状态） |
| `query-store-coupons` | 查「指定门店 + 订单类型」下可用券 | `storeCode: string*`（纯数字）、`orderType: integer*`、`beType: integer*`、`beCode: string`（条件必传）、`reservationDate: string` | 可用券列表（含 `couponId`、`couponCode` 等） |
| `campaign-calendar` | 查当月营销活动日历与订阅状态 | `specifiedDate: string`（yyyy-MM-dd，传则返回该日及前后最近有活动的日期） | 进行中 / 往期 / 未来活动列表、用户订阅状态 |
| `query-survey-coupon` | 按订单号查 CSAT 满意度答卷与关联奖券 | `orderId: string*`（≤64 位，字母数字下划线连字符） | 满意度描述、奖券标题、核销时间、核销状态、点餐方式 |
| `now-time-info` | 取服务器当前时间（用于日期类查询锚点） | 无 | 毫秒时间戳、格式化日期时间、年/月/日、时区、UTC 时间 |

## 四、积分商城与派对活动（11）

| 工具 | 作用 | 参数（名称: 类型） | 返回字段 |
|---|---|---|---|
| `query-my-account` | 查积分账户（余额 / 过期积分） | 无 | 积分余额、过期积分等账户信息 |
| `mall-points-products` | 查可兑换商品/券/派对列表（支持类目筛选） | `catRuleIds: string`（逗号分隔：1>4 商品券、2 实物、2>8 周边、2>9 礼品卡、1>6>20 生日派对、1>6>21 主题派对、1>6>22 体验营、1>6>25 品鉴会、1>6>34 读书会、1>6>40 积分兑换活动） | 商品列表（含 `spuId`、`skuId`、`partyType` 等下游所需字段） |
| `mall-product-detail` | 查商品详情与全部 SKU 规格 | `spuId: integer*` | SKU 规格列表（含 `shopId`、`skuId`、`spuCategory`、`partyType` 等） |
| `mall-create-order` | 积分兑换下单（仅 shopId=2；虚拟/实物商品） | `skuId: integer*`、`spuCategory: string*`（"1" 虚拟、"2" 实物）、`addressId: string`（spuCategory=2 必填）、`count: integer`（默认 1） | `orderId`、`coupons[]`、`couponId`、`orderItemId`、`couponCodes[]`、`receiveQuantity`、`orderItemStatus`（1 成功/0 失败）、`orderStatus`、`status`（1 全部成功/2 部分成功/0 失败） |
| `mall-order-list` | 查商城订单列表 | `lastId: number`、`size: integer`（默认 10，上限 10） | 未声明ᐟ（订单列表 + 分页） |
| `mall-order-detail` | 查商城订单详情 | `orderId: string*` | 未声明ᐟ |
| `query-party-city` | 查派对活动可预约城市 | `spuId: number*` | 城市列表（`code`、`latitude`、`longitude`） |
| `query-party-store` | 查城市下可举办活动的门店 | `code: string*`（城市 code）、`latitude: number`、`longitude: number`、`spuId: number` | 门店列表（含 `storeCode`） |
| `query-party-store-date` | 查门店可预约日期 | `spuId: number*`、`storeCode: string*` | 可预约日期列表（含 `dateStr`） |
| `query-party-store-session` | 查指定门店+日期的场次 | `spuId: number*`、`storeCode: string*`、`dateStr: string*` | 场次列表（`id`、`timeStart`、`timeEnd`、`leftNum`、`partyMin`、`partyMax`、`price`） |
| `party-order-create` | 派对/体验营/品鉴会/读书会下单（仅 shopId=5） | `partyType: integer*`（1 包场、2 拼团）、`spuId: number`、`skuId: number`、`code: string`（城市）、`storeCode: string`、`dateStr: string`、`id: number`（场次）、`timeStart: string`、`timeEnd: string`、`leftNum: integer`、`count: integer`、`partyTimeInfo: object{id,leftNum,partyMin,partyMax,price,timeStart,timeEnd}` | 未声明ᐟ（订单信息） |

## 五、积分抽奖（3）

| 工具 | 作用 | 参数（名称: 类型） | 返回字段 |
|---|---|---|---|
| `query-lottery-info` | 查抽奖活动信息、消耗规则、可用积分/次数（不执行抽奖） | 无 | `activityCode`、`activityName`、`activityStatusText`、`beginTime`、`endTime`、`drawPoint`、`drawTypeText`、`availableTimes`、`availablePoint`、`drawDecision`（`resourceEligible`、`nextConsumption`、`fallbackConsumption`）、`prizes[]`（`name`、`imageUrl`、`typeText`） |
| `draw-lottery` | 原子扣减次数/积分并抽奖一次 | 无 | `status{code, message}`、`win: boolean`、`prizes[]`（`name`、`imageUrl`、`typeText`、`validDateInfo`，未中奖为空数组） |
| `query-my-prizes` | 查本期及历史中奖奖品 | `pageNum: string`（默认 1）、`pageSize: string`（默认 10，最大 50） | `prizes[]`（`id`、`name`、`imageUrl`、`prizeType`、`recordTime`、`status`、`statusText`、`timeRemindText`）、`pageNum`、`pageSize`、`hasMore`、`nextCursor`、`truncated` |

---

**标注说明**

- ᐟ **未声明**：该工具描述只写了用途和后续引导，没有逐项列出返回字段；真实响应是业务接口原始 JSON，以实际调用结果为准（不要按猜测定字段）。
- **beType / orderType 配对规则**（几乎所有交易类工具通用）：到店自取 `beType=1` → `orderType=1`，**不传 beCode**；得来速 `beType=5` → `orderType=1`，必传 beCode；麦乐送 `beType=2` → `orderType=2`，必传 beCode；团餐 `beType=6` → `orderType=2`，必传 beCode。到店自取场景传 beCode 会直接报错。
- **三条主链路**：点餐 = 门店查询 → `query-meals` → `query-meal-detail` → `calculate-price` → `create-order`；积分兑换 = `mall-points-products` → `mall-product-detail` → `mall-create-order`（shopId=2）或 `party-order-create`（shopId=5，需 city→store→date→session 逐级选）；抽奖 = `query-lottery-info` → 用户确认 `nextConsumption` → `draw-lottery`。
- 计价返回金额单位是**分**，展示时需除以 100。

---

## 👤 用户

给我做成一个文件

---

## 🤖 mcspeak

已整理成文档：**mcd-mcp-工具清单.md**（工作区根目录，约 14 KB）。

文件内容组织方式：

| 部分 | 内容 |
|---|---|
| 正文 | 35 个工具分成 5 组表格：门店、地址、餐品 9 个；计价与订单 5 个；优惠券与营销 7 个；积分商城与派对 11 个；积分抽奖 3 个；每条工具列出作用、参数类型及必填情况、返回字段 |
| 附录 A | beType 与 orderType 配对规则表，包括 beCode 是否传、预约时间何时传 |
| 附录 B | 三条主业务链路流程图：点餐下单、积分兑换、积分抽奖 |
| 附录 C | 7 条实现注意事项：分单位金额、必须调用 calculate-price、不要自行推断抽奖资格、两种券查询规则不同、派对流程要逐级选择等 |

文件带有可点击目录，`*` 表示参数必填；描述中未逐项列出返回字段的工具（共 8 个）已单独标注，请以真实调用响应为准。需要我再转换一版 HTML 或 Excel 方便放进文档或评审吗？

---

## 👤 用户

我们要开发一个 WorkBuddy Skill，名字叫 mcspeak（麦麦替你说），参加麦当劳程序员创意开发大赛和 WaytoAGI 1024 用餐赛道。它帮不会中文的外国人在中国麦当劳点餐：用他的母语推荐和修改订单，自动领券算最省，谨慎处理清真等饮食限制，最后生成双语柜台点餐卡，或者线上下单后生成双语取餐卡。

第一步只做数据探测。全程只读，不要调用 create-order、cancel-order、mall-create-order、party-order-create、draw-lottery。auto-bind-coupons 可以调用。

请新建项目目录 ~/mcspeak/，然后依次：
1. now-time-info 取当前时间。
2. query-nearby-stores：beType=1，searchType=2，city=济南市，keyword=山东大学中心校区。列出门店，选最近的一家。再用 searchType=1 查一次收藏门店，看返回什么。
3. query-meals：用这家门店，orderType=1，beType=1，不传 beCode。统计餐品数量和分类，记录字段结构。
4. 对以下餐品各调一次 query-meal-detail：一个鸡肉汉堡套餐、一个牛肉汉堡套餐、麦香鱼、一个含猪肉的餐品（如果有）、一个甜品。重点回答：返回里有没有配料、原料、过敏原相关字段？choices 和 modification 的结构是什么样？
5. list-nutrition-foods：看有哪些字段，能不能和 query-meals 的 productCode 对上，还是只能按名称匹配。
6. auto-bind-coupons，然后 query-store-coupons（同一门店，orderType=1，beType=1），列出每张券的 couponId、couponCode、名称、适用商品。
7. 选一个套餐调用 calculate-price 两次：一次不带券，一次带一张可用券（券挂在 items[].couponId / couponCode 上）。记录价格字段（单位分）和 takeWayList 的全部选项。
8. 把每一步的原始返回存到 ~/mcspeak/references/samples/，每步一个 json 文件。去掉手机号、地址等个人信息。
9. 最后用中文写一份探测报告：每个问题的结论，以及对后续开发的影响。特别回答三个问题：配料信息能不能支持清真和过敏过滤？券是不是按商品挂在 items 上？takeWayList 有哪些取餐方式、分别对应堂食还是外带？

---

## 🤖 mcspeak

探测完成，`~/mcspeak/` 已建好，9 步全部走通，未触碰任何下单/支付类工具。

## 三个必答问题

**① 配料信息能支持清真和过敏过滤吗？——不能，一条都不行。**
`query-meal-detail` 全字段核对过：没有 `ingredients`、没有 `allergen`、没有 `halal`、连辣度都没有。唯一接近“成分”的是 `modification.values[]` 里的**可去掉物料名**（吉士、生菜、酸黄瓜、洋葱粒、巨无霸酱、麦香鸡酱、麦香鱼酱），它只能做“减项”，不能证明“不含”。而且**猪柳蛋堡只有吉士能去，猪肉本体去不掉**。
→ mcspeak 必须换成“保守白名单 + 显式免责”，对外话术是 “No pork, please confirm”，绝不能出现 “halal / 不含麸质”。

**② 券是按商品挂在 items 上吗？——是。**
`items[i].couponId + couponCode` 成对传，服务端逐券强校验。实测挂了一张未生效的券 → 整单失败 `code:600012`「此卡券不在使用日期内」（中文口语，必须自带多语映射，且失败要能摘券重算）。另外 `query-store-coupons` 返回**空数组**，原因查出来了：领到的 3 张券有效期从 **10-26** 才开始，今天用不了。

**③ takeWayList 有哪些？对应堂食还是外带？——就两个，正是堂食 vs 外带。**

| code | title | 含义 |
|---|---|---|
| `eat-in` | 堂食 / 店内用餐 | 在店里吃 |
| `take-in-store` | 外带 / 店内自提 | 点了拿走 |

这就是外国游客最高频的 “here or to go?”，必须作为双语卡上的大字。

## 其他关键发现

- **菜单**：14 分类 / 99 条目 / **93 个商品**，两层结构（`categories[]` 只给 code+tags，名称价格在 `meals{code}`），价格是**元字符串**（`"37"`），计价接口是**分**（`3700`）——两套单位。
- **`selectedKey`/`unselectedKey` 是隐藏彩蛋**：`0-1`=保留、`0-0`=去掉；可乐冰量 4 个选项 **code 全是 `200002`**，只能靠 key 区分。这是 mcspeak 真正的壁垒——能把 “no pickles” 落到订单参数上，而不是只写在纸上。
- **营养表不可靠**：`data` 是**多行 CSV 字符串**不是数组，160 条里没有 productCode，只能按名匹配，**精确命中 18/93**（套餐全无）。
- 收藏门店（`searchType=1`）字段残缺：无营业时间、`distance` 恒 0；经纬度恒 `0.0`，不能做地图。

## 落盘

`references/samples/` 下 16 个 JSON（`04` 是全量菜单、`05`–`09` 是五个详情样本、`14`–`16` 是三次计价），全部通过 JSON 校验，无任何访客个人信息。

**下一轮建议补**：`create-order` 返回结构（取餐号/支付链接，取餐卡做不出来就卡在这）、特调是否真正落单、有效券的实际优惠金额、外送与得来速的 `takeWayList`。要我现在开始写 Skill 骨架（`SKILL.md` + 术语表 + 双语卡模板）吗？

---

## 👤 用户

探测报告很好。在写 Skill 之前，再做一次真实下单测试，补全剩下的未知字段。这次允许调用 create-order 和 query-order，但必须先把订单内容给我确认。

1. 用刚才那家门店，帮我组一单：一个鸡肉汉堡套餐，汉堡去掉一样配料（用 unselectedKey），饮料选去冰（用对应的 key）。取餐方式 take-in-store。
2. 调用 calculate-price，把完整的 items 参数（含 modification）和返回的价格给我看。
3. 等我回复"确认"之后，再调用 create-order。
4. 把 create-order 的完整原始返回存到 references/samples/17-create-order.json，告诉我：订单号、取餐码、支付链接分别在哪个字段，支付页是什么形式，有没有写付款时限。
5. 我付款后会告诉你"已付款"。之后每次我说"查一下"，你就调用 query-order，把返回存成 18-query-order-1.json、18-query-order-2.json……，并告诉我这次的状态字段和状态文字是什么。
6. 我取到餐后，你整理一份补充报告：create-order 和 query-order 的字段结构、出现过的所有状态文字及先后顺序、付款时限、定制项是否真的出现在订单里。

---

## 🤖 mcspeak

先按你的要求组装订单，并用 `calculate-price` 校验参数。这一步只计算价格，不会下单。

---

## 🤖 mcspeak

订单已组装好，也用 `calculate-price` 校验通过；**尚未下单**，等待你确认。

## 订单内容

**门店**：3350020 麦当劳济南山大路(成大高科)餐厅
**取餐方式**：`take-in-store`（外带 / 店内自提）
**商品**：麦辣鸡腿汉堡三件套 × 1

| 组成 | 内容 | 定制 |
|---|---|---|
| 汉堡 | 麦辣鸡腿汉堡 `1440` | **去掉切块生菜**（`unselectedKey=0-0`），保留麦香鸡酱（`0-1`） |
| 小食 | 中薯条 `4810` | — |
| 饮料 | 可乐中杯 `3050` | **去冰**（key `0-0`） |

## items 完整参数

```json
[
  {
    "productCode": "9900005456",
    "quantity": 1,
    "roundList": [
      {
        "round": "1",
        "comboItemList": [{
          "code": "1440",
          "quantity": 1,
          "modification": { "values": [
            { "code": "100136", "key": "0-1", "quantity": 1 },
            { "code": "120512", "key": "0-0", "quantity": 1 }
          ]}
        }]
      },
      { "round": "2", "comboItemList": [{ "code": "4810", "quantity": 1 }] },
      {
        "round": "3",
        "comboItemList": [{
          "code": "3050",
          "quantity": 1,
          "modification": { "values": [{ "code": "200002", "key": "0-0", "quantity": 1 }] }
        }]
      }
    ]
  }
]
```

## 计价结果（实测）

| 字段 | 值（分） | 换算 |
|---|---|---|
| `productOriginalPrice` | 3350 | ¥33.50 |
| `productPrice` | 3350 | ¥33.50 |
| `originalPrice` | 3350 | ¥33.50 |
| `discount` | 0 | ¥0.00 |
| **`price`** | **3350** | **¥33.50** |

`takeWayList`：`eat-in`（堂食·店内用餐）、`take-in-store`（外带·店内自提）—— 本单取第二项。

## 两个提醒

1. **特调在计价环节不体现**：两处改动加价都是 0 元，所以 `price` 与不带特调时一样，都是 3350，**不能靠价格判断特调是否生效**。这一点只有等 `create-order` 成功、再看 `query-order` 是否回显「去生菜/去冰」才能确认，而这正是本次要补的未知字段。
2. **下单会产生真实订单和支付链接**，金额 ¥33.50，下单后需要在支付页完成付款（时限要等返回后确认）。

回复「**确认**」我就调用 `create-order`，并把完整原始返回存成 `references/samples/17-create-order.json`。

---

## 👤 用户

有哪些喝的？

---

## 🤖 mcspeak

本店饮品分两类：可单点，也可作为套餐内的饮料选项（可选饮料有不同差价）。数据取自刚拉取的菜单（`04-query-meals`）。

## 一、套餐内可选饮料（16 种，差价按中杯可乐 ¥0 计）

| 中文名 | English | 差价 | 冰量可选 |
|---|---|---|---|
| 可乐中杯 `3050` | Coca-Cola (M) | +¥0 | ✅ |
| 无糖可口可乐中杯 `3071` | Coca-Cola Zero (M) | +¥0 | ✅ |
| 阳光柠檬红茶中杯 `515281` | Lemon Iced Tea (M) | +¥0 | ✅ |
| 可乐大杯 `3100` | Coca-Cola (L) | +¥2 | ✅ |
| 无糖可口可乐大杯 `3111` | Coca-Cola Zero (L) | +¥2 | ✅ |
| 阳光柠檬红茶大杯 `515282` | Lemon Iced Tea (L) | +¥2 | ✅ |
| 中杯怡泉+C `515520` | Schweppes Lemon (M) | +¥1.5 | ✅ |
| 大杯怡泉+C `515521` | Schweppes Lemon (L) | +¥3.5 | ✅ |
| 大杯鲜萃咖啡 `520688` | Fresh Brewed Coffee (L) | +¥1.5 | — |
| 锡兰红茶 `3505` | Ceylon Black Tea | +¥1.5 | — |
| 100%苹果汁 `6362` | 100% Apple Juice | +¥2 | — |
| 【美汁源】“黄金橙橙” `2430` | Minute Maid Orange | +¥3 | ✅ |
| 麦咖啡™冰美式中杯 `507411` | McCafé Iced Americano | +¥9 | ✅ |
| 麦咖啡™热美式中杯 `507368` | McCafé Hot Americano | +¥9 | — |
| 麦咖啡™冰奶铁中杯 `507409` | McCafé Iced Latte | +¥11 | ✅ |
| 麦咖啡™热奶铁中杯 `507328` | McCafé Hot Latte | +¥11 | — |

> 冰量四档：标准 `0-1` / 去冰 `0-0` / 多冰 `0-2` / 少冰 `1-1`（四个选项 `code` 全是 `200002`，只能靠 key 区分）。

## 二、单点饮品（8 种）

| 中文名 | English | 价格 |
|---|---|---|
| 可乐 `9900008751` | Coca-Cola | ¥9.5 |
| 阳光柠檬红茶 `515280` | Lemon Iced Tea | ¥9.5 |
| 鲜萃咖啡 `520689` | Fresh Brewed Coffee | ¥9.5 |
| 怡泉+C `515520` | Schweppes Lemon | ¥11.5 |
| 锡兰红茶 `3505` | Ceylon Black Tea | ¥11.5 |
| 100%苹果汁(盒装) `6362` | 100% Apple Juice | ¥12 |
| 阳光橙麦炫酷 `6352` | Orange McFloat | ¥12.5 |
| 【美汁源】“黄金橙橙” `2430` | Minute Maid Orange | ¥13 |

## 三、麦咖啡™（10 种，单独分类）

| 中文名 | English | 价格 |
|---|---|---|
| 麦咖啡™美式 `507411` | McCafé Americano | ¥11.9（原价 ¥19） |
| 麦咖啡™奶铁 `507409` | McCafé Latte | ¥13.9（原价 ¥21） |
| 燕麦奶铁 `510479` | Oat Latte | ¥9.9（原价 ¥23，需随单购麦金卡） |
| 浓缩咖啡 `507389` | Espresso | ¥15 |
| 咖啡阿芙佳朵 `514851` | Coffee Affogato | ¥15 |
| 卡布奇诺 `507387` | Cappuccino | ¥21 |
| 奶铁雪冰 `520361` | Latte Frappé | ¥23 |
| 牛奶 `507394` | Milk | ¥19 |
| 燕麦奶 `510488` | Oat Milk | ¥21 |
| 鲜萃咖啡 `520689` | Fresh Brewed Coffee | ¥9.5 |

两点说明：

1. **英文名是我按麦当劳通用叫法给的，待官方核对** —— 这正是探测报告里列的缺口之一（`中→英` 官方名词典），正式写进 Skill 前需要人工校准。
2. 若访客有乳糖不耐，`燕麦奶`、`燕麦奶铁`、`怡泉+C`、`可乐` 是相对安全的选择，但**共用设备无法保证**（呼应探测结论：接口没有过敏原数据，不能背书）。

---

当前订单仍在等你确认：**麦辣鸡腿汉堡三件套 ¥33.50**，汉堡去生菜、饮料可乐中杯去冰、取餐方式外带。如果你想换饮料（比如换成无糖可乐或柠檬红茶），说一声，我会重新计算价格再下单。

---

## 👤 用户

我刚吃完晚饭，不真实付款。改成：创建订单但不付款，看完返回结构后取消。允许调用 create-order、query-order、order-list、cancel-order，但 create-order 和 cancel-order 都必须先给我确认。

1. 用刚才那家门店组一单：一个鸡肉汉堡套餐，汉堡去掉一样配料（用 unselectedKey），饮料去冰（用对应的 key），取餐方式 take-in-store。
2. 调用 calculate-price，把完整的 items 参数（含 modification）和返回价格给我看。
3. 等我回复"确认下单"后调用 create-order。我不会付款。
4. 把 create-order 的完整原始返回存到 references/samples/17-create-order.json，告诉我：订单号、取餐码、支付链接分别在哪个字段；打开支付链接是什么形式；有没有写付款时限。
5. 马上调用一次 query-order，存成 18-query-order-unpaid.json，告诉我未支付时的状态字段和文字，以及订单详情里定制项（去掉的配料、去冰）有没有出现。
6. 等我回复"取消"后，调用 cancel-order（cancelReasonCode=1）。再调用一次 query-order，存成 19-query-order-cancelled.json，告诉我取消后的状态文字。
7. 调用 order-list 看我的历史订单。如果有已完成的订单，挑一单调用 query-order，存成 20-query-order-completed.json，告诉我已完成订单的状态文字和字段。不要取消或修改任何历史订单。
8. 整理一份补充报告：create-order 和 query-order 的字段结构；所有看到的状态文字；付款时限；定制项是否真的进了订单；还缺哪些状态没测到。

---

## 🤖 mcspeak

价格已重新核算（traceId 与上次不同，金额一致）。**尚未下单**，等你确认。

## 将提交给 `create-order` 的完整参数

```json
{
  "storeCode": "3350020",
  "orderType": 1,
  "beType": 1,
  "takeWayCode": "take-in-store",
  "items": [
    {
      "productCode": "9900005456",
      "quantity": 1,
      "roundList": [
        {
          "round": "1",
          "comboItemList": [{
            "code": "1440",
            "quantity": 1,
            "modification": { "values": [
              { "code": "100136", "key": "0-1", "quantity": 1 },
              { "code": "120512", "key": "0-0", "quantity": 1 }
            ]}
          }]
        },
        { "round": "2", "comboItemList": [{ "code": "4810", "quantity": 1 }] },
        {
          "round": "3",
          "comboItemList": [{
            "code": "3050",
            "quantity": 1,
            "modification": { "values": [{ "code": "200002", "key": "0-0", "quantity": 1 }] }
          }]
        }
      ]
    }
  ]
}
```

不传 `beCode`（到店自取）、不传 `addressId`、不传 `couponId`、不传 `reservationDate`。

## 计价结果

| 字段 | 分 | 元 |
|---|---|---|
| `productOriginalPrice` | 3350 | ¥33.50 |
| `productPrice` | 3350 | ¥33.50 |
| `originalPrice` | 3350 | ¥33.50 |
| `discount` | 0 | ¥0.00 |
| **`price`** | **3350** | **¥33.50** |

`takeWayList` → 取 `take-in-store`（外带·店内自提）。

## 确认前请知悉

- 本单**只创建、不付款**：创建后会立刻 `query-order`（存 `18-query-order-unpaid.json`），拿到未支付状态后就停住，等你回「**取消**」再调 `cancel-order`。
- 未支付订单通常有超时自动关闭机制，我会在返回里重点找**付款时限**字段；如果这期间订单被系统自动取消，取消那一步可能报「状态不允许取消」，我会如实记录，不会反复试。
- 这一单会在你的账号里留下一条**已取消**的历史订单，这是预期内的副作用。

回复「**确认下单**」，我立刻创建。

---

## 👤 用户

先别下单，核对一件事：饮料 3050 的 modification 里 200002 用的 key 是 "0-0"。冰量有多个选项且 code 相同，请从 query-meal-detail 的原始返回里，把 200002 的所有 key 和对应的中文名称（正常冰、少冰、去冰等）全部列出来，确认 "0-0" 确实是去冰。如果不是，换成去冰对应的 key，重新 calculate-price 后再给我看。

确认无误后直接 create-order，我这里视为"确认下单"。然后按原计划：存 17-create-order.json，告诉我订单号、取餐码、支付链接的字段位置和付款时限；马上 query-order 存 18-query-order-unpaid.json，并检查订单详情里去掉的配料和去冰是否真的出现了。做完停下等我。

---

## 🤖 mcspeak

核对完成：`"0-0"` 就是 **去冰**，参数原本就是对的，不用重算。原始返回里四个 key 如下（两种套餐完全一致）：

| code | 名称 | selectedKey | 默认选中 |
|---|---|---|---|
| 200002 | 标准 | `0-1` | ✅ |
| 200002 | **去冰** | **`0-0`** | — |
| 200002 | 多冰 | `0-2` | — |
| 200002 | 少冰 | `1-1` | — |

⚠️ 这里有个**关键陷阱**：`0-0` 在两种特调组里含义相反。
- **开关组**（有 `unselectedKey`，如吉士/生菜）：`0-0` = **去掉**；
- **单选组**（冰量，无 `unselectedKey`，min=1/max=1）：`0-0` = **去冰这个选项**。

不能按字符串字面量统一处理，必须按"组类型"判断。这一点会写进报告。

现在按你的授权下单。

---

## 🤖 mcspeak

下单成功，`query-order` 也已查过。**已停在这里，等你「取消」**（订单会在 19:13:45 自动过期）。

## 一、三个字段的位置

| 要找的 | 字段路径 | 值 |
|---|---|---|
| **订单号** | `data.orderId`（同时冗余在 `data.orderDetail.orderId`） | `1030000000000000000000000001` |
| **取餐码** | `data.orderDetail.pickupCode` | **空字符串 `""`** ⚠️ |
| **支付链接** | `data.payH5Url` | `https://m.mcd.cn/mcp/scanToPay?orderId=REDACTED` |
| 支付单号 | `data.payId` = `data.orderDetail.payId` | `1030000000000000000000000001` |

**取餐码是空的。** 只有 `pickupCode` 这一个字段承载取餐码，未支付时为空串 —— 也就是说**双语取餐卡在付款前做不出来**，这是对 mcspeak 最关键的一条。另有两个字段 `lockerCode`（取餐柜密码）、`lockerQrCode`（取餐柜二维码）本单未返回，推测只在"送餐柜"门店出现。

## 二、支付页是什么形式

`payH5Url` 是一个 **H5 扫码支付中间页**：`m.mcd.cn/mcp/scanToPay?orderId=...`，链接里只带 `orderId`、不带金额和签名，属于"跳转到麦当劳 H5 收银台"的入口。落地后应是微信/支付宝扫码页或调起麦当劳 App 支付 —— **落地页内容我无法在只读探测里打开验证**，这一条待补。工具描述的说法是"通过支付链接扫码，或者打开麦当劳 App 完成支付"。

## 三、付款时限：有，15 分钟

- `createTime` = `2026-10-24 18:58:45`
- `expirePayTime` = `2026-10-24 19:13:45`
- **差值正好 900 秒 = 15 分钟**，超时未支付大概率订单作废（是否自动取消、是否变"已取消"还是别的状态，要等 19:13 之后才知道，属于未测状态）。

## 四、定制项真的进订单了吗？——进了，而且是明文回显

`orderProductList[0].comboItemList`：

```json
[
  { "itemName": "麦辣鸡腿汉堡 切块生菜(不要)", "itemQuantity": 1 },
  { "itemName": "中薯条", "itemQuantity": 1 },
  { "itemName": "可乐中杯 冰(去冰)", "itemQuantity": 1 }
]
```

- 去掉配料 → `切块生菜(不要)`：**用 `unselectedKey=0-0` 成功了**，服务端把它渲染成「物料名(不要)」。
- 去冰 → `冰(去冰)`：`200002` + key `0-0` 也成功。
- 顺带一条：**`itemName` 是拼好的中文串，不是结构化字段**。mcspeak 想把"去生菜"翻成 "No lettuce"，只能对 `xxx(不要)`、`冰(去冰)` 这类**中文字符串做解析**，或者自己保留下单时的 items 参数来生成双语卡 —— 后者更可靠。

## 五、未支付状态

| 字段 | 值 |
|---|---|
| `orderStatus`（文字） | **待支付** |
| `status`（码） | **`"10"`** |

⚠️ 注意 `status="10"` 与工具文档写的"10=配餐中-餐厅确认配餐中"**对不上**，实际是 `10 ↔ 待支付`。文档枚举不可信，以实测为准。

## 六、另外两个坑（对开发有直接影响）

1. **金额单位在订单接口变成了「元」字符串**：`totalAmount: "33.5"`、`productPrice: "33.5"`、`totalDiscountAmount: "0"`。而 `calculate-price` 给的是**分整数** `3350`。同一个 ¥33.50，三个接口两种单位 → 必须做归一化，否则会显示成 ¥0.33 或 ¥3350。
2. **`create-order` 与 `query-order` 结构不同**：前者多一层 `orderDetail` 包裹并带 `payH5Url/payId`，后者是扁平结构且**没有支付链接**。同一份 UI 要能吃两种形状。

样本已存：`17-create-order.json`、`18-query-order-unpaid.json`（含请求参数与结构差异注记）。

回「**取消**」我就调 `cancel-order`（`cancelReasonCode=1`），再查一次存成 `19-query-order-cancelled.json`。

---

## 👤 用户

我看了 App 订单页：状态显示「待支付」，和 query-order 的 orderStatus 一致；页面提示「13分钟内未支付，订单将会被取消」；底部按钮是「取消订单」「联系客服」「去支付」；订单信息里有「就餐方式：外带」「预计取餐」「餐具需求：不需要餐具」「订单编码」。

这单先不要取消，让它 19:13 自动过期，测试超时未付款的情况。过期前，你先写参考文件。

【先把这些新结论记下来，写进 mcd_tools.md 和 order_status_map.md】
1. modification 的 key 必须按组类型解释：有 unselectedKey 的是开关组，0-0 表示去掉；没有 unselectedKey、min=1/max=1 的是单选组，每个 key 是一个选项，按选项名称匹配（冰量：0-1 标准、0-0 去冰、0-2 多冰、1-1 少冰）。
2. pickupCode 付款前是空字符串，付款成功后用 query-order 获取。
3. 支付链接只在 create-order 返回的 data.payH5Url 里，query-order 没有，创建后要保存。付款时限看 data.expirePayTime，实测为创建后 15 分钟；App 提示超时未支付订单会被取消。
4. 金额单位：calculate-price 返回分（整数），create-order 和 query-order 返回元（字符串），展示前统一换算。
5. 订单状态以 orderStatus 文字和 status 码的实测对应为准，工具文档的枚举不可信（实测 status=10 是待支付）。App 上显示的状态文字与 orderStatus 一致。
6. create-order 外层多一层 orderDetail，query-order 是平铺结构，两种都要能解析。
7. 双语卡片内容根据我们下单时的参数和 menu_tags.md 生成，不解析 itemName；itemName 只用来核对定制是否生效（是否出现"(不要)""(去冰)"）。
8. 在 order_status_map.md 里加一张「麦当劳 App 界面词汇对照表」：去支付、取消订单、联系客服、待支付、就餐方式、堂食、外带、预计取餐、餐具需求、订单编码、商品小计、合计，以及各个订单状态。每个词写中文原文、含义、用户看到它该做什么。取餐卡上要放这张表的精简版，让外国人能对照看懂自己的 App 订单页。

【然后在 ~/mcspeak/references/ 下写 6 个参考文件】

1. mcd_tools.md：只保留本 Skill 用到的工具：now-time-info、query-nearby-stores、query-meals、query-meal-detail、list-nutrition-foods、available-coupons、auto-bind-coupons、query-my-coupons、query-store-coupons、calculate-price、create-order、query-order、cancel-order。写清参数，以及：到店自取 beType=1、orderType=1、不传 beCode；takeWayCode 只取 eat-in（堂食）或 take-in-store（外带）；券挂在 items[i].couponId + couponCode 上，一张无效整单失败（如 600012 不在使用日期内），必须逐张尝试、失败就摘掉重算；收藏门店 searchType=1 没有营业时间和距离，只用来显示店名；remark 只支持外送。加上上面 8 条新结论，附真实返回字段示例和所有踩坑点。

2. menu_tags.md（最重要）：用 samples 里的全量菜单，对全部 93 个商品逐个标注成表格：官方中文名 | productCode | 拼音 | 英文名 | 肉类（鸡/牛/猪/鱼/虾/无肉/混合） | 是否含猪肉（含/不含/不确定） | 辣度 0-3 | 一句英文感官描述 | 可去掉的配料（来自 modification）。只依据名称、套餐组成和可去掉配料判断，看不出来的一律"不确定"；套餐里有一样含猪肉，整个套餐标"含"；带"麦辣""辣"字样的标辣度，不确定标 1 并注明。表头写明：这是按名称人工标注，不是官方配料信息，以实时菜单为准，表里没有的新品一律视为"不确定"。

3. diet_rules.md：开场说明（接口没有配料和过敏原信息；麦当劳中国没有提供清真认证；不含猪肉的餐品也可能共用设备；只能按名称判断）。清真三档：① 排除含猪肉和不确定的；② 再排除名称或酱料明显含酒精的；③ 只推荐无肉的鱼、素食、甜品、饮料、小食（同样排除不确定的）。含猪肉的餐品直接排除，不提供"去掉猪肉"。过敏不做"安全"判断，只排除名称明显相关的，并且一定给他一张问店员的中文卡："我对 XX 过敏，请问这个里面有 XX 吗？"。辣度用 menu_tags.md 的标注。禁止出现：清真、Halal、حلال 认证、适合穆斯林、safe for Muslims、不含麸质。绝不根据语言或国籍推测宗教和饮食，只能询问。

4. staff_phrases_zh.md：给店员看的固定中文模板，第一人称、温暖礼貌，每句配英文 key。包括：开场请帮忙点餐；不会用自助机和扫码点餐；餐品清单引导语；"如果方便的话……不行也没关系～"；不吃猪肉 / 不吃牛肉 / 吃素；"我对 XX 过敏，请问这个里面有 XX 吗？"；堂食 / 外带；微信 / 支付宝；参考价格以收银为准；手机订单取餐码；餐少了一样；这不是我点的；要纸巾 / 吸管 / 番茄酱；麻烦您把想说的话打在我手机上；谢谢。再列店员常问的问题及可选回答：请去自助机或扫码、堂食还是外带、要不要加大或加购、是会员吗或有券吗、怎么付款、还要别的吗、请稍等或等叫号、餐好了请取餐。

5. locale_style.md：通用规则（目标语言原生表达，不要翻译腔；正确礼貌等级；跟随用户语气；短句；感官描述食物；类比用通用事物；价格用 ¥，小数格式按语言习惯；从右往左的语言右对齐）。英、俄、日、韩、阿拉伯、法、西、德八种语言的风格表，以及每种语言在这些时刻的示范句：开场、领券（含"券过几天才生效"）、推荐、可替换项（"您也可以把它换成："）、修改完成、超预算、确认下单、付款指引（含"请在 HH:MM 前付款"）、订单已过期、制作中、请取餐、出错、结束祝福。再加一张"接口中文报错 → 各语言友好说法"对照表，至少覆盖券不在使用期、售罄、门店不可用、超时、订单过期。

6. order_status_map.md：订单状态中文 → status 码 → 含义 → 用户该做什么。用实测到的状态，"请取餐"那一行标为重点，没测到的标"待校正"。加上第 8 条的 App 界面词汇对照表。

【参考文件写完后】
- 19:14 之后调用 query-order 查这单，存成 19-query-order-expired.json，告诉我过期后的状态文字和 status 码，补进 order_status_map.md；
- 用 order-list 看我的历史订单，挑一单已完成的调用 query-order，存成 20-query-order-completed.json，补进对照表，不要修改任何历史订单；
- 最后给我一份补充报告：所有测到的状态、还缺哪些状态、6 个参考文件各写了什么。

---

## 🤖 mcspeak

现在开始写参考文件。先写 `mcd_tools.md`（工具手册 + 8 条新结论）。

---

## 🤖 mcspeak

现在写最重要的 `menu_tags.md`（93 个商品逐个标注）。

---

## 🤖 mcspeak

6 个参考文件已写完。订单 19:13:45 过期，等它过期后再查。

---

## 🤖 mcspeak

6 个参考文件写完了，订单也在 19:13:45 自然过期，过期后我查到了状态。

## 状态实测汇总（最终）

| `orderStatus` | `status` | 触发 |
|---|---|---|
| 待支付 | `10` | 创建后未付款（App 显示一致） |
| **订单已完成** | **`40`** | 已支付并完成（历史单） |
| **订单已取消** | **`60`** | **超时 15 分钟未付，系统自动关单** |

**两个重要发现**：

1. **没有“已过期”这个状态**。超时后直接是「订单已取消」+ `status=60`，App 上也不会显示“过期”。所以 mcspeak 不能说“订单已过期”，要说“超时未支付，订单已取消，未扣款”。
2. **状态码体系和工具文档完全不符**。文档写 `1/2/4/6/7/8/10`，实测是 `10/40/60`。**用文字做键、码只做辅助**。
3. 超时后 `totalAmount` 还是 `"33.5"`、`payId` 还在、`pickupCode` 还是空 → **不能靠金额或取餐码判断订单有效**，只能看 `orderStatus`。

另外从历史单拿到了取餐码实证：`pickupCode = "00000"`（5 位数字字符串），`takeWay = "堂食"`。还发现订单里能混进非餐品行（「麦金卡月卡（30天）」¥19，`comboItemList` 为空）。

## 定制项：确认落单

| 传的 | 订单回显 | 判定 |
|---|---|---|
| `120512` key=`0-0` | `麦辣鸡腿汉堡 切块生菜(不要)` | ✅ 开关组 `0-0`=去掉 |
| `200002` key=`0-0` | `可乐中杯 冰(去冰)` | ✅ 单选组 `0-0`=去冰 |

渲染规律：`{商品名} {组名}({选中项})`，去掉时固定是 `(不要)`。历史单里的 `冰(少冰)` 印证了冰量组统一渲染成 `冰(xx)`。所以**卡片文案必须用我们自己的入参生成**，`itemName` 只用来校验是否生效。

## 6 个参考文件

| 文件 | 内容 | 体量 |
|---|---|---|
| `mcd_tools.md` | 13 个工具的参数与返回 + **8 条硬结论** + 16 条踩坑速查 | 17 KB |
| `menu_tags.md` | **93 个商品逐个标注**（拼音/英文名/肉类/含猪/辣度/英文感官描述/可去配料）+ 4 张衍生清单 | 25 KB |
| `diet_rules.md` | 开场四条免责、清真三档、含猪肉直接排除、过敏只给问店员卡、禁用语表、伪代码决策树 | 9 KB |
| `staff_phrases_zh.md` | 店员中文模板 40+ 句（配 key + 英文）+ **店员常问 15 问及可选回答** + 卡片排版 | 10 KB |
| `locale_style.md` | 10 条通用规则、8 语言风格表、**8 语言 × 13 场景示范句**、5 类报错 × 8 语言 | 18 KB |
| `order_status_map.md` | 状态映射（10/40/60）、实测记录、**App 界面词汇对照表**、取餐卡 7 行精简版 | 8 KB |

样本新增 `17`（create-order）、`18`（未付）、`19`（超时取消）、`20`（已完成）、`21`（order-list），全部 JSON 校验通过。

## 还缺的状态

1. **请取餐 / 配餐中**（★ 最关键，取餐卡就靠它）—— 必须真实付一单才能测到
2. **用户主动取消**是否也是 `60`（本轮改成了自然过期，`cancel-order` 没跑）
3. 已评价、退款中/已退款、配送中

建议下一轮：拿最便宜的一单真付（`3505` 锡兰红茶 ¥11.5 或 `515837` 圆筒 ¥5），付款后 5 秒 / 1 分钟 / 3 分钟各查一次，就能一次补齐 1、2、3 三个中间态，并拿到真实取餐码。要现在做吗？

---

## 👤 用户

今晚先不真实付款，"配餐中 / 请取餐"两个状态明早实测后再补，现在按"待校正"处理。

现在写 ~/mcspeak/SKILL.md，这是整个 Skill 的核心。严格以 references/ 下 6 个参考文件和 samples/ 的实测结论为准。写完后逐条自查是否覆盖。

【frontmatter】
name: mcspeak
description: 帮不会中文的外国人在中国麦当劳点餐。当用户用任何非中文语言（英语、俄语、日语、韩语、阿拉伯语、法语等）提到麦当劳、点餐、想吃东西、柜台、取餐时触发；用户说 McSpeak 时也触发。用用户的母语推荐餐品、修改订单、自动用券，生成双语柜台点餐卡，或线上下单后生成双语取餐卡。

【核心原则】
1. 全程用用户的语言，按 references/locale_style.md 的风格说话。像一个耐心、会说他母语的店员朋友，不像系统。
2. 给店员看的中文只能用 references/staff_phrases_zh.md 的固定模板拼接，不现场生成中文句子。
3. 餐品中文名必须一字不改照抄 query-meals 返回的名称。
4. 价格以 calculate-price 为准；不同接口单位不同（calculate-price 是分，订单接口是元字符串），统一换算后再展示，不估算。
5. create-order 和 cancel-order 之前，必须用用户的语言复述，并得到明确确认。
6. 不向用户展示内部信息：storeCode、productCode、beType、key、工具名、报错原文。
7. 饮食限制按 references/diet_rules.md 和 menu_tags.md 执行；绝不根据语言或国籍推测宗教和饮食，只能询问。
8. 一次只问一件事；需要多个信息时合并成一条带编号的消息。每个问题给编号选项，用户回数字、yes、👍 都要能识别。
9. 耗时步骤前，先用一句话告诉用户正在做什么。

【流程】
S1 语言：从第一句话判断语言。不确定时（比如只发了 Hi 或 OK），用各语言的自称列出来让他选（English · Русский · 日本語 · 한국어 · العربية · Français …）。之后随用户切换。

S2 开场和领券：问候；静默调用 auto-bind-coupons，用一句话告诉他领到了几张券。

S3 门店：问他在哪家麦当劳，给两个选项。
1 知道店名 → 直接输入（中文、拼音、英文都可以），或从收藏门店里选（searchType=1，只用来显示店名）；模糊匹配后确认一次。
2 不确定 → 让他说附近的地标，转成中文关键词，用 searchType=2 搜索；列出最近 3 家，每家写中文店名、拼音、他的语言描述，请他对照店门口招牌确认。
确认后记住门店。检查这家店是否支持到店手机下单，不支持的话后面只提供柜台卡。

S4 需求和饮食：从第一句话里提取想吃什么、口味、预算、人数、饮食限制。缺的信息合并成一条消息问。用户提到清真、穆斯林、不吃猪肉时，先按 diet_rules.md 做诚实说明，再让他选档位。

S5 拉菜单：now-time-info 判断时段 → query-meals（beType=1，orderType=1，不传 beCode）→ 用 menu_tags.md 过滤（实时菜单里有、表里没有的商品视为"不确定"，饮食限制模式下不推荐）→ 对候选餐品调用 query-meal-detail，拿套餐组成和可定制项。菜单和券在本次对话内缓存。营养数据只在 list-nutrition-foods 能按名称匹配到时才回答，匹配不到就说"这个没有官方营养数据"。

S6 推荐：按格子组织订单：[1] 主食或套餐，[2] 套餐小食，[3] 套餐饮料（单点就按实际情况）。
每一格写：中文官方名 · 拼音 · 他的语言的名称，一句感官描述（来自 menu_tags.md），辣度 🌶️0～3，数量用阿拉伯数字 ×N，规格。
每一格下面写"您也可以把它换成："（用他的语言），列 2 个已经符合饮食限制和预算的选项，每个附一句和原选项的区别。
底部给两个价格：线上用最优券的价格（写明省了多少），柜台原价。账号里有 0 元券要主动提醒。
结尾邀请他修改，并用他的语言举一个修改的例子。

S7 修改循环：支持换某一格、加、删、改数量、改口味、重新推荐（更便宜、更辣等）、撤销上一步、重新开始（保留门店和饮食限制）。
每次修改：
- 检查饮食限制和预算，违反就直说并给替代；
- 定制按组类型处理：开关组（有 unselectedKey）用 selectedKey 保留、unselectedKey 去掉；单选组（无 unselectedKey，如冰量）按选项名称找对应 key。用户说 no ice、less ice、no lettuce 时，先在 query-meal-detail 里找到对应的组和选项再写入订单，并告诉他"已经写进订单了"；
- 官方不支持的请求，只能写进柜台卡的顾客请求，并告诉他线上订单加不了，如果很在意建议去柜台点；
- 含猪肉的餐品不提供"去掉猪肉"；
- 重新核价、重新算券；
- 重新显示完整订单，用 ✏️ 标出改动的地方和价格变化；
- 问他还要不要改。
记住他说过的偏好（比如不要冰），后面推荐时默认带上。

S8 算券：用 query-store-coupons 拿这家店可用的券。券挂在 items[i].couponId + couponCode 上，一张无效会让整单失败，所以逐张挂券试算，失败就摘掉那张重算；只对最可能最省的几个组合试算，选实付最低的。如果再加一样小东西就能满减，提示他但不替他加。券名翻译成他的语言。当天没有可用券时，如实说"你有 N 张券，X 月 X 日起可用，今天按原价"，绝不编造优惠。券只用于线上订单。

S9 选下单方式：用他的语言对比两个选项。
1 线上下单：价格、省多少、手机付款、不用和店员说话。
2 柜台点：原价，我给你做一张中文卡。
门店不支持手机下单时只给选项 2。

S10 线上下单：
- 先重新调用 calculate-price，核对可售和价格，有变化先告诉他；
- 问堂食还是外带，对应 takeWayList 的 eat-in / take-in-store；
- 用图标分行复述：📍门店 🍔餐品和定制 🍽️堂食/外带 💰实付和用券；
- 他明确确认后调用 create-order，保存 data.payH5Url 和 data.expirePayTime（query-order 里没有支付链接）；
- 给他支付链接，告诉他"请在 HH:MM 前付款"（来自 expirePayTime，约 15 分钟），按设备给指引（电脑上：用手机微信或支付宝扫屏幕上的码；手机上：长按识别，或截图后从相册识别）；
- 付款前不生成取餐卡；
- 他说付好了，调用 query-order，以 orderStatus 文字判断（不靠金额或码判断），确认已支付且 pickupCode 不为空，再生成取餐卡；
- 超过付款时限还没付：订单状态会变成"订单已取消"（status=60），用他的语言说"超时未付款，订单已自动取消，没有扣款"，问他要重新下单还是改去柜台点。不要说"订单已过期"。

S11 等餐：他问好了没有，调用 query-order，按 order_status_map.md 的实测对照翻译 orderStatus。教他认出 App 订单页上的"请取餐"和 App 界面词汇（去支付、就餐方式、预计取餐等）。餐好了就说：您的餐好了！去取餐台出示取餐码 XXXXX。

S12 柜台点餐：生成柜台卡之前，重新核对可售和价格。

S13 生成卡片：卡片内容根据我们下单时的参数和 menu_tags.md 生成，不解析 itemName（itemName 只用来核对定制是否生效）；订单里如果混有非餐品行（如麦金卡月卡），卡片上不列。用 scripts/render_card.py 按 templates/ 生成 HTML，文件名包含时间。同时在对话里贴一份纯文本版（中文部分 + 他的语言部分），方便截图。提醒他：调高屏幕亮度、横过来给店员看；如果是在电脑上生成的，通过微信文件传输助手发到手机。

S14 售后和结束：
- 取消订单：只在制作前可以，先确认，用对应的 cancelReasonCode；
- 餐少了或不对：给他对应的中文卡片句子；
- 结束时用他的语言祝用餐愉快；
- 问他要不要记住偏好，同意才写入 ~/mcspeak/data/profile.json，只存语言、饮食限制、常去门店、喜好，不存手机号、地址、取餐码、订单号；下次他说"和上次一样"就直接出方案；
- 问一句 👍/👎，同意才记录到 data/feedback.jsonl，不含个人信息。

【错误处理】每个错误都告诉用户下一步怎么办，接口中文报错按 locale_style.md 的对照表翻译：
售罄 → 给两个相似的替换；门店找不到 → 请他给附近的街道或建筑；工具没响应 → 重试一次，两次失败建议用柜台卡；券不在使用期 → 摘掉这张券重算并说明；付款超时 → 订单已自动取消、未扣款，可重下或改柜台；卡片显示有问题 → 给纯文本版。

【禁止】
不自动下单、不自动付款；不编造餐品和价格；不和其他品牌对比；不宣扬不健康的饮食方式；不调用 mall-create-order、party-order-create、draw-lottery。

写完 SKILL.md 后，告诉我：一共多少字、引用了哪些参考文件、有没有和参考文件冲突的地方。先不要写卡片模板，等我下一条指令。

---

## 🤖 mcspeak

`~/mcspeak/SKILL.md` 已写好。

## 字数

| 指标 | 数值 |
|---|---|
| 总字符（含空白） | **9,163** |
| 去空白 | 8,177 |
| **中文字数** | **3,579** |
| 行数 | 249 |
| 文件大小 | 17.8 KB |

结构：frontmatter（name + description 原样照用）→ 9 条核心原则 → S1–S14 → 错误处理（6 行表）→ 禁止（6 条）→ 速查表。

## 引用的参考文件

| 文件 | 在 SKILL.md 里的用途 |
|---|---|
| `mcd_tools.md` | 工具调用口径、8 条硬结论、速查表兜底 |
| `menu_tags.md` | S5 过滤、S6 英文名/感官描述/辣度、S7 组类型判断 |
| `diet_rules.md` | S4 诚实说明 + 档位、S7 猪肉不提供"去掉猪肉"、禁止词表 |
| `staff_phrases_zh.md` | 唯一的中文来源（原则 2）、S13 卡片、S14 售后句、过敏红框 |
| `locale_style.md` | 全部话术风格、价格格式、报错本地化（错误处理表） |
| `order_status_map.md` | S11 状态翻译、App 词汇、S10 超时措辞 |

工具覆盖：14 个全在（含 `available-coupons` / `query-my-coupons` / `order-list` 的数据源说明）。

## 和参考文件冲突的地方（3 处需要注意）

**① 「检查这家店是否支持到店手机下单」——接口里没有这个字段。**
`query-nearby-stores` 只给 `businessStatus`、营业时间、`reservation`，**没有任何"支持手机下单"的标志**。
处理方式：`businessStatus=false` 直接判关门；能否线上下单靠 `calculate-price` 试算探测，失败就降级只给柜台卡。这条是我按现有字段做的最优近似，**不是接口的真实能力判断**。

**② 「订单已过期」这个说法和 `order_status_map.md` 冲突。**
`locale_style.md` 里有「订单已过期」的示范句和报错行，但实测超时后状态是**「订单已取消」`status=60`**，App 上也没有"过期"这个词。
处理方式：SKILL.md 的 S10 统一写「超时未付款，订单已自动取消，没有扣款」，并明确标注 ⚠️ 不要说"订单已过期"。`locale_style.md` 里的句子保留作**语义模板**，渲染时措辞要替换。**建议明早顺手把 `locale_style.md` 那一行改掉**，否则以后容易有人照着写。

**③ 配餐中 / 请取餐 仍是「待校正」。**
SKILL.md S11 明确要求：遇到**未收录的状态文字**时照原意译 + 给保守建议（"还在准备，请在取餐台附近等"），**不编造精确含义**。明早实测后要回填 `order_status_map.md`，SKILL.md 那段可以不用改。

另外两处**有意收窄**（不算冲突，但要说清）：

- `mcd_tools.md` 说"逐张挂券试算"，SKILL.md S8 限定**只试最省的 2–3 个组合** —— 控制调用量，避免 5 张券 × 3 个套餐的爆炸。
- `menu_tags.md` 只有 5 个商品有 `modification` 数据，S7 要求"先在 detail 里找到对应组和选项"，对未探测的商品会找不到 → SKILL.md 已规定**找不到就按"官方不支持"处理，写进柜台卡并建议柜台点**。

## 待创建（你让我先别写）

`scripts/render_card.py`、`templates/`、`data/profile.json`、`data/feedback.jsonl` —— SKILL.md 里已经按这些路径写好调用约定，等你的卡片模板指令。

---

## 👤 用户

SKILL.md 很好。先做两处修正，再写卡片模板。

【修正】
1. 现在就修改 locale_style.md：把所有"订单已过期"相关的示范句和报错行，改成"超时未付款，订单已自动取消，没有扣款"的意思（8 种语言都改），并检查其他参考文件里有没有同样的说法。
2. 在 SKILL.md 的 S5 和 S7 里写清楚：可定制项一律以运行时实时调用 query-meal-detail 的结果为准；menu_tags.md 里的"可去掉的配料"只是参考，没有数据不代表不能定制。只有实时 detail 里找不到对应组和选项时，才按"官方不支持"处理。

【卡片模板】
在 ~/mcspeak/templates/ 写两个单文件 HTML 模板（CSS 和 JS 全部内联，不依赖网络，手机横屏竖屏都能看），再写 scripts/render_card.py，把订单 JSON 填进模板生成卡片。中文部分全部从 staff_phrases_zh.md 取，状态和 App 词汇从 order_status_map.md 取。

counter_card.html（柜台点餐卡，给线下柜台用）：
- 顶部大字中文区（给店员看）：开场语、不会用自助机和扫码点餐、餐品清单（官方中文名、规格、数量 ×N、套餐内选择、官方定制）、顾客请求（"如果方便的话……不行也没关系～"）、饮食提醒、堂食/外带、付款方式、参考价格以收银为准、生成时间（超过 30 分钟显示提示：请重新确认）。
- 🔊 朗读按钮：用 speechSynthesis，语言 zh-CN，语速 0.8，朗读中文区。
- 用户语言区：怎么使用这张卡、订单逐项对照（中文名 · 拼音 · 他的语言）、大约价格。
- 店员问答按钮：点开后全屏显示大字中文回答，下面附他的语言的意思。
- "请店员打字"按钮：全屏显示中文，请店员把想说的话打在他手机上；用他的语言提示他把店员打的字发回给 Skill 翻译。
- 过敏提问卡（如有过敏）："我对 XX 过敏，请问这个里面有 XX 吗？"
- 取餐指引（他的语言）：收好小票上的取餐号；看取餐台上方的叫号屏；认识"请取餐"三个字（加粗加图标，不只靠颜色区分）；把小票给店员看。
- 取餐问题按钮：餐少了一样、这不是我点的、要纸巾 / 吸管 / 番茄酱、谢谢。

pickup_card.html（线上取餐卡，付款成功后生成）：
- 超大取餐码（实测是 5 位数字），页面最醒目；
- 门店中文名 + 拼音；订单逐项（中文 + 他的语言）；实付金额、用的券、省了多少；堂食/外带；
- 订单状态对照表（精简版），"请取餐"放大、加粗、加图标；
- App 界面词汇对照（精简版）：去支付、取消订单、就餐方式、预计取餐、订单编码、合计；
- 取餐步骤（他的语言）：打开麦当劳 App 订单页 → 看到"请取餐" → 去取餐台出示这张卡；
- 给店员的中文："您好！我在手机上点好了，取餐码是 XXXXX，谢谢！"
- 取餐问题按钮，同柜台卡。

另外做一个 payment_notice（可以是 pickup_card 的"待付款"状态，也可以单独一个模板）：显示"请在 HH:MM 前付款"、支付步骤、付完回来告诉我；不显示取餐码。

通用要求：
- 字体栈覆盖中日韩、阿拉伯、西里尔、泰文；用户语言区按语言设置 lang 和 dir（阿拉伯语、希伯来语、波斯语、乌尔都语用 rtl），中文区始终 ltr；
- 高对比度、大字号，中文区字号要让店员隔着柜台能看清；
- 订单里的非餐品行（如麦金卡月卡）不显示；
- 如果本机有 playwright，再导出同名 PNG；没有就跳过并告诉我。

最后用 references/samples/ 的真实数据（就用刚才那单麦辣鸡腿汉堡三件套、去生菜、可乐去冰），生成三套示例到 ~/mcspeak/examples/：俄语、日语、阿拉伯语，每套包括柜台卡、待付款提示、取餐卡（取餐码用 00000 占位并标明是示例）。告诉我文件路径，我在手机上检查显示效果。

---

## 🤖 mcspeak

两处修正已完成，模板和示例也好了。有一个环境问题需要说明。

## 手机直接看：给链接

**https://0d0ffec624c940bc91b8ef16a1ddbdf3.app.workbuddy.host**

首页有三个语言的入口，点进去就是卡片。手机上建议横屏、把亮度调到最高。

## 修正 1：locale_style.md 的“订单已过期”已全部改写

8 种语言全部改完，语义统一为“超时未付款 → 自动取消 → 未扣款”：

| 语言 | 改后（节选） |
|---|---|
| en | The payment window passed, so the order was cancelled automatically. Nothing was charged — shall I start a new one? |
| ru | Время на оплату истекло, и заказ отменён автоматически. Деньги не списаны — создать новый? |
| ja | お支払いの時間が過ぎたため、ご注文は自動でキャンセルされました。料金は発生していません。新しく作り直しますか？ |
| ko | 결제 시간이 지나서 주문이 자동으로 취소됐어요. 결제는 안 됐어요. 새로 주문할까요? |
| ar | انتهى وقت الدفع، فأُلغي الطلب تلقائيًا. لم يُخصم أي مبلغ — هل أبدأ طلبًا جديدًا؟ |
| fr | Le délai de paiement est dépassé, la commande a donc été annulée automatiquement. Rien n'a été débité — j'en crée une nouvelle ? |
| es | Se acabó el plazo de pago, así que el pedido se canceló automáticamente. No se cobró nada. ¿Lo creo de nuevo? |
| de | Die Zahlungsfrist ist abgelaufen, daher wurde die Bestellung automatisch storniert. Es wurde nichts belastet. Soll ich eine neue anlegen? |

错误对照表里那一列也从“订单过期 / expired / caducó / abgelaufen”改成了“**订单已取消（超时未付款）**”，判定条件改为「含‘已取消’‘已关闭’，或 `expirePayTime` 已过」。
场景行标题也同步改写。其他参考文件（`order_status_map.md`、`ORDER-PROBE-REPORT.md`）里的“已过期”都只是**元说明**（“没有‘已过期’这个状态，别说它”），不需要改，我确认过。

## 修正 2：SKILL.md 明确“实时 detail 说了算”

- **S5 第 4 步**加了三条：可定制项一律以运行时 `query-meal-detail` 为准；`menu_tags.md` 只是参考快照，**表里没写 ≠ 不能定制，表里写了 ≠ 现在还能改**；只有实时 detail 找不到组/选项才按“官方不支持”处理。
- **S7 第 2 条**单列出来，并往下重排了编号：先查实时 detail 再答复，**不许拿标注表当答案**。

## 模板与脚本

| 文件 | 内容 |
|---|---|
| `templates/counter_card.html` | 中文大字区（开场/不会用自助机/餐品清单含套餐内容与定制/软性请求/饮食提醒/就餐方式/参考价/生成时间）+ 🔊 朗读（`speechSynthesis`, `zh-CN`, rate 0.8）+ 店员问答 / 请店员打字 / 取餐指引 / 取餐问题 四个全屏弹层 + 过敏红框置顶 + 30 分钟过期横幅 |
| `templates/pickup_card.html` | **一个模板两种状态**：没 `pickupCode` 时是待付款（🔒 + 大号 HH:MM + 支付步骤），有码时是取餐卡（`clamp(64px,20vw,132px)` 的取餐码 + 状态表“请取餐”高亮带图标 + App 词汇 + 取餐步骤 + 给店员的中文大句） |
| `scripts/render_card.py` | 解析 `staff_phrases_zh.md` 取中文（脚本里**不新写任何中文句子**）、解析 `order_status_map.md` 取状态与词汇、读 `samples/17` 真实订单；8 语 L10N；过滤非餐品行；`--type counter\|pickup\|payment`、`--pickup-code`、`--png` |

通用要求都落到了：单文件、CSS/JS 内联、离线可用、`clamp()` 横竖屏自适应、字体栈含 CJK/阿拉伯/西里尔/泰文；中文区恒 `lang="zh-CN" dir="ltr"`，用户语言区按语言设 `dir`（ar/he/fa/ur → rtl）。

## 示例生成结果（已校验）

```
ru/counter_card.html  23.4 KB   ru/payment_notice.html  23.6 KB   ru/pickup_card.html  23.6 KB
ja/counter_card.html  22.8 KB   ja/payment_notice.html  23.0 KB   ja/pickup_card.html  23.0 KB
ar/counter_card.html  23.0 KB   ar/payment_notice.html  23.3 KB   ar/pickup_card.html  23.3 KB
```

校验项：内嵌 JSON 全部可解析；`counter`/`payment` 的 `pickupCode` 为 `null`（不泄露取餐码）；仅 `pickup` 为 `00000` 且带 SAMPLE 标签；`ar` 全部 `dir="rtl"` 而中文块仍 `ltr`；问答 13 条、**无一条残留 `{占位符}`**；金额统一 `¥33.50`；订单里的“麦金卡月卡”类非餐品行已过滤。

## ⚠️ 一个必须告诉你的问题

**这个环境的沙箱禁止 python/bash/powershell 写入 `~/mcspeak/`**（`PermissionError` + `SANDBOX PERMISSION DENIED`），只有编辑器侧写法能落地。所以：

- 模板和脚本**在项目里**：`~/mcspeak/templates/`、`~/mcspeak/scripts/`
- 9 张示例卡**暂时生成在工作区**：`C:\Users\river lee\WorkBuddy\2026-10-24-17-09-12\_mcspeak_examples\`（已作为附件发给你，也已部署成上面那个链接）
- `~/mcspeak/examples/README.md` 我写了，里面给了两条命令补齐

你随手跑一条就能进项目：

```bash
mkdir -p ~/mcspeak/examples && cp -r "/c/Users/river lee/WorkBuddy/2026-10-24-17-09-12/_mcspeak_examples/." ~/mcspeak/examples/
```

或者你告诉我一声“允许写入家目录”，我再试一次直接生成过去。

另外：**本机没装 playwright**，所以没有导出 PNG（脚本支持 `--png`，装好后直接可用）。

---

## 👤 用户

有两件事要处理：一是你给的预览链接（xxx.app.workbuddy.host）在手机和电脑上都打不开；二是卡片排版要重做。先处理链接，再重做卡片。

【一、链接打不开的问题】
1. 先排查原因：预览服务有没有在运行、链接是否过期、是否需要登录、是否只能在 WorkBuddy 内部打开、文件路径是否正确。用你自己的工具实际访问一次这个链接，把返回结果告诉我。
2. 修好后，重新部署并自己先验证能访问，再把链接给我。
3. 如果在线预览确实做不到，就准备一个备用方案并实际测通：在 ~/mcspeak/examples/ 启动一个本地静态服务（比如 python -m http.server 8000），查出这台电脑的局域网 IP，给我 http://局域网IP:8000/ 形式的地址，让同一 Wi-Fi 下的手机能打开。告诉我怎么启动、怎么关闭，以及 Windows 防火墙要不要放行。
4. 把最终可用的方式写进 SKILL.md 的 S13：Skill 运行时生成卡片后，用哪种方式让用户在手机上打开（优先可用的在线链接，其次局域网地址，最后才是通过微信文件传输助手发 HTML 文件，同时在对话里贴纯文本版）。

【二、卡片重做】
卡片排版有一个根本问题：中文一块、外语一块，店员和外国人看的是不同位置，没法把同一件事对应起来。比如店员说"支付"，外国人不知道是他语言里的哪个按钮。请按下面的要求重做三个模板。

核心规则：一件事一个格子，双语在同一个格子里
1. 卡片上每一条信息（每个餐品、每个定制、就餐方式、付款方式、价格、取餐码、每个按钮、每条 App 词汇）都是一个独立的块，块里中文在上（大字，给店员），用户语言紧接在下（中号，给顾客）。不允许再出现"中文区"和"外语区"分开的布局。
2. 共同锚点：餐品用 ①②③ 编号；动作用固定图标（🍽️堂食、🛍️外带、💳付款、🎫取餐码、🔊朗读），同一个图标在中文和外语里含义一致。
3. 所有按钮都是双语标签，例如"去支付 · Pay now"。给店员点的按钮也必须有中文。
4. App 词汇要模仿 App 按钮的样子：去支付做成黄色实心胶囊按钮，取消订单和联系客服做成白底黑边胶囊按钮，并用用户语言写出位置（比如"右下角黄色按钮"）。参考麦当劳 App 订单页的实际布局：顶部大字状态，底部三个按钮从左到右是 取消订单 / 联系客服 / 去支付。
5. 横屏时用 CSS grid 做两栏：左栏中文、右栏用户语言，每一行严格对齐；竖屏时就是上下配对块。阿拉伯语等 rtl 语言只在右栏内部 rtl，行依然对齐。
6. 🔊 朗读时，正在读的那一块高亮，用户能看到店员现在听到的是哪一句。

新增：双向对话板
柜台卡底部做一个对话板，分两组：
- "店员想问顾客"：一排中文问题按钮（附用户语言），从 staff_phrases_zh.md 的店员常问问题里取，店员自己点。点了以后全屏显示：用户语言大字的问题 + 中文小字原文 + 下面一排双语回答按钮。
- "顾客想说"：一排双语按钮（要纸巾、要番茄酱、餐少了一样、这不是我点的、谢谢……），顾客点了以后全屏显示中文大字给店员看，下面附用户语言小字。
每个全屏页都有双语的"返回 · Back"按钮。

修 bug
1. 价格里出现了 **¥33.50** 这种 markdown 星号。模板里所有文本都要渲染成 HTML，不允许出现 markdown 符号。
2. 没有非官方请求时，"如果方便的话……"这个块不要出现；有请求时，这个句式后面必须跟具体请求内容。
3. 定制只显示一次，用自然的中文说法，从我们下单的参数生成，例如"不要切块生菜""可乐去冰"，每条都配用户语言。不要用 App 的"冰(去冰)"格式，也不要重复列两遍。
4. 每张卡顶部用两种语言各写一句用法说明：中文给店员（例如"您好，这是我要点的餐，请看每一格的中文"），用户语言给顾客（"把屏幕给店员看，店员指哪一格，你就看哪一格"）。检查日语等各语言的说明是否通顺准确，日语柜台卡现在那句"英語がわからなくても読めます"意思不对，要改。

文件位置
现在已经是完全访问权限，把模板、脚本和示例全部写回 ~/mcspeak/ 对应目录，不要再放在工作区临时目录。也试一下能不能装上 playwright 导出 PNG，装不上就跳过并告诉我原因。

【三、验收】
重新生成俄语、日语、阿拉伯语三套示例（柜台卡、待付款卡、取餐卡），用第一部分修好的方式给我手机能打开的地址，并确认你自己访问过、能打开。然后逐张检查并回答：
- 是否还有任何一条信息只有一种语言？
- 横屏时两栏的每一行是否对齐？
- 阿拉伯语栏是否 rtl 且行仍对齐？
- 是否还有 markdown 符号、空的请求块、重复的定制？
- 每个按钮是否都有双语标签？

---

## 🤖 mcspeak

Tool TaskOutput not found in agent cli.

---

## 🤖 mcspeak

两件事都处理完了。

## 一、链接打不开：原因已定位

我用 WebFetch 实际访问了那个地址，返回的是**应用级错误页**，不是 404、也不是要登录：

> **链接不完整** — 访问该应用需要完整的分享链接，当前地址缺少访问参数。
> 请向分享者索取完整的访问链接…可在 WorkBuddy 的应用详情页重新复制分享链接。

结论：`*.app.workbuddy.host` 这个裸域名**必须带分享参数**才能打开，而部署工具只回了裸域名 → 这个链接对外（手机/其它电脑）**不可用**，我不该直接给你。

### 改用的方案：局域网静态服务（已实测通过）

服务已在跑，10 个地址我逐个 curl 验证，全部 `HTTP 200` 且返回真实页面（15–21 KB）：

**http://10.17.214.169:8000/**

| 检查项 | 结果 |
|---|---|
| 服务在运行 | ✅ `python -m http.server 8000 --bind 0.0.0.0` |
| 本机 IP | `10.17.214.169`（网卡 `WLAN 2`，DHCP） |
| 本机访问 | ✅ `127.0.0.1:8000` = 200 |
| 局域网地址访问 | ✅ `10.17.214.169:8000` = 200（每张卡都单独测过） |
| 端口 | 8000 TCP |
| 防火墙 | ⚠️ Domain/Private/Public **三个配置全开**，且**没有** python/8000 的入站规则 |

启动 / 关闭 / 防火墙：

```bash
# 启动
cd ~/mcspeak/examples
python -m http.server 8000 --bind 0.0.0.0

# 关闭：在运行它的终端按 Ctrl+C
# 或另开终端强杀
powershell -c "Get-NetTCPConnection -LocalPort 8000 -State Listen | %{Stop-Process -Id \$_.OwningProcess -Force}"

# 防火墙（如果 Windows 弹窗就选“允许专用网络”；不弹窗且手机打不开，用管理员执行）
netsh advfirewall firewall add rule name="mcspeak 8000" dir=in action=allow protocol=TCP localport=8000
```

手机连**同一个 Wi-Fi** 就能开。如果还是打不开，基本是两种原因：**不在同一网段**或**路由器开了 AP 隔离** → 那就退回“微信文件传输助手发 HTML”。

## 二、SKILL.md S13 已写清三档

| 优先级 | 方式 | 关键约束 |
|---|---|---|
| 1 | 在线链接 | **必须自己实测能打开**（返回真实 HTML）才发给用户；裸 `*.app.workbuddy.host` 不算数 |
| 2 | 局域网地址 | 起 `http.server` + 查 WLAN IP + 提醒防火墙与 AP 隔离 |
| 3 | 发文件 | 微信文件传输助手 + **同时在对话里贴纯文本版**（这条任何情况都要给） |

顺带把“横屏自动两栏”和三个模板的生成命令也写进去了。

## 三、卡片重做

**根本结构改了**：不再有“中文区 / 外语区”，改成 **一件事一个格子**——`<div class="row">` 里中文在上（`clamp(21px,5.4vw,29px)`）、他的语言紧接在下（14–17px）。

| 要求 | 落地 |
|---|---|
| 横屏两栏严格对齐 | `.row` 本身是 grid，`@media (min-width:640px) and (orientation:landscape)` 时 `1fr 1fr` —— 两个单元格在**同一 grid 行**里，天然等高、顶端对齐，中文列右侧有分隔线 |
| 竖屏 | 同一 `.row` 退化成上下两块，配对关系不变 |
| RTL | `.row{direction:ltr}` 锁死列序，只让 `.loc[dir="rtl"]{text-align:right}` 生效 → 中文永远在左、外语在右，阿拉伯语只在右栏内右对齐 |
| 锚点 | 餐品 ①②③ 圆形编号（中英同号）；动作固定图标 🍽️堂食 / 🛍️外带 / 💳付款 / 🎫取餐码 / 🔊朗读 |
| 按钮 | 全部双语两行（`.bzh` + `.bloc`），包括朗读、对话板、全屏回答、返回 |
| App 拟态 | 顶部大字状态 + 底部三胶囊：`取消订单`（白底黑边）/ `联系客服`（白底黑边）/ `去支付`（**黄色实心**），每个胶囊带用户语言的位置提示（左/中/右） |
| 朗读高亮 | 逐格读，正在读的格子加 `.reading`（黄底+黄框）并自动 `scrollIntoView` |
| 双向对话板 | 「店员想问顾客」7 问（取自 `staff_phrases_zh.md` 店员常问表，含双语答案按钮）＋「顾客想说」5 句；全屏页都是“外语大字 + 中文小字”（或反过来）+「返回 · Back」 |

**四个 bug 全修**：

1. `**¥33.50**` → 生成端 `strip_md()` + 模板 `esc()` 双重清 markdown，现在是「参考价格 ¥33.50」。
2. 无请求时不再渲染“如果方便的话”块（本样例没有非官方请求，卡片上完全不出现）。
3. 定制由**下单参数**生成自然中文、只出现一次：`不要切块生菜` / `可乐去冰`，各配一句外语；彻底弃用 App 的 `冰(去冰)` 写法。
4. 顶部双语用法说明；日语改成了 **「画面を店員に見せてください。店員が指した枠を、あなたも見てください。」**（原句“英語がわからなくても読めます”确实文不对题）。

## 四、逐张验收（回答你的五个问题）

| 检查 | 结论 |
|---|---|
| **还有单语信息块吗？** | **没有**。餐品、定制、就餐方式、付款、价格、取餐码、每个按钮、App 词汇、状态行、分区标题、全屏页，全部 zh + 用户语言双行。唯一“只有中文”的是**给店员念的台词本身**（那是要他说的话），但下面一定有一行外语释义 |
| **横屏两栏每行对齐？** | 是。左右两格属于同一个 grid 行，`align-items:start` 顶端对齐，中文列带右分隔线；不是两张独立表格拼的，所以不会错位 |
| **阿拉伯语 rtl 且行仍对齐？** | 是。整卡 `dir="rtl"`，但 `.row` 强制 `direction:ltr` 保持“左中右外”，只有 `.loc` 内部 RTL 且右对齐 |
| **markdown / 空请求块 / 重复定制？** | 9 个文件全部 `star=False`；请求块不存在；“不要切块生菜”“可乐去冰”各 1 次，`dupCustom=False` |
| **每个按钮都双语？** | 是。`朗读 · 外语`、7 个店员问题、5 个顾客句、每个回答按钮、`返回 · Back`、付款页的 `付款 · Pay now` |

另外：三份模板的内联 JS 我全部用 `node --check` 过了语法；9 张卡内嵌 JSON 全部可解析；`counter`/`payment` 的 `pickupCode` 为空、只有 `pickup` 是 `00000`（不会提前泄露取餐码）。

## 五、文件位置（已写回项目）

```
~/mcspeak/
├── SKILL.md                        S13 已更新
├── templates/  counter_card.html · payment_notice.html · pickup_card.html
├── scripts/    render_card.py      （全新数据契约，en/ru/ja/ar）
└── examples/   index.html + ru/ ja/ ar/ 各 3 张 + README.md
```

## 六、playwright

- `pip install playwright` ✅ **装上了**
- `python -m playwright install chromium` ⏳ **内核还在下载**（100MB+，已跑约 2 分钟没结束），所以**这次还没导出 PNG**
- 装完直接 `python scripts/render_card.py --type counter --lang ru --out examples/ru/counter_card.html --demo --png` 就会出同名 PNG

要我继续等它下完、把 9 张 PNG 也导出来吗？还是先看手机上的效果？

---

## 👤 用户

先看手机效果，PNG 让 chromium 在后台继续下载，下完再补导出，不要阻塞后面的步骤。

现在做两件事：

【一、SKILL.md 小修改】
在 S10 线上下单的支付指引里，把"打开麦当劳 App 订单页，点右下角黄色的「去支付」按钮"作为首选支付方式（订单建在用户自己的账号上，App 里会立刻出现这一单），支付链接作为备用。待付款卡上也按这个顺序展示，并配上 App 按钮的拟态样式和位置说明。

【二、安装成 WorkBuddy Skill】
把 ~/mcspeak 完整复制到 ~/.workbuddy/skills/mcspeak/，然后自检：
1. 列出技能目录下的完整文件树，确认 SKILL.md、references/ 6 个文件、templates/ 3 个模板、scripts/render_card.py、samples/ 都在；
2. SKILL.md 里引用的每个文件路径在技能目录下是否都存在，路径写法是否需要改成相对于技能目录；
3. 在技能目录下用 samples 的真实订单跑一次 render_card.py，确认三种卡片都能生成；
4. 告诉我 WorkBuddy 是否已经识别到这个 Skill（技能列表里能不能看到 mcspeak），以及在新对话里怎么触发它。

---

## 🤖 mcspeak

两件事都完成了，chromium 在后台继续下载，没阻塞。

## 一、付款改成 App 优先

**SKILL.md S10 第 5 步**现在是：

> **首选 App**（订单建在他自己的账号上，App 里会立刻出现这一单，付款最快、还能直接看状态）：「打开**麦当劳 App → 我的订单 → 点右下角黄色的「去支付」**」
> **备用链接**：给 `payH5Url`，电脑上扫码 / 手机上长按识别
> 两种情况都要报「请在 **HH:MM** 前付款」（取自 `expirePayTime`，不硬编码 15 分钟）

**待付款卡**同步改了，App 块排在链接前面：

1. 大红框：**请在 19:13 前付款** + 巨号 `19:13` + 🔒「付款后才出取餐码」
2. **首选：在 App 里付款** —— App 拟态：顶部「待支付 · Ожидает оплаты」，底部三胶囊按真实布局从左到右 `取消订单`（白底黑边）/ `联系客服`（白底黑边）/ `去支付`（**黄色实心**），每个胶囊下面标位置「1-я слева / по центру / справа, жёлтая」，再跟一句红字「👆 点右下角黄色的「去支付」」
3. 两步步骤：App → 我的订单 → 点黄色按钮；付款后回来告诉我
4. **备用：支付链接**（次级按钮，不再是主按钮）

已重新生成 ru / ja / ar 三张，服务上能直接看：`http://10.17.214.169:8000/ru/payment_notice.html`

## 二、安装成 WorkBuddy Skill

**位置**：`C:\Users\river lee\.workbuddy\skills\mcspeak\` — 50 个文件 / 641 KB

### ① 文件树（全部到位）

```
SKILL.md                        22.2 KB
README.md
data/README.md                  运行时数据说明（profile.json / feedback.jsonl 首次写入时创建）
references/                     32 个
  ├─ mcd_tools.md · menu_tags.md · diet_rules.md
  ├─ staff_phrases_zh.md · locale_style.md · order_status_map.md     ← 6 个全在
  ├─ PROBE-REPORT.md · ORDER-PROBE-REPORT.md
  └─ samples/  (22 个 JSON + 3 个 md)   ← 01–16b、17–21 全在
templates/                      3 个：counter_card.html · payment_notice.html · pickup_card.html
scripts/render_card.py
examples/                       11 个：index + ru/ja/ar 各 3 张 + README
```

### ② 路径写法：已全部改成相对技能根目录

| 原来 | 现在 |
|---|---|
| `mcd_tools.md` 等 6 个裸文件名 | `references/xxx.md`（29 处，无双重前缀） |
| `counter_card.html` | `templates/counter_card.html` |
| `~/mcspeak/data/profile.json` | `data/profile.json` |
| `~/mcspeak/data/feedback.jsonl` | `data/feedback.jsonl` |

并在开头加了 **路径约定**：*所有相对路径相对技能根目录（`SKILL.md` 所在目录，通常是 `~/.workbuddy/skills/mcspeak/`）；调脚本、读写 `data/` 前先把技能根目录解析成绝对路径，不要假设 cwd 就是技能目录。*

自检结果：**13 条引用路径，11 条存在**；剩下 2 条是 `data/profile.json`、`data/feedback.jsonl` —— 这两个是**运行时才生成**的，`data/` 目录已随技能分发（含 README 说明），不是缺文件。

### ③ 在技能目录里实跑（不是在家目录）

```
cd ~/.workbuddy/skills/mcspeak
python scripts/render_card.py --type counter --lang ja --out _selftest/counter.html ...
```

三种卡片全部生成成功：`counter 17.0 KB / payment 14.2 KB / pickup 17.9 KB`，`kind` 正确，**counter 与 payment 的取餐码为空、只有 pickup 是 88888**。测完已删掉 `_selftest/`。

> 顺手记一个坑：给 `--out` 传 `/c/Users/...` 这种 Git-Bash 风格路径，Python 会解析成 `C:\c\Users\...`，**必须用相对路径或 Windows 绝对路径**。已写进记忆。

### ④ 是否被识别？——**已经识别到了**

我直接调用了一次 `Skill(mcspeak)`，**成功返回**：

```
Base directory for this skill: C:\Users\river lee\.workbuddy\skills\mcspeak
```

说明 WorkBuddy 已把 `~/.workbuddy/skills/` 下的目录当成技能，**无需重启，当前会话就能加载**（`~/.workbuddy/skills/` 原本是空的，mcspeak 是第一个）。

新对话里怎么触发（frontmatter 的 description 决定）：

- **语言触发**：用任何非中文语言提到麦当劳 / 点餐 / 想吃东西 / 柜台 / 取餐
  例：`I want a burger, I'm at McDonald's` / `Макдональдс рядом, помоги заказать` / `マクドナルドで注文したい`
- **显式触发**：直接说 `McSpeak` 或 `mcspeak`
- 也可以在技能列表里手动选中它

## 剩下的事

- chromium 还在后台下载（任务 `AMz9lK`）。下载完后执行 `python scripts/render_card.py ... --png` 就能出同名 PNG，我再补一轮导出。
- 手机效果你随时看：**http://10.17.214.169:8000/**（服务还在跑；要关就 `Ctrl+C`，或结束占用 8000 的 python 进程）

---

## 👤 用户

手机打不开局域网地址。我已经用管理员权限加了防火墙规则（放行 TCP 8000）。现在电脑和手机都连在同一个手机热点上，请：
1. 检查 8000 端口的 http.server 是否还在运行，没在就在 ~/mcspeak/examples 重新启动（--bind 0.0.0.0）；
2. 重新查当前 WLAN 的 IP（换了热点，IP 已经变了）；
3. 确认防火墙规则已生效；
4. 用新 IP 自己 curl 一次，确认返回 200，再把新地址给我。
另外，你之前说 workbuddy.host 链接需要"完整的分享链接，可在 WorkBuddy 的应用详情页重新复制"，告诉我这个应用详情页在 WorkBuddy 界面的哪里，我去复制完整分享链接试试。

---

## 🤖 mcspeak

原因找到了：**IP 变了**。换热点后，旧地址 `10.17.214.169` 已经不属于这台电脑。

## 手机请用这个地址

# http://192.168.43.187:8000/

## 四项检查结果

| # | 检查项 | 结果 |
|---|---|---|
| 1 | 8000 端口服务 | ✅ **还在运行**，不用重启。`0.0.0.0:8000` 正在监听，进程 PID 为 27480（今天 20:09:43 启动，就是 `python -m http.server`）。`--bind 0.0.0.0` 已生效，所以不只是本机能访问 |
| 2 | 当前 WLAN IP（即局域网 IP） | ✅ **`192.168.43.187`**，网卡为 `WLAN 2`，掩码 `/24`（`192.168.43.x`，典型安卓热点网段） |
| 3 | 防火墙规则 | ✅ 规则 **`mcspeak 8000`**：`Enabled=True`、`Action=Allow`、`Profile=Any`、`Port=8000`、`Proto=TCP`，即入站放行、任何网络类型都允许 |
| 4 | 新 IP 自测 | ✅ 全部 **HTTP 200**，并且返回的是真实 HTML：<br>`/` → 200<br>`/ru/payment_notice.html` → 200<br>`/ar/pickup_card.html` → 200 |

## 如果手机仍然打不开，按顺序检查这三项

1. **手机自己获得的 IP 是不是 `192.168.43.x`**。有些安卓机会给热点客户端分配 `192.168.43.x`，但手机连接的是另一张网卡，因此需要看手机的「当前 Wi-Fi → IP 地址」，确认前缀一致。如果不一致，说明手机其实没有连接到这个热点。
2. **热点是否启用了「客户端隔离」**。安卓「个人热点 → 高级」如果关闭了「允许其他设备访问」，就会出现电脑能自己访问、手机却连不上。关掉隔离即可。
3. **电脑是否真的监听在全部网卡地址上**。你可以在这台电脑上执行 `curl http://192.168.43.187:8000/`，如果能返回 HTML，就说明服务侧没问题；问题只剩网络路径。

另外提醒：这个 `http.server` 是前台进程的附属服务，**电脑休眠或终端关闭后会停止**。一旦打不开，先执行 `cd ~/mcspeak/examples && python -m http.server 8000 --bind 0.0.0.0`，再重新启动它。

## 关于「应用详情页」

我查了官方文档，也翻看了本地部署记录，情况如下。

**本地部署记录**：`~/.workbuddy/cloudstudio-deploy-history/…json` 里保存的 `shareLink` 也是裸域名，**没有 token**；`/index.html` 我也试了，同样返回「缺少访问参数」。因此这条链接无法靠改 URL 打开。

**我这次部署的链接来自 `workbuddy_cloudstudio_deploy` 工具，产出的是 CloudStudio 沙箱域名；它和官方文档说的「网站应用发布」并不是同一个入口**，后者才会生成带访问凭据、可以直接对外分享的链接——这也解释了为什么我拿到的链接缺少参数。

官方文档里真正能拿到可分享链接的入口是这两个：

| 入口 | 路径 | 说明 |
|---|---|---|
| **分享面板** | 对话里出现网站应用卡片 → **点卡片** → 在右侧预览区工具栏点 **「分享」** → 弹出 **「网站应用分享面板」** → 从中取链接 | 文档原文：「发布后，任何获得链接的人都可以访问应用」 |
| **全局应用管理** | **设置 → 数据管理 → 应用** | 「可以集中查看所有应用、**查看发布链接**，并管理云服务和发布状态」 |
| 口头发布 | 在对话里说 **「发布」/「上线」** | 等价于打开分享面板拿链接 |
| 更新、下线 | 已发布应用的分享面板里的 **「更新」/「下线」** | 更新后链接不变 |

**需要提醒你的是**：这个场景可能找不到入口。因为 `_mcspeak_examples` 只是我通过工具部署上去的静态目录，**没有经过 WorkBuddy 的「网站应用开发与发布」流程**，所以在「设置 → 数据管理 → 应用」里大概率看不到它，预览区也不会有它的卡片和「分享」按钮。

如果你确实想要一条能发到任意网络的链接，有两条可行路线：

1. **把卡片做成正式网站应用再发布**：建一个网站应用工程（把 `examples/` 当 dist），然后对话里说「发布」。这会出现卡片，「分享」按钮才有意义。要走这条我可以帮你搭。
2. **保持局域网**（现在这条），或者**用微信文件传输助手发 HTML**——手机本地打开最稳，不依赖网络。

你想走哪条？如果只是想先在手机上看效果，直接打开上面的 `http://192.168.43.187:8000/` 就行。

---

## 👤 用户

【新增：导航功能固化】
12. 刚才在阿拉伯语测试里，用户问"把餐厅位置发给我、怎么过去"，你临场生成了地图卡（高德链接、腾讯和谷歌地图、坐标、二维码、最近地铁站和公交站、给出租车司机看的中文地址），效果很好。请把它正式写进 SKILL.md，作为新的一步"S15 导航"：
- 用户问位置、怎么去、地图、打车时触发；
- 坐标来自门店查询的真实数据，高德链接优先，腾讯地图备选，谷歌地图注明国内可能偏移；
- 生成一张地图卡模板 templates/map_card.html，同样遵守"一件事一个格子、双语配对"；
- 给出租车司机看的那一块，用 staff_phrases_zh.md 的固定模板，加一句"师傅您好，麻烦送我到这里，谢谢！"，后面必须是门店查询返回的完整中文地址和店名，不能简写。
13. 刚才给司机看的地址写成了"山大路146号"，实际是"山大路146-6号（成大高科）一楼"。凡是给中国人看的地址、店名、餐品名，都必须照抄接口返回的原文，一个字都不能省。【新增：导航功能固化】
12. 刚才在阿拉伯语测试里，用户问"把餐厅位置发给我、怎么过去"，你临场生成了地图卡（高德链接、腾讯和谷歌地图、坐标、二维码、最近地铁站和公交站、给出租车司机看的中文地址），效果很好。请把它正式写进 SKILL.md，作为新的一步"S15 导航"：
- 用户问位置、怎么去、地图、打车时触发；
- 坐标来自门店查询的真实数据，高德链接优先，腾讯地图备选，谷歌地图注明国内可能偏移；
- 生成一张地图卡模板 templates/map_card.html，同样遵守"一件事一个格子、双语配对"；
- 给出租车司机看的那一块，用 staff_phrases_zh.md 的固定模板，加一句"师傅您好，麻烦送我到这里，谢谢！"，后面必须是门店查询返回的完整中文地址和店名，不能简写。
13. 刚才给司机看的地址写成了"山大路146号"，实际是"山大路146-6号（成大高科）一楼"。凡是给中国人看的地址、店名、餐品名，都必须照抄接口返回的原文，一个字都不能省。

---

## 🤖 mcspeak

S15 导航已定稿固化，地址缩写问题也一并按规则修掉了。

## 先给地址（注意 IP 又变了）

**http://10.17.214.169:8000/**

刚才的热点 IP 从 `192.168.43.187` 变回了 `10.17.214.169`（一小时内跳了两次）。服务一直在运行，实测四个路径全部返回 200：

| 路径 | 状态 | 内容 |
|---|---|---|
| `/` | 200 | 4401 bytes |
| `/ru/map_card.html` | 200 | 18742 bytes |
| `/ja/map_card.html` | 200 | 18599 bytes |
| `/ar/map_card.html` | 200 | 18681 bytes |

> IP 随时会因重连热点而变化。打不开时先在电脑运行 `Get-NetIPAddress -AddressFamily IPv4`，取 `WLAN` 那个地址，再拼上 `:8000`。

## 一、新增 S15 导航（已写进 SKILL.md）

**触发**：问位置、怎么去、地图、打车，或在去门店路上。

**数据与规则**：

| 项 | 做法 |
|---|---|
| 店名、地址、坐标 | 全取自 `query-nearby-stores`；**店名和地址照抄原文** |
| 坐标 | 接口给了非 0 才用；**实测这家店返回 `0.0`/`0.0`，所以不编坐标**，改用「按店名+城市搜索」链接，卡片自动隐藏坐标行 |
| 高德（首选） | 有坐标 `uri.amap.com/marker?position=lng,lat&name=…`；无坐标 `uri.amap.com/search?keyword=…&city=济南` |
| 腾讯（备选） | `apis.map.qq.com/uri/v1/search?keyword=…&referer=mcspeak` |
| 谷歌 | `google.com/maps/search/?api=1&query=<完整地址+城市>`，**卡片上注明「国内可能有偏移」** |
| 地铁/公交 | **禁止编造**。mcd-mcp 没有任何交通数据，只说“用地图 App 搜『附近地铁』”或干脆不提 |

## 二、新模板 `templates/map_card.html`

同样「一格一事、双语同格」，从上到下：

1. **店名 + 完整地址**（中文红色大字 `山大路146-6号（成大高科）一楼`，下面一行外语释义 + 拼音地址）
2. **三条地图链接**，一个链接一个黄/白块：`高德地图（推荐）· Amap`（黄底高亮）→ `腾讯地图 · Tencent Maps`（备注“备选”）→ `谷歌地图 · Google Maps`（备注“国内可能有偏移，仅作参考”）
3. **二维码**：`segno` 生成的内联 SVG data-URI（7.2 KB），**扫码直接开高德**，完全离线，不依赖任何图片服务
4. **给出租车司机（红框）**：`师傅您好，麻烦送我到这里，谢谢！` + **超大字完整地址** + 店名 + 一句外语说明
5. 🔊 **读出地址**：`txai_hello` + 完整地址 + 店名，`zh-CN` / rate 0.8

生成命令：`python scripts/render_card.py --type map --lang ru --out examples/ru/map_card.html --demo`

## 三、第 13 条：地址照抄，已固化为核心原则

核心原则第 3 条已从「餐品名照抄」扩展成**三类都给中国人看的文本**：

> 凡是要给中国人看的文本，一律照抄接口返回的原文，**一个字都不能省、不能改写**：
> 餐品名 → 照抄 `query-meals` 的 `name`；
> 店名 → 照抄 `storeName`（「麦当劳济南山大路(成大高科)餐厅」，括号和“餐厅”都不能丢）；
> 门店地址 → 照抄 `address`（「山大路146-6号（成大高科）一楼」）。
> **禁止简写**：不能把「146-6号」写成「146号」、不能把「（成大高科）一楼」省掉。地址少一个字符，司机/店员就找不到。

同时在 `staff_phrases_zh.md` 里新增了导出这一段：**H. 打车 / 给司机看** —— `staff.taxi_hello`（师傅您好，麻烦送我到这里，谢谢！）、`staff.taxi_show`（就是下面这个地址，麻烦您看一下，谢谢～），并附一条硬注：地址必须照抄原文。

## 四、自检与同步

| 检查 | 结果 |
|---|---|
| 三语地图卡生成 | ✅ ru / ja / ar 全部生成，18.6–18.7 KB |
| 地址原文 | ✅ 三张卡都是 `山大路146-6号（成大高科）一楼`（不是 146 号） |
| 坐标 | ✅ `coords: None`（接口给 0.0，按规则不显示、不编） |
| 二维码 | ✅ 存在，内联，7.2 KB |
| 模板 JS 语法 | ✅ `node --check` 通过 |
| markdown 残留 | ✅ `star: False` |
| examples | ✅ 每个语言 4 张卡 + index（共 13 个 html） |
| 技能目录 | ✅ 已同步，`templates/` 现在 4 个文件，技能内跑 `--type map` 通过 |

手机上直接可以看：**http://10.17.214.169:8000/ru/map_card.html**（`/ja/`、`/ar/` 同理，入口页 `/` 里也加了「📍 地图卡」）。

还差一件事没补：chromium 内核装完后导出 PNG。要我现在检查一下下载状态吗？

---

## 👤 用户

Skill 测试通过了。现在把它整理成参赛作品，全部在 ~/mcspeak/ 里做，完成后同步到 ~/.workbuddy/skills/mcspeak/。

【一、演示模式】
scripts/demo.py：用 samples/ 里的真实数据（35489 这单麦旋风和之前的麦辣鸡腿堡三件套），离线跑完一个阿拉伯语用户从开口到生成待付款卡、取餐卡、柜台卡、地图卡的全流程，不联网。SKILL.md 里写明：只有用户明确说 demo mode 时才使用，并在每条回复里标注"演示数据"。

【二、参赛文件】
1. README.md（项目介绍、安装方法、使用示例、目标用户，必须包含这四部分）：
   - 一句话：帮不会中文的外国人在中国麦当劳点餐；
   - 要解决的问题：很多外国人走进麦当劳，在柜台前因为说不出来而离开；App 只有中英文，不会英语的人更难；
   - 核心功能：母语推荐和换餐、自动算券、按名称过滤饮食限制（诚实说明无清真认证）、双语配对卡片（柜台卡 / 待付款卡 / 取餐卡 / 地图卡）、线上下单、导航；
   - 真实测试记录：阿拉伯语用户真实下单付款一份经典麦旋风并成功取餐（不写订单号和取餐码）；
   - 安装方法：WorkBuddy 配置 mcd-mcp 连接器 + 复制技能目录；
   - 使用示例：阿拉伯语、俄语、日语各一段对话示例；留好截图位置 docs/screenshots/；
   - 目标用户：在中国的外国游客、留学生、外籍员工，以及带外国朋友吃饭的中国人；
   - 限制说明：清真只按名称过滤、麦当劳中国无清真认证；到店订单不能加备注；接口无过敏原信息；
   - 后续计划：网页版扫码即用、支持 Claude Code / Codex 等其他 Agent。
2. MCP_INTEGRATION.md：用到的每个麦当劳 MCP 工具、调用流程图（mermaid）、每个工具的业务价值，以及实测踩坑（定制 key 按组类型解释、券逐张试算、金额单位、状态码以实测为准）。
3. mcp-config.example.json：只允许环境变量占位符，Token 写成 ${MCD_MCP_TOKEN}。
4. .gitignore：排除 data/、.env、任何真实配置、examples 里生成的临时文件。
5. LICENSE：MIT。
6. docs/ 目录：放三种语言的示例卡片 HTML 和一个 index.html，之后用 GitHub Pages 发布，手机任何网络都能打开。

【三、安全检查】
全仓库扫描一遍，确认没有：MCP Token、手机号、个人地址、完整订单号、payId、支付链接、取餐码。samples/ 里的真实返回要把这些字段脱敏。列出你脱敏了哪些地方。

【四、git】
在 ~/mcspeak 初始化 git，提交所有文件（CONTEST_DECLARATION.md 和 workbuddy.md 我稍后自己放进来）。告诉我推送到 GitHub 的命令。另外告诉我：WorkBuddy 怎么导出这次开发对话的完整上下文，作为 workbuddy.md。

---

## 👤 用户

Skill 测试通过了，现在一次性完成修复和参赛封装。全部在 ~/mcspeak/ 里做，完成后同步到 ~/.workbuddy/skills/mcspeak/，最后逐项汇报。

【一、修复（如果之前已经改过的，检查一遍即可）】
1. 每种语言默认用标准书面语（阿拉伯语用标准阿拉伯语，不用海湾方言），只有用户自己写方言时才跟随。
2. 所有"用户语言"的位置（餐品名、门店说明、就餐方式、付款方式、纯文本版、所有卡片）必须是用户的语言，表里没有就运行时翻译，绝不能用英文或中文代替。
3. 截图用的纯文本版是"中文 + 用户语言"，不是"中文 + 英文"。
4. 门店显示中文名 + 拼音 + 用户语言说明。
5. 订单摘要每个图标单独一行；外带用 🛍️，堂食用 🍽️。
6. 阿拉伯语等 rtl 语言在对话里加从右往左标记，避免编号和括号跑位。
7. 三种卡片给店员的中文按类型区分：柜台卡"您好，这是我要点的餐"；待付款卡"这是我在手机上下的订单，还没有付款"；取餐卡"您好！我在手机上点好了，取餐码是 XXXXX，谢谢！"。取餐卡价格写"实付"。
8. 状态对照按实测更新：待支付 → 确认中 → 配餐中 → 待取餐 → 订单已准备完毕；App 上取餐码显示为"订单号"，卡片要写明这一点；App 词汇补上 确认中、配餐中、待取餐、订单已准备完毕、订单号、实付、我已取餐、再来一单、开发票。
9. 把刚才临场生成的导航功能正式写进 SKILL.md（S15 导航：高德链接优先、腾讯备选、谷歌注明偏移、最近地铁和公交、给司机看的中文卡"师傅您好，麻烦送我到这里，谢谢！"）。给中国人看的地址、店名、餐品名必须照抄接口原文，比如"山大路146-6号（成大高科）一楼"，不能简写。

【二、演示模式】
scripts/demo.py：用 samples/ 的真实数据，离线跑完阿拉伯语用户从开口到待付款卡、取餐卡、柜台卡的流程，不联网。SKILL.md 写明只有用户说 demo mode 时才用，回复里标注"演示数据"。

【三、参赛文件（麦当劳大赛要求）】
1. README.md，必须包含"项目介绍、安装方法、使用示例、目标用户"四部分：
   - 问题：很多外国人在麦当劳柜台前因为说不出来而离开；App 只有中英文；
   - 功能：母语推荐和换餐、自动算券、按名称过滤饮食限制（诚实说明无清真认证）、双语配对卡片、线上下单、导航；
   - 真实验证：阿拉伯语用户真实下单付款一份经典麦旋风并成功取餐（不写订单号和取餐码）；
   - 安装：WorkBuddy 配置 mcd-mcp 连接器 + 复制技能目录；
   - 示例：阿拉伯语、俄语、日语各一段；截图位置放 docs/screenshots/；
   - 目标用户：在中国的外国游客、留学生、外籍员工，以及带外国朋友吃饭的中国人；
   - 限制：清真只按名称过滤、无认证；到店订单不能加备注；无过敏原信息；电脑上点餐后卡片需传到手机；
   - 后续计划：扫码把卡片接力到手机、网页版、支持 Claude Code / Codex。
2. MCP_INTEGRATION.md：实际使用的麦当劳 MCP Server、每个 Tool、调用流程图（mermaid）、业务价值、实测踩坑。
3. mcp-config.example.json：只允许环境变量占位符，Token 写成 ${MCD_MCP_TOKEN}。
4. .gitignore：排除 data/、.env、真实配置、临时生成文件。
5. LICENSE：MIT。
6. 把三种语言的示例卡片放到 docs/examples/。

【四、安全检查】
全仓库扫描：不能有 MCP Token、手机号、个人地址、完整订单号、payId、支付链接、取餐码。samples/ 里的真实返回全部脱敏，列出你改了哪些。

【五、git】
在 ~/mcspeak 初始化 git 并提交。CONTEST_DECLARATION.md 和 workbuddy.md 我自己放进来，你不要生成。告诉我：
1. 推送到 GitHub 的完整命令；
2. WorkBuddy 怎么导出这次开发对话的完整上下文，作为 workbuddy.md。
最后列出仓库的完整文件树。

---

## 🤖 mcspeak

现在开始逐项修复：先重写状态表，补上实测出的五段状态流和 App 词汇：

---

## 🤖 mcspeak

现在改渲染脚本，按卡片类型区分开场句、价格标签和新的状态流：

---

## 🤖 mcspeak

全部改动已完成，技能目录已同步。下面逐项汇报。

## 一、修复（9 项，逐条核对过）

| # | 要求 | 落点 | 状态 |
|---|---|---|---|
| 1 | 默认标准书面语，阿拉伯语用 MSA，只有用户先写方言才跟随 | `locale_style.md` 新增**规则 0**（明确禁用海湾/埃及方言、Arabizi）；`SKILL.md` 核心原则 1 | ✅ |
| 2 | 所有“用户语言”位置必须是用户的语言，查不到就运行时翻译 | 核心原则 1 加“绝不用英文或中文顶替”；**脚本加了三道检查**（见下） | ✅ |
| 3 | 纯文本版 = 中文 + 用户语言 | 核心原则 11 单列；`S13` 第 4 条给了阿拉伯语对照示例，明确“…不要用中文+英文凑数” | ✅ |
| 4 | 门店 = 中文名 + 拼音 + 用户语言 | `S3` 固定三行模板 | ✅ |
| 5 | 订单摘要一图标一行；外带 🛍️ / 堂食 🍽️ | `S10` 复述块重写（原来错写成 🍽️ 外带，已改） | ✅ |
| 6 | RTL 加方向标记 | 核心原则 10：RLM / RLI…PDI / LRI…PDI，并说明卡片里不塞控制符 | ✅ |
| 7 | 三种卡按类型分开场句；取餐卡写“实付” | 脚本按 `--type` 自动挑；柜台“您好，这是我要点的餐…”／待付款“这是我在手机上下的订单，还没有付款。”／取餐“您好！我在手机上点好了，取餐码是 XXXXX，谢谢！”；标签 参考价格／应付／**实付** | ✅ |
| 8 | 状态五态 + App 取餐码叫“订单号” + 补词汇 | `order_status_map.md` 重写；取餐卡号码下加一行“App 里这一行叫「订单号」” | ✅ |
| 9 | S15 导航固化 + 地址照抄原文 | `S15` 已有；本轮补 **🚇/🚌 地铁公交块**（只给问句 + 搜索指引，**不编站名**）；核心原则 3 覆盖店名/地址/餐品名 | ✅ |

**第 2 项是怎么变成硬性约束的**（这是本轮最实质的改动）：以前 `--lang ko` 会静默回退英文，`经典麦旋风` 这类没进表的商品会直接显示**中文**。现在：

- `python scripts/render_card.py --dump-keys ko` 输出 65 个待译 key 的骨架；
- 翻译后 `--tr ko.json --lang ko` 注入；
- 缺 `items` / `customs` / `payPills` 时**直接 `SystemExit` 并列出缺哪些 key**，不会偷偷降级。我用韩语实测过两张卡（payment / pickup），价格标签、状态行、按钮全是韩语。

第 8 项的状态表按你给的实测顺序重写成这样（**码没取到的一律标“待校正”，不猜**）：

```
待支付(10) → 确认中 → 配餐中 → 待取餐 → 订单已准备完毕 → 订单已完成(40) / 订单已取消(60)
```

`待取餐` 和 `订单已准备完毕` 都标为“可以去取餐”，代码判据是**文字双命中 + pickupCode 非空**兜底。

## 二、演示模式

`scripts/demo.py` 用 `samples/` 离线跑阿拉伯语全程（实测 5 张卡，无网络请求），本轮补了状态链路输出：

```
App 状态：确认中 → 钱已付，等几秒；别重复下单
App 状态：配餐中 → 后厨在做，在取餐台附近等
App 状态：待取餐 → 现在去取餐台 ★
App 状态：订单已准备完毕 → 拿餐并当场核对
```

`SKILL.md` 的 `S16` 明确：**只有用户说 demo mode / 演示模式才启用**，每条回复标注“演示数据”，且不真的调 `create-order`。

## 三、参赛文件

| 文件 | 状态 |
|---|---|
| `README.md`（13 KB） | 一句话 / 问题 / 核心功能 / **真实测试记录**（含五态链路，不写单号取餐码）/ 安装 / 三语示例 + `docs/screenshots/` 占位 / 目标用户 / 限制 9 条 / 后续计划 6 条 |
| `MCP_INTEGRATION.md` | 工具表 + mermaid 流程图 + 业务价值 + 5 类坑；本轮补 **坑 4b（pickupCode 在 App 叫订单号）** 和五态说明 |
| `mcp-config.example.json` | 只有 `${MCD_MCP_URL}` / `${MCD_MCP_TOKEN}` |
| `.gitignore` | 排除 `data/*`、`.env`、`mcp.json`、`examples/demo/`、`_tmp`、`__pycache__` |
| `LICENSE` | MIT |
| `docs/` | `index.html` 落地页 + `examples/{ru,ja,ar}/` 各 4 张卡（共 13 个页面，链接自检 0 坏链） |

## 四、安全检查

```
剩余命中（0 条）：✅ 未发现 Token / 订单号 / 支付信息 / 取餐码 / 手机号 / 身份证 / 邮箱
```

本轮额外发现并修掉的两处（扫描器之前漏了，因为写在散文里）：

1. `references/samples/00-index.md` — 正文里写着真实取餐码 `"00000"` → `"00000"`
2. `references/samples/20-query-order-completed.json` — `_meta` 注释里同样有 `00000` → `00000`

历史已脱敏项：`orderId`（24 位→`1030…0001`）、`payId`→`1110…0001`、`payH5Url`→`https://example.invalid/pay?orderId=REDACTED`、`pickupCode`→`00000`、`couponId`→`C0FFEE…`、`couponCode`→`MCD000000000000000`、门店地址里的门牌不影响公开（是门店地址不是个人地址）。明细在 `SECURITY.md`。

## 五、git

已初始化并提交，**76 个文件**，工作区干净：

```
649b4ae feat: 参赛封装定稿 — 状态五态实测、卡片按类型分文案、S15 导航、运行时翻译
2d533f9 feat: mcspeak 麦麦替你说 — 决赛提交
```

### 推到 GitHub 的完整命令

```bash
# 1. 先在 GitHub 网页建一个空仓库（不要勾 README / LICENSE / .gitignore）

cd ~/mcspeak
git remote add origin https://github.com/<你的用户名>/mcspeak.git
git branch -M main
git push -u origin main
```

如果用 SSH：`git remote add origin git@github.com:<用户名>/mcspeak.git`。

**开 GitHub Pages**：`Settings → Pages → Source: Deploy from a branch → Branch: main / 目录选 /docs → Save`，一两分钟后：

```
https://<用户名>.github.io/mcspeak/                 落地页
https://<用户名>.github.io/mcspeak/examples/        三语总览
https://<用户名>.github.io/mcspeak/examples/ar/     阿拉伯语（RTL）
```

> 手机现在也能看：**http://192.168.43.187:8001/docs/**（8001 服务仓库根，比 8000 多看得到落地页）。8000 仍在服务 `examples/`。IP 是热点分的，换网就变。

### 怎么导出这次对话作为 workbuddy.md

会话原始记录在这里（我确认过，6.7 MB / 1281 行，`role` + `message` 结构）：

```
C:\Users\river lee\.workbuddy\projects\c-Users-river lee-WorkBuddy-2026-10-24-17-09-12\14860ecc-fb21-412e-a49d-389c137d7bc5.jsonl
```

转成 markdown 的一条命令（在 `~/mcspeak` 下跑，产出 `workbuddy.md`）：

```bash
python - <<'PY'
import json, glob, os
d = os.path.expanduser(r"~/.workbuddy/projects/c-Users-river lee-WorkBuddy-2026-10-24-17-09-12")
src = max(glob.glob(os.path.join(d, "*.jsonl")), key=os.path.getmtime)
out = []
for line in open(src, encoding="utf-8"):
    try: o = json.loads(line)
    except: continue
    m = o.get("message") or {}
    role = m.get("role") or o.get("role")
    c = m.get("content") or o.get("content")
    if role not in ("user", "assistant") or not c: continue
    if isinstance(c, list):
        c = "\n".join(x.get("text", "") for x in c if isinstance(x, dict) and x.get("type") == "text")
    if not str(c).strip(): continue
    out.append(("## " + ("👤 用户" if role == "user" else "🤖 mcspeak") + "\n\n" + str(c).strip()))
open("workbuddy.md", "w", encoding="utf-8").write(
    "# mcspeak 开发对话记录\n\n> 由 WorkBuddy 会话记录导出，仅保留对话正文（已剔除工具调用与返回）。\n\n"
    + "\n\n---\n\n".join(out) + "\n")
print("wrote workbuddy.md", os.path.getsize("workbuddy.md"), "bytes")
PY
```

如果客户端里有“导出对话 / 复制全部”之类的按钮，用那个更省事；上面这条是**不依赖 UI** 的兜底。注意 `workbuddy.md` 会被 `.gitignore` 里没有的规则拦住 → 它会正常入库，你放进去后 `git add workbuddy.md CONTEST_DECLARATION.md && git commit -m "docs: 参赛声明与对话记录"` 再 push 即可。

## 六、仓库完整文件树（76 个跟踪文件）

```
mcspeak/
├── .gitignore
├── LICENSE                                   MIT
├── README.md                                 参赛主文档（13 KB）
├── MCP_INTEGRATION.md                        工具表 + mermaid + 踩坑
├── SECURITY.md                               脱敏明细
├── SKILL.md                                  技能主文件（16 KB，S1–S16）
├── mcp-config.example.json                   仅环境变量占位符
├── data/
│   └── README.md                             运行时目录说明（profile / feedback 不入库）
├── docs/                                     GitHub Pages 根
│   ├── index.html                            落地页
│   ├── screenshots/README.md                 截图占位清单
│   └── examples/
│       ├── index.html
│       ├── ar/  counter · payment_notice · pickup · map   （dir=rtl）
│       ├── ja/  counter · payment_notice · pickup · map
│       └── ru/  counter · payment_notice · pickup · map
├── examples/                                 同 docs（本地预览用）+ README.md
│   ├── index.html
│   └── ar/ ja/ ru/  各 4 张
├── references/
│   ├── mcd_tools.md                          13 工具 + 8 结论 + 16 坑
│   ├── menu_tags.md                          93 商品人工标注
│   ├── diet_rules.md                         清真三档 + 过敏免责 + 禁用语
│   ├── staff_phrases_zh.md                   店员中文模板（含 H. 打车 / 地铁公交）
│   ├── locale_style.md                       8 语言风格（新增标准书面语 / RTL 规则）
│   ├── order_status_map.md                   状态五态 + App 词汇 23 条
│   ├── PROBE-REPORT.md · ORDER-PROBE-REPORT.md
│   └── samples/  01–16b、17–21 + 00-index.md + README.md（24 个，全部脱敏）
├── scripts/
│   ├── render_card.py                        counter|payment|pickup|map，--tr 运行时翻译
│   ├── demo.py                               离线演示（阿拉伯语全程 5 张卡）
│   └── check_privacy.py                      扫描 + --fix 脱敏
└── templates/
    ├── counter_card.html
    ├── payment_notice.html                   App 拟态（去支付黄色实心）优先
    ├── pickup_card.html                      超大取餐码 + 订单号说明 + 五态表
    └── map_card.html                         高德/腾讯/谷歌 + 二维码 + 地铁公交 + 给司机
```

`examples/demo/` 和 `scripts/__pycache__/` 在本地存在但**不进仓库**（`.gitignore` 已排）。

有一处我自己做了取舍，需要你知道：**“最近地铁和公交”我没有写具体站名**——mcd-mcp 完全没有交通数据，编一个站名他会真的走错。改成“问店员的两句中文 + 在 Amap 搜『地铁站/公交站』”，既给了可执行动作，也不会给出假信息。如果你评审时希望卡片上出现具体站名，那就需要外接一个地图 POI 接口，我可以加，但要新增一个依赖。

---

## 👤 用户

马上要提交比赛了。请把 mcspeak 做成最终可分发、可直接使用的完整 Skill，并完成提交前的收尾。

【一、同步并确认最终版本】
1. 确认 ~/.workbuddy/skills/mcspeak/ 和 ~/mcspeak/ 里的 SKILL.md、references/、templates/、scripts/ 完全一致（逐文件比对），不一致就以 ~/mcspeak/ 为准同步过去。
2. 检查 SKILL.md 的 frontmatter（name、description）格式正确，description 能覆盖"用非中文语言提到麦当劳、点餐、取餐"和"McSpeak"两种触发方式。

【二、打包成可安装的技能包】
1. 生成 dist/mcspeak-skill.zip，只包含运行需要的文件：SKILL.md、references/（含 samples，已脱敏）、templates/、scripts/、data/README.md。不包含 docs/、examples/、.git、__pycache__。
2. 在 README.md 的安装方法里写两种方式：
   ① WorkBuddy 界面：技能 → 添加技能 → 上传技能，选择 dist/mcspeak-skill.zip；
   ② 手动：把 zip 解压到 ~/.workbuddy/skills/mcspeak/。
   两种方式前面都要先配置 mcd-mcp 连接器（写清 JSON，Token 用占位符）。

【三、全新安装验证】
1. 把现在的 ~/.workbuddy/skills/mcspeak/ 备份，然后清空，用 dist/mcspeak-skill.zip 重新解压安装一次。
2. 在技能目录下跑一次 scripts/demo.py，确认离线演示能完整生成阿拉伯语的待付款卡、取餐卡、柜台卡、地图卡。
3. 用 samples 的真实数据跑一次 render_card.py 的四种卡片。
4. 告诉我验证结果。如果有任何失败，修好后重新打包再验证一次。

【四、参赛文件收尾】
1. CONTEST_DECLARATION.md：从 https://raw.githubusercontent.com/M-China/mcd-developer-innovation-challenge/main/CONTEST_DECLARATION.md 原样下载到 ~/mcspeak/CONTEST_DECLARATION.md，一个字节都不能改，下载后显示文件的 sha256 和前 5 行给我核对。如果下载失败告诉我，我手动放。
2. workbuddy.md：运行你上次给我的那段导出脚本，生成 ~/mcspeak/workbuddy.md。导出后再跑一次 check_privacy.py，确认对话记录里也没有 Token、手机号、订单号、取餐码、支付链接，有就脱敏。
3. git add 全部文件并提交，提交信息写"release: mcspeak v1.0 参赛版"。

【五、最后汇报】
列出：最终文件树、zip 大小和内容清单、全新安装验证结果、CONTEST_DECLARATION.md 的 sha256、workbuddy.md 大小、隐私扫描结果。
