#!/usr/bin/env python3
"""
generate_landing_page.py

Generates a landing page (index.html) with:
- Hero/Summary section explaining the stock screener
- Aggregated news section from all tickers
- Stock summary table with links to reports
"""

import json
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path("reports")
RECOMMENDATIONS_DIR = Path("recommendations")
NEWS_DIR = Path("news_data")


def load_all_recommendations():
    """Load all recommendation JSON files."""
    recommendations = []

    for filepath in RECOMMENDATIONS_DIR.glob("*_recommendation.json"):
        if filepath.name == "recommendation_summary.json":
            continue

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                ticker = data['metadata']['ticker']
                recommendations.append({
                    'ticker': ticker,
                    'company': data['metadata']['company_name'],
                    'sector': data['metadata']['sector'],
                    'date': data['metadata']['analysis_date'],
                    'signal': data['executive_summary']['recommendation']['signal'],
                    'confidence': data['executive_summary']['recommendation']['confidence'],
                    'time_horizon': data['executive_summary']['recommendation']['time_horizon'],
                    'current_price': data['executive_summary']['price_targets']['current'],
                    'base_target': data['executive_summary']['price_targets']['base_target'],
                    'upside': data['executive_summary']['price_targets'].get('potential_upside', {}).get('base', 'N/A'),
                    'overall_signal': data['traffic_light_scores']['overall']['signal'],
                    'fundamental': data['traffic_light_scores']['components']['fundamental_health']['signal'],
                    'technical': data['traffic_light_scores']['components']['technical_setup']['signal'],
                    'sentiment': data['traffic_light_scores']['components']['market_sentiment']['signal'],
                    'risk': data['traffic_light_scores']['components']['risk_assessment']['signal'],
                })
        except Exception as e:
            print(f"[WARN] Failed to load {filepath}: {e}")

    recommendations.sort(key=lambda x: x['ticker'])
    return recommendations


def load_all_news():
    """Load and aggregate news from all tickers."""
    all_news = []

    for filepath in NEWS_DIR.glob("*_news_data.json"):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                ticker = data['metadata']['symbol']

                # Get top 3 articles per ticker (most recent)
                articles = data.get('articles', [])[:3]
                for article in articles:
                    article['ticker'] = ticker
                    all_news.append(article)
        except Exception as e:
            print(f"[WARN] Failed to load news {filepath}: {e}")

    # Sort by timestamp (most recent first)
    all_news.sort(key=lambda x: x.get('timestamp', 0), reverse=True)

    # Return top 12 articles
    return all_news[:12]


def get_signal_color(signal):
    """Get CSS color for signal."""
    if '🟢' in signal or 'GREEN' in signal or 'BUY' in signal:
        return '#0D7A47'
    elif '🟡' in signal or 'YELLOW' in signal or 'HOLD' in signal:
        return '#F59E0B'
    elif '🔴' in signal or 'RED' in signal or 'SELL' in signal:
        return '#C41E3A'
    return '#6B7280'


def get_signal_bg(signal):
    """Get CSS background color for signal."""
    if '🟢' in signal or 'GREEN' in signal or 'BUY' in signal:
        return '#ECFDF5'
    elif '🟡' in signal or 'YELLOW' in signal or 'HOLD' in signal:
        return '#FFFBEB'
    elif '🔴' in signal or 'RED' in signal or 'SELL' in signal:
        return '#FEF2F2'
    return '#F3F4F6'


def get_sentiment_badge(sentiment):
    """Get sentiment badge HTML."""
    if sentiment == 'positive':
        return '<span class="sentiment-badge positive">Bullish</span>'
    elif sentiment == 'negative':
        return '<span class="sentiment-badge negative">Bearish</span>'
    else:
        return '<span class="sentiment-badge neutral">Neutral</span>'


def format_datetime(dt_str):
    """Format datetime string for display."""
    try:
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        return dt.strftime('%b %d, %I:%M %p')
    except:
        return dt_str


def generate_html(recommendations, news):
    """Generate the landing page HTML."""

    # Calculate summary stats
    buy_count = sum(1 for r in recommendations if 'BUY' in r['signal'])
    hold_count = sum(1 for r in recommendations if 'HOLD' in r['signal'])
    sell_count = sum(1 for r in recommendations if 'SELL' in r['signal'])

    # Calculate average upside
    valid_upside = [r['upside'] for r in recommendations if isinstance(r['upside'], (int, float))]
    avg_upside = sum(valid_upside) / len(valid_upside) if valid_upside else 0

    # Build ticker options
    ticker_options = '\n'.join([
        f'<option value="{r["ticker"]}">{r["ticker"]} - {r["company"]}</option>'
        for r in recommendations
    ])

    # Build table rows
    table_rows = ''
    for r in recommendations:
        signal_color = get_signal_color(r['signal'])
        signal_bg = get_signal_bg(r['signal'])
        report_filename = f"{r['ticker']}_MiniMax_Report_{datetime.now().strftime('%Y%m%d')}.html"

        upside_display = f"+{r['upside']:.1f}%" if isinstance(r['upside'], (int, float)) else str(r['upside'])

        table_rows += f'''
        <tr>
            <td>
                <div class="ticker-cell">
                    <span class="ticker-symbol">{r['ticker']}</span>
                    <span class="company-name">{r['company']}</span>
                </div>
            </td>
            <td><span class="sector-tag">{r['sector']}</span></td>
            <td class="price">${r['current_price']:.2f}</td>
            <td class="price target">${r['base_target']:.2f}</td>
            <td class="upside">{upside_display}</td>
            <td>
                <span class="signal-badge" style="background: {signal_bg}; color: {signal_color}; border: 1px solid {signal_color};">
                    {r['signal']}
                </span>
            </td>
            <td><span class="confidence">{r['confidence']}</span></td>
            <td>
                <a href="{report_filename}" class="view-btn">View Report</a>
            </td>
        </tr>
        '''

    # Build news cards
    news_cards = ''
    for article in news:
        image_html = f'<img src="{article.get("image", "")}" alt="" class="news-image" onerror="this.style.display=\'none\'">' if article.get('image') else ''

        news_cards += f'''
        <div class="news-card">
            {image_html}
            <div class="news-content">
                <div class="news-meta">
                    <span class="news-ticker">{article['ticker']}</span>
                    <span class="news-source">{article.get('source', 'Unknown')}</span>
                    {get_sentiment_badge(article.get('sentiment', 'neutral'))}
                </div>
                <h3 class="news-headline">{article.get('headline', 'No headline')}</h3>
                <p class="news-summary">{article.get('summary', '')[:120]}...</p>
                <span class="news-time">{format_datetime(article.get('datetime', ''))}</span>
            </div>
        </div>
        '''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stock Analysis Dashboard | AI-Powered Equity Research</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Sans+Pro:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            --fool-green: #3D8B37;
            --fool-navy: #1E3A5F;
            --fool-red: #C41E3A;
            --fool-yellow: #F59E0B;
            --bg-dark: #0F172A;
            --bg-card: #1E293B;
            --border: #334155;
            --text-primary: #F9FAFB;
            --text-secondary: #94A3B8;
            --accent: #3B82F6;
        }}

        body {{
            font-family: 'Inter', 'Source Sans Pro', sans-serif;
            background: var(--bg-dark);
            color: var(--text-primary);
            min-height: 100vh;
            line-height: 1.6;
        }}

        /* Hero Section */
        .hero {{
            background: linear-gradient(135deg, var(--fool-navy) 0%, #0F172A 50%, #1E3A5F 100%);
            padding: 80px 20px;
            text-align: center;
            border-bottom: 3px solid var(--fool-green);
            position: relative;
            overflow: hidden;
        }}

        .hero::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at 20% 50%, rgba(61, 139, 55, 0.15) 0%, transparent 50%),
                        radial-gradient(circle at 80% 50%, rgba(59, 130, 246, 0.1) 0%, transparent 50%);
            pointer-events: none;
        }}

        .hero-content {{
            max-width: 800px;
            margin: 0 auto;
            position: relative;
            z-index: 1;
        }}

        .hero h1 {{
            font-size: 48px;
            font-weight: 700;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 16px;
        }}

        .hero-icon {{
            font-size: 56px;
        }}

        .hero p {{
            font-size: 20px;
            color: var(--text-secondary);
            margin-bottom: 32px;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }}

        .hero-stats {{
            display: flex;
            justify-content: center;
            gap: 48px;
            flex-wrap: wrap;
        }}

        .hero-stat {{
            text-align: center;
        }}

        .hero-stat-value {{
            font-size: 36px;
            font-weight: 700;
            color: var(--fool-green);
        }}

        .hero-stat-label {{
            font-size: 14px;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        /* Features Section */
        .features {{
            background: var(--bg-card);
            padding: 48px 20px;
            border-bottom: 1px solid var(--border);
        }}

        .features-container {{
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 32px;
        }}

        .feature {{
            text-align: center;
            padding: 24px;
        }}

        .feature-icon {{
            font-size: 40px;
            margin-bottom: 16px;
        }}

        .feature h3 {{
            font-size: 18px;
            margin-bottom: 8px;
            color: var(--text-primary);
        }}

        .feature p {{
            font-size: 14px;
            color: var(--text-secondary);
        }}

        /* News Section */
        .news-section {{
            padding: 64px 20px;
            max-width: 1400px;
            margin: 0 auto;
        }}

        .section-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 32px;
        }}

        .section-header h2 {{
            font-size: 28px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .section-header h2 span {{
            font-size: 28px;
        }}

        .last-updated {{
            color: var(--text-secondary);
            font-size: 14px;
        }}

        .news-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 24px;
        }}

        .news-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            overflow: hidden;
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .news-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(0,0,0,0.3);
        }}

        .news-image {{
            width: 100%;
            height: 160px;
            object-fit: cover;
            background: var(--bg-dark);
        }}

        .news-content {{
            padding: 20px;
        }}

        .news-meta {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 12px;
            flex-wrap: wrap;
        }}

        .news-ticker {{
            background: var(--accent);
            color: white;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
        }}

        .news-source {{
            color: var(--text-secondary);
            font-size: 12px;
        }}

        .sentiment-badge {{
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
        }}

        .sentiment-badge.positive {{
            background: #ECFDF5;
            color: #059669;
        }}

        .sentiment-badge.negative {{
            background: #FEF2F2;
            color: #DC2626;
        }}

        .sentiment-badge.neutral {{
            background: #F3F4F6;
            color: #6B7280;
        }}

        .news-headline {{
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 8px;
            line-height: 1.4;
            color: var(--text-primary);
        }}

        .news-summary {{
            font-size: 13px;
            color: var(--text-secondary);
            margin-bottom: 12px;
            line-height: 1.5;
        }}

        .news-time {{
            font-size: 12px;
            color: var(--text-secondary);
        }}

        /* Table Section */
        .table-section {{
            padding: 64px 20px;
            max-width: 1400px;
            margin: 0 auto;
        }}

        .table-wrapper {{
            background: var(--bg-card);
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid var(--border);
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
        }}

        thead {{
            background: rgba(0,0,0,0.2);
        }}

        th {{
            padding: 16px;
            text-align: left;
            font-weight: 600;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-secondary);
            border-bottom: 1px solid var(--border);
        }}

        td {{
            padding: 16px;
            border-bottom: 1px solid var(--border);
            font-size: 14px;
        }}

        tr:hover {{
            background: rgba(255,255,255,0.03);
        }}

        tr:last-child td {{
            border-bottom: none;
        }}

        .ticker-cell {{
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}

        .ticker-symbol {{
            font-size: 18px;
            font-weight: 700;
            color: var(--accent);
        }}

        .company-name {{
            font-size: 13px;
            color: var(--text-secondary);
        }}

        .sector-tag {{
            background: rgba(59, 130, 246, 0.15);
            color: #60A5FA;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 500;
        }}

        .price {{
            font-family: 'SF Mono', monospace;
            font-weight: 600;
        }}

        .price.target {{
            color: #4ADE80;
        }}

        .upside {{
            color: #4ADE80;
            font-weight: 600;
        }}

        .signal-badge {{
            display: inline-block;
            padding: 6px 12px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 13px;
        }}

        .confidence {{
            color: var(--text-secondary);
            font-size: 13px;
        }}

        .view-btn {{
            background: var(--accent);
            color: white;
            text-decoration: none;
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 13px;
            display: inline-block;
            transition: background 0.2s;
        }}

        .view-btn:hover {{
            background: #2563EB;
        }}

        /* Footer */
        .footer {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 32px 20px;
            text-align: center;
            color: var(--text-secondary);
            font-size: 13px;
            border-top: 1px solid var(--border);
        }}

        .footer a {{
            color: var(--accent);
            text-decoration: none;
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .hero h1 {{
                font-size: 32px;
            }}

            .hero-icon {{
                font-size: 40px;
            }}

            .hero p {{
                font-size: 16px;
            }}

            .hero-stats {{
                gap: 24px;
            }}

            .hero-stat-value {{
                font-size: 28px;
            }}

            .news-grid {{
                grid-template-columns: 1fr;
            }}

            .section-header {{
                flex-direction: column;
                gap: 16px;
                align-items: flex-start;
            }}

            .table-wrapper {{
                overflow-x: auto;
            }}

            table {{
                min-width: 800px;
            }}
        }}
    </style>
</head>
<body>
    <!-- Hero Section -->
    <section class="hero">
        <div class="hero-content">
            <h1>
                <span class="hero-icon">📊</span>
                Stock Analysis Dashboard
            </h1>
            <p>AI-powered equity research reports with traffic light scoring. Get actionable insights, price targets, and sentiment analysis for {len(recommendations)} tracked stocks.</p>
            <div class="hero-stats">
                <div class="hero-stat">
                    <div class="hero-stat-value">{len(recommendations)}</div>
                    <div class="hero-stat-label">Stocks Tracked</div>
                </div>
                <div class="hero-stat">
                    <div class="hero-stat-value">{buy_count}</div>
                    <div class="hero-stat-label">Buy Signals</div>
                </div>
                <div class="hero-stat">
                    <div class="hero-stat-value">+{avg_upside:.0f}%</div>
                    <div class="hero-stat-label">Avg Upside</div>
                </div>
            </div>
        </div>
    </section>

    <!-- Features -->
    <section class="features">
        <div class="features-container">
            <div class="feature">
                <div class="feature-icon">🤖</div>
                <h3>AI-Powered Analysis</h3>
                <p>DeepSeek AI analyzes fundamentals, technicals, and sentiment to generate intelligent recommendations.</p>
            </div>
            <div class="feature">
                <div class="feature-icon">🚦</div>
                <h3>Traffic Light Scoring</h3>
                <p>Clear visual signals: Green (Buy), Yellow (Hold), Red (Sell) based on multi-factor analysis.</p>
            </div>
            <div class="feature">
                <div class="feature-icon">📈</div>
                <h3>Price Targets</h3>
                <p>AI-generated price targets with confidence levels and time horizons for each stock.</p>
            </div>
            <div class="feature">
                <div class="feature-icon">📰</div>
                <h3>Real-Time News</h3>
                <p>Latest market news with sentiment analysis to keep you informed on market movements.</p>
            </div>
        </div>
    </section>

    <!-- News Section -->
    <section class="news-section">
        <div class="section-header">
            <h2><span>📰</span> Latest Market News</h2>
            <span class="last-updated">Updated: {datetime.now().strftime('%B %d, %Y')}</span>
        </div>
        <div class="news-grid">
            {news_cards}
        </div>
    </section>

    <!-- Stock Table Section -->
    <section class="table-section">
        <div class="section-header">
            <h2><span>🎯</span> Stock Recommendations</h2>
        </div>
        <div class="table-wrapper">
            <table>
                <thead>
                    <tr>
                        <th>Company</th>
                        <th>Sector</th>
                        <th>Current Price</th>
                        <th>Target Price</th>
                        <th>Upside</th>
                        <th>Signal</th>
                        <th>Confidence</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <p>Data powered by YFinance, Finnhub, and DeepSeek AI | Reports generated with MiniMax M2.5 via OpenRouter</p>
        <p style="margin-top: 8px;">
            <a href="design.md">View Design System</a> |
            <a href="AGENTS.md">Project Documentation</a>
        </p>
    </footer>

    <script>
        // Add click handling for news cards
        document.querySelectorAll('.news-card').forEach(card => {{
            card.style.cursor = 'pointer';
            card.addEventListener('click', function() {{
                const link = this.querySelector('a');
                if (link) window.open(link.href, '_blank');
            }});
        }});
    </script>
</body>
</html>
'''

    return html


def main():
    print("=" * 70)
    print("GENERATING LANDING PAGE")
    print("=" * 70)

    # Load all recommendations
    print("\n[DATA] Loading recommendations...")
    recommendations = load_all_recommendations()
    print(f"[DATA] Loaded {len(recommendations)} tickers")

    for r in recommendations:
        signal_clean = r['signal'].replace('🟢', 'BUY').replace('🟡', 'HOLD').replace('🔴', 'SELL')
        print(f"  - {r['ticker']}: {signal_clean} ({r['confidence']})")

    # Load all news
    print("\n[DATA] Loading news...")
    news = load_all_news()
    print(f"[DATA] Loaded {len(news)} news articles")

    # Generate HTML
    print("\n[GEN] Generating landing page HTML...")
    html = generate_html(recommendations, news)

    # Save
    output_path = OUTPUT_DIR / "index.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"[SAVED] Landing page saved to: {output_path}")
    print(f"[SAVED] File size: {len(html):,} bytes")

    print("\n" + "=" * 70)
    print("SUCCESS!")
    print("=" * 70)
    print(f"Open reports/index.html in your browser to view the dashboard.")


if __name__ == "__main__":
    main()
