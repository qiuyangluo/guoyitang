#!/usr/bin/env python3
"""Generate service landing pages. Run from repository root: python3 scripts/generate-service-landings.py"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOKING = "/book"


def shell() -> str:
    return r"""<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-M3EJ79RT1R"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'G-M3EJ79RT1R');
gtag('config', 'AW-17707030959');
</script>
<script src="/assets/phone-analytics.js"></script>
<!-- Event snippet for 预约服务 - 跳转预约网站 conversion page -->
<script>
function gtag_report_conversion(url) {
  var callback = function () {
    if (typeof(url) != 'undefined') {
      window.location = url;
    }
  };
  gtag('event', 'conversion', {
      'send_to': 'AW-17707030959/31h4CI-R5egbEK-zr_tB',
      'event_callback': callback
  });
  return false;
}
</script>
<!-- Vercel Web Analytics — enable in Vercel → Analytics -->
<script>window.va=window.va||function(){(window.vaq=window.vaq||[]).push(arguments);};</script>
<script defer src="/_vercel/insights/script.js"></script>
</head>
<body>
<nav class="navbar" aria-label="主导航">
<div class="nav-container">
<a class="logo" href="/"><img src="image/guoyitang-logo-header-125x42.webp" width="125" height="42" alt="国医堂中医诊所标志（Guoyitang TCM）"></a>
<ul class="nav-links">
<li><a href="/">主页</a></li>
<li><a href="/about-us">关于我们</a></li>
<li><a href="/doctors">国医堂团队</a></li>
<li><a href="/services">诊疗服务</a></li>
<li><a href="/successful-cases">成功案例</a></li>
<li><a href="/patient-review">病人好评</a></li>
<li><a href="/blog/">健康专栏</a></li>
<li><a href="/contact-us">联系我们</a></li>
</ul>
<div class="nav-actions">
<a class="language-btn" href="tel:+17188881133" onclick="return gtag_report_phone_conversion('tel:+17188881133');">718-888-1133</a>
<a class="cta-nav" href="$BOOKING">在线预约</a>
</div>
<button type="button" class="mobile-menu-toggle" aria-label="打开菜单" aria-expanded="false" aria-controls="mobileMenu">☰</button>
</div>
<div class="mobile-menu" id="mobileMenu">
<ul class="mobile-nav-links">
<li><a href="/">主页</a></li>
<li><a href="/about-us">关于我们</a></li>
<li><a href="/doctors">国医堂团队</a></li>
<li><a href="/services">诊疗服务</a></li>
<li><a href="/successful-cases">成功案例</a></li>
<li><a href="/patient-review">病人好评</a></li>
<li><a href="/blog/">健康专栏</a></li>
<li><a href="/contact-us">联系我们</a></li>
</ul>
<div class="mobile-actions">
<a class="language-btn" href="tel:+17188881133" onclick="return gtag_report_phone_conversion('tel:+17188881133');">致电 718-888-1133</a>
<a class="cta-nav" href="$BOOKING">在线预约</a>
</div>
</div>
</nav>

<main class="page-main">
<div class="page-hero">
<div class="container">
<h1>$H1</h1>
<p class="page-lead">$LEAD</p>
<div class="actions" style="justify-content:center;margin-top:1.25rem">
<a class="cta-btn" href="$BOOKING">立即预约</a>
<a class="learn-more" href="tel:+17188881133" onclick="return gtag_report_phone_conversion('tel:+17188881133');">电话预约</a>
</div>
</div>
</div>

<div class="container inner-block">
$BODY
<section class="section">
<div class="section__inner">
<h2>更多专题</h2>
<p class="prose" style="margin-bottom:0">按疗法与科室浏览：<a href="/service-acupuncture-flushing">针灸</a>、<a href="/service-cupping-tcm">拔罐</a>、<a href="/service-tuina-massage">推拿按摩</a>；按症状：<a href="/service-back-pain-tcm">腰痛</a>、<a href="/service-neck-shoulder-pain">肩颈痛</a>；按专科：<a href="/service-gynecology-tcm">妇科</a>、<a href="/service-andrology-tcm">男科</a>、<a href="/service-urology-tcm">泌尿科</a>。返回<a href="/services">全部诊疗服务</a>。</p>
</div>
</section>
</div>
</main>
<footer class="site-footer">
<div class="container">
<div class="footer-content">
<div class="footer-section">
<img src="image/guoyitang-logo-footer.webp" width="241" height="80" alt="国医堂中医诊所标志" loading="lazy" decoding="async" style="max-width:180px;opacity:.95;margin-bottom:1rem;height:auto">
<p>国医堂中医诊所 · Flushing Guoyitang TCM Clinic<br>纽约法拉盛 · 针灸 · 中药 · 推拿</p>
</div>
<div class="footer-section">
<h3>导航</h3>
<ul>
<li><a href="/">主页</a></li>
<li><a href="/about-us">关于诊所</a></li>
<li><a href="/services">诊疗服务</a></li>
<li><a href="/doctors">国医堂团队</a></li>
<li><a href="/successful-cases">成功案例</a></li>
<li><a href="/patient-review">病人好评</a></li>
<li><a href="/blog/">健康专栏</a></li>
<li><a href="/contact-us">联系我们</a></li>
</ul>
</div>
<div class="footer-section">
<h3>联系</h3>
<p><a href="tel:+17188881133" onclick="return gtag_report_phone_conversion('tel:+17188881133');">(718) 888-1133</a><br>
<a href="tel:+17188868979" onclick="return gtag_report_phone_conversion('tel:+17188868979');">(718) 886-8979</a></p>
<p>142-38 37th Ave #1C1D<br>Flushing, NY 11354</p>
</div>
</div>
<div class="footer-bottom">Copyright © 2026 Guoyitang</div>
</div>
</footer>
<script src="assets/nav.js" defer></script>
<script src="assets/page-reveal.js" defer></script>
</body>
</html>
"""


def json_ld(fname: str, name: str, desc: str) -> str:
    d = {
        "@context": "https://schema.org",
        "@type": "MedicalWebPage",
        "name": name,
        "description": desc[:200],
        "url": f"https://guoyitangus.com/{fname[:-5] if fname.endswith('.html') else fname}",
        "inLanguage": "zh-Hans",
        "isPartOf": {"@type": "WebSite", "name": "国医堂中医诊所", "url": "https://guoyitangus.com/"},
        "about": {
            "@type": "MedicalClinic",
            "name": "国医堂中医诊所 Guoyitang TCM Clinic",
            "url": "https://guoyitangus.com/",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "142-38 37th Ave #1C1D",
                "addressLocality": "Flushing",
                "addressRegion": "NY",
                "postalCode": "11354",
                "addressCountry": "US",
            },
        },
    }
    return json.dumps(d, ensure_ascii=False)


def build_page(
    fname: str,
    title: str,
    desc: str,
    keywords: str,
    h1: str,
    lead: str,
    body: str,
) -> str:
    head = f"""<!DOCTYPE html>
<html lang="zh-Hans">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{keywords}">
<link rel="canonical" href="https://guoyitangus.com/{fname[:-5] if fname.endswith('.html') else fname}">
<meta name="theme-color" content="#354d2c">
<link rel="icon" href="/favicon-32x32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">
<link rel="stylesheet" href="assets/main.min.css">
<link rel="stylesheet" href="assets/fonts-defer.css" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="assets/fonts-defer.css"></noscript>
<script type="application/ld+json">
{json_ld(fname, title.split("｜")[0], desc)}
</script>
"""
    rest = (
        shell()
        .replace("$BOOKING", BOOKING)
        .replace("$H1", h1)
        .replace("$LEAD", lead)
        .replace("$BODY", body)
    )
    return head + rest


PAGES: list[tuple[str, str, str, str, str, str, str]] = [
    (
        "service-urology-tcm.html",
        "中医泌尿科｜法拉盛针灸中药调理｜纽约国医堂",
        "国医堂法拉盛针灸中医诊所：中医泌尿科尿频尿急、夜尿、前列腺相关不适等辨证论治，针药与生活方式建议结合；急症请先急诊。718-888-1133。",
        "中医泌尿科,泌尿科,法拉盛中医,纽约中医,国医堂,针灸,中药,尿频",
        "纽约法拉盛中医泌尿科调理",
        "国医堂位于华美大楼一层，由执照中医师面诊，针对<strong>中医泌尿科</strong>常见困扰（如尿频尿急、夜尿增多、排尿不尽感、前列腺相关不适及伴发的睡眠与疲劳）进行<strong>辨证论治</strong>，可结合<strong>针灸</strong>、<strong>中药</strong>与<strong>推拿按摩</strong>等综合调理。<strong>并非替代西医泌尿专科检查</strong>；若出现发热、血尿、剧烈疼痛等，请及时急诊或泌尿专科就诊。",
        """<section class="section"><div class="section__inner"><h2><span class="section-eyebrow">泌尿</span>常见就诊方向</h2><div class="grid2"><div class="card"><h3>排尿与下焦</h3><p>尿频尿急、夜尿、排尿不尽；体质偏虚或湿热等证型不同，用药与取穴各异。</p></div><div class="card"><h3>前列腺相关</h3><p>中老年常见下尿路症状的中西医结合思路：中医缓解不适、改善睡眠与焦虑；必要时配合实验室或影像复查。</p></div><div class="card"><h3>伴发症状</h3><p>腰酸、乏力、失眠等可一并纳入辨证，与<strong>男科</strong>调理有交叉时可转诊医师评估。</p></div></div></div></section>
<section class="section"><div class="section__inner"><h2>诊疗说明</h2><p class="prose">首诊以问诊、舌脉与体征为主，结合既往检查报告；疗程与是否适合<strong>拔罐</strong>或<strong>针灸</strong>由医师决定。疗效因人而异。</p></div></section>""",
    ),
    (
        "service-gynecology-tcm.html",
        "中医妇科｜法拉盛针灸中药调经备孕｜国医堂",
        "国医堂法拉盛中医妇科：月经不调、痛经、更年期、备孕产后调理；针灸中药结合，须医师面诊。纽约法拉盛华美大楼一层。",
        "中医妇科,妇科,法拉盛针灸,纽约中医,国医堂,备孕,痛经,针灸",
        "法拉盛中医妇科与针灸调理",
        "国医堂<strong>中医妇科</strong>面向月经先后不定期、痛经、经量少或多、更年期潮热失眠、备孕与产后体虚等，采用<strong>针灸</strong>与<strong>中药</strong>分期调养，并可配合<strong>推拿按摩</strong>放松盆底与腰背肌群。就诊以<strong>医师面诊评估</strong>为准，急腹症请先急诊。",
        """<section class="section"><div class="section__inner"><h2><span class="section-eyebrow">妇科</span>常见方向</h2><div class="grid2"><div class="card"><h3>月经与周期</h3><p>痛经、周期紊乱、经前综合征；针药调周，配合作息与情绪管理建议。</p></div><div class="card"><h3>备孕与产后</h3><p>孕前体质、产后恶露与体虚恢复；与医师团队随访调整方案。</p></div><div class="card"><h3>更年期与睡眠</h3><p>潮热汗出、烦躁失眠；可联合<strong>针灸</strong>与中药滋阴清热或补肾安神等辨证思路。</p></div></div></div></section>
<section class="section"><div class="section__inner"><h2>与痛症理疗的衔接</h2><p class="prose">合并<strong>腰痛</strong>、<strong>肩颈痛</strong>者，可在妇科方案基础上由医师安排<strong>拔罐</strong>或推拿辅助松解肌肉。</p></div></section>""",
    ),
    (
        "service-andrology-tcm.html",
        "中医男科｜法拉盛中药针灸调理｜纽约国医堂",
        "国医堂中医男科：精力疲劳、睡眠、尿频等辨证；针药与推拿结合。纽约法拉盛针灸中医诊所，华美大楼一层。",
        "中医男科,男科,法拉盛中医,纽约中医,国医堂,针灸,中药,泌尿",
        "纽约法拉盛中医男科调理",
        "国医堂<strong>中医男科</strong>关注精力不足、疲劳失眠、性功能相关困扰及与下尿路症状的交叉问题，以<strong>中药</strong>、<strong>针灸</strong>与体质调养为主，必要时建议完善西医检查。诊疗强调隐私与沟通，<strong>个体化方案</strong>须面诊后确定。",
        """<section class="section"><div class="section__inner"><h2><span class="section-eyebrow">男科</span>常见方向</h2><div class="grid2"><div class="card"><h3>精力与睡眠</h3><p>工作压力大、熬夜导致的疲劳、浅睡；补肾疏肝等辨证取穴与方药。</p></div><div class="card"><h3>下尿路症状</h3><p>与<strong>泌尿科</strong>重叠的尿频尿急，由医师区分证型并协调诊疗路径。</p></div><div class="card"><h3>腰背与久坐</h3><p>久坐伴<strong>腰痛</strong>、<strong>肩颈痛</strong>，可辅以<strong>推拿按摩</strong>与功能建议。</p></div></div></div></section>
<section class="section"><div class="section__inner"><h2>说明</h2><p class="prose">中医男科不等同于单一“补肾”；是否适合<strong>拔罐</strong>或强刺激手法由医师评估。</p></div></section>""",
    ),
    (
        "service-back-pain-tcm.html",
        "腰痛针灸推拿拔罐｜法拉盛痛症｜纽约国医堂",
        "国医堂法拉盛腰痛调理：针灸、推拿按摩、拔罐、艾灸协同；腰肌劳损、久坐腰痛等须面诊。纽约针灸中医诊所。",
        "腰痛,腰痛针灸,拔罐,针灸,推拿,按摩,法拉盛针灸,国医堂",
        "法拉盛腰痛｜针灸推拿拔罐综合调理",
        "针对<strong>腰痛</strong>、腰肌劳损、久坐与姿势不良引起的慢性酸痛，国医堂在<strong>法拉盛针灸</strong>基础上，常联合<strong>推拿按摩</strong>、<strong>拔罐</strong>、艾灸与中药内服外敷思路（以医师评估为准），帮助缓解肌肉紧张、改善活动度。<strong>急性外伤、马尾症状、发热伴腰痛</strong>请先急诊或骨科。",
        """<section class="section"><div class="section__inner"><h2><span class="section-eyebrow">痛症</span>诊疗组合</h2><div class="grid2"><div class="card"><h3>针灸</h3><p>局部与远端取穴，改善气血运行，适合慢性劳损与反复发作型腰痛。</p></div><div class="card"><h3>推拿按摩</h3><p>松解臀腰筋膜链、调整肌张力；配合居家拉伸建议。</p></div><div class="card"><h3>拔罐</h3><p>寒湿瘀滞型可酌情<strong>拔罐</strong>或走罐；皮肤禁忌与体质须医师把关。</p></div></div></div></section>
<section class="section"><div class="section__inner"><h2>与肩颈的关联</h2><p class="prose">上交叉体态常同时出现<strong>肩颈痛</strong>与腰痛，可预约医师做整体评估。详见<a href="/service-neck-shoulder-pain">肩颈痛专题</a>。</p></div></section>""",
    ),
    (
        "service-neck-shoulder-pain.html",
        "肩颈痛颈椎病针灸推拿｜法拉盛｜纽约国医堂",
        "国医堂肩颈痛与颈椎病针灸、推拿按摩、艾灸调理；法拉盛针灸中医诊所，久坐办公族欢迎面诊评估。",
        "肩颈痛,颈椎病,针灸,推拿,按摩,法拉盛针灸,国医堂,纽约中医",
        "法拉盛肩颈痛与颈椎病针灸调理",
        "<strong>肩颈痛</strong>、颈椎病、肩周炎、上背部僵硬与久坐办公族常见紧张，国医堂以<strong>针灸</strong>疏通经络，配合<strong>推拿按摩</strong>、艾灸及必要的<strong>拔罐</strong>松解筋膜。是否适合手法强度与器械治疗须<strong>面诊</strong>；急性神经损伤或外伤请先急诊。",
        """<section class="section"><div class="section__inner"><h2><span class="section-eyebrow">筋骨</span>常见表现</h2><div class="grid2"><div class="card"><h3>颈肩综合征</h3><p>转头受限、肩胛内侧酸痛、手臂麻木需鉴别神经根型颈椎病。</p></div><div class="card"><h3>头痛与紧张</h3><p>颈源性头痛、紧张性头痛可纳入针灸与推拿方案。</p></div><div class="card"><h3>体态与恢复</h3><p>含胸驼背、肩胛动力不足；训练建议与理疗结合。</p></div></div></div></section>
<section class="section"><div class="section__inner"><h2>联合腰痛调理</h2><p class="prose">上交叉与骨盆前倾常与<strong>腰痛</strong>并存，可参考<a href="/service-back-pain-tcm">腰痛专题</a>综合干预。</p></div></section>""",
    ),
    (
        "service-cupping-tcm.html",
        "拔罐走罐｜法拉盛中医理疗｜纽约国医堂",
        "国医堂拔罐、走罐与针灸推拿结合：寒湿瘀滞、颈肩腰背紧张等须医师辨证后操作。法拉盛华美大楼一层。",
        "拔罐,走罐,法拉盛中医,针灸,推拿,国医堂,纽约中医,理疗",
        "法拉盛拔罐与走罐理疗",
        "<strong>拔罐</strong>、走罐、留罐为中医外治法，适用于部分寒湿瘀滞、肌肉紧张型体质；国医堂在<strong>法拉盛针灸</strong>与<strong>推拿按摩</strong>流程中由医师或理疗师评估后选用，避免在皮肤破损、出血倾向或特定禁忌部位操作。<strong>腰痛</strong>、<strong>肩颈痛</strong>患者是否适合拔罐以面诊为准。",
        """<section class="section"><div class="section__inner"><h2><span class="section-eyebrow">拔罐</span>适用与禁忌（概要）</h2><div class="grid2"><div class="card"><h3>可能适合</h3><p>风寒湿型肌筋膜疼痛、感冒初起肩背紧等；常与<strong>针灸</strong>同疗程分期使用。</p></div><div class="card"><h3>需谨慎</h3><p>皮肤敏感、凝血功能异常、孕妇腰骶部、严重静脉曲张区域等不宜或慎用。</p></div><div class="card"><h3>与其他疗法</h3><p>可先<strong>推拿按摩</strong>松解后再拔罐，或针灸后加强温通；具体顺序由医师决定。</p></div></div></div></section>
<section class="section"><div class="section__inner"><h2>提示</h2><p class="prose">罐斑淤血为常见反应，若持续剧痛或水泡感染请及时回院或就医。</p></div></section>""",
    ),
    (
        "service-acupuncture-flushing.html",
        "法拉盛针灸｜纽约针灸痛症失眠妇科｜国医堂",
        "国医堂法拉盛针灸：执照针灸师主理痛症、失眠、妇科男科及体质调理；中药推拿拔罐可协同。华美大楼一层预约。",
        "法拉盛针灸,针灸,纽约针灸,痛症,失眠,妇科,男科,国医堂",
        "法拉盛针灸诊所｜执照针灸师辨证取穴",
        "国医堂<strong>针灸</strong>服务由纽约州执照针灸师主理，覆盖<strong>痛症</strong>（含<strong>腰痛</strong>、<strong>肩颈痛</strong>）、失眠焦虑、<strong>妇科</strong>与<strong>男科</strong>相关调理及内科体质调养。针刺可与<strong>中药</strong>、<strong>推拿按摩</strong>、艾灸、<strong>拔罐</strong>等组合，方案以<strong>辨证与面诊</strong>为准。",
        """<section class="section"><div class="section__inner"><h2><span class="section-eyebrow">针灸</span>可覆盖方向</h2><div class="grid2"><div class="card"><h3>痛症与运动系统</h3><p>急慢性颈肩腰、关节劳损；配合功能训练建议。</p></div><div class="card"><h3>神经与睡眠</h3><p>失眠、焦虑相关躯体化症状；取穴与刺激量个体化。</p></div><div class="card"><h3>妇泌尿与内科</h3><p>与<strong>妇科</strong>、<strong>泌尿科</strong>、脾胃体质等交叉问题，由团队医师协同评估。</p></div></div></div></section>
<section class="section"><div class="section__inner"><h2>首次到院</h2><p class="prose">请携带既往检查与用药清单；晕针史、出血倾向或植入器械等请提前告知医师。</p></div></section>""",
    ),
    (
        "service-tuina-massage.html",
        "中医推拿按摩｜法拉盛理疗松筋｜纽约国医堂",
        "国医堂推拿按摩与针灸拔罐协同：颈肩腰痛、运动劳损、久坐亚健康。纽约法拉盛华美大楼一层，医师或理疗师评估后操作。",
        "推拿,按摩,中医推拿,理疗,法拉盛,针灸,拔罐,国医堂,纽约中医",
        "法拉盛中医推拿按摩与理疗",
        "国医堂<strong>推拿按摩</strong>（中医推拿）侧重松筋活络、改善局部循环与姿势代偿，常与<strong>针灸</strong>、艾灸、<strong>拔罐</strong>及<strong>中药</strong>内服配合，服务<strong>腰痛</strong>、<strong>肩颈痛</strong>及运动劳损人群。禁忌与力度由持牌理疗师或医师评估；本页内容为健康科普与到院指引，<strong>非个体化医疗承诺</strong>。",
        """<section class="section"><div class="section__inner"><h2><span class="section-eyebrow">推拿</span>常见场景</h2><div class="grid2"><div class="card"><h3>办公久坐</h3><p>颈肩腰背整体松解，配合拉伸与工位建议。</p></div><div class="card"><h3>运动恢复</h3><p>肌肉拉伤恢复期在医师指导下循序渐进的手法治疗。</p></div><div class="card"><h3>与专科协同</h3><p>合并<strong>妇科</strong>、<strong>男科</strong>体虚或<strong>泌尿科</strong>症状时，以全科辨证为主轴安排疗程。</p></div></div></div></section>
<section class="section"><div class="section__inner"><h2>与针灸拔罐的搭配</h2><p class="prose">可先推拿放松软组织再针刺或<strong>拔罐</strong>，或针灸后轻柔理筋；顺序与频次因人而异。</p></div></section>""",
    ),
]


def main() -> None:
    for tup in PAGES:
        fname, title, desc, keywords, h1, lead, body = tup
        html = build_page(fname, title, desc, keywords, h1, lead, body)
        path = ROOT / fname
        path.write_text(html, encoding="utf-8")
        print("wrote", path.relative_to(ROOT))


if __name__ == "__main__":
    main()
