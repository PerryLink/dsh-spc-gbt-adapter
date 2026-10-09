# dsh-spc-gbt-adapter — नियंत्रण चार्ट स्थिरांक और प्रक्रिया क्षमता सूचकांक की संगति की जाँच

[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)

`dsh-spc-gbt-adapter` एक नियंत्रण चार्ट रजिस्टर पढ़ता है — पंक्तियाँ रजिस्टर के अपने कॉलम नामों से बनी, चीनी या अंग्रेज़ी — और उसी रजिस्टर की अंकगणितीय तथा स्थिरांक-सारणी संगति की जाँच करता है: क्या विशेषता और चार्ट प्रकार दर्ज हैं, क्या नियंत्रण सीमाएँ केंद्र रेखा, परिसर और पैक में स्थिर किए गए चार्ट स्थिरांकों से निकलती हैं, क्या केंद्र रेखा सीमाओं के बीच है, क्या दर्ज Cp और Cpk अपनी परिभाषाओं के अनुरूप हैं, क्या उपसमूह आकार स्थिरांक-सारणी में शामिल है, और क्या हेडर उत्पाद तथा प्रक्रिया बताता है।

## आउटपुट कैसा दिखता है

![Terminal demo of dsh-spc-gbt-adapter: real output over its SP-003 fixture](https://raw.githubusercontent.com/PerryLink/dsh-spc-gbt-adapter/main/docs/assets/dsh-spc-gbt-adapter-demo.png)

इस प्लगइन का अपने ही `SP-003` टेस्ट फ़िक्स्चर पर वास्तविक आउटपुट — कोई नकली चित्र नहीं। नियम-पैक उद्धरण नहीं गढ़ता, इसलिए हर निष्कर्ष लागू किए गए खंड का नाम और यह भी बताता है कि उसका मूल पाठ इस बार प्राप्त नहीं हुआ।

## यह किन सवालों का जवाब देता है

| आपका सवाल | इसका जवाब |
|---|---|
| किसी पंक्ति में विशेषता और चार्ट प्रकार दोनों खाली हैं। क्या यह दर्ज होता है? | हाँ। `SP-001` कहता है कि जिस पंक्ति में इन दोनों में से कोई कॉलम मौजूद है, उसमें `characteristic` और `chartType` में से कम से कम एक भरा हो, और दोनों खाली होने पर वह पंक्ति दर्ज करता है। यह देखता है कि एक दर्ज है, यह नहीं कि उस विशेषता पर चार्ट बनना चाहिए या चार्ट प्रकार सही चुना गया। |
| रजिस्टर में दर्ज नियंत्रण सीमाएँ केंद्र रेखा, परिसर और स्थिरांकों से निकलने वाली सीमाओं से मेल नहीं खातीं। | `SP-002` उस `sampleSize` के गुणांक तथा `centerLine` और `range` से `ucl` और `lcl` दोबारा निकालता है (सहनशीलता 0.005) और दर्ज तथा अपेक्षित दोनों मानों के साथ पंक्ति दर्ज करता है। यह केवल यह देखता है कि ये संख्याएँ आपस में संगत हैं — यह नहीं कि सीमाएँ या परिसर सही हैं, और कभी यह नहीं कि प्रक्रिया नियंत्रण में है। स्थिर की गई सारणी X̄-R चार्ट की है: X̄-s, I-MR, p या c चार्ट के गुणांक भिन्न होते हैं, इसलिए नियम बंद करें या `coefficients` बदलें। |
| केंद्र रेखा ऊपरी नियंत्रण सीमा से ऊपर दर्ज है। | `SP-003` कहता है कि जिस पंक्ति में तीनों मान भरे हैं वहाँ `lcl` ≤ `centerLine` ≤ `ucl` हो, और जहाँ यह क्रम टूटता है वह पंक्ति दर्ज करता है। यह केवल तीनों संख्याओं का क्रम देखता है, यह नहीं कि वे सही गणना की गईं। परिसर चार्ट में निचली सीमा 0 होना सामान्य है और इस कारण कोई प्रविष्टि नहीं होती। |
| रजिस्टर में Cp और Cpk दर्ज हैं, पर रिपोर्ट उनके बारे में कुछ नहीं कहती। क्यों? | `SP-004` केवल उन्हीं पंक्तियों पर चलता है जिनमें `cp` या `cpk` के साथ `usl`, `lsl`, `stdDev` और `mean` भी भरे हों; जब कोई पंक्ति ये सब नहीं रखती, तो नियम चुपचाप पास होने के बजाय `skipped` दर्ज करता है। जहाँ चलता है वहाँ दोनों परिभाषाएँ जाँचता है: Cp = (USL − LSL) / 6σ तथा Cpk = min(USL − X̄, X̄ − LSL) / 3σ, सहनशीलता 0.02। अंतर प्रायः σ के मापदंड मिले होने का संकेत है: Cp/Cpk उपसमूह के भीतर का मानक विचलन लेते हैं, Pp/Ppk समग्र। यह तय नहीं करता कि क्षमता पर्याप्त है। |
| इस प्रक्रिया की क्षमता पर्याप्त है या नहीं? | इसका उत्तर यह जाँच नहीं देती। `SP-005` केवल उस `cpk` को दर्ज करता है जो आपके तय मानदंड से नीचे है, और वह `threshold: 0` के साथ आता है, यानी अनकॉन्फ़िगर, इसलिए वह मानदंड गढ़ने के बजाय `skipped` में चला जाता है; सामान्य 1.33 और 1.67 उद्योग, ग्राहक और विशेषता की महत्ता पर निर्भर हैं। इस नियम की प्रविष्टि का अर्थ केवल यह है कि मान आपके अपने मानदंड से नीचे है, यह नहीं कि प्रक्रिया अयोग्य है, और यह `info` गंभीरता के साथ दर्ज होती है। |
| हमारे प्रत्येक उपसमूह में 15 माप हैं। तब क्या होता है? | `SP-007` वह पंक्ति दर्ज करता है: पैक में स्थिर की गई स्थिरांक-सारणी केवल 2 से 10 तक के उपसमूह आकारों को कवर करती है। उस आकार के लिए प्रविष्टि न होने पर `SP-002` भी गुणांक नहीं देख पाता, इसलिए वह भी इसे दर्ज करता है, चुप नहीं रहता। यह नियम देखता है कि आकार सूचीबद्ध श्रेणी है या नहीं, यह नहीं कि वह उपसमूह आकार प्रक्रिया के लिए उपयुक्त है। बड़े उपसमूहों के लिए उस श्रेणी को `SP-002` के `coefficients` में जोड़ें और इस नियम के `values` बढ़ाएँ — यह नियम-पैक का संपादन है, कोड का नहीं। |

## यह किन मानकों पर आधारित है

| दस्तावेज़ | संख्यांक | इन्हें उद्धृत करने वाले नियम |
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

| सतह | स्थिति |
|---|---|
| Harness | peer रेंज `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — `0.2.0-rc.2` और `0.2.1-alpha.1` दोनों को स्वीकार करने के लिए सत्यापित। **`engines.dsh` जानबूझकर घोषित नहीं**: इसका कोई पाठक नहीं और यह किसी होस्ट को अस्वीकार नहीं कर सकता |
| Node | `^22.19.0 || >=24.0.0` |
| प्लेटफ़ॉर्म | सभी (शुद्ध ESM; कोई नेटिव कोड नहीं, कोई नेटवर्क नहीं, कोई मॉडल कॉल नहीं) |
| टूल मोड | `native`, `ptc` और `both` में काम करता है; पूरे फ़ोल्डर के लिए `ptc` चुनें |

## What it does

नियम-सूची, फ़ील्ड और विस्तृत व्यवहार [README.md](README.md#what-it-does) (अंग्रेज़ी मुख्य संस्करण) में हैं। यह प्लगइन केवल उद्धृत धाराओं के सामने शाब्दिक अंतर सूचीबद्ध करता है और हर न चल पाई जाँच को `skipped` में बताता है।

## Install

```sh
dsh plugin --profile <name> add dsh-spc-gbt-adapter
dsh --profile <name> --dump-config | grep 'dsh-spc-gbt-adapter'
```

## Configuration

सभी समायोज्य पैरामीटर `src/config.ts` की Schemastery स्कीमा में हैं, इसलिए कोड बदले बिना `cordis.yml` से बदले जा सकते हैं; प्रति-नियम सीमाएँ `rules/` के नियम-पैक में हैं।

| कुंजी | प्रकार | डिफ़ॉल्ट | विवरण |
|---|---|---|---|
| `rulesFile` | string | `rules/spc-gbt-adapter.yaml` | नियम-पैक का पथ, पैकेज रूट के सापेक्ष |
| `disabledRules` | string[] | `[]` | बंद करने वाले नियम id; प्रत्येक `skipped` में दिखता है |
| `onlyRules` | string[] | `[]` | केवल ये नियम चलाएँ; खाली होने पर सभी नियम चलते हैं |
| `skipNotes` | string | `""` | हर `skipped` कारण के आगे जोड़ी जाने वाली टिप्पणी |
| `timeoutMs` | number | `120000` | उपकरण का सहकारी समय-सीमा बजट |

## Material format

JSON या YAML स्वीकार्य है। पूरा फ़ील्ड उदाहरण [README.md](README.md#material-format) (अंग्रेज़ी मुख्य संस्करण) में है। पढ़ने की परत में फ़ील्ड वैकल्पिक हैं और जाँच इंजन उन्हें सत्यापित करता है, इसलिए आंशिक निर्यात पर क्रैश के बजाय "अनुपस्थित" श्रेणी के निष्कर्ष मिलते हैं।

## Rule sources

नियम-डेटा कोड से अलग है: प्रत्येक नियम में दस्तावेज़, संख्या, स्रोत की अपनी क्रमांकन-प्रणाली के अनुसार धारा, शब्दशः उद्धरण और स्रोत URL होता है। लोडर लागू करता है कि उद्धरण कम से कम आठ अक्षरों का वास्तविक उद्धरण हो, और जिस जाँच का आधार केवल सामान्य सिद्धांत (`kind: derived-from-principle`, अधिकतम `warn`) या स्थानीय नीति (`kind: institutional-configuration`, अधिकतम `info`) हो, उसे कभी `error` घोषित न किया जाए।

सत्यापित सीमाएँ और जान-बूझकर **न** कहे गए निष्कर्ष [README.md](README.md#rule-sources) (अंग्रेज़ी मुख्य संस्करण) और `rules/evidence/` में हैं।

## Troubleshooting

- **प्लगइन इंस्टॉल हो गया पर टूल दिखता नहीं**: जाँचें कि `main` `lib/index.mjs` पर जाता है और `pnpm run build` ने उसे बनाया है।
- **`dsh plugin add` असंगत बताकर मना करता है**: peer range `0.1.x` और `0.2.x` दोनों को कवर करती है; बाहर होने पर स्पष्ट छूट दें: `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`।
- **कोई नियम नहीं चला**: `skipped` सरणी देखें।
- **`check` में `manifest-peers` विफल दिखता है**: यह `dsh-plugin-dev` की ज्ञात अपस्ट्रीम समस्या है; रनटाइम इंस्टॉल के समय अनुकूलता लागू करता है।
- **समय खिसका हुआ लगता है**: सारी गणना दिए गए स्ट्रिंग पर वॉल-क्लॉक है।

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-spc-gbt-adapter
```

अंतिम कमांड `../_shared` का साझा किट `src/shared/` में कॉपी करता है; हर साझा बदलाव के बाद इसे दोबारा चलाएँ।

## License

[Apache License 2.0](LICENSE) © 2026 dsh-spc-gbt-adapter contributors.
