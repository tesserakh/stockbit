# Stockbit Newsletter

Fetches the latest newsletter from [Snips](https://snips.stockbit.com/) by Stockbit. Also can be used to look for articles related to some topics using a tag. Stockbit does not provide an option to be able to subscribe to the articles via RSS feed, must be via email. The main goal of this project is intended to send the latest news and market analysis results by Stockbit team to other social media channels, especially Telegram using its Bot API.

![stockbit snips](media/stockbit-snips.gif)

### Requirements

- Python 3
- Requests
- Beautiful Soup 4

### Usage

You can use a ticker or a keyword for tag and keep category as default (recent news).

**Tag usage**

- ticker: `ANTM` or `TLKM` in uppercase
- single word: `inflasi`, `kredit`, `konstruksi`
- multiple word: `batu bara`, `mobil listrik`, `rights issue`

Example:

Return recently published Snips' articles:

```
python3 snips.py
```

Save currently available newsletter with tag `konstruksi`

```
python3 snips.py -t konstruksi -s
```

Save currently available newsletter with tag `mobil listrik`

```
python3 snips.py -t 'mobil listrik' -s
```

For more details:

```
python3 snips.py -h
```

### Disclaimer

This work is not directly affiliated with Stockbit.

