import { describeTablePlugin } from './table-plugin-suite.ts'
import { Config } from '../src/config.ts'
import { parseMaterial, runCheck, SPEC } from '../src/model.ts'
import { buildView } from '../src/view.ts'
import { inject, name, resolvePackageFile, TOOL_NAME } from '../src/index.ts'

describeTablePlugin({
  name,
  inject,
  TOOL_NAME,
  resolvePackageFile,
  Config,
  rulesFile: 'rules/spc-gbt-adapter.yaml',
  parseMaterial,
  runCheck,
  buildView,
  columnNames: SPEC.columns,
  samples: {
    good: {
      productNo: 'P-2026-001',
      processName: '精车外圆',
      rows: [
        {
          控制图编号: 'Xbar-R-001',
          特性名称: '外径',
          控制图类型: 'Xbar-R',
          子组大小: '5',
          均值: '10.00',
          极差: '0.50',
          标准差: '0.215',
          中心线: '10.00',
          上控制限: '10.2885',
          下控制限: '9.7115',
          上规格限: '10.60',
          下规格限: '9.40',
          Cp: '0.9302',
          Cpk: '0.9302',
        },
      ],
    },
    unknownColumn: { rows: [{ 备注: '甲' }] },
  },
})
