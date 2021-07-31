import pyupbit
import datetime
import requests

# def post_message(token, channel, text):
#     response = requests.post("https://slack.com/api/chat.postMessage",
#         headers={"Authorization": "Bearer "+token},
#         data={"channel ": channel,"text": text}
#     )
#     print(response)
 
# myToken = "xoxb-2184276957348-2163375553719-grkPKNlTIGvN6E8evUyOBfNl"
# ##
# post_message(myToken,"#stock","jocoding")


#test2  
access = "2yMdlMtyu9SM1LX5yZCw0pbMymHftbDxcybWI3pY"          # 본인 값 으로 변경
secret = "gbuvuGctSV37k0XEscWHJ7TkkbpgZcacM8LIcwsa"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

print(upbit.get_balance("KRW"))     # KRW- XRP 조회
print(upbit.get_balance("KRW-ETC"))     # KRW-XRP 조회
print(upbit.get_balance("KRW-EOS"))     # KRW-XRP 조회
print(upbit.get_balance("KRW-BCH"))     # 보유 현금 조회


df = pyupbit.get_ohlcv("KRW-MED", count=5)
df['ma'] = df['close'].rolling(window=5).mean()
df['rate'] = (df['range'] / df['close']) * 100
print(df)
now = datetime.datetime.now()
print(now)

# df = pyupbit.get_ohlcv("KRW-MED", interval="day", count=1) # 9시 가져옴
# start_time = df.index[0]
# end_time = start_time + datetime.timedelta(days=1)
# print(end_time- datetime.timedelta(seconds=20))

# nohup python3 bitcoinautotray.py > output.log &
# git pull origin master
