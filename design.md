# Stock Analysis - Ticker View Design System

## Overview
Standardized HTML report format for equity research reports generated via MiniMax M2.5 through OpenRouter API.

## Design Philosophy
- **Consistent Structure**: All tickers follow the same layout pattern
- **Narrative-First**: Story-driven analysis like Motley Fool
- **Mobile-Responsive**: Works on all devices
- **Data-Rich**: Key metrics prominently displayed
- **Professional**: Clean, modern aesthetic

---

## Color Palette

### Brand Colors
| Name | HEX | Usage |
|------|-----|-------|
| Fool Green | #3D8B37 | BUY signals, positive metrics, accent border |
| Fool Red | #C41E3A | SELL signals, negative metrics, risk warnings |
| Fool Yellow | #F59E0B | HOLD signals, cautionary notes |
| Fool Navy | #1E3A5F | Primary text, headers, ticker badges |
| White | #FFFFFF | Background |
| Light Gray | #F7F7F7 | Section backgrounds, price box |
| Border Gray | #E5E7EB | Dividers, borders |
| Text Gray | #6B7280 | Secondary text, labels |
| Muted Text | #9CA3AF | Dates, tertiary info |

---

## Typography

### Font Stack
```css
font-family: 'Source Sans Pro', 'Helvetica Neue', Arial, sans-serif;
```

### Type Scale
| Element | Size | Weight | Usage |
|---------|------|--------|-------|
| H1 (Company) | 36px | 700 | Company name |
| H2 (Section) | 24px | 700 | Bull/Bear case headers |
| H3 (Subsection) | 20px | 600 | Sub-headers |
| Body | 18px | 400 | Article text |
| Lead | 20px | 400 | Introduction paragraph |
| Data | 28px | 700 | Current price display |
| Label | 14px | 600 | Price box labels, uppercase |
| Small | 14px | 400 | Footnotes, metadata |

---

## Layout Structure

### Container
- Max-width: 700px
- Centered with auto margins
- Padding: 40px 20px
- Background: White

### Page Structure
```
┌─────────────────────────────────────────────────────────┐
│ ARTICLE HEADER                                          │
│ Company Name [TICKER]                                   │
│ Thesis statement subtitle                               │
│ Publication date                                        │
├─────────────────────────────────────────────────────────┤
│ PRICE BOX (Floats right on desktop)                     │
│ ┌─────────────────────────────────────────────────┐     │
│ │ Current Price: $XXX.XX                          │     │
│ │ Price Change: +/- X.X%                          │     │
│ │ Entry Zone: $XXX-$XXX                           │     │
│ │ Base Target: $XXX (+XX%)                        │     │
│ │ Bull Target: $XXX (+XX%)                        │     │
│ │ Stop Loss: $XXX                                 │     │
│ └─────────────────────────────────────────────────┘     │
├─────────────────────────────────────────────────────────┤
│ SIGNAL BANNER                                           │
│ 🟢 BUY | Confidence: HIGH | Time Horizon: X months     │
├─────────────────────────────────────────────────────────┤
│ EXECUTIVE SUMMARY                                       │
│ Brief investment thesis paragraph                       │
├─────────────────────────────────────────────────────────┤
│ INTRODUCTION                                            │
│ 2-3 paragraphs setting context                          │
├─────────────────────────────────────────────────────────┤
│ BULL CASE                                               │
│ Why the stock could outperform                          │
│ • Key strength 1                                        │
│ • Key strength 2                                        │
│ • Key strength 3                                        │
├─────────────────────────────────────────────────────────┤
│ BEAR CASE                                               │
│ Why the stock could underperform                        │
│ • Key risk 1                                            │
│ • Key risk 2                                            │
│ • Key risk 3                                            │
├─────────────────────────────────────────────────────────┤
│ TRAFFIC LIGHT ANALYSIS                                  │
│ ┌─────────┬───────────┬────────────┬──────────┐         │
│ │ Overall │ Fundamental│ Technical │ Sentiment│ Risk     │
│ │   🟢    │    🟢      │    🟢     │    🟡    │   🟢     │
│ │  BUY    │  STRONG   │ OVERSOLD  │  MIXED   │ MODERATE │
│ └─────────┴───────────┴────────────┴──────────┘         │
├─────────────────────────────────────────────────────────┤
│ MARKET CONDITIONS                                       │
│ Why the stock declined + Contrarian view                │
├─────────────────────────────────────────────────────────┤
│ RECENT NEWS                                             │
│ Key headlines with sentiment analysis                   │
├─────────────────────────────────────────────────────────┤
│ INVESTMENT STRATEGY                                     │
│ • Recommended Action                                    │
│ • Entry Strategy                                        │
│ • Exit Strategy                                         │
│ • Timeframe                                             │
├─────────────────────────────────────────────────────────┤
│ CONCLUSION                                              │
│ What It Means for Investors                             │
│ • Investment thesis summary                             │
│ • Who should buy                                        │
│ • Who should avoid                                      │
│ • Final verdict                                         │
├─────────────────────────────────────────────────────────┤
│ FOOTER                                                  │
│ Disclaimer | Data sources | Analysis date               │
└─────────────────────────────────────────────────────────┘
```

---

## Component Specifications

### Article Header
```html
<header class="article-header">
    <h1>Company Name <span class="ticker">TICKER</span></h1>
    <p class="thesis">One-line investment thesis statement</p>
    <p class="publication-date">March 5, 2026</p>
</header>
```
- Border-bottom: 3px solid #3D8B37 (Fool Green)
- Padding-bottom: 24px
- Margin-bottom: 32px

### Price Box
```html
<div class="price-box">
    <h3>Price Analysis</h3>
    <div class="current-price">$XXX.XX</div>
    <div class="price-change positive">+X.X%</div>
    <!-- Price rows -->
</div>
```
- Floats right on desktop (width: 240px)
- Full width on mobile
- Background: #F7F7F7
- Border-left: 4px solid signal color
- Border-radius: 8px
- Padding: 20px

### Signal Banner
```html
<div class="signal-banner buy">
    <span class="signal-icon">🟢</span>
    <span class="signal-text">BUY</span>
    <span class="signal-divider">|</span>
    <span>Confidence: HIGH</span>
    <span class="signal-divider">|</span>
    <span>Time Horizon: 12-18 months</span>
</div>
```
- Background: Gradient based on signal
- Border-radius: 8px
- Padding: 16px 24px
- Font-size: 16px
- Font-weight: 600

### Traffic Light Grid
```html
<div class="traffic-light-grid">
    <div class="light-item">
        <div class="light-label">Overall</div>
        <div class="light-signal">🟢</div>
        <div class="light-rating">BUY</div>
    </div>
    <!-- Repeat for each component -->
</div>
```
- Display: grid (5 columns on desktop, 2 on mobile)
- Gap: 16px
- Text-align: center
- Padding: 16px
- Background: #F7F7F7
- Border-radius: 8px

### Section Headers
```html
<h2>Bull case:</h2>
```
- Font-size: 24px
- Font-weight: 700
- Margin-top: 48px
- Margin-bottom: 24px
- Color: #1E3A5F

### Content Sections
- Line-height: 1.6
- Margin-bottom: 24px
- Bullet lists with generous spacing

---

## Responsive Breakpoints

### Desktop (>900px)
- Price box floats right
- Traffic lights: 5 columns
- Full layout

### Tablet (600-900px)
- Price box above content
- Traffic lights: 3 columns
- Adjusted padding

### Mobile (<600px)
- Single column
- Price box: 100% width
- Traffic lights: 2 columns
- Reduced font sizes slightly
- Increased touch targets

---

## Signal Colors by Type

| Signal | Background | Border | Text |
|--------|------------|--------|------|
| BUY (🟢) | #ECFDF5 | #0D7A47 | #0D7A47 |
| HOLD (🟡) | #FFFBEB | #F59E0B | #B45309 |
| SELL (🔴) | #FEF2F2 | #C41E3A | #C41E3A |

---

## Data Sources

Reports are generated using:
- **Fundamental Data**: YFinance API
- **Technical Data**: TA-Lib indicators
- **News Data**: Finnhub API
- **AI Analysis**: DeepSeek V3.1 Terminus (recommendations)
- **HTML Generation**: MiniMax M2.5 via OpenRouter

---

## File Naming Convention

```
reports/{TICKER}_MiniMax_Report_{YYYYMMDD}.html
```

Examples:
- `AAPL_MiniMax_Report_20260305.html`
- `BABA_MiniMax_Report_20260305.html`
- `NVDA_MiniMax_Report_20260305.html`

---

## Supported Tickers

| Ticker | Company | Sector |
|--------|---------|--------|
| AAPL | Apple Inc. | Technology |
| ADBE | Adobe Inc. | Technology |
| AMZN | Amazon.com Inc. | Consumer Cyclical |
| AVGO | Broadcom Inc. | Technology |
| BABA | Alibaba Group | Consumer Cyclical |
| BAC | Bank of America | Financials |
| CRM | Salesforce Inc. | Technology |
| DIS | Walt Disney Co. | Communication Services |
| GOOGL | Alphabet Inc. | Communication Services |
| HD | Home Depot Inc. | Consumer Cyclical |
| JNJ | Johnson & Johnson | Healthcare |
| JPM | JPMorgan Chase | Financials |
| MA | Mastercard Inc. | Financials |
| META | Meta Platforms | Communication Services |
| MSFT | Microsoft Corp. | Technology |
| NFLX | Netflix Inc. | Communication Services |
| NVDA | NVIDIA Corp. | Technology |
| PG | Procter & Gamble | Consumer Defensive |
| TSLA | Tesla Inc. | Consumer Cyclical |
| UNH | UnitedHealth Group | Healthcare |
| V | Visa Inc. | Financials |

---

## Generation Pipeline

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  pull_yfinance   │────▶│ generate_rec     │────▶│ generate_html    │
│  _data.py        │     │ _recommendation  │     │ _minimax.py      │
│  (Fundamentals)  │     │ (DeepSeek V3.1)  │     │ (MiniMax M2.5)   │
└──────────────────┘     └──────────────────┘     └──────────────────┘
         │                        │                        │
         ▼                        ▼                        ▼
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ pull_technical   │     │  recommendations │     │      reports     │
│ _data.py         │     │  /{TICKER}_rec.  │     │  /{TICKER}_Mini  │
│  (TA Indicators) │     │      json        │     │  Max_Report.html │
└──────────────────┘     └──────────────────┘     └──────────────────┘
         │
         ▼
┌──────────────────┐
│  pull_news_data  │
│     .py          │
│  (Finnhub News)  │
└──────────────────┘
```

---

## API Configuration

### AWS Secrets Manager
- **Region**: us-east-2
- **Secret Name**: `OpenRouterAPIKey`
- **Format**: `{"api_key": "sk-or-v1-..."}`

### OpenRouter Models
| Model | Usage | Status |
|-------|-------|--------|
| `deepseek/deepseek-v3.1-terminus` | Recommendations | ✅ Active |
| `minimax/minimax-m2.5` | HTML Generation | ✅ Active |

---

## Maintenance Notes

1. **API Keys**: Stored in AWS Secrets Manager (us-east-2)
2. **Rate Limits**: OpenRouter has generous limits for both models
3. **Timeouts**: MiniMax M2.5 has 300s timeout configured
4. **Caching**: Data files cached for 24 hours
5. **Unicode**: Windows-compatible (no emoji issues)

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2026-03-05 | 1.0 | Initial standardized ticker view with MiniMax M2.5 |
