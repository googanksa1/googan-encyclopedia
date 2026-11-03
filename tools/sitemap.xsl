<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:s="http://www.sitemaps.org/schemas/sitemap/0.9">
<xsl:output method="html" encoding="UTF-8" indent="yes"/>
<xsl:template match="/">
<html lang="ar" dir="rtl"><head><meta charset="utf-8"/><meta name="robots" content="noindex"/><title>خريطة موقع موسوعة جوجان</title>
<style>body{font-family:Tahoma,Arial,sans-serif;margin:0;background:#f5f6fb;color:#1f2033}header{background:#1c1b42;color:#fff;padding:24px 16px}h1{margin:0;font-size:22px}p{margin:6px 0 0;color:#d6d5f3}main{max-width:980px;margin:20px auto;padding:0 16px}table{width:100%;border-collapse:collapse;background:#fff;border:1px solid #e2e4ef}th,td{padding:9px 12px;border-bottom:1px solid #e2e4ef;text-align:right;font-size:14px}th{background:#eef0f7}a{color:#2456d6;direction:ltr;unicode-bidi:embed}</style></head>
<body><header><h1>خريطة موقع موسوعة جوجان</h1><p>هذه الصفحة مخصصة لمحركات البحث، وتضم <xsl:value-of select="count(s:urlset/s:url)"/> رابطاً.</p></header>
<main><table><tr><th>الرابط</th><th>آخر تحديث</th></tr>
<xsl:for-each select="s:urlset/s:url"><tr><td><a href="{s:loc}"><xsl:value-of select="s:loc"/></a></td><td><xsl:value-of select="s:lastmod"/></td></tr></xsl:for-each>
</table></main></body></html>
</xsl:template>
</xsl:stylesheet>
