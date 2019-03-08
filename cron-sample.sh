# parameters:
# 1- twitter account to clone
# 2- Diaspora login
# 3- Diaspora password
# 4- pod domain (you need to add https:// )

# fire every hour
0 * * * * cd /path/to/twitter2diaspora/; ./twitter2diaspora.py s04 s04bot **password** https://diasp.eu
