# SECURITY.md — 隐私与安全检查说明

> 本仓库包含**真实接口返回**（`references/samples/`），全部经过脱敏。
> 复现检查：`python scripts/check_privacy.py`（当前结果：**0 命中**）。

---

## 1. 脱敏了哪些地方

| # | 字段 | 原值形态 | 现在的值 | 涉及文件 |
|---|---|---|---|---|
| 1 | `orderId`（完整订单号） | 28 位真实订单号 | `1030000000000000000000000001` 起（历史单按序 `…0001/0002/0003`） | `samples/17`、`18`、`19`、`20`、`21` |
| 2 | `payId`（支付单号） | 20 位真实支付单号 | `1110000000000000000001` | `samples/17`、`18`、`19`、`20` |
| 3 | `payH5Url`（支付链接） | `https://m.mcd.cn/mcp/scanToPay?orderId=…` | `https://example.invalid/pay?orderId=REDACTED` | `samples/17` |
| 4 | `pickupCode`（取餐码） | 真实 5 位取餐码 | `00000` | `samples/17`、`18`、`19`、`20` |
| 5 | `couponId`（优惠券 ID） | 32 位十六进制 | `C0FFEE0000000000C0FFEE0000000000` | `samples/11`、`13`；`references/mcd_tools.md` |
| 6 | `couponCode`（优惠券码） | `MCD…` 长串 | `MCD000000000000000` | `samples/11`、`13`、`15`；`references/PROBE-REPORT.md`、`mcd_tools.md` |
| 7 | 文档里裸写的订单号 | 28 位 | `1030……9529` → 省略中间位 | `samples/00-index.md` |

### 没有脱敏（并说明原因）

| 内容 | 为什么不脱敏 |
|---|---|
| **门店名称、门店地址**（如「麦当劳济南山大路(成大高科)餐厅」「山大路146-6号（成大高科）一楼」） | 公开营业信息，本身就在高德/点评上；且**必须原样保留**才能给司机和店员看 |
| **餐品名、`productCode`、价格** | 菜单公开数据 |
| **`traceId`** | 单次请求的追踪号，不含账号信息，且已随请求失效 |
| **`storeCode` / `beCode`** | 门店标识，公开可查 |
| **营业时间、预约时段** | 公开信息 |

### 从未进入仓库的内容

- 手机号、收货地址、联系人姓名（`deliveryInfo` 相关字段本轮未采集）
- 身份证、邮箱、真实姓名
- **MCP Token / 任何凭据**：`mcp-config.example.json` 只有 `${MCD_MCP_URL}` / `${MCD_MCP_TOKEN}` 占位符
- 真实用户偏好（`data/profile.json`）、反馈记录（`data/feedback.jsonl`）——`data/` 已被 `.gitignore` 排除

---

## 2. 检查脚本

```bash
python scripts/check_privacy.py          # 只报告
python scripts/check_privacy.py --fix    # 就地脱敏 samples 与 references 文档
```

覆盖 11 类模式：`TOKEN`（token/api_key/client_secret 字段 + Bearer）、`ORDER_ID`、`PAY_ID`、`PAY_URL`、`PICKUP`、`COUPON_ID`、`COUPON_CODE`、`PHONE`、`IDCARD`、`EMAIL`。

脚本内置白名单，脱敏后的占位值（`C0FFEE…`、`MCD0000…`、`example.invalid`、`00000`）不会自己触发告警。

**当前状态：**

```
剩余命中（0 条）：
  ✅ 干净：未发现 Token / 订单号 / 支付信息 / 取餐码 / 手机号 / 身份证 / 邮箱
```

---

## 3. 提交前自检清单

- [x] `python scripts/check_privacy.py` 为 0 命中
- [x] `mcp-config.example.json` 里没有真实 Token
- [x] `.gitignore` 排除 `data/`、`.env`、`mcp.json`、`examples/demo/`
- [x] 没有任何 `.env` / `mcp.json` 被提交
- [ ] README 截图里不含订单号、取餐码、手机号（**提交截图时请再确认一遍**）
- [ ] 演示卡片底部保留 `SAMPLE` 标记

---

## 4. 已知取舍

1. **取餐码 `00000` 是占位值**：取餐卡模板需要非空值才会渲染取餐码区，所以统一用 `00000`，页面上另有 `SAMPLE` 标记。
2. **历史订单的三个单号现在都是占位值**，看起来像同一单；这是为了不暴露真实单号，保留"三条不同订单"的结构（`…0001/0002/0003`）。
3. **支付链接已失效**（`example.invalid`），点开不会跳转——这是有意为之。
