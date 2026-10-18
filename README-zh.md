# dsh-spc-gbt-adapter — 控制图常数与过程能力指数核对

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)

`dsh-spc-gbt-adapter` 读取一份控制图台账——行按台账自身的列名组织，中英文列名均可——核对这份台账自身的算术与常数表自洽性：特性名称与控制图类型是否填写、控制限是否由中心线、极差与规则库固化的控制图常数推出、中心线是否落在上下控制限之间、填报的 Cp 与 Cpk 是否符合定义式、子组大小是否落在常数表覆盖的档位内、表头是否写明产品与工序。

## Install

```sh
dsh plugin --profile <name> add dsh-spc-gbt-adapter
dsh --profile <name> --dump-config | grep 'dsh-spc-gbt-adapter'
```

## 实际输出长什么样

![Terminal demo of dsh-spc-gbt-adapter: real output over its SP-003 fixture](https://raw.githubusercontent.com/PerryLink/dsh-spc-gbt-adapter/main/docs/assets/dsh-spc-gbt-adapter-hero.png)

![Animated terminal demo of dsh-spc-gbt-adapter](https://raw.githubusercontent.com/PerryLink/dsh-spc-gbt-adapter/main/docs/assets/dsh-spc-gbt-adapter-demo.gif)

本插件对自己 `SP-003` 测试夹具的**真实输出**，不是示意图。规则库不伪造引文，因此每条发现都会同时写明所引条款，以及该条款原文本次未取得。

## 它回答什么问题

| 你会问 | 它怎么答 |
|---|---|
| 某行的特性名称与控制图类型都空着，会被报出吗？ | 会。`SP-001` 要求凡是带有这两列之一的行，`characteristic` 与 `chartType` 至少填写一项，两项都空即报出该行。它只核对是否填了一项，不判断该特性是否应当作控制图、图种是否选对。 |
| 台账里填的控制限，与中心线、极差和常数表算出来的对不上。 | `SP-002` 按 `centerLine`、`range` 与该行 `sampleSize` 对应的系数重算 `ucl` 与 `lcl`（容差 0.005），把填报的一组与应有的一组一并报出。它只核对这些数彼此是否自洽——不判断控制限或极差算得对不对，更不判断过程是否受控。固化的系数表是 X̄-R 图的：X̄-s 图、单值移动极差（I-MR）图、p 图或 c 图系数不同，此时请停用本条或替换 `coefficients`。 |
| 中心线填得比上控制限还高。 | `SP-003` 要求凡是三个数都填了的行满足 `lcl` ≤ `centerLine` ≤ `ucl`，次序不满足即报出该行。它只核对这三个数的次序，不判断这些数值算得是否正确。下控制限为 0 是极差图的正常形态，本条不会因此报差异。 |
| 台账里填了 Cp 和 Cpk，报告里却什么都没说，为什么？ | `SP-004` 只在同时填写 `cp` 或 `cpk` 与 `usl`、`lsl`、`stdDev`、`mean` 的行上执行；没有任何这样的行时，本条报告 `skipped`，而不是静默通过。执行时它核对两个定义式：Cp = (USL − LSL) / 6σ、Cpk = min(USL − X̄, X̄ − LSL) / 3σ，容差 0.02。出现差异通常意味着 σ 的口径混用了：Cp/Cpk 用组内标准差，Pp/Ppk 用总体标准差。本条不判断能力是否足够。 |
| 这个过程的能力够不够？ | 这个问题本条不作回答。`SP-005` 只报出低于你配置准则的 `cpk`，而它出厂是 `threshold: 0`，即未配置，因此进 `skipped`，而不是替你编一个准则；常见的 1.33、1.67 因行业、顾客与特性重要度而异。命中本条只表示低于你自己配置的准则，不表示过程能力不合格；本条以 `info` 级报出。 |
| 我们的子组每个有 15 个测量值，会怎样？ | `SP-007` 会报出该行：规则库固化的常数表只覆盖子组大小 2~10。该档位没有系数，`SP-002` 也查不到系数，因此同样报出，而不是静默通过。本条只核对档位是否在册，不判断子组大小选得是否恰当。要用更大的子组，请把该档位补进 `SP-002` 的 `coefficients` 并同步扩大本条的 `values`——改规则库即可，无需改代码。 |

## 依据的标准

| 文件 | 文号 | 引用它的规则 |
|---|---|---|
| 《常规控制图》 | GB/T 17989.2—2020（控制图 第2部分：常规控制图，采标 ISO；替代已废止的 GB/T 4091—2001；条号本次未取得） | SP-001, SP-002, SP-003, SP-004, SP-005, SP-006, SP-007 |

**边界（中文译文，以英文原文为准）：** 本插件核对一份 **控制图台账** 的算术与常数表一致性——是否记录特性与控制图类型，控制限是否由中心线、离散统计量与图常数推出，中心线是否落在控制限之间，Cp 与 Cpk 是否符合其定义，子组大小是否为常数表所覆盖的取值，以及控制图是否写明其产品与工序。它**不**判定过程是否处于受控状态、是否存在趋势，或过程能力是否充分。**读图需要模式规则；能力是否充分取决于顾客的验收准则。**

> ### ⚠️ 本规则库能引用什么、不能引用什么（以英文原文为准）
>
> 控制限系数（A₂、D₃、D₄）与能力指数的定义确有出处：**GB/T 4091《常规控制图》**（与 ISO 7870 系列等同）。这些系数是*数学常数*，只随子组大小变化，因此可以固化进规则库。**但核验环节未取得 GB/T 4091 的逐字原文**，所以每条规则的 `excerpt` 都照实写明这一点，每条规则都停留在 `warn` 或 `info`，而不去声称拥有引文。
>
> 在相信任何一条发现之前，有三项局限值得了解：
>
> - **`SP-002` 假定的是 X̄-R 控制图。** X̄-s、I-MR、p 或 c 控制图使用的系数完全不同，因此该条规则会报出差异。请停用它，或者把 `coefficients` 换成正确的系数表——这是改规则库，不是改代码。
> - **系数表覆盖 n = 2…10。** `SP-007` 会报出任何超出该范围的子组大小，所以「查不到」永远不会被静默读成「没有问题」。
> - **`SP-005` 的判定标准出厂为 `0`，含义是「未配置」。** 典型值是 1.33 与 1.67，但哪个才对取决于行业、顾客以及该特性的关键程度，因此该条规则会报告自己无法执行，而不会凭空编一个值。
>
> σ 的口径也很重要：Cp/Cpk 使用**组内**标准差，而 Pp/Ppk 使用**整体**标准差。台账中的 σ 与其指数不匹配，是 `SP-004` 发现的最常见成因，这也是该条发现会写明这一点的原因。

## Compatibility

| 项目 | 状态 |
|---|---|
| Harness | 对等版本范围 `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` —— 已实测同时接受 `0.2.0-rc.2` 与 `0.2.1-rc.2`。**已声明 `engines.dsh`**：0.2.1 起由宿主单独裁决，范围为 `>=0.2.1-0 <0.3.0` |
| Node | `^22.19.0 || >=24.0.0` |
| 平台 | 全平台（纯 ESM；无原生代码、无联网、不调用模型） |
| 工具模式 | `native` / `ptc` 均可；批量校验整个目录时建议 `ptc`，schema 成本只付一次 |

## What it does

规则表、字段说明与行为细节见 [README.md](README.md#what-it-does)（英文主版本）。本插件只列出材料与所引条款之间的字面差异，并对无法执行的检查在 `skipped` 中逐项说明。

## Configuration

全部可调参数都在 `src/config.ts` 的 Schemastery schema 中，只改 `cordis.yml` 即可生效，无需改代码；逐条阈值在 `rules/` 下的规则库文件里。

| 键 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `rulesFile` | string | `rules/spc-gbt-adapter.yaml` | 规则库文件路径，相对插件包根目录 |
| `disabledRules` | string[] | `[]` | 要停用的规则 id 列表；每条都会出现在 `skipped` 中 |
| `onlyRules` | string[] | `[]` | 只执行这些规则 id；留空表示执行全部规则 |
| `skipNotes` | string | `""` | 附加到每条 `skipped` 说明后的备注 |
| `timeoutMs` | number | `120000` | 工具协作式超时预算（毫秒） |

## Material format

支持 JSON 与 YAML。完整字段示例见 [README.md](README.md#material-format)（英文主版本）。字段在读取层是可选的，由检查引擎校验，因此部分导出的材料会产生"缺项"类差异，而不是让程序崩溃。

## Rule sources

规则数据与代码分离，每条规则都带文件名、文号、按原文自身编号体系的条款号、逐字摘录与来源地址。加载期强制：摘录必须是真实引文且不少于八个字符；依据仅为原则性条款（`kind: derived-from-principle`，严重级上限 `warn`）或本机构配置（`kind: institutional-configuration`，上限 `info`）的检查不得标为 `error`。夸大依据的规则库会在加载期失败，而不会产出一份看起来很有底气的报告。

核验中确认的边界与"刻意没有作出的结论"见 [README.md](README.md#rule-sources)（英文主版本）与随包的 `rules/evidence/` 目录。

## Troubleshooting

- **插件装上了但工具不出现**：确认 `main` 指向 `lib/index.mjs` 且 `pnpm run build` 已生成该文件；`main` 写错会让加载器静默跳过该条目。
- **`dsh plugin add` 报版本不兼容**：peer 范围覆盖 `0.1.x` 与 `0.2.x`；若运行时在其之外，可显式豁免：`dsh plugin --profile <name> allow-version <包名@版本> --dsh-version <runtime> --accept-risk`
- **某条规则没有执行**：查看 `skipped` 数组，其中写明了规则 id 与原因。
- **`check` 报 `manifest-peers` 失败**：静态检查器比对的是一份早于 0.2 世代的硬编码 peer 范围；安装期的 peer 校验以运行时为准。这是 `dsh-plugin-dev` 的已知上游问题。
- **时间看起来偏移**：全部计算都是对输入字符串做墙上时钟运算，不做时区换算。

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-spc-gbt-adapter
```

第 4 项把 `../_shared` 的共享件同步进 `src/shared/`；每次改动共享件后都要重跑。

## License

[Apache License 2.0](LICENSE) © 2026 dsh-spc-gbt-adapter contributors.
