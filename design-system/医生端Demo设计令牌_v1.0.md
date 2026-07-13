# 痛风智能体 · 医生端 Demo 设计令牌文档

> 版本：v1.0.0 · 2025-07
> 用途：医生端 1.0 Demo 原型构建专用设计令牌，供原型构建师直接照做 HTML/CSS
> 令牌来源：`design-system/tokens.css`（复用，不另起炉灶）
> 适用范围：医生端全部页面（登录 / 工作站 / 患者队列 / 患者详情档案 / 看诊前资料 / AI辅助 / 医生确认 / 建档码 / 复诊逾期）

---

## 1. Visual Theme（视觉主题）

**Philosophy**: 专科医生工作台——可追溯、可确认、任务优先的高密度信息界面。

**Direction**: data-dense, utilitarian, low-decoration, clinical-blue

**Personality**: confident, precise, trustworthy, restrained

**Reference**: Linear 的工作站密度感 + 医院信息系统(HIS)的蓝色专业感，去掉一切装饰性插画和拟物效果。

**核心原则**:
- 白卡片 + 灰背景 + 蓝主色，三色构成 90% 画面
- 低圆角（主用 10px / 14px / 18px），不用大圆角和胶囊形（状态标签除外）
- 高密度列表：紧凑行高、小字号、信息分层用字重而非颜色
- 状态语义严格：橙=待确认提醒、绿=已确认完成、红=异常风险，不混用
- 每个数据字段必须可追溯（来源标记），每个操作必须可确认（确认按钮 + 时间戳）

---

## 2. Color Palette（调色板）

> 所有色值直接复用 `tokens.css` 中 `--doctor-*` 变量，不新增色值。

### 2.1 主色（Primary）

| Token | HEX | CSS 变量 | 使用场景 |
|-------|-----|----------|---------|
| 主色 | `#0052d9` | `--doctor-primary` | 顶部栏渐变起点、主按钮实色、关键链接、选中态、主任务卡片描边 |
| 主色亮 | `#1f73f1` | `--doctor-primary-2` | 顶部栏渐变终点、主按钮 hover、进度条、蓝色图标底 |
| 主色软 | `#eaf2ff` | `--doctor-blue-soft` | 来源标记 badge 底色、蓝色图标背景、选中行高亮底 |

**顶部栏渐变**: `linear-gradient(135deg, var(--doctor-primary), var(--doctor-primary-2))`

### 2.2 中性色（Neutral）

| Token | HEX | CSS 变量 | 使用场景 |
|-------|-----|----------|---------|
| 页面背景 | `#eef2f7` | `--doctor-bg` | 手机内屏底色、列表间隙背景 |
| 面板/卡片 | `#ffffff` | `--doctor-panel` | 所有卡片、列表容器、弹层底色 |
| 描边 | `#e5eaf2` | `--doctor-line` | 卡片边框、列表分割线、输入框边框 |
| 主文字 | `#1d2530` | `--doctor-text` | 标题、列表主文、字段值、数字指标 |
| 次文字 | `#566579` | `--doctor-sub` | 副标题、描述文案、字段名 |
| 弱文字 | `#8a94a6` | `--doctor-hint` | 时间戳、提示语、placeholder、来源标记文字 |

### 2.3 语义状态色（Semantic）

| Token | HEX | CSS 变量 | 软底色 | 使用场景 |
|-------|-----|----------|--------|---------|
| 橙色·待确认 | `#ed7b2f` | `--doctor-orange` | `--doctor-orange-soft` `#fff4e8` | **仅用于**待确认类状态标签、待确认提醒徽标、待办列表中待确认任务的图标底色 |
| 绿色·已确认 | `#2ba471` | `--doctor-green` | `--doctor-green-soft` `#eaf8f2` | 已确认状态标签、完成态图标底色、已确认操作时间戳 |
| 红色·异常 | `#d54941` | `--doctor-red` | `--doctor-red-soft` `#fff0ee` | 异常指标、风险预警标签、异常风险图标底色、删除操作 |

**状态色使用铁律**:
- 橙色**绝不**用于装饰或普通强调，仅限"待确认/待处理/提醒"语义
- 绿色**绝不**用于普通成功提示弹窗，仅限"已确认/已完成"状态标记
- 红色**绝不**用于普通按钮，仅限"异常/风险/删除"语义
- 状态标签文字用对应状态色，底色用对应 soft 色

---

## 3. Typography（排版）

### 3.1 字体栈

```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
```

统一使用 `--gout-font-family`，医生端不引入额外字体。

### 3.2 字号层级表

> 医生端采用更小字号、更紧凑行高，体现高密度工作台特征。全部复用 `--text-*` 变量。

| 层级 | CSS 变量 | 字号 | 字重 | 行高 | 使用场景 |
|------|----------|------|------|------|---------|
| 页面大标题 | `--text-2xl` | 22px | 900 | 1.25 | 顶部栏医生姓名、工作站主指标数字 |
| 区块标题 | `--text-xl` | 18px | 850 | 1.3 | 任务卡主标题、档案分块标题 |
| 次级标题 | `--text-lg` | 16px | 800 | 1.35 | 顶部栏标题文字、列表组标题 |
| 列表主文 | `--text-base` | 14px | 800 | 1.4 | 患者姓名、待办标题、字段值主文 |
| 正文/描述 | `--text-md` | 13px | 700 | 1.45 | 任务描述、档案字段值、辅助说明 |
| 副文/标签 | `--text-sm` | 12px | 700 | 1.4 | 字段名、来源标记、时间、状态标签 |
| 辅助标注 | `--text-xs` | 11px | 850 | 1.3 | 状态 chip 文字、来源 badge 文字、极小标注 |
| 微标 | `--text-xxs` | 10px | 800 | 1.2 | 角标数字、计数器、超紧凑场景 |

**行高规则**: 医生端行高统一偏紧（1.2–1.45），不用患者端的 1.55–1.6 宽松行高。列表项内多行文字行高不超过 1.45。

**字重规则**:
- 标题用 850–900（粗体偏重，信息锚点）
- 列表主文用 800（中粗，可扫描）
- 副文/描述用 700（常规偏粗，辅助阅读）
- 标签/chip 用 850（小字号需加重保证可读）

---

## 4. Component Styles（组件规范）

> 以下每个组件原型构建师可直接照抄 CSS 类名和样式。

### 4.1 顶部栏（Top Bar）

**用途**: 医生端工作台顶栏（工作站首页）和详情页导航栏。

**工作台顶栏（渐变蓝底）**:
```css
.ds-doctor-topbar {
  background: linear-gradient(135deg, var(--doctor-primary), var(--doctor-primary-2));
  color: #ffffff;
  padding: 15px 16px;
  border-radius: var(--radius-md); /* 14px */
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}
/* 左侧：医生姓名 18px/850 + 科室/职称 12px/700 半透明白 */
/* 右侧：幽灵按钮（建档码/设置）rgba(255,255,255,0.16) 底，白字，9px圆角 */
```

**详情页导航栏（白底）**:
```css
.ds-doctor-navbar {
  height: 48px;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 16px;
  background: var(--doctor-panel);
  border-bottom: 1px solid var(--doctor-line);
  flex-shrink: 0;
}
/* 左：返回按钮 30x30 圆角9px 灰底 */
/* 中：标题 16px/800 居中 */
/* 右：操作图标位（可选） */
```

### 4.2 工作站指标卡（Stat Grid）

**用途**: 工作站首页展示今日数据概览。

```css
.ds-doctor-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}
.ds-doctor-stat {
  min-height: 72px;
  border-radius: var(--radius-sm); /* 10px */
  background: var(--doctor-panel);
  border: 1px solid var(--doctor-line);
  padding: 11px 10px;
}
/* 数字：22px/900，颜色 --doctor-text */
/* 标签：12px/700，颜色 --doctor-hint，margin-top 8px */
```

### 4.3 待办列表项（Todo Item）

**用途**: 工作站首页待办任务列表。

```css
.ds-doctor-todo-list {
  border-radius: var(--radius-md); /* 14px */
  background: var(--doctor-panel);
  border: 1px solid var(--doctor-line);
  overflow: hidden;
}
.ds-doctor-todo {
  display: flex;
  gap: 10px;
  padding: 12px;
  border-bottom: 1px solid #f0f3f8;
}
.ds-doctor-todo:last-child { border-bottom: 0; }
/* 左侧图标 34x34 圆角10px，三色变体：
   - blue:  bg --doctor-blue-soft, color --doctor-primary  （常规任务）
   - orange: bg --doctor-orange-soft, color --doctor-orange （待确认任务）
   - red:   bg --doctor-red-soft, color --doctor-red       （异常/风险任务）
*/
/* 标题 14px/800 --doctor-text */
/* 描述 12px/700 --doctor-hint margin-top 3px */
```

### 4.4 患者列表行（Patient Row）

**用途**: 患者队列页面的高密度列表行。

```css
.ds-doctor-patient-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 11px 12px;
  border-bottom: 1px solid var(--doctor-line);
  background: var(--doctor-panel);
}
/* 结构：[头像/ initials 圆形 36x36] [信息区 flex:1] [状态标签] [时间/箭头] */
/* 信息区：
   - 第一行：姓名 14px/800 + 性别年龄 12px/700 --doctor-hint（同行，gap 8px）
   - 第二行：脱敏手机号 12px/700 --doctor-sub
   - 第三行：病程摘要 12px/700 --doctor-hint（单行省略）
*/
/* 右侧：状态 chip + 时间 11px/850 --doctor-hint */
```

### 4.5 状态标签 Chip（Status Chip）

**用途**: 患者列表、待办、档案中的状态标记。低圆角矩形，不用胶囊形。

```css
.ds-doctor-chip {
  display: inline-flex;
  align-items: center;
  min-height: 25px;
  border-radius: var(--radius-xs); /* 7px - 低圆角矩形 */
  padding: 0 9px;
  font-size: var(--text-xs); /* 11px */
  font-weight: 850;
  white-space: nowrap;
}
/* 待接诊/待确认：bg --doctor-orange-soft, color --doctor-orange */
/* 已确认/已完成：bg --doctor-green-soft, color --doctor-green  */
/* 异常/风险：     bg --doctor-red-soft, color --doctor-red    */
/* 来源标记 badge：bg --doctor-blue-soft, color --doctor-primary */
```

### 4.6 结构化档案分块（Field Block）

**用途**: 患者详情档案页，将结构化数据分块展示。

```css
.ds-doctor-field-card {
  border-radius: var(--radius-md); /* 14px */
  background: var(--doctor-panel);
  border: 1px solid var(--doctor-line);
  padding: 14px;
}
/* 分块标题：14px/850 --doctor-text，底部 margin 10px */
/* 字段行结构：
   .ds-doctor-field-row { display:flex; justify-content:space-between; gap:10px; padding:7px 0; border-bottom:1px solid #f5f7fa; }
   - 字段名：12px/700 --doctor-hint（左）
   - 字段值：13px/850 --doctor-text（右，text-align right）
   - 来源标记：紧跟字段值后方，11px/850 badge 样式
*/
/* 来源标记 badge 样式同 4.5 的蓝色变体 */
```

### 4.7 主按钮 / 次按钮 / 文字链

**主按钮（蓝实色）**:
```css
.ds-doctor-btn-primary {
  height: 40px;
  border-radius: var(--radius-sm); /* 10px - 低圆角 */
  border: 0;
  background: var(--doctor-primary);
  color: #ffffff;
  font-size: var(--text-base); /* 14px */
  font-weight: 800;
  padding: 0 16px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  cursor: pointer;
}
/* hover: background var(--doctor-primary-2) */
/* 必须带真实 SVG 图标（如确认✓、扫码、保存等） */
```

**次按钮（白底蓝字描边）**:
```css
.ds-doctor-btn-secondary {
  height: 40px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--doctor-line);
  background: #ffffff;
  color: var(--doctor-primary);
  font-size: var(--text-base);
  font-weight: 800;
  padding: 0 13px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  cursor: pointer;
}
```

**文字链**:
```css
.ds-doctor-link {
  background: transparent;
  border: 0;
  color: var(--doctor-primary);
  font-size: var(--text-sm); /* 12px */
  font-weight: 800;
  cursor: pointer;
}
```

### 4.8 AI 诊疗辅助卡片（AI Assist Card）

**用途**: AI 辅助页面，展示诊疗辅助建议（依据/风险/建议三段式）。必须明确标注"诊疗辅助建议"。

```css
.ds-doctor-ai-card {
  border-radius: var(--radius-md); /* 14px */
  background: var(--doctor-panel);
  border: 1px solid rgba(0, 82, 217, 0.18); /* 蓝色描边 */
  box-shadow: 0 2px 8px rgba(31, 42, 68, 0.06);
  padding: 14px;
}
/* 顶部标识行：AI图标(蓝色圆角方块28x28) + "诊疗辅助建议"标题 14px/850 + 置信度标签 */
/* 三段式内容：
   - 依据区：左侧3px蓝色竖条 + 浅灰底 #f7f9fc，内容 12px/700 --doctor-sub
   - 风险区：左侧3px红色竖条 + --doctor-red-soft 底，内容 12px/700 --doctor-red
   - 建议区：左侧3px绿色竖条 + --doctor-green-soft 底，内容 12px/700 --doctor-green
*/
/* 底部：医生确认按钮（主按钮）+ 忽略按钮（次按钮/文字链） */
```

**证据引用块**:
```css
.ds-doctor-evidence {
  margin-top: 10px;
  border-left: 3px solid var(--doctor-primary);
  background: #f7f9fc;
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  padding: 9px 10px;
  color: var(--doctor-sub);
  font-size: var(--text-sm); /* 12px */
  line-height: 1.5;
}
```

### 4.9 底部操作条（Action Bar）

**用途**: 医生端详情页/确认页底部固定操作区。**不用**患者端的四胶囊底部导航，改用操作条。

```css
.ds-doctor-actionbar {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 64px;
  background: var(--doctor-panel);
  border-top: 1px solid var(--doctor-line);
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 16px;
  box-shadow: 0 -4px 16px rgba(31, 42, 68, 0.06);
  flex-shrink: 0;
}
/* 典型布局：左侧文字链（拒绝/返回）+ 右侧主按钮 flex:1（确认/通过） */
/* 或：次按钮 + 主按钮 flex:1 */
```

### 4.10 主任务卡（Main Task Card）

**用途**: 工作站首页突出展示当前优先任务。

```css
.ds-doctor-main-task {
  border-radius: var(--radius-md); /* 14px */
  background: var(--doctor-panel);
  border: 1px solid rgba(0, 82, 217, 0.18);
  box-shadow: 0 2px 8px rgba(0, 82, 217, 0.07);
  padding: 14px;
}
/* 顶部 kicker 标签：蓝底圆角胶囊 24px高，11px/800 */
/* 标题：18px/900 --doctor-text */
/* 描述：12px/700 --doctor-sub line-height 1.55 */
/* 底部操作行：主按钮 + 次按钮，gap 8px，margin-top 13px */
```

---

## 5. Layout（布局）

### 5.1 手机内屏栅格

- **内屏尺寸**: 390 × 844px（固定，iPhone 14 比例）
- **安全区**: 顶部状态栏 42px + 顶部栏区域，底部操作条 64px（如有）
- **内容区水平边距**: 16px 左右
- **内容区垂直间距**: 区块间 14px，卡片内边距 14px

### 5.2 间距体系（Spacing）

> 全部复用 `--space-*` 变量。

| Token | 值 | 医生端使用场景 |
|-------|-----|---------------|
| `--space-1` | 4px | 图标与文字间距、chip 内部微调 |
| `--space-2` | 8px | 列表项 gap、按钮组间距、卡片内元素间距 |
| `--space-3` | 12px | 卡片内边距（紧凑）、列表行 padding、分块标题间距 |
| `--space-4` | 16px | 卡片标准内边距、内容区水平边距、区块间距 |
| `--space-5` | 20px | 大卡片内边距、重要区域间距 |
| `--space-6` | 24px | 顶部栏内边距、页面级大间距 |

### 5.3 圆角体系（Radius）

> 医生端用**低圆角**，主用 sm / md / lg，不用 2xl 和 pill（状态标签 chip 也不用 pill）。

| Token | 值 | 医生端使用场景 |
|-------|-----|---------------|
| `--radius-xs` | 7px | 状态标签 chip、来源 badge |
| `--radius-sm` | 10px | **按钮圆角**、指标卡、待办图标、输入框 |
| `--radius-md` | 14px | **标准卡片圆角**、列表容器、档案分块、AI辅助卡 |
| `--radius-lg` | 18px | **大卡片圆角**、主任务卡、顶部渐变栏 |
| `--radius-xl` | 22px | 仅特殊强调卡片（少用） |
| `--radius-2xl` | 26px | 医生端**不用** |
| `--radius-pill` | 999px | 仅顶部 kicker 标签（胶囊形），其余不用 |

---

## 6. Depth & Elevation（深度与层级）

### 6.1 阴影体系

| 层级 | 阴影值 | CSS 来源 | 使用场景 |
|------|--------|----------|---------|
| 无阴影 | none | — | 列表行、内嵌字段行、分割块 |
| 卡片轻阴影 | `0 2px 8px rgba(31,42,68,0.06)` | 自定义 | 标准卡片、指标卡、待办列表、档案分块 |
| 主任务阴影 | `0 2px 8px rgba(0,82,217,0.07)` | 自定义 | 主任务卡、AI辅助卡（蓝色调阴影） |
| 浮层阴影 | `0 16px 44px rgba(31,42,68,0.16)` | `--shadow-doctor` | 弹窗、浮层、底部操作条投影 |
| 手机框阴影 | `0 42px 88px rgba(15,23,42,0.38), 0 16px 34px rgba(15,23,42,0.22), 0 0 0 1px rgba(255,255,255,0.16) inset` | `--shadow-showcase-device` | 展示外壳手机框 |

### 6.2 Z-index 规范

| 层级 | Z-index | 使用场景 |
|------|---------|---------|
| 内容区 | 0 | 列表、卡片、字段块 |
| 顶部栏（sticky） | 10 | 导航栏、顶部渐变栏 |
| 底部操作条 | 10 | 固定底部操作区 |
| 状态标签/角标 | 5 | chip、badge（相对卡片内） |
| 弹窗/浮层 | 100 | 确认弹窗、下拉菜单 |
| 遮罩 | 90 | 弹窗背景遮罩 |

---

## 7. Cautions（注意事项）

### 7.1 禁止（Never Do）

- **禁止**使用患者端的青绿渐变 `linear-gradient(234deg, #03d49f, #01a1ff)` 作为医生端主色——医生端统一用蓝色 `#0052d9`
- **禁止**使用 emoji 或单字占位作为功能图标（如用"✓"代替确认图标、"QR"代替扫码图标）
- **禁止**使用大圆角（22px+）和胶囊形按钮——医生端是工作台不是消费应用
- **禁止**将橙色用于普通强调或装饰——橙色仅限"待确认"语义
- **禁止**将红色用于普通按钮——红色仅限"异常/风险/删除"
- **禁止**在列表行中使用患者端的圆角任务卡样式——医生端列表用低圆角矩形 + 分割线
- **禁止**使用渐变文字、阴影文字、描边文字等装饰性文字效果
- **禁止**在医生端使用患者端的四胶囊底部导航
- **禁止**在 AI 诊疗辅助卡片中省略"诊疗辅助建议"标题——必须明确标注是辅助建议而非诊断结论
- **禁止**使用"等待医生确认"作为按钮文案——医生端自己是操作方，用"确认"/"通过"/"驳回"

### 7.2 推荐（Prefer）

- 功能图标统一用 SVG 线性图标（stroke 1.5–2px），风格统一为 outline 或 duotone，不混用
- 列表行用分割线分隔，不用卡片间隙——高密度场景下分割线更紧凑
- 数字指标右对齐，文字信息左对齐
- 状态标签放在列表行右侧，时间放在状态标签下方或更右
- 字段值与字段名分行显示时，字段名在上（12px 灰色），字段值在下（13px 深色加粗）
- AI 辅助内容用左竖条颜色区分语义（蓝=依据、红=风险、绿=建议）

---

## 8. Responsive Behavior（响应式行为）

### 8.1 展示场景

医生端 Demo 为**固定手机框展示**，不做响应式适配。所有页面在 390×844px 内屏内完成布局。

### 8.2 多屏切换

Demo 内部通过 JS 切换 `.screen.active` 实现多屏切换，不做路由。每个 screen 独立滚动。

### 8.3 横向布局规则

- 单列布局为主（手机端宽度限制）
- 指标卡可用 3 列 grid（gap 8px）
- 按钮组用 flex（gap 8px），主按钮 `flex:1`
- 字段行用 flex space-between（字段名左 + 字段值右）
- 不使用 grid 超过 3 列

### 8.4 滚动规则

- 内容区 `.body` 独立滚动，隐藏滚动条（`::-webkit-scrollbar { display: none }`）
- 底部操作条固定不滚动
- 顶部栏固定不滚动（sticky 或固定高度）

---

## 9. Icon Rules（图标规则）

### 9.1 图标体系

- **类型**: SVG 线性图标（outline 风格），stroke-width 1.5–2px
- **尺寸**: 功能图标 20×20px（按钮内）、24×24px（列表图标位）、16×16px（辅助标注）
- **颜色**: 继承当前文字色，或使用 `currentColor`
- **来源**: 优先使用 Lucide / Heroicons (outline) 风格，统一一套不混用

### 9.2 必须使用真实图标的场景

| 场景 | 图标 | 说明 |
|------|------|------|
| 确认按钮 | check-circle / check | 确认/通过操作 |
| 扫码按钮 | scan-line / qr-code | 建档码、扫码就诊 |
| 返回按钮 | chevron-left | 详情页导航返回 |
| 待办图标 | clipboard-list / alert-circle | 根据任务类型选择 |
| 患者头像位 | user-round | 无照片时用 initials 圆形 |
| AI辅助标识 | sparkles / brain-circuit | AI 诊疗辅助卡片顶部 |
| 风险标识 | alert-triangle | 风险预警 |
| 时间标识 | clock | 时间戳前缀 |
| 来源标识 | file-text / upload | 来源标记 badge |
| 设置/更多 | settings / more-horizontal | 顶部栏右侧 |

### 9.3 禁止

- 禁止用 emoji（如 ✅ ⚠️ 📱）代替功能图标
- 禁止用单字（如"扫""确""返"）占位
- 禁止用纯色方块占位图标位
- 禁止混用 filled 和 outline 风格图标

---

## 10. Showcase Shell（展示外壳规范）

> 医生端与患者端共享同一展示外壳，内部色板不同。

### 10.1 外层背景

```css
body {
  background: #1a1a2e; /* 深色演示背景 */
  min-height: 100vh;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 24px;
  overflow-x: auto;
}
```

### 10.2 手机框

```css
.ds-phone {
  width: 390px;
  min-width: 390px;
  height: 844px;
  border-radius: 44px;
  background: #ffffff;
  overflow: hidden;
  position: relative;
  box-shadow: 0 30px 80px rgba(0, 0, 0, 0.6); /* 深色背景上的强投影 */
  display: flex;
  flex-direction: column;
}
```

### 10.3 内屏背景

```css
.ds-doctor-screen {
  width: 100%;
  height: 100%;
  background: var(--doctor-bg); /* #eef2f7 浅灰 */
  overflow: hidden;
  position: relative;
  display: flex;
  flex-direction: column;
}
```

### 10.4 多屏切换机制

```css
.ds-doctor-screen { display: none; }
.ds-doctor-screen.active { display: flex; }
```

### 10.5 状态栏

```css
.ds-doctor-statusbar {
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  font-size: 13px;
  font-weight: 700;
  color: var(--doctor-text);
  flex-shrink: 0;
}
```

---

## 附录 A：CSS 变量速查（直接复制使用）

```css
:root {
  /* 字体 */
  --gout-font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;

  /* 医生端色板 */
  --doctor-primary: #0052d9;
  --doctor-primary-2: #1f73f1;
  --doctor-bg: #eef2f7;
  --doctor-panel: #ffffff;
  --doctor-line: #e5eaf2;
  --doctor-text: #1d2530;
  --doctor-sub: #566579;
  --doctor-hint: #8a94a6;
  --doctor-blue-soft: #eaf2ff;
  --doctor-orange: #ed7b2f;
  --doctor-orange-soft: #fff4e8;
  --doctor-green: #2ba471;
  --doctor-green-soft: #eaf8f2;
  --doctor-red: #d54941;
  --doctor-red-soft: #fff0ee;

  /* 圆角 */
  --radius-xs: 7px;
  --radius-sm: 10px;
  --radius-md: 14px;
  --radius-lg: 18px;
  --radius-xl: 22px;
  --radius-2xl: 26px;
  --radius-pill: 999px;

  /* 阴影 */
  --shadow-doctor: 0 16px 44px rgba(31, 42, 68, 0.16);
  --shadow-doctor-card: 0 2px 8px rgba(31, 42, 68, 0.06);
  --shadow-doctor-task: 0 2px 8px rgba(0, 82, 217, 0.07);

  /* 字号 */
  --text-xxs: 10px;
  --text-xs: 11px;
  --text-sm: 12px;
  --text-md: 13px;
  --text-base: 14px;
  --text-lg: 16px;
  --text-xl: 18px;
  --text-2xl: 22px;

  /* 间距 */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
}
```

---

## 附录 B：页面清单与核心组件映射

| 页面 | 核心组件组合 | 关键状态色 |
|------|-------------|-----------|
| 登录页 | 表单卡(手机号输入 + 已绑定医生展示) + 主按钮 | 蓝主色 |

> **登录方式（强制）**：医生端登录页**使用手机号登录**，不使用工号。登录表单为「手机号输入框（可输入，默认演示号 138****0666）+ 已绑定医生展示（王文龙 医生 · 风湿免疫科 · 温岭市第一人民医院）」，点击「登录工作台」进入。禁止出现"工号"字段。
| 工作站首页 | 渐变顶栏 + 指标卡grid + 主任务卡 + **诊间快捷入口(grid)** + 待办列表 | 蓝 + 橙(待办) |

> **工作台入口闭环（强制）**：登录进入工作台后，除主任务卡「去确认档案」「患者队列」按钮外，必须在「待办」上方提供**「诊间快捷入口」**区块（3 列 grid 图标卡），覆盖：看诊前资料、AI 辅助、语音接诊、就诊码、主动建档、复诊逾期，点击直达对应屏。禁止仅依赖右侧全局导航才能进入诊间屏——登录后第一屏应一眼可见完整诊间能力。
| 患者队列 | 导航栏 + 搜索框 + 患者列表行(多) | 橙/绿/红(状态) |
| 患者详情档案 | 导航栏 + 档案分块(多) + 来源badge | 蓝 + 状态色 |
| 看诊前资料 | 导航栏 + 资料分块 + 确认状态 | 绿(已确认) + 橙(待确认) |
| AI辅助 | 导航栏 + AI辅助卡(依据/风险/建议) + 确认按钮 | 蓝 + 红(风险) + 绿(建议) |
| 医生确认页 | 导航栏 + 确认内容卡 + 底部操作条 | 蓝(确认) + 红(驳回) |
| 建档码 | 导航栏 + 二维码区 + 操作说明 | 蓝主色 |
| 复诊逾期 | 导航栏 + 逾期列表(红色标注) + 操作按钮 | 红(逾期) + 橙(即将逾期) |

---

## 附录 C：与患者端的差异对照

| 维度 | 患者端 | 医生端 |
|------|--------|--------|
| 主色 | 青绿 `#03d49f` + 蓝 `#01a1ff` 渐变 | 蓝色 `#0052d9`（不渐变主色） |
| 调性 | 温暖、鼓励、引导式 | 专业、紧凑、任务驱动 |
| 圆角 | 大圆角 22–26px | 低圆角 10–18px |
| 行高 | 宽松 1.55–1.6 | 紧凑 1.2–1.45 |
| 字号 | 偏大 14–16px 常用 | 偏小 12–14px 常用 |
| 信息密度 | 低（大卡片、大间距） | 高（紧凑列表、分割线） |
| 底部导航 | 四胶囊浮动导航 | 底部操作条（按页面定制） |
| 装饰 | 渐变、柔光、圆形装饰 | 无装饰、纯色、直线 |
| 图标 | 圆角方块彩色图标 | 线性 SVG outline 图标 |
| 展示外壳 | 深色背景 + 手机框 | **相同**（共享外壳） |
