# examples/ — 三语示例卡（一格一事 · 双语同格）

> 数据来自 `references/samples/17-create-order.json` 的**真实订单**：
> 麦辣鸡腿汉堡三件套 ×1 · 不要切块生菜 · 可乐去冰 · 外带 · ¥33.50 · 取餐码 `00000`（**占位示例**）

## 文件

```
examples/
├── index.html                 入口（列出 12 张卡）
├── ru/counter_card.html       柜台点餐卡 · 俄语
├── ru/payment_notice.html     待付款提示 · 俄语
├── ru/pickup_card.html        取餐卡 · 俄语
├── ru/map_card.html           地图 / 打车卡 · 俄语
├── ja/…  ar/…                同上 4 张（日语 / 阿拉伯语，ar 整卡 dir=rtl）
```

## 在手机上看（局域网）

```bash
cd ~/mcspeak/examples
python -m http.server 8000 --bind 0.0.0.0
# 另开一个终端查 IP（取 WLAN 那条 IPv4）
powershell -c "Get-NetIPAddress -AddressFamily IPv4 | Select IPAddress,InterfaceAlias"
```

手机连**同一个 Wi-Fi**，浏览器打开 `http://<局域网IP>:8000/`。

- 关闭：终端里 `Ctrl+C`
- 防火墙：Windows 弹窗选「允许专用网络」；没弹窗且手机打不开，用管理员执行
  `netsh advfirewall firewall add rule name="mcspeak 8000" dir=in action=allow protocol=TCP localport=8000`
- 电脑和手机不在同一 Wi-Fi / 路由器开了 AP 隔离时只能走"发文件"。

## 版式规则（四个模板一致）

| 规则 | 实现 |
|---|---|
| 一件事一个格子 | `.row` = 一个 grid，中文在上、用户语言在下；不再有"中文区/外语区" |
| 横屏两栏严格对齐 | `@media (min-width:640px) and (orientation:landscape)` → `.row{grid-template-columns:1fr 1fr}`，同一 grid 行天然等高对齐 |
| RTL 只在右栏内 | `.loc[dir="rtl"]{text-align:right}`，`.row` 自身 `direction:ltr`，行序不变 |
| 餐品锚点 | ①②③ 圆形编号，中英同一编号 |
| 动作锚点 | 🍽️堂食 / 🛍️外带 / 💳付款 / 🎫取餐码 / 🔊朗读，中英同图标 |
| 按钮双语 | 每个 `<button>` 内 `.bzh` + `.bloc` 两行 |
| App 拟态 | 顶部大字状态 + 底部三胶囊（取消订单 / 联系客服 / 去支付），去支付黄色实心、其余白底黑边，附用户语言位置提示 |
| 朗读高亮 | `data-read` + `.reading`（黄色底+描边+自动滚动到可视区） |
| 地图卡 | 店名+**完整地址照抄原文**、高德(首选)/腾讯(备选)/谷歌(注明偏移)、内联 SVG 二维码(segno)、红框给司机大字块；坐标仅当接口非 0 才显示 |
| 无 markdown | `esc()` 里清 `**`，生成端 `strip_md()` 再兜一层 |

## 重新生成

```bash
cd ~/mcspeak
for L in ru ja ar; do
  python scripts/render_card.py --type counter --lang $L --out examples/$L/counter_card.html --demo
  python scripts/render_card.py --type payment --lang $L --out examples/$L/payment_notice.html --demo
  python scripts/render_card.py --type pickup  --lang $L --out examples/$L/pickup_card.html --pickup-code 00000 --demo
done
```

`--png` 需要 playwright + chromium；本次已装并导出同名 PNG（若某张缺失说明该平台内核未装成功）。
