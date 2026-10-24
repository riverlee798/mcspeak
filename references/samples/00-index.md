# samples/ — mcd-mcp 原始返回（索引）

> 采集时间：2026-10-24 17:22–19:14（GMT+8）
> 门店：`3350020` 麦当劳济南山大路(成大高科)餐厅
> 场景：到店自取 `orderType=1` / `beType=1`（不传 beCode）
> **脱敏**：所有响应不含访客个人信息（无手机号、无地址、无联系人）。门店地址属公开营业信息，保留到门牌级。
> 文件结构：`_meta`（采集说明/请求参数/结论）+ `raw_response`（原样返回）。纯原始单行 JSON 的样本（05–09）只有 `raw_response` 本体。

| # | 文件 | 内容 | 关键结论 |
|---|---|---|---|
| 01 | `01-now-time-info.json` | 服务端时间 + 统一信封 | 时间唯一可信源；`success && code===200` 才成功 |
| 02 | `02-query-nearby-stores-nearby.json` | 5 家门店（searchType=2） | 最近 3350020，513 m；经度纬度恒 0 |
| 03 | `03-query-nearby-stores-favorite.json` | 收藏门店（searchType=1） | 字段残缺：无营业时间、distance=0 |
| 04 | `04-query-meals-store3350020.json` | 14 分类 / 99 条目 / **93 商品** | 两层结构；价格是元字符串；无配料/过敏原 |
| 05 | `05-…-9900005456-chicken-set.json` | 麦辣鸡腿堡三件套 | 3 个 round；冰量 4 选项 code 全同 |
| 06 | `06-…-9900005466-beef-set.json` | 巨无霸三件套 | 5 个可去配料，全用 `0-1/0-0` 开关 |
| 07 | `07-…-1600-fish.json` | 麦香鱼（单品） | `rounds=[]` 但 `supportModify=true`，特调在 data 层 |
| 08 | `08-…-521730-pork.json` | 猪柳蛋堡 | 只有"吉士"可去，猪肉本体去不掉 |
| 09 | `09-…-9900008754-dessert.json` | 经典麦旋风 | 只能二选一口味，不可特调 |
| 10 | `10-list-nutrition-foods.json` | 160 条营养 CSV | `data` 是字符串；无 code；仅 18/93 名称命中 |
| 11 | `11-auto-bind-coupons.json` | 领券 3 张 | 文本返回，含 couponId/couponCode，无适用商品 |
| 12 | `12-query-store-coupons-empty.json` | 门店可用券 | `data: []`（券未到生效日） |
| 13 | `13-query-my-coupons.json` | 券包 2 张 | 有效期 10-26 起；无 couponId |
| 14 | `14-calculate-price-no-coupon.json` | 巨无霸三件套计价 | 3700 分；takeWayList 2 项 |
| 15 | `15-calculate-price-with-coupon-error.json` | 带无效券计价 | `600012`「此卡券不在使用日期内」整单失败 |
| 16 | `16-calculate-price-with-modification.json` | 带 roundList/特调计价 | 不报错、价格不变（0 元特调看不出生效） |
| 16b | `16b-calculate-price-confirmed-cart.json` | 正式下单前的购物车计价 | 3350 分；含完整 items 请求参数 |
| **17** | `17-create-order.json` | **真实下单（未付款）** | `orderId`/`payH5Url`/`expirePayTime`（+15min）；`pickupCode=""`；**特调进单了** |
| **18** | `18-query-order-unpaid.json` | 未支付查询 | `待支付` / `10`；结构平铺、无 `payH5Url` |
| **19** | `19-query-order-expired.json` | **超时未付后查询** | **`订单已取消` / `60`**（没有"已过期"状态）；金额与 pickupCode 不归零 |
| **20** | `20-query-order-completed.json` | **已完成历史单** | **`订单已完成` / `40`**；`pickupCode="35214"`；含券明细与"麦金卡月卡"非餐品行 |
| 21 | `21-order-list.json` | 历史订单列表 | 只给 `orderStatus` 文字、**不给 status 码**；comboItemList 是结构化字段 |

## 本轮状态码实测汇总

| orderStatus | status | 触发 |
|---|---|---|
| 待支付 | `10` | 创建后未付款 |
| 订单已完成 | `40` | 已支付并完成 |
| 订单已取消 | `60` | 超时未付被系统关闭 |

> 工具文档写的 `1/2/4/6/7/8/10` 与实测完全不符，**不要用文档枚举**。

## 关键对照（同一单，三个接口三种形状）

| | `calculate-price` | `create-order` | `query-order` |
|---|---|---|---|
| 金额 | **分**（`3350` 整数） | **元**（`"33.5"` 字符串） | **元**（`"33.5"` 字符串） |
| 结构 | `data.xxx` 平铺 | `data.orderDetail.xxx` | `data.xxx` 平铺 |
| 支付链接 | — | `data.payH5Url` ✅ | ❌ 没有 |
| 取餐码 | — | `pickupCode`（空） | `pickupCode`（空/有值） |
| 定制回显 | ❌ 无 | ✅ `comboItemList[].itemName` | ✅ 同上 |
