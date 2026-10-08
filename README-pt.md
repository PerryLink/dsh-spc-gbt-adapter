# dsh-spc-gbt-adapter — Constantes de cartas de controlo e verificação da coerência dos índices de capacidade do processo

`dsh-spc-gbt-adapter` lê um registo de cartas de controlo —linhas organizadas pelos nomes de coluna do próprio registo, em chinês ou em inglês— e verifica a coerência aritmética e de tabela de constantes desse registo: se a característica e o tipo de carta estão registados, se os limites de controlo decorrem da linha central, da amplitude e das constantes de carta que o pacote fixa, se a linha central fica entre os limites, se o Cp e o Cpk registados cumprem as suas definições, se a dimensão do subgrupo é uma das cobertas pela tabela de constantes e se o cabeçalho indica o produto e o processo.

## O que ele responde

| Você pergunta | O que ele responde |
|---|---|
| Uma linha deixa vazios a característica e o tipo de carta. Isso é reportado? | Sim. `SP-001` exige que, em cada linha que traga uma dessas duas colunas, esteja preenchido pelo menos um de `characteristic` e `chartType`, e reporta a linha quando ambos estão vazios. Verifica que um deles está registado, não se essa característica deveria ser controlada por carta nem se o tipo de carta foi bem escolhido. |
| Os limites de controlo registados não batem com o que dão a linha central, a amplitude e as constantes. | `SP-002` recalcula `ucl` e `lcl` a partir de `centerLine`, `range` e do coeficiente desse `sampleSize`, com tolerância de 0.005, e reporta a linha com o par registado e o esperado. Verifica apenas que esses números são coerentes entre si: não se os limites ou a amplitude estão corretos, e nunca se o processo está sob controlo. A tabela fixada é a da carta X̄-R: uma carta X̄-s, I-MR, p ou c usa outros coeficientes, pelo que deve desativar a regra ou substituir `coefficients`. |
| A linha central está registada acima do limite de controlo superior. | `SP-003` exige `lcl` ≤ `centerLine` ≤ `ucl` em cada linha que preencha os três, e reporta a linha cuja ordem falha. Verifica apenas a ordem dos três números, não se foram bem calculados. Um limite inferior de 0 é uma forma normal na carta de amplitudes e não é reportado por esse motivo. |
| O registo tem Cp e Cpk, mas o relatório não diz nada sobre eles. Porquê? | `SP-004` só corre em linhas que tragam `cp` ou `cpk` junto com `usl`, `lsl`, `stdDev` e `mean`; quando nenhuma linha traz todos, a regra reporta `skipped` em vez de passar em silêncio. Onde corre, confronta as duas definições, Cp = (USL − LSL) / 6σ e Cpk = min(USL − X̄, X̄ − LSL) / 3σ, com tolerância de 0.02. Uma diferença costuma significar que o critério de σ foi misturado: Cp/Cpk usam o desvio-padrão dentro do subgrupo e Pp/Ppk o global. Não decide se a capacidade é suficiente. |
| A capacidade deste processo é suficiente? | Isso a verificação não responde. `SP-005` apenas reporta um `cpk` registado abaixo do critério que configurar, e vem com `threshold: 0`, ou seja por configurar, pelo que passa a `skipped` em vez de inventar um critério; os habituais 1.33 e 1.67 dependem do setor, do cliente e da importância da característica. Um achado desta regra significa que o valor está abaixo do seu próprio critério, não que o processo seja inapto, e é reportado com severidade `info`. |
| Os nossos subgrupos têm 15 medições cada. O que acontece? | `SP-007` reporta a linha: a tabela de constantes fixada no pacote cobre apenas dimensões de subgrupo de 2 a 10. Sem entrada para essa dimensão, `SP-002` também não consegue consultar os coeficientes, pelo que reporta isso em vez de ficar em silêncio. A regra verifica se a dimensão é um escalão listado, não se essa dimensão de subgrupo serve o processo. Para usar subgrupos maiores, acrescente o escalão aos `coefficients` de `SP-002` e alargue os `values` desta regra: é uma edição do pacote de regras, não do código. |

## Normas que segue

| Documento | Número | Regras que o citam |
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

| Superfície | Estado |
|---|---|
| Harness | Faixa de peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verificada para aceitar tanto `0.2.0-rc.2` quanto `0.2.1-alpha.1`. **`engines.dsh` não é declarado**: não tem leitor e não pode recusar nenhum host |
| Node | `^22.19.0 || >=24.0.0` |
| Plataformas | Todas (ESM puro; sem código nativo, sem rede, sem chamada ao modelo) |
| Modo de ferramenta | Funciona em `native`, `ptc` e `both`; para um diretório inteiro use `ptc` |

## What it does

A tabela de regras, os campos e o comportamento detalhado estão em [README.md](README.md#what-it-does) (versão principal em inglês). O plugin apenas lista divergências literais frente às cláusulas citadas e indica em `skipped` cada verificação que não pôde ser executada.

## Install

```sh
dsh plugin --profile <name> add dsh-spc-gbt-adapter
dsh --profile <name> --dump-config | grep 'dsh-spc-gbt-adapter'
```

## Configuration

Todos os parâmetros ajustáveis ficam no esquema Schemastery de `src/config.ts`, portanto mudam pelo `cordis.yml` sem editar código; os limites por regra ficam no pacote de regras sob `rules/`.

| Chave | Tipo | Padrão | Descrição |
|---|---|---|---|
| `rulesFile` | string | `rules/spc-gbt-adapter.yaml` | Caminho do pacote de regras, relativo à raiz do pacote |
| `disabledRules` | string[] | `[]` | Ids de regras a desativar; cada uma aparece em `skipped` |
| `onlyRules` | string[] | `[]` | Executar apenas estas regras; vazio executa todas |
| `skipNotes` | string | `""` | Nota acrescentada a cada motivo de `skipped` |
| `timeoutMs` | number | `120000` | Orçamento de tempo limite cooperativo da ferramenta |

## Material format

Aceita JSON ou YAML. O exemplo completo de campos está em [README.md](README.md#material-format) (versão principal em inglês). Os campos são opcionais na camada de leitura e validados pelo motor, de modo que uma exportação parcial gera achados sobre o que falta em vez de falhar.

## Rule sources

Os dados das regras ficam separados do código: cada regra traz documento, número, cláusula na numeração própria da fonte, trecho literal e URL de origem. O carregador impõe que o trecho seja citação real de pelo menos oito caracteres e que uma verificação baseada apenas em princípio geral (`kind: derived-from-principle`, teto `warn`) ou em política local (`kind: institutional-configuration`, teto `info`) nunca seja declarada `error`.

Os limites verificados e as conclusões deliberadamente **não** afirmadas estão em [README.md](README.md#rule-sources) (versão principal em inglês) e em `rules/evidence/`.

## Troubleshooting

- **O plugin instala mas a ferramenta não aparece**: confirme que `main` resolve para `lib/index.mjs` e que `pnpm run build` o gerou.
- **`dsh plugin add` recusa o pacote**: a faixa de peers cobre `0.1.x` e `0.2.x`; fora dela, conceda isenção explícita com `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`.
- **Uma regra não executou**: leia o arranjo `skipped`.
- **`check` informa `manifest-peers` como falha**: problema conhecido do `dsh-plugin-dev`; o runtime aplica a compatibilidade na instalação.
- **Os horários parecem deslocados**: toda a aritmética é de hora local sobre as cadeias fornecidas.

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-spc-gbt-adapter
```

O último comando copia o kit compartilhado de `../_shared` para `src/shared/`; execute-o novamente após cada alteração compartilhada.

## License

[Apache License 2.0](LICENSE) © 2026 dsh-spc-gbt-adapter contributors.
