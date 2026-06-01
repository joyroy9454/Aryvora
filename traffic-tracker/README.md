# Aryvora Traffic Log

Track weekly traffic metrics for aryvora.tech. Fill in data from GoatCounter and Buttondown each week.

## Quick Start

### Add a week of data
```bash
cd traffic-tracker
python3 update_traffic_log.py
```

The script will prompt you for each metric. Press Enter to skip any field.

### View summary
```bash
python3 update_traffic_log.py --summary
```

### View top posts chart
```bash
python3 update_traffic_log.py --chart
```

## Weekly Workflow (Every Sunday, 5 minutes)

1. **GoatCounter** → https://joy-roy.goatcounter.com
   - Total page views, visitors
   - Top 3 pages by views

2. **Buttondown** → https://buttondown.email
   - Total subscribers
   - New subscribers this week

3. **Run the tracker:**
   ```bash
   python3 update_traffic_log.py
   ```

4. **Check trends:**
   ```bash
   python3 update_traffic_log.py --summary
   ```

## Data Sources

| Metric | Source | Where to Find |
|--------|--------|---------------|
| Page views | GoatCounter | Dashboard → Total |
| Unique visitors | GoatCounter | Dashboard → Visitors |
| Top posts | GoatCounter | Dashboard → Pages |
| Total subscribers | Buttondown | Dashboard → Audience |
| New subs this week | Buttondown | Dashboard → Activity |
| Deals clicks | GoatCounter | Goals |
| Prompt library | Buttondown | Tags → prompt-library |

## Google Sheets Alternative

If you prefer a spreadsheet:
1. Open Google Sheets
2. Import `traffic-log.csv`
3. Update weekly in the browser

## Auto-Tracking (Future)

To enable auto-fill from GoatCounter API:
```bash
export GOATCOUNTER_API_KEY="your-key-here"
python3 update_traffic_log.py --auto
```

Get your API key at: https://joy-roy.goatcounter.com/settings#api
