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
access = "ASc4pLpj5pNA2U06jaBDbIx7bpxqOx2UTioPowhG"          # 본인 값 으로 변경
secret = "xrwdu1ELJ0VxxL8GqwWKkqoNxUqQKdYhYxGh8BbD"          # 본인 값으 로 변경
# upbit = pyupbit.Upbit(access, secret)

# print(upbit.get_balance("KRW"))     # KRW- XRP 조회
# print(upbit.get_balance("KRW-SC"))     # KRW-XRP 조회
# print(upbit.get_balance("KRW-POWR"))     # KRW-XRP 조회
# print(upbit.get_balance("KRW-BTC"))     # 보유 현금 조회

# df = pyupbit.get_ohlcv("KRW-MED", count=5)
# df['ma'] = df['close'].rolling(window=5).mean()
# # df['rate'] = (df['range'] / df['close']) * 100
# print(df)
# now = datetime.datetime.now()
# print(now)     



url = "https://api.upbit.com/v1/ticker"

headers = {"Accept": "application/json"}

response = requests.request("GET", url, headers=headers)

print(response.text)



# df = pyupbit.get_ohlcv("KRW-MED", interval="day", count=1) # 9시 가져옴
# start_time = df.index[0]
# end_time = start_time + datetime.timedelta(days=1)
# print(end_time- datetime.timedelta(seconds=20))

# nohup python3 autotray.py > output.log & 
# git pull origin main
# 
