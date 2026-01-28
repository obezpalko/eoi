<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" 
                xmlns:html="http://www.w3.org/TR/REC-html40"
                xmlns:sitemap="http://www.sitemaps.org/schemas/sitemap/0.9"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"/>
    <xsl:template match="/">
        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="es" lang="es">
            <head>
                <title>Sitemap | EOI - Español A1</title>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1" />
                <link rel="preconnect" href="https://fonts.googleapis.com" />
                <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="" />
                <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&amp;family=Inter:wght@400;500;700&amp;display=swap" rel="stylesheet" />
                <style type="text/css">
                    :root {
                        --primary: #7b97aa;
                        --primary-rgb: 123, 151, 170;
                        --accent: #84a59d;
                        --bg: #161618;
                        --surface: #232326;
                        --text: #ebebec;
                        --text-muted: #a0a0a5;
                        --border: rgba(255, 255, 255, 0.1);
                        --glass: rgba(35, 35, 38, 0.7);
                    }

                    @media (prefers-color-scheme: light) {
                        :root {
                            --primary: #284b63;
                            --primary-rgb: 40, 75, 99;
                            --accent: #84a59d;
                            --bg: #faf8f8;
                            --surface: #ffffff;
                            --text: #2b2b2b;
                            --text-muted: #666666;
                            --border: rgba(0, 0, 0, 0.1);
                            --glass: rgba(255, 255, 255, 0.8);
                        }
                    }

                    * {
                        box-sizing: border-box;
                        margin: 0;
                        padding: 0;
                    }

                    body {
                        font-family: 'Inter', system-ui, -apple-system, sans-serif;
                        background-color: var(--bg);
                        color: var(--text);
                        line-height: 1.6;
                        min-height: 100vh;
                        padding: 2rem 1rem;
                    }

                    .container {
                        max-width: 1000px;
                        margin: 0 auto;
                        position: relative;
                    }

                    .header {
                        margin-bottom: 3rem;
                        text-align: center;
                        animation: fadeInDown 0.8s ease-out;
                    }

                    h1 {
                        font-family: 'Outfit', sans-serif;
                        font-size: 3.5rem;
                        font-weight: 700;
                        background: linear-gradient(135deg, var(--primary), var(--accent));
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        margin-bottom: 0.5rem;
                        letter-spacing: -0.02em;
                    }

                    .stats {
                        display: flex;
                        gap: 2rem;
                        justify-content: center;
                        margin-top: 1rem;
                        font-family: 'Outfit', sans-serif;
                    }

                    .stat-item {
                        background: var(--glass);
                        backdrop-filter: blur(10px);
                        border: 1px solid var(--border);
                        padding: 0.5rem 1.5rem;
                        border-radius: 100px;
                        font-size: 0.9rem;
                        color: var(--text-muted);
                        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
                    }

                    .stat-item strong {
                        color: var(--primary);
                        margin-right: 0.25rem;
                    }

                    .sitemap-list {
                        background: var(--glass);
                        backdrop-filter: blur(12px);
                        border: 1px solid var(--border);
                        border-radius: 24px;
                        overflow: hidden;
                        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                        animation: fadeInUp 0.8s ease-out;
                    }

                    table {
                        width: 100%;
                        border-collapse: collapse;
                        text-align: left;
                    }

                    th {
                        background: rgba(var(--primary-rgb), 0.1);
                        padding: 1.25rem 1.5rem;
                        font-family: 'Outfit', sans-serif;
                        font-weight: 600;
                        text-transform: uppercase;
                        font-size: 0.75rem;
                        letter-spacing: 0.1em;
                        color: var(--primary);
                        border-bottom: 1px solid var(--border);
                    }

                    td {
                        padding: 1.25rem 1.5rem;
                        border-bottom: 1px solid var(--border);
                        font-size: 0.95rem;
                    }

                    tr:last-child td {
                        border-bottom: none;
                    }

                    tr:hover td {
                        background: rgba(var(--primary-rgb), 0.03);
                    }

                    .loc-link {
                        color: var(--text);
                        text-decoration: none;
                        font-weight: 500;
                        transition: color 0.2s;
                        display: flex;
                        align-items: center;
                        gap: 0.5rem;
                    }

                    .loc-link:hover {
                        color: var(--primary);
                    }

                    .loc-link:after {
                        content: '→';
                        opacity: 0;
                        transform: translateX(-10px);
                        transition: all 0.2s;
                    }

                    .loc-link:hover:after {
                        opacity: 1;
                        transform: translateX(0);
                    }

                    .lastmod {
                        color: var(--text-muted);
                        font-family: 'Outfit', sans-serif;
                        font-size: 0.85rem;
                    }

                    .path-badge {
                        display: inline-block;
                        padding: 0.2rem 0.6rem;
                        border-radius: 6px;
                        background: rgba(var(--primary-rgb), 0.1);
                        color: var(--primary);
                        font-size: 0.75rem;
                        font-weight: 600;
                        margin-right: 0.75rem;
                        vertical-align: middle;
                    }

                    @keyframes fadeInDown {
                        from { opacity: 0; transform: translateY(-20px); }
                        to { opacity: 1; transform: translateY(0); }
                    }

                    @keyframes fadeInUp {
                        from { opacity: 0; transform: translateY(20px); }
                        to { opacity: 1; transform: translateY(0); }
                    }

                    @media (max-width: 768px) {
                        h1 { font-size: 2.5rem; }
                        td, th { padding: 1rem; }
                        .lastmod-col { display: none; }
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <header class="header">
                        <h1>Sitemap</h1>
                        <div class="stats">
                            <div class="stat-item">
                                <strong><xsl:value-of select="count(sitemap:urlset/sitemap:url)"/></strong> Páginas Totales
                            </div>
                            <div class="stat-item">
                                Actualizado: <strong><xsl:value-of select="substring(sitemap:urlset/sitemap:url[1]/sitemap:lastmod, 1, 10)"/></strong>
                            </div>
                        </div>
                    </header>

                    <main class="sitemap-list">
                        <table>
                            <thead>
                                <tr>
                                    <th>Página</th>
                                    <th class="lastmod-col">Última Modificación</th>
                                </tr>
                            </thead>
                            <tbody>
                                <xsl:for-each select="sitemap:urlset/sitemap:url">
                                    <xsl:sort select="sitemap:lastmod" order="descending"/>
                                    <tr>
                                        <td>
                                            <a class="loc-link" href="{sitemap:loc}">
                                                <xsl:variable name="itemPath" select="substring-after(sitemap:loc, 'obezpalko.github.io/eoi/')"/>
                                                <xsl:if test="$itemPath != ''">
                                                    <span class="path-badge">
                                                        <xsl:choose>
                                                            <xsl:when test="contains($itemPath, '/')">
                                                                <xsl:value-of select="substring-before($itemPath, '/')"/>
                                                            </xsl:when>
                                                            <xsl:otherwise>Raíz</xsl:otherwise>
                                                        </xsl:choose>
                                                    </span>
                                                </xsl:if>
                                                <xsl:choose>
                                                    <xsl:when test="$itemPath = ''">Inicio</xsl:when>
                                                    <xsl:otherwise>
                                                        <xsl:value-of select="translate(substring-after($itemPath, '/'), '-', ' ')"/>
                                                        <xsl:if test="not(contains($itemPath, '/'))">
                                                            <xsl:value-of select="translate($itemPath, '-', ' ')"/>
                                                        </xsl:if>
                                                    </xsl:otherwise>
                                                </xsl:choose>
                                            </a>
                                        </td>
                                        <td class="lastmod-col">
                                            <span class="lastmod">
                                                <xsl:value-of select="substring(sitemap:lastmod, 1, 10)"/>
                                                <xsl:if test="contains(sitemap:lastmod, 'T')">
                                                    <span style="margin: 0 0.5rem; opacity: 0.3;">|</span>
                                                    <xsl:value-of select="substring(sitemap:lastmod, 12, 5)"/>
                                                </xsl:if>
                                            </span>
                                        </td>
                                    </tr>
                                </xsl:for-each>
                            </tbody>
                        </table>
                    </main>
                </div>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
