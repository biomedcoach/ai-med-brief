import os, json

base = r'D:\Qclaw\AiMedbrief\articles'
os.makedirs(base, exist_ok=True)

articles = [
    {
        'id': '01',
        'date': '2026-06-02',
        'category': '创新药',
        'cat_en': 'Innovative Drug',
        'title_cn': 'ASCO 2026：中国ADC全面炸场！一线突破+双抗迭代+多靶点齐爆发',
        'title_en': "ASCO 2026: China's ADC Explosion — First-Line Breakthrough, Bispecific Iteration, Multi-Target Surge",
        'summary_cn': '2026年ASCO大会上，中国ADC产业实现三大里程碑式进阶。其一，治疗场景从后线挽救正式跃迁至一线标准治疗——科伦博泰芦康沙妥珠单抗（sac-TMT）联合帕博利珠单抗对比K药单药，将疾病进展或死亡风险降低65%，首次以头对头随机对照试验证实"ADC+免疫疗法"可击败PD-1单药。其二，分子结构从传统单抗ADC突破至全球首创双抗ADC，中国企业率先将双特异性抗体与细胞毒素偶联，开辟了新一代ADC的设计范式。其三，靶点布局从HER2等少数靶标全面扩容至TROP2、CLDN18.2、B7-H3、Nectin-4等多种实体瘤驱动基因，覆盖肺癌、胃癌、乳腺癌、尿路上皮癌等大适应症。本届ASCO中国ADC相关口头报告数量创历史新高，标志着中国已从ADC跟随者跃升为全球ADC创新的核心策源地之一。',
        'summary_en': 'At the ASCO 2026 Annual Meeting, China\'s ADC sector achieved three landmark advances. First, a formal leap from late-line salvage to first-line standard-of-care — Kelun-Biotech\'s sacituzumab tirumotecan (sac-TMT) combined with pembrolizumab reduced the risk of disease progression or death by 65% versus pembrolizumab monotherapy in a head-to-head randomized controlled trial, marking the first-ever proof that "ADC + immunotherapy" can defeat PD-1 monotherapy. Second, molecular architecture evolved from conventional monoclonal antibody ADCs to first-in-class bispecific ADCs, with Chinese companies pioneering the conjugation of bispecific antibodies with cytotoxic payloads, opening a new paradigm for next-generation ADC design. Third, the target landscape expanded dramatically from a handful of targets such as HER2 to a broad portfolio encompassing TROP2, CLDN18.2, B7-H3, Nectin-4, and other solid tumor driver genes, covering major indications including lung, gastric, breast, and urothelial cancers. With a record number of oral presentations featuring Chinese ADCs at this year\'s ASCO, China has vaulted from an ADC follower to a core global epicenter of ADC innovation.',
        'source': '动脉网 / vbdata.cn',
        'url': 'https://www.vbdata.cn/',
        'points': [
            "Kelun-Biotech's sac-TMT + pembrolizumab reduced disease progression/death risk by 65% vs pembrolizumab alone — first RCT proof that ADC+IO beats PD-1",
            "Chinese companies pioneered first-in-class bispecific ADCs, opening a next-gen design paradigm",
            "Target expansion from HER2 to TROP2, CLDN18.2, B7-H3, Nectin-4 across lung, gastric, breast, urothelial cancers"
        ]
    },
    {
        'id': '02',
        'date': '2026-06-02',
        'category': '创新药',
        'cat_en': 'Innovative Drug',
        'title_cn': 'ASCO 2026：α核素引爆！从β到α，中国核药抢占全球风口',
        'title_en': "ASCO 2026: Alpha Isotope Ignition — From Beta to Alpha, China's Radiopharma Seizes the Global Spotlight",
        'summary_cn': '2026年ASCO年会上，放射性配体疗法（RLT）和放射性核素偶联药物（RDC）成为全场焦点。这类"核药"通过靶向分子将放射性核素精准递送至肿瘤细胞，实现"诊疗一体化"——既能定位病灶，又能定点杀伤。诺华在会上展示了其明星产品Pluvicto在不同疾病负荷下的疗效数据，进一步验证了靶向放射性疗法的临床价值。更重要的趋势是：全球核药研发正从β核素向α核素加速切换——α粒子射程更短（仅几层细胞）、能量更高、对周围健康组织的损伤更小，有望将核药疗效推向新高度。中国企业如远大医药、东诚药业等已抢先布局α核素管线，中国丰富的同位素堆产能力和快速成长的CRO/CDMO体系为核药国产化提供了独特优势，ASCO 2026或将成为中国核药从跟跑到领跑的转折点。',
        'summary_en': 'At the ASCO 2026 Annual Meeting, radioligand therapy (RLT) and radionuclide drug conjugates (RDC) took center stage. These "radiopharmaceuticals" use targeting molecules to precisely deliver radioactive isotopes to tumor cells, achieving "theranostics" — the ability to both localize lesions and deliver targeted cell killing. Novartis showcased efficacy data for its flagship product Pluvicto across varying disease burden levels, further validating the clinical value of targeted radiotherapy. A more significant trend is emerging: global radiopharma R&D is accelerating its shift from beta-emitters to alpha-emitters — alpha particles have a shorter range (just a few cell layers), higher linear energy transfer, and cause less collateral damage to surrounding healthy tissue, promising to elevate radiopharma efficacy to new heights. Chinese enterprises such as Grand Pharma and Dongcheng Pharmaceutical have already taken proactive steps to build alpha-isotope pipelines. China\'s abundant isotope production capacity and rapidly maturing CRO/CDMO ecosystem offer unique advantages for domestic radiopharma. ASCO 2026 may well become the inflection point where China\'s radiopharma sector transitions from follower to leader.',
        'source': '动脉网 / vbdata.cn',
        'url': 'https://www.vbdata.cn/',
        'points': [
            "RLT/RDC became ASCO 2026's centerpiece as radiopharma shifts from beta to alpha emitters for higher potency and less collateral damage",
            "Novartis' Pluvicto data validated targeted radiotherapy — theranostics enables simultaneous imaging and therapy",
            "Chinese firms Grand Pharma and Dongcheng have proactively built alpha-isotope pipelines, leveraging domestic isotope production and CRO/CDMO"
        ]
    },
    {
        'id': '03',
        'date': '2026-06-02',
        'category': '创新药',
        'cat_en': 'Innovative Drug',
        'title_cn': 'ASCO 2026 LBA | 君赛生物GC101 TIL关键Ⅱ期成功，疗效与安全性优异',
        'title_en': "ASCO 2026 LBA | JunCell Bio's GC101 TIL Therapy Aces Pivotal Phase II with Outstanding Efficacy and Safety",
        'summary_cn': '君赛生物自主研发的肿瘤浸润淋巴细胞（TIL）疗法GC101在ASCO 2026大会上以最高规格的"最新突破摘要"（LBA）形式亮相并进行口头报告，公布了关键Ⅱ期临床试验的优异结果。针对晚期非小细胞肺癌患者，GC101的客观缓解率（ORR）达到41.7%，安全性显著优于传统TIL疗法——君赛独创的"非清淋"技术路线使患者无需接受大剂量化疗预处理即可接受TIL回输，大幅降低了治疗相关毒性。GC101的非病毒载体基因修饰技术平台也为其建立了差异化优势。在实体瘤治疗领域，传统TIL疗法长期受困于清淋预处理的高风险和技术工艺的复杂性，君赛的方案从两个维度打破了行业瓶颈：疗效上实现了与已获批的细胞疗法可比甚至更优的客观缓解数据，安全性上通过免清淋工艺大幅拓宽了适用人群。该数据被视为中国TIL赛道对标全球标杆企业Iovance Biotherapeutics的关键里程碑。',
        'summary_en': 'JunCell Bio\'s independently developed tumor-infiltrating lymphocyte (TIL) therapy GC101 debuted at ASCO 2026 as a Late-Breaking Abstract (LBA) — the meeting\'s highest-profile format — with an oral presentation disclosing outstanding pivotal Phase II clinical trial results. In patients with advanced non-small cell lung cancer, GC101 achieved an objective response rate (ORR) of 41.7%, with a safety profile significantly superior to conventional TIL therapies. JunCell\'s proprietary "lymphodepletion-free" approach enables patients to receive TIL infusion without high-dose chemotherapy preconditioning, dramatically reducing treatment-related toxicity. The company\'s non-viral vector gene-modification platform further provides a differentiated competitive advantage. In the solid tumor arena, traditional TIL therapy has long been constrained by the high risk of lymphodepleting preconditioning and the complexity of manufacturing processes. JunCell\'s solution breaks through both industry bottlenecks simultaneously: delivering objective response rates comparable to or exceeding those of approved cell therapies, while the lymphodepletion-free protocol vastly broadens the eligible patient population. This dataset is widely regarded as a pivotal milestone for China\'s TIL sector as it benchmarks against global leader Iovance Biotherapeutics.',
        'source': '动脉网 / vbdata.cn',
        'url': 'https://www.vbdata.cn/',
        'points': [
            "GC101 achieved 41.7% ORR in advanced NSCLC with a novel lymphodepletion-free approach eliminating high-dose chemo preconditioning",
            "Non-viral vector gene-modification platform adds differentiation vs conventional TIL manufacturing",
            "ASCO LBA oral presentation; widely seen as China's TIL watershed benchmark against Iovance"
        ]
    },
    {
        'id': '04',
        'date': '2026-06-02',
        'category': 'AI+医药',
        'cat_en': 'AI + Pharma',
        'title_cn': '解码生命的语言——AI蛋白质设计如何重塑止痛药的未来',
        'title_en': "Decoding the Language of Life — How AI Protein Design Is Reshaping the Future of Painkillers",
        'summary_cn': '上海交通大学陈海峰教授团队基于多年的计算生物学积累，开发出国内目前性能最优的AI蛋白质药物理性设计平台——不依赖大规模的湿实验筛选，仅通过蛋白质结构预测、分子动力学模拟与深度学习生成模型的三者耦合，即可从第一性原理出发设计全新的功能性蛋白质药物分子。团队已将该平台应用于止痛药研发，成功设计出一种同时靶向μ阿片受体和NK1受体的双靶点蛋白质药物分子——在动物模型中该分子镇痛效果与吗啡相当甚至更优，但在呼吸抑制、成瘾性及消化道副作用三项关键安全性指标上为零。中国每年数以百万计的癌痛和慢性疼痛患者长期面临阿片类药物成瘾风险，该平台的突破意味着蛋白质药物的AI理性设计具备了可复制、可推广的工程化能力，有望从根本上改变镇痛药物的风险收益比格局。',
        'summary_en': 'Professor Chen Haifeng\'s team at Shanghai Jiao Tong University, drawing on years of accumulated expertise in computational biology, has developed what is currently China\'s top-performing AI platform for rational protein drug design. Without relying on large-scale wet-lab screening, the platform couples protein structure prediction, molecular dynamics simulation, and deep-learning generative models to design entirely novel functional protein drug molecules from first principles. The team has applied this platform to analgesic drug development and successfully designed a dual-target protein drug molecule that simultaneously engages the μ-opioid receptor and the NK1 receptor. In animal models, the molecule\'s analgesic efficacy matched or exceeded that of morphine, yet it registered zero signal across three critical safety dimensions: respiratory depression, addiction liability, and gastrointestinal side effects. With millions of cancer-pain and chronic-pain patients in China facing long-term opioid addiction risk each year, this platform breakthrough means that AI-driven rational protein drug design has attained replicable, scalable engineering capability, holding the potential to fundamentally reshape the risk-benefit landscape of analgesic medications.',
        'source': '动脉网 / vbdata.cn',
        'url': 'https://www.vbdata.cn/',
        'points': [
            "SJTU's AI platform couples structure prediction + molecular dynamics + deep generative models to design proteins from first principles",
            "Dual-target (μ-opioid + NK1) analgesic matched morphine efficacy with zero addiction, respiratory depression, or GI toxicity",
            "Breakthrough signals AI-driven rational protein design has reached replicable engineering capability for the analgesic pharmacopeia"
        ]
    }
]

# Write individual article pages
for a in articles:
    fpath = os.path.join(base, f'2026-06-02-{a["id"]}.html')
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{a["title_en"]}</title>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display','Segoe UI',sans-serif;background:#fafafa;color:#1d1d1f;line-height:1.6;-webkit-font-smoothing:antialiased}}
.top-bar{{background:rgba(255,255,255,0.8);backdrop-filter:blur(20px);border-bottom:1px solid #f0f0f5;position:sticky;top:0;z-index:100;padding:8px 24px;font-size:12px;color:#86868b}}
.top-bar-inner{{max-width:860px;margin:0 auto;display:flex;justify-content:space-between;align-items:center}}
.top-bar a{{color:#0071e3;text-decoration:none;font-weight:500}}
.container{{max-width:860px;margin:0 auto;padding:48px 24px 80px}}
.back-link{{display:inline-flex;align-items:center;gap:6px;color:#0071e3;text-decoration:none;font-size:14px;margin-bottom:24px}}
.category{{display:inline-block;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;padding:3px 10px;border-radius:6px;margin-bottom:16px;color:#5856d6;background:rgba(88,86,214,0.08)}}
.date{{font-size:13px;color:#86868b;margin-bottom:12px}}
h1{{font-size:32px;font-weight:700;letter-spacing:-0.5px;line-height:1.2;margin-bottom:16px}}
h2{{font-size:22px;font-weight:600;color:#1d1d1f;margin-top:40px;margin-bottom:12px;padding-top:24px;border-top:1px solid #f0f0f5}}
.summary{{font-size:17px;color:#424245;line-height:1.7;margin-bottom:32px}}
.translation{{font-size:16px;color:#6e6e73;line-height:1.65;background:#fff;border-radius:16px;padding:28px 32px;border:1px solid #e5e5ea}}
.source{{font-size:12px;color:#86868b;margin-top:32px}}
.source a{{color:#0071e3}}
@media(max-width:640px){{.container{{padding:24px 16px}}h1{{font-size:24px}}}}
</style>
</head>
<body>
<nav class="top-bar"><div class="top-bar-inner"><span style="font-weight:600;color:#1d1d1f">AiMedbrief</span><a href="../../">Back to Home</a></div></nav>
<div class="container">
<a href="../../" class="back-link">Home</a>
<p class="category">{a["cat_en"]}</p>
<p class="date">June 2, 2026</p>
<h1>{a["title_en"]}</h1>
<h2>中文报道</h2>
<div class="summary">{a["summary_cn"]}</div>
<h2>English</h2>
<div class="translation">{a["summary_en"]}</div>
<p class="source">Source: {a["source"]} · <a href="{a["url"]}" target="_blank" rel="noopener">{a["url"]}</a></p>
</div>
</body>
</html>'''
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  Created: {a["id"]}')

# Save JSON data for index generation
with open(os.path.join(base, 'data.json'), 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False)

print(f'Done: {len(articles)} article pages + data.json')
