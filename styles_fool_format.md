# Motley Fool-Style Equity Research Format
## Clean, Narrative-Driven Investment Analysis

---

## Design Philosophy
- **Narrative First**: Tell the investment story clearly
- **Readable**: Generous spacing, clear hierarchy
- ** approachable**: Not intimidating like Wall Street research
- **Information Rich**: Key metrics highlighted visually
- **Balanced**: Clear Bull vs Bear presentation

---

## Color Palette

### Brand Colors
| Name | HEX | Usage |
|------|-----|-------|
| Fool Green | #3D8B37 | Primary brand, buy signals |
| Dark Green | #2D6A32 | Headers, strong buy |
| Fool Orange | #FF6B35 | Accent, highlights |
| Navy | #1E3A5F | Text, headers |
| Light Gray | #F7F7F7 | Section backgrounds |
| White | #FFFFFF | Background |

### Signal Colors
| Name | HEX | Usage |
|------|-----|-------|
| Positive | #0D7A47 | Price up, positive metrics |
| Negative | #C41E3A | Price down, negative metrics |
| Neutral | #6B7280 | Neutral data |

---

## Typography

### Font Stack
```css
font-family: 'Source Sans Pro', 'Helvetica Neue', Arial, sans-serif;
```

### Type Scale
| Element | Size | Weight | Usage |
|---------|------|--------|-------|
| Article Title | 36px | 700 | Main headline |
| Section Header | 24px | 700 | Bull/Bear headers |
| Subheader | 20px | 600 | Subsections |
| Body | 18px | 400 | Article text |
| Lead | 20px | 400 | Intro paragraph |
| Data | 16px | 600 | Metrics |
| Small | 14px | 400 | Footnotes |

---

## Layout Structure

```
┌─────────────────────────────────────────────────────────────┐
│ ARTICLE HEADER                                              │
│ Company Name (Ticker)                                       │
│ Brief one-line thesis statement                             │
├─────────────────────────────────────────────────────────────┤
│ PRICE BOX (Right-aligned or floating)                       │
│ Today's Change                    Current Price             │
│ +1.72% (+$1.90)                   $112.56                   │
├─────────────────────────────────────────────────────────────┤
│ INTRODUCTION                                                │
│ 2-3 paragraphs setting up the analysis                      │
│ Context about the company and why it matters                │
├─────────────────────────────────────────────────────────────┤
│ BULL CASE                                                   │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Why this stock could outperform:                        │ │
│ │ • Key strength #1 with explanation                      │ │
│ │ • Key strength #2 with explanation                      │ │
│ │ • Key strength #3 with explanation                      │ │
│ └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ BEAR CASE                                                   │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Why this stock could underperform:                      │ │
│ │ • Key risk #1 with explanation                          │ │
│ │ • Key risk #2 with explanation                          │ │
│ │ • Key risk #3 with explanation                          │ │
│ └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ KEY METRICS (Visual grid)                                   │
│ Revenue: $XXB | P/E: XX | Growth: XX% | Margin: XX%         │
├─────────────────────────────────────────────────────────────┤
│ WHAT IT MEANS FOR INVESTORS                                 │
│ Summary recommendation with time horizon                    │
│ Clear stance on who should buy/hold/avoid                   │
├─────────────────────────────────────────────────────────────┤
│ FOOTER                                                      │
│ Disclosure, analyst info, date                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Components

### 1. Article Header
```
┌────────────────────────────────────────────────────────────┐
│ ACCENTURE (ACN)                                            │
│ A high-quality consulting stock trading at oversold levels │
└────────────────────────────────────────────────────────────┘
```
- Large company name with ticker
- One-line thesis statement below
- Clean, no decorative elements

### 2. Price Highlight Box
```
┌─────────────────────────────────┐
│ Today's Change                  │
│ ┌─────────────────────────────┐ │
│ │  🟢 +35.4%   │   $260.00   │ │
│ │   (+$67.92)  │   Target    │ │
│ └─────────────────────────────┘ │
│ Current: $192.08                │
│ Stop Loss: $165.00              │
└─────────────────────────────────┘
```
- Floats right or prominent placement
- Green for positive, red for negative
- Shows today's change and current price

### 3. Section Headers
```
## Bull case:

[Content here]

## Bear case:

[Content here]
```
- Large, bold headers
- Colon after header text
- Generous spacing above

### 4. Narrative Content
- 18px body text
- Line height 1.6
- Paragraphs separated by 24px
- Bullet points for key arguments
- Bold key terms within text

### 5. Key Metrics Bar
```
Revenue (TTM): $70.7B    |    P/E Ratio: 15.8    |    Div Yield: 3.3%    |    RSI: 21.6
```
- Horizontal bar with pipe separators
- 4-6 key metrics
- Clean, scannable

### 6. "What it means" Section
```
## What it means for investors

[Clear recommendation in plain English]

[Suitable for / Not suitable for breakdown]
```
- Final recommendation
- Time horizon guidance
- Investor suitability

---

## Content Style

### Writing Tone
- **Conversational but professional**: Like a smart friend explaining
- **Educational**: Explain why things matter
- **Balanced**: Present both sides fairly
- **Actionable**: Clear recommendation at the end

### Paragraph Structure
1. **Lead paragraph**: Hook the reader, set the stage
2. **Body paragraphs**: 3-5 sentences each, one idea per paragraph
3. **Transition sentences**: Connect ideas smoothly

### Use of Bold
- **Company names**: First mention
- **Key metrics**: Revenue, growth rates
- **Important concepts**: Competitive advantage, risks

---

## Responsive Design

### Desktop (>900px)
- Two-column layout possible
- Price box floats right
- Full-width content

### Tablet (600-900px)
- Single column
- Price box above content
- Maintains readability

### Mobile (<600px)
- Single column
- Larger touch targets
- Collapsed sections if needed

---

## Example Section

```html
<article>
  <header>
    <h1>Accenture (ACN)</h1>
    <p class="thesis">A world-class consulting firm trading at rare discount</p>
  </header>
  
  <aside class="price-box">
    <div class="change positive">+35.4% potential</div>
    <div class="current-price">$192.08</div>
    <div class="target">Target: $260</div>
  </aside>
  
  <section class="intro">
    <p>Accenture has been a massive winner over the last decade, 
    delivering consistent returns for long-term investors. But recent 
    concerns about AI disruption and slowing enterprise spending have 
    sent shares down 47% from their highs...</p>
  </section>
  
  <section class="bull-case">
    <h2>Bull case:</h2>
    <p>Accenture's competitive moat is deeper than investors realize. 
    The company doesn't just advise on technology—it implements it. 
    <strong>Here's why that matters:</strong></p>
    
    <ul>
      <li><strong>Recurring revenue</strong>: $70.7B annually with 
      90%+ client retention</li>
      <li><strong>AI tailwind, not threat</strong>: Companies need 
      consultants to implement AI, creating more demand</li>
      <li><strong>Valuation support</strong>: 3.3% dividend yield 
      provides floor while waiting for recovery</li>
    </ul>
  </section>
  
  <section class="bear-case">
    <h2>Bear case:</h2>
    <p>Despite the positives, investors must consider the downside risks:</p>
    
    <ul>
      <li><strong>Enterprise spending freeze</strong>: Companies are 
      cutting discretionary IT budgets</li>
      <li><strong>Multiple compression</strong>: P/E compressed from 
      25x to 16x as growth expectations reset</li>
    </ul>
  </section>
  
  <section class="key-metrics">
    <div class="metric-bar">
      <span>Revenue: $70.7B</span>
      <span>P/E: 15.8</span>
      <span>Yield: 3.3%</span>
      <span>RSI: 21.6</span>
    </div>
  </section>
  
  <section class="conclusion">
    <h2>What it means for investors</h2>
    <p>Accenture presents a compelling opportunity for patient investors 
    with a 3-5 year horizon. The stock is oversold, fundamentals remain 
    strong, and the dividend provides income while waiting.</p>
    
    <p><strong>Best for:</strong> Value investors, dividend seekers, 
    long-term holders</p>
    <p><strong>Avoid if:</strong> You need immediate returns or can't 
    stomach volatility</p>
  </section>
</article>
```

---

## CSS Notes

```css
/* Key styling principles */
body {
  font-family: 'Source Sans Pro', sans-serif;
  font-size: 18px;
  line-height: 1.6;
  color: #1E3A5F;
  max-width: 700px;
  margin: 0 auto;
  padding: 40px 20px;
}

h1 {
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 8px;
}

.thesis {
  font-size: 20px;
  color: #6B7280;
  font-style: italic;
  margin-bottom: 32px;
}

h2 {
  font-size: 24px;
  font-weight: 700;
  margin-top: 48px;
  margin-bottom: 24px;
}

.price-box {
  float: right;
  background: #F7F7F7;
  padding: 20px;
  margin: 0 0 20px 20px;
  border-radius: 8px;
}

.positive { color: #0D7A47; }
.negative { color: #C41E3A; }

.metric-bar {
  display: flex;
  justify-content: space-between;
  background: #F7F7F7;
  padding: 16px 24px;
  margin: 32px 0;
  border-radius: 8px;
}
```

---

## Key Differentiators from Traditional Research

| Traditional Research | Fool Format |
|---------------------|-------------|
| Dense tables | Narrative storytelling |
| Technical jargon | Plain English |
| Bullet-heavy | Paragraph-driven |
| Multiple pages | Single-scroll article |
| Institutional tone | Conversational |
| Complex models | Simple key metrics |
