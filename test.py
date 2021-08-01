import pyupbit
import datetime
import requests
import json 
import time
import pyupbit
import pandas as pd

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
def get_possible_coin_list() : 
    url = "https://api.upbit.com/v1/market/all"
    querystring = {"isDetails":"false"}
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    json_data = (json.loads(response.text))
    possible_coin_list = []
    
    for i in json_data:
        # print(i)
        # print(type(i)) #type dict 즉, dict의 모음을 list로 인식중
        # print(i['market']) # 이게 된다!!
        if(i['market'].startswith('KRW')):
            possible_coin_list.append(i['market'])

    # print(possible_coin_list)  
    return possible_coin_list
    
# ####업비트 내 특정 코인의 24시간 거래 대금 가져오기 
def get_acc_trade_price_24h(coin):
    # print("called : " + str(coin))
    
    # 요청 가능회수 확보를 위해 기다리는 시간(초)
    err_sleep_time = 0.3
    time.sleep(err_sleep_time)
    url = "https://api.upbit.com/v1/ticker"
    # querystring = {"markets":"KRW-DOGE"}
    querystring = {"markets": coin}   
    headers = {"Accept": "application/json"} 
    response = requests.request("GET", url, headers=headers, params=querystring)
    try:
        # json 변환 참고 https://www.python2.net/questions-479121.htm
        # 누적대금 가져오기 참고 https://docs.upbit.com/reference#ticker%ED%98%84%EC%9E%AC%EA%B0%80-%EB%82%B4%EC%97%AD
        #24시간 거래 누적대금 가져오기

        json_data = (json.loads(response.text))
        # print(type(json_data))
        if(json_data[0]['acc_trade_price_24h']>0):
            # print(json_data[0]['acc_trade_price_24h'])
            return json_data[0]['acc_trade_price_24h']

    except Exception as e:
        print(e)
        print(response) 
 
    
 
#거래대금 상위 10개 코인 리스트 가져오기
def df_sort_group_top10():
    possible_coin_list = get_possible_coin_list()
        # print(possible_coin_list)

    df = pd.DataFrame(columns = ['coin' , 'trade_price'])

    # for i in possible_coin_list:
    #     # print("call : " + str(i))
    #     result = get_acc_trade_price_24h(i)
    #     # print(result)
    #     df.loc[1]=[ 'Mango', 4, 'No' ]

    for i in range(0,len(possible_coin_list)):
        # print("call : " + str(i))
        result = get_acc_trade_price_24h(possible_coin_list[i])
        # print(result)
        
        df.loc[i]=[ possible_coin_list[i], result]

    # 거래대금 상위 10 코인리스트
    df_sort_group_top10 = df.sort_values(by="trade_price", ascending=False).head(10)
    return df_sort_group_top10


while True:  
    try:
        # 거래대금 상위 10 코인리스트(코인명,거래대금) 에서 코인명만 list에 넣기
        # df_sort_group_top10 = df_sort_group_top10()
        # symbol_list = df_sort_group_top10['coin']
        upbit = pyupbit.Upbit(access, secret)

        balances = upbit.get_balances()

        df = pd.DataFrame(columns = ['coin' , 'balance'])
        # print(balances)
        print(len(balances))
        for i in range(0,len(balances)) :
            df.iloc[i]=[ str(balances[i]['currency']), str(balances[i]['balance'])]
            print("i"+str(i))
            print("x"+str(balances[i]))
            print("y"+str(balances[i]['currency']))
            print("z"+str(balances[i]['balance']))
            print("xxx"+str(df))
            print("df"+str(df))
        # print(df)     

        time.sleep(1) 
    except Exception as e:
        print(e)
        time.sleep(1)

 
# print(json_val['acc_trade_price_24h'])
# df = pyupbit.get_ohlcv("KRW-MED", interval="day", count=1) # 9시 가져옴
# start_time = df.index[0]
# end_time = start_time + datetime.timedelta(days=1)
# print(end_time- datetime.timedelta(seconds=20))

# nohup python3 autotray.py > output.log & 
# git pull origin main
# 
