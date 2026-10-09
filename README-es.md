# dsh-spc-gbt-adapter — Constantes de cartas de control y verificación de la coherencia de los índices de capacidad del proceso

[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)

`dsh-spc-gbt-adapter` lee un registro de cartas de control —filas organizadas con los nombres de columna del propio registro, en chino o en inglés— y comprueba la coherencia aritmética y de tabla de constantes de ese registro: que se registren la característica y el tipo de carta, que los límites de control se sigan de la línea central, la amplitud y las constantes de carta que el paquete fija, que la línea central quede entre los límites, que el Cp y el Cpk registrados cumplan sus definiciones, que el tamaño del subgrupo sea uno de los cubiertos por la tabla de constantes y que la cabecera indique el producto y el proceso.

## Cómo se ve la salida

![Terminal demo of dsh-spc-gbt-adapter: real output over its SP-003 fixture](https://raw.githubusercontent.com/PerryLink/dsh-spc-gbt-adapter/main/docs/assets/dsh-spc-gbt-adapter-demo.png)

Salida real de este plugin sobre su propio fixture de prueba `SP-003` — no es un montaje. El paquete de reglas no inventa citas, así que cada hallazgo nombra la cláusula aplicada y advierte que su texto no se obtuvo.

## Qué responde

| Usted pregunta | Qué responde |
|---|---|
| Una fila deja vacíos la característica y el tipo de carta. ¿Se informa de eso? | Sí. `SP-001` exige que, en toda fila que traiga una de esas dos columnas, se rellene al menos uno de `characteristic` y `chartType`, e informa de la fila cuando ambos están vacíos. Comprueba que uno de los dos esté registrado, no si esa característica debería llevarse en una carta ni si el tipo de carta se eligió bien. |
| Los límites de control registrados no coinciden con lo que dan la línea central, la amplitud y las constantes. | `SP-002` recalcula `ucl` y `lcl` a partir de `centerLine`, `range` y el coeficiente de ese `sampleSize`, con una tolerancia de 0.005, e informa de la fila con el par registrado y el esperado. Solo comprueba que esos números concuerden entre sí: no si los límites o la amplitud son correctos, y nunca si el proceso está bajo control. La tabla fijada es la de la carta X̄-R: una carta X̄-s, I-MR, p o c usa otros coeficientes, así que desactive la regla o sustituya `coefficients`. |
| La línea central está registrada por encima del límite de control superior. | `SP-003` exige `lcl` ≤ `centerLine` ≤ `ucl` en toda fila que rellene los tres, e informa de la fila cuyo orden falla. Solo comprueba el orden de los tres números, no si se calcularon bien. Un límite inferior de 0 es una forma normal en la carta de amplitudes y no se informa por ese motivo. |
| El registro trae Cp y Cpk, pero el informe no dice nada de ellos. ¿Por qué? | `SP-004` solo se ejecuta en filas que traigan `cp` o `cpk` junto con `usl`, `lsl`, `stdDev` y `mean`; cuando ninguna fila los trae todos, la regla informa `skipped` en lugar de pasar en silencio. Donde se ejecuta contrasta las dos definiciones, Cp = (USL − LSL) / 6σ y Cpk = min(USL − X̄, X̄ − LSL) / 3σ, con una tolerancia de 0.02. Una diferencia suele significar que se mezcló el criterio de σ: Cp/Cpk usan la desviación típica dentro del subgrupo y Pp/Ppk la global. No decide si la capacidad es suficiente. |
| ¿Es suficiente la capacidad de este proceso? | Eso no lo responde la comprobación. `SP-005` solo informa de un `cpk` registrado que queda por debajo del criterio que usted configure, y viene con `threshold: 0`, es decir sin configurar, de modo que pasa a `skipped` en vez de inventar un criterio; los habituales 1.33 y 1.67 dependen del sector, del cliente y de la importancia de la característica. Un hallazgo de esta regla significa que el valor está por debajo de su propio criterio, no que el proceso no sea apto, y se informa con severidad `info`. |
| Nuestros subgrupos tienen 15 mediciones cada uno. ¿Qué ocurre? | `SP-007` informa de la fila: la tabla de constantes fijada en el paquete solo cubre tamaños de subgrupo de 2 a 10. Sin entrada para ese tamaño, `SP-002` tampoco puede consultar los coeficientes, así que también lo informa en lugar de callar. La regla comprueba si el tamaño es un escalón listado, no si ese tamaño de subgrupo conviene al proceso. Para trabajar con subgrupos mayores, añada el escalón a los `coefficients` de `SP-002` y amplíe los `values` de esta regla: es una edición del paquete de reglas, no del código. |

## Normas que sigue

| Documento | Número | Reglas que lo citan |
|---|---|---|
| 《常规控制图》 | GB/T 17989.2—2020（控制图 第2部分：常规控制图，采标 ISO；替代已废止的 GB/T 4091—2001；条号本次未取得） | SP-001, SP-002, SP-003, SP-004, SP-005, SP-006, SP-007 |

**Boundary:** this plugin checks a **控制图台账** for arithmetic and constant-table consistency — that the
characteristic and chart type are recorded, that the control limits follow from the centre line, the
dispersion statistic and the chart constants, that the centre line sits between the limits, that Cp and Cpk
follow their definitions, that the subgroup size is one the constant table covers, and that the chart names
its product and process. It does **not** decide whether a process is in control, whether a trend is present,
or whether capability is sufficient. **Reading a chart needs the pattern rules; sufficiency depends on the
customer's acceptance criterion.**

> ### ⚠️ What this pack can and cannot cite
>
> The control-limit coefficients (A₂, D₃, D₄) and the capability-index definitions do have a home:
> **GB/T 4091《常规控制图》** (identical to the ISO 7870 series). Those coefficients are *mathematical
> constants* that vary only with subgroup size, which is why they can be frozen into the rule pack. **But the
> verification pass did not obtain GB/T 4091's verbatim text**, so every rule's `excerpt` says so plainly and
> every rule stays at `warn` or `info` rather than claiming a quotation.
>
> Three limits are worth knowing before trusting a finding:
>
> - **`SP-002` assumes the X̄-R chart.** An X̄-s, I-MR, p or c chart uses entirely different coefficients, so
>   the rule will report differences. Disable it, or replace `coefficients` with the right table — a rule-pack
>   edit, not a code change.
> - **The coefficient table covers n = 2…10.** `SP-007` reports any subgroup size outside that range, so
>   "cannot look it up" is never silently read as "no problem".
> - **`SP-005`'s criterion ships as `0`, meaning "not configured".** Typical values are 1.33 and 1.67, but the
>   right one depends on the industry, the customer and how critical the characteristic is, so the rule
>   reports that it could not run rather than inventing one.
>
> The σ convention matters too: Cp/Cpk use the **within-subgroup** standard deviation while Pp/Ppk use the
> **overall** one. A mismatch between a ledger's σ and its index is the commonest cause of a `SP-004` finding,
> which is why the finding says so.

## Compatibility

| Superficie | Estado |
|---|---|
| Harness | Rango de peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verificado para aceptar tanto `0.2.0-rc.2` como `0.2.1-alpha.1`. **No se declara `engines.dsh`**: no tiene lector y no puede rechazar ningún host |
| Node | `^22.19.0 || >=24.0.0` |
| Plataformas | Todas (ESM puro; sin código nativo, sin red, sin llamada al modelo) |
| Modo de herramienta | Funciona en `native`, `ptc` y `both`; para un directorio completo use `ptc` |

## What it does

La tabla de reglas, los campos y el comportamiento detallado están en [README.md](README.md#what-it-does) (versión principal en inglés). El plugin sólo enumera divergencias literales frente a las cláusulas citadas e indica en `skipped` cada comprobación que no pudo ejecutarse.

## Install

```sh
dsh plugin --profile <name> add dsh-spc-gbt-adapter
dsh --profile <name> --dump-config | grep 'dsh-spc-gbt-adapter'
```

## Configuration

Todos los parámetros ajustables viven en el esquema Schemastery de `src/config.ts`, por lo que se cambian desde `cordis.yml` sin tocar el código; los umbrales por regla están en el paquete de reglas bajo `rules/`.

| Clave | Tipo | Predeterminado | Descripción |
|---|---|---|---|
| `rulesFile` | string | `rules/spc-gbt-adapter.yaml` | Ruta del paquete de reglas, relativa a la raíz del paquete |
| `disabledRules` | string[] | `[]` | Ids de reglas que se dejan de ejecutar; cada una aparece en `skipped` |
| `onlyRules` | string[] | `[]` | Ejecutar solo estas reglas; vacío ejecuta todas |
| `skipNotes` | string | `""` | Nota añadida a cada motivo de `skipped` |
| `timeoutMs` | number | `120000` | Presupuesto de tiempo de espera cooperativo de la herramienta |

## Material format

Acepta JSON o YAML. El ejemplo completo de campos está en [README.md](README.md#material-format) (versión principal en inglés). Los campos son opcionales en la capa de lectura y los valida el motor, de modo que una exportación parcial produce hallazgos sobre lo que falta en lugar de un fallo.

## Rule sources

Los datos de las reglas están separados del código: cada regla lleva documento, número, cláusula en la numeración propia de la fuente, extracto literal y URL de origen. El cargador impone que el extracto sea una cita real de al menos ocho caracteres y que una comprobación basada sólo en un principio general (`kind: derived-from-principle`, tope `warn`) o en una política local (`kind: institutional-configuration`, tope `info`) nunca se declare `error`.

Los límites verificados y las conclusiones deliberadamente **no** afirmadas están en [README.md](README.md#rule-sources) (versión principal en inglés) y en `rules/evidence/`.

## Troubleshooting

- **El plugin se instala pero la herramienta no aparece**: compruebe que `main` resuelve a `lib/index.mjs` y que `pnpm run build` lo generó.
- **`dsh plugin add` rechaza el paquete**: la faixa de peers cubre `0.1.x` y `0.2.x`; fuera de ella, conceda una exención explícita con `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`.
- **Una regla no se ejecutó**: lea el arreglo `skipped`.
- **`check` informa `manifest-peers` como fallo**: es un problema conocido de `dsh-plugin-dev`; el runtime aplica la compatibilidad al instalar.
- **Los horarios parecen desplazados**: toda la aritmética es de hora local sobre las cadenas entregadas.

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-spc-gbt-adapter
```

El último comando copia el kit compartido de `../_shared` a `src/shared/`; vuelva a ejecutarlo tras cada cambio compartido.

## License

[Apache License 2.0](LICENSE) © 2026 dsh-spc-gbt-adapter contributors.
