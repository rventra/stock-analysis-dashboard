# Stock Analysis Project - AGENTS.md

## Project Overview
Automated equity research report generation pipeline with AI-powered recommendations and Motley Fool-style HTML reporting.

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Data Sources   │───▶│  Processing     │───▶│   Outputs       │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ • YFinance      │    │ • SEC EDGAR     │    │ • JSON Recs     │
│ • Finnhub News  │    │ • DeepSeek AI   │    │ • HTML Reports  │
│ • TA Library    │    │ • Sentiment     │    │ • S3 Data       │
│ • SEC EDGAR     │    │ • AWS Lambda    │    │ • DynamoDB      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### AWS Lambda Functions

| Function | Trigger | Purpose | Output |
|----------|---------|---------|--------|
| `price_fetcher_lambda.py` | EventBridge (5 min) | Real-time prices | DynamoDB, S3 |
| `lambda_edgar_fetcher.py` | EventBridge (6 AM ET) | SEC filings | S3 (rolling_4.json) |

## Directory Structure
```
stock_analysis/
├── financial_data/          # YFinance fundamental data
│   └── {ticker}_financial_data.json
├── technical_data/          # TA indicators (RSI, MACD, etc.)
│   └── {ticker}_technical_data.json
├── news_data/               # Finnhub news with sentiment
│   └── {ticker}_news_data.json
├── recommendations/         # AI-generated JSON recommendations
│   └── {ticker}_recommendation.json
├── reports/                 # Final HTML reports + landing page
│   ├── index.html          # Landing page with hero + news
│   └── {ticker}_*_report.html
├── lambda_edgar_fetcher.py  # AWS Lambda: SEC EDGAR filing fetcher
├── price_fetcher_lambda.py  # AWS Lambda: Real-time price fetcher
├── generate_landing_page.py # Landing page generator (hero + news)
├── pull_news_data.py        # Finnhub news + sentiment
├── generate_recommendation.py  # DeepSeek AI recommendations
├── generate_fool_report_direct.py # Motley Fool style HTML (direct)
├── styles_fool_format.md    # Motley Fool design specification
├── .github/workflows/       # CI/CD automation
│   └── deploy.yml          # Amplify auto-deploy workflow
└── AGENTS.md               # This file
```

## API Configuration

### AWS Secrets (us-east-2)
| Secret Name | Format | Usage |
|-------------|--------|-------|
| `OpenRouterAPIKey` | `{"api_key": "sk-or-v1-..."}` | LLM calls |
| `finnhub-api-key` | Plain string | News data |

### GitHub Secrets (for Amplify Deploy)
| Secret Name | Value |
|-------------|-------|
| `AWS_ACCESS_KEY_ID` | AWS access key with Amplify permissions |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key |
| `AMPLIFY_APP_ID` | `d2oj62s24a5j4l` |

### LLM Models
| Model | Cost | Use Case | Status |
|-------|------|----------|--------|
| `deepseek/deepseek-v3.1-terminus` | $0.21/M in, $0.79/M out | Recommendations | ✅ Working |
| `MiniMax/MiniMax-M2.5` | Cheaper | HTML Generation | ❌ Timeout issues |

## Data Pipeline

### 1. Fundamental Data (`pull_fundamental_data.py`)
- Uses `yfinance` for financial statements
- Cache logic: skips if <24h old
- Outputs: revenue, margins, ratios, dividend yield

### 2. Technical Data (`pull_technical_data.py`)
- Uses `ta` library for indicators
- RSI, MACD, Bollinger Bands, MAs
- 3-month and 1-year price history

### 3. News Data (`pull_news_data.py`)
- Finnhub API: 120 days of news
- Sentiment analysis: keyword-based
- Outputs: articles array with sentiment scores

### 4. SEC EDGAR (`lambda_edgar_fetcher.py`)
- **AWS Lambda** triggered daily at 6 AM ET via EventBridge
- CIK lookup via SEC API with S3 caching
- Fetches latest 10-K and 10-Q filings
- XBRL parsing for key financial metrics
- Maintains "rolling 4" archive (1 annual + 3 quarterly or 4 quarterly)
- Handles rate limiting (10 req/sec max)
- S3 storage: `s3://{bucket}/edgar/{ticker}/rolling_4.json`

### 5. Recommendations (`generate_recommendation.py`)
- Aggregates all data sources
- DeepSeek V3.1 for structured JSON output
- Traffic light scoring system:
  - 🟢 GREEN: Strong fundamentals, buy
  - 🟡 YELLOW: Mixed signals, hold
  - 🔴 RED: Weak fundamentals, sell
- Weights: Fundamental 35%, Technical 25%, Sentiment 20%, Risk 20%

### 6. EDGAR Fetcher Lambda (`lambda_edgar_fetcher.py`)
AWS Lambda function triggered daily at 6:00 AM ET to maintain a "rolling 4" of SEC filings.

**Rolling 4 Logic:**
- Most recent 10-K + 3 most recent 10-Qs, OR
- 4 most recent 10-Qs between annual reports

**Data Sources:**
- SEC Submissions API: `https://data.sec.gov/submissions/CIK{cik}.json`
- SEC Filings: `https://www.sec.gov/Archives/edgar/data/{cik}/{accession}/{filename}`

**XBRL Metrics Extracted:**
- Revenue / Total Revenues
- Net Income / Net Income Loss
- Earnings Per Share (Diluted)
- Total Assets
- Total Liabilities
- Stockholders Equity
- Operating Cash Flow

**Rate Limiting:**
- 100ms delay between requests (max 10 req/sec)
- SECRateLimiter class for consistent throttling
- Required User-Agent header with contact email

**Environment Variables:**
```bash
S3_BUCKET_NAME=stock-analysis-data
TRACKED_TICKERS=AAPL,MSFT,GOOGL,AMZN,TSLA,NVDA,META,JPM,JNJ,V,PG,UNH,HD,MA,DIS,NVDA,BAC,ADBE,CRM,ACN,NFLX
SEC_USER_AGENT="YourName contact@email.com"
```

**S3 Output Structure:**
```
s3://{bucket}/
├── edgar/{ticker}/
│   ├── rolling_4.json          # Main rolling 4 archive
│   └── raw/{accession}.xml     # Raw XBRL filings
└── edgar/cache/
    └── cik_lookup.json         # CIK cache
```

**Rolling 4 JSON Schema:**
```json
{
  "ticker": "AAPL",
  "cik": "0000320193",
  "lastUpdated": "2025-02-27T12:00:00Z",
  "filings": [
    {
      "form": "10-Q",
      "fiscalPeriod": "Q1",
      "fiscalYear": "2025",
      "filingDate": "2025-02-07",
      "accessionNumber": "0000320193-25-000008",
      "metrics": {
        "revenue": 124300000000,
        "netIncome": 36300000000,
        "eps": 2.40,
        "totalAssets": 380000000000,
        "totalLiabilities": 290000000000,
        "shareholdersEquity": 90000000000,
        "operatingCashFlow": 35830000000
      }
    }
  ]
}
```

**IAM Permissions Required:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::stock-analysis-data/edgar/*"
    }
  ]
}
```

### 7. HTML Reports

#### Option A: LLM-Based (`generate_html_report_fool.py`)
- Uses DeepSeek to generate HTML from design spec
- More narrative, varied content
- ⚠️ API timeout issues on large requests

#### Option B: Direct Generation (`generate_fool_report_direct.py`)
- Template-based, no LLM call
- Faster, more reliable
- Motley Fool style with:
  - Article header with thesis
  - Price box (current/target)
  - Bull case section
  - Bear case section
  - Key metrics bar
  - "What it means for investors" conclusion

## Design Specification

### Motley Fool Style (`styles_fool_format.md`)
- **Philosophy**: Narrative-first, approachable, balanced
- **Colors**: Fool Green (#3D8B37), Navy (#1E3A5F), Light Gray (#F7F7F7)
- **Typography**: Source Sans Pro, 18px body, generous line-height
- **Layout**: Max-width 700px, centered, mobile-responsive

## Deployment

### AWS Amplify Hosting
- **App ID**: `d2oj62s24a5j4l`
- **Region**: us-east-2
- **Console**: https://console.aws.amazon.com/amplify/apps/d2oj62s24a5j4l/
- **GitHub Repo**: https://github.com/rventra/stock-analysis-dashboard
- **Auto-deploy**: GitHub Actions triggers on push to master

### Landing Page (`generate_landing_page.py`)
- Hero section with stock count, buy signals, average upside
- Features section (AI Analysis, Traffic Lights, Price Targets, News)
- Aggregated news grid from all tracked tickers
- Stock recommendations table with signals and links to reports
- Dark theme with Motley Fool color palette

### GitHub Actions Workflow
- File: `.github/workflows/deploy.yml`
- Triggers: Push to master branch
- Steps: Checkout → Generate Landing Page → Deploy to Amplify

## Current Status (2026-03-06)

### ✅ Completed
- [x] Data pipeline (fundamental, technical, news)
- [x] SEC EDGAR integration with caching
- [x] AI recommendation engine (DeepSeek)
- [x] Traffic light scoring system
- [x] Motley Fool style design spec
- [x] Direct HTML generation (template-based)
- [x] Price Fetcher Lambda (EventBridge triggered)
- [x] EDGAR Fetcher Lambda (daily 6 AM ET)
- [x] CIK lookup with S3 caching
- [x] Rolling 4 filing maintenance
- [x] Landing page with hero + news section
- [x] AWS Amplify hosting setup
- [x] GitHub Actions auto-deploy

### ⚠️ Known Issues
1. **MiniMax M2.5 Timeout**: 180s+ response times for HTML generation
   - **Workaround**: Using DeepSeek or direct template generation
2. **Windows Unicode**: Removed emojis from print statements
3. **API Costs**: DeepSeek ~$0.21/M input, monitor usage

### 📊 ACN Analysis Results (Latest)
- **Current Price**: $192.12
- **Signal**: 🟢 BUY (HIGH confidence)
- **Base Target**: $285 (+48.4% upside)
- **Time Horizon**: 12-18 months
- **Thesis**: Deeply oversold (RSI 21.6), strong fundamentals, 3.3% yield
- **Traffic Lights**: Fundamental STRONG, Technical OVERSOLD, Sentiment MIXED, Risk MODERATE

## Usage

### Generate Full Pipeline
```bash
cd stock_analysis

# 1. Pull all data
python pull_fundamental_data.py  # Enter: ACN
python pull_technical_data.py    # Enter: ACN
python pull_news_data.py         # Enter: ACN

# 2. Generate recommendation
python generate_recommendation.py  # Enter: ACN

# 3. Generate HTML report
python generate_fool_report_direct.py  # Enter: ACN
```

### Quick Report Generation
```bash
cd stock_analysis
echo "ACN" | python generate_fool_report_direct.py
```

### Generate Landing Page
```bash
cd stock_analysis
python generate_landing_page.py
# Outputs: reports/index.html
```

### Deploy to Amplify
```bash
# Push to master - auto-deploys via GitHub Actions
git add .
git commit -m "Update reports"
git push
```

## Future Enhancements
1. Add charts/visualization (Plotly or Chart.js)
2. Batch processing for multiple tickers
3. Email delivery of reports
4. Compare functionality (side-by-side stocks)
5. Historical recommendation tracking
6. Web dashboard for viewing reports

## Notes
- All scripts use AWS Secrets Manager for API keys
- Cache logic prevents redundant API calls
- Reports auto-open in browser after generation
- Unicode handling fixed for Windows environments
