from newsplease import NewsPlease
article = NewsPlease.from_url('https://www.vox.com/2019/12/10/21004584/usmca-democrats-trump-nafta-trade-deal')
print(article.text)