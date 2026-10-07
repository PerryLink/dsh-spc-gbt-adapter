/**
 * dsh-spc-gbt-adapter — table shape and material contract.
 *
 * The plugin is data-only: this file declares which columns the material may use
 * and how they map onto canonical field names; the shared kit supplies the reader
 * and the check engine, and the rule pack declares every check. Adding a check
 * that fits an existing kind is a rule-pack edit, not a code change.
 */

import { canonicaliseRow, parseTable, type TableSpec } from './shared/table.ts'
import { runTableCheck, type TableCheckOptions, type TableInput } from './shared/rows.ts'
import type { Ruleset } from './shared/rules.ts'

/** Tool id exposed to the model, and the row id in `cordis.patch.yml`. */
export const TOOL_NAME = 'spc_gbt_adapter'

/** The register's column aliases, declared once so both the spec and the guard see them. */
const COLUMNS = {
  chartNo: ['控制图编号', '图表编号', '编号', 'chartNo'],
  characteristic: ['特性名称', '质量特性', '控制特性', 'characteristic', 'ctq'],
  chartType: ['控制图类型', '图种', 'chartType'],
  subgroupNo: ['子组号', '样本号', '组号', 'subgroupNo'],
  sampleSize: ['子组大小', '样本容量', '样本量', 'sampleSize', 'n'],
  mean: ['均值', '平均值', 'Xbar', 'mean'],
  range: ['极差', 'R', 'range'],
  stdDev: ['标准差', '组内标准差', 'sigma', 'stdDev'],
  ucl: ['上控制限', 'UCL', 'ucl'],
  lcl: ['下控制限', 'LCL', 'lcl'],
  centerLine: ['中心线', 'CL', 'centerLine'],
  cp: ['Cp', '过程能力指数Cp', 'cp'],
  cpk: ['Cpk', '过程能力指数Cpk', 'cpk'],
  pp: ['Pp', 'pp'],
  ppk: ['Ppk', 'ppk'],
  usl: ['上规格限', 'USL', '规格上限', 'usl'],
  lsl: ['下规格限', 'LSL', '规格下限', 'lsl'],
  measuredAt: ['测量日期', '采样日期', '日期', 'measuredAt'],
  outOfControl: ['失控', '是否失控', '异常', 'outOfControl'],
} as const

/** How the material declares its table. */
export const SPEC: TableSpec = {
  rowKeys: ['rows', 'items', 'samples', '子组'],
  columns: COLUMNS,
  header: {
  productNo: ['productNo', '产品编号', '零件号'],
  processName: ['processName', '工序名称', '过程名称'],
  chartNo: ['chartNo', '控制图编号'],
  subgroupSize: ['subgroupSize', '子组大小', '样本容量'],
  checkedAt: ['checkedAt', '核对日期'],
  },
}

/** Fields the material must carry somewhere for the reader to accept it. */
export const REQUIRE_ANY_OF = [
  '特性名称',
  'characteristic',
  '控制图类型',
  'chartType',
  '子组号',
  'subgroupNo',
  '均值',
  'mean',
]

/**
 * Parse the material and attach its canonical field names.
 * @param source - JSON or YAML text.
 * @param target - description of where the material came from.
 * @returns the normalized table, with each row's aliases resolved to field names.
 */
export function parseMaterial(source: string, target: string): TableInput {
  const table = parseTable(source, target, {
    ...SPEC,
    ...(REQUIRE_ANY_OF === undefined ? {} : { requireAnyOf: REQUIRE_ANY_OF }),
  })
  for (const row of table.rows) canonicaliseRow(row, SPEC)
  return table
}

/**
 * Run the rule pack against the material.
 * @param input - normalized table.
 * @param ruleset - validated rule pack.
 * @param options - plugin identity, clock value, rule selection and overrides.
 * @returns the report.
 */
export function runCheck(input: TableInput, ruleset: Ruleset, options: TableCheckOptions) {
  return runTableCheck(input, ruleset, options)
}

export type { TableCheckOptions, TableInput }
