import pyupbit
import datetime
import requests
import json 

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


####업비트 내 거래가능 목록 가져오기
url = "https://api.upbit.com/v1/market/all"

querystring = {"isDetails":"false"}

headers = {"Accept": "application/json"}

response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text)
json_data = (json.loads(response.text))

# print(json_data) 

possible_coin_list = []
 
for i in json_data:
    # print(i)
    # print(type(i)) #type dict 즉, dict의 모음을 list로 인식중
    # print(i['market']) # 이게 된다!!
    possible_coin_list.append(i['market'])

print(possible_coin_list)  
 
# ####업비트 내 특정 코인의 24시간 거래대금 가져오기 
# url = "https://api.upbit.com/v1/ticker"

# querystring = {"markets":"KRW-BTC"}

# headers = {"Accept": "application/json"}

# response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text)
# # json 변환 참고 https://www.python2.net/questions-479121.htm
# # 누적대금 가져오기 참고 https://docs.upbit.com/reference#ticker%ED%98%84%EC%9E%AC%EA%B0%80-%EB%82%B4%EC%97%AD
# #24시간 거래 누적대금 가져오기
# json_data = (json.loads(response.text))
# print(type(json_data))
# print(json_data[0]['acc_trade_price_24h'])


# print(json_val['acc_trade_price_24h'])
# df = pyupbit.get_ohlcv("KRW-MED", interval="day", count=1) # 9시 가져옴
# start_time = df.index[0]
# end_time = start_time + datetime.timedelta(days=1)
# print(end_time- datetime.timedelta(seconds=20))

# nohup python3 autotray.py > output.log & 
# git pull origin main
# 
