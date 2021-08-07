import pyupbit
import datetime
import requests
import json 
import time
import pandas as pd


access = "ASc4pLpj5pNA2U06jaBDbIx7bpxqOx2UTioPowhG"          #  본인  값으로 변경
secret = "xrwdu1ELJ0VxxL8GqwWKkqoNxUqQKdYhYxGh8BbD"          # 본인 값으로 변경
coin_ticker = "KRW-BTC" #   구매하고자 하는 코인 티커
buy_currency = "KRW" # 구매 통화(무조건 원화)
bought_list = [] #매수된종목
sell_ticker = "BTC" # 판매 종목
bestK = 0.5 # 최적의 K값
isBuying = False # 매수 여부 상태
high = "" # 고가 
low = "" # 저가
open = "" # 시가
close = "" # 종가
startFlag = False  
myToken = "xoxb-2169356768131-2166089342501-hLWTBMNoT3jLYtPv5NQTehaJ" # slack Key
buy_krw = "" # 매수 원화 합계 
sell_krw = "" # 매도 원화 합계
symbol_list = []#위 상위 10개를 담는 리스트
first_running_YN = "Y"
#
 
   

def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )
    print(response)
 


def get_target_price(ticker, k):
    #"""변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2) #어제오늘 ohlcv 가져옴
    # df.iloc[0]['close'] = 어제 종가 or 오늘 시가로 해도 될듯
    # df.iloc[0]['high'] = 어제 고가
    # df.iloc[0]['low'] = 어제 저가
    high = df.iloc[0]['high']
    low = df.iloc[0]['low']
    close = df.iloc[0]['close']
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    target_rate = (((df.iloc[0]['high'] - df.iloc[0]['low']) * bestK) / df.iloc[0]['close']) * 100
    return (target_price, target_rate)

def get_start_time(ticker):
   # """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1) # 9시 가져옴
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    #"""잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_balance_all():
    balances = upbit.get_balances()
    df = pd.DataFrame(columns = ['coin' , 'balance'])
    for i in range(0,len(balances)) :
        df.loc[i]=[ str(balances[i]['currency']), str(balances[i]['balance'])]
            # print("i"+str(i))
            # print("x"+str(balances[i]))
            # print("y"+str(balances[i]['currency']))
            # print("z"+str(balances[i]['balance']))
            # print("xxx"+str(df))
            # print("df"+str(df))
    # print("Balance : ")
    # print(df)
    return df   


def get_ma5(ticker):
    "5일 이동 평균선 조회"
    df = pyupbit.get_ohlcv(ticker, interval="day", count=5)
    ma5 = df['close'].rolling(5).mean().iloc[-1]
    return ma5    

def get_current_price(ticker):
 #   """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]




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
    return  df_sort_group_top10

def buy_coin(coin_ticker):
    """인자로 받은 종목을 최유리 지정가 FOK 조건으로 매수한다."""
    try:
        global bought_list      # 함수 내에서 값 변경을 하기 위해 global로 지정
        if coin_ticker in bought_list: # 매수 완료 종목이면 더 이상 안 사도록 함수 종료
            #printlog('code:', code, 'in', bought_list)
            return False

        #필요한 데이터 구하기    
        ma5 = get_ma5(coin_ticker) # 5일 이동평균선 구하기
        current_price = get_current_price(coin_ticker) # 현재가 구하기
        (target_price, target_rate) = get_target_price(coin_ticker, bestK) #목표가 구하기

        #루핑도는 Top10코인에 대한 로그 남기기
        #print('[Target coin] :',coin_ticker,'[Target price] :', target_price, '[Now price] : ',current_price,'[5days average] :',ma5 )
        
        if target_price < current_price and ma5 < current_price: # 타겟가 도달하고 현재가가 5일 이동평균선 위일 경우

            print('Got target point!!')
            print('[Target coin] :',coin_ticker,'[Target price] :', target_price, '[Now price] : ',current_price,'[5days average] :',ma5 )
    
            krw = get_balance(buy_currency) #잔고조회
            if krw > 5000 and buy_amount > 5000: # 최소 주문금액인 5000원 이상일 때 시장가 매수(계좌 잔고와, 설정된 코인 별 타겟 매수가가 5000원 이상일 때 )
                # print(upbit.buy_limit_order("KRW-XRP", 500, 20)) #500원에 리플20개 매수
                # upbit.buy_market_order(coin_ticker, krw*0.9995) #수수료 0.05% 포함
                upbit.buy_market_order(coin_ticker, buy_amount) 
                buy_krw = krw 
                print(str(coin_ticker) + 'is bought!')
                post_message(myToken,"#coin-trading","매수 완료")

                #구매한 코인 구매된 목록에 추가
                bought_list.append(coin_ticker)

                #현 잔고조회
                # get_balance_all()           

    except Exception as ex:
        print("`buy_coin("+ str(coin_ticker) + ") -> exception! " + str(ex) + "`")

def sell_all():
    """보유한 모든 종목을 매도한다."""
    try:

        df_get_balance_all = get_balance_all()
        list_get_balance_all = df_get_balance_all['coin']

        for i in range(0,len(list_get_balance_all)):
            if(str(list_get_balance_all[i])!='KRW'):
                sell_coin = list_get_balance_all[i]
                sell_amount = df_get_balance_all.loc[i]['balance']

                sell_coin_and_currency = "KRW-"+str(sell_coin)
                print("Trying to Sell [",sell_coin_and_currency,"] Coin [",sell_amount,"] Amount" ) 

                # current_price = get_current_price(df_get_balance_all['coin'])
                # upbit.sell_market_order(df_get_balance_all['coin'],  s_balance*0.9995) 
                # print(upbit.sell_market_order("KRW-XRP", 30))  #리플 30개 시장가매도
                upbit.sell_market_order(sell_coin_and_currency, sell_amount)  #보유수량 시장가매도
                sell_krw = get_balance(buy_currency) # 매도 후 원화 잔액
                print(sell_coin, ' Sell Comlete..')
                time.sleep(10)
    except Exception as ex:
        print("sell_all() -> exception! " + str(ex))

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("Autotrade start..!!")

ma5 = get_ma5(coin_ticker) # 5일 이동평균선

# 자동매매 시작
# 매수 조건 충족 시 한방에 모든 원화를 털어서 사기 때문에 한번 매수하면 이후 while문은 원화 잔고가 없어 그냥 루프만 돔
while True:
    try:
        df_get_balance_all = get_balance_all() #잔고확인
        bought_list = df_get_balance_all['coin']# 매수 완료된 종목 리스트

        if(first_running_YN=="Y"):
            target_buy_count = 5 # 매수할 종목 수
            buy_percent = 0.2 #증거금 대비 매수비율
            total_cash = int(get_balance(buy_currency))   # 100% 증거금 주문 가능 금액 조회
            buy_amount = total_cash * buy_percent  # 종목별 주문 금액 계산
            print('[setting]Balance status :', str(df_get_balance_all)) # 보유종목정보
            print('[setting]Buy Targets :', target_buy_count) # 매수할 종목 수
            print('[setting]100% cash amount :', total_cash) #100% 증거금 주문 가능 금액
            print('[setting]Buy percent per target :', buy_percent) #종목별 주문 비율
            print('[setting]Buy amont per target :', buy_amount) #종목별 주문 금액
            first_running_YN = "N"

        now = datetime.datetime.now()
        now_date = now.strftime('%Y-%m-%d')
        start_time = get_start_time(coin_ticker) #9:00 장 시작시간
        exit_time = start_time + datetime.timedelta(days=1) #9:00 + 1일 장 마감시간
        sell_time = exit_time - datetime.timedelta(seconds=10) #장마감 10초전
        
        # 9:00 < 현재 < 8:59:50 사이에 타겟가를 충족 시 매수
        if start_time < now < sell_time :
            symbol_list = []
            
            if len(symbol_list) < 10:
                time.sleep(1)
                # 거래대금 상위 10 코인리스트(코인명,거래대금) 에서 코인명만 list에 넣기
                df_sort_group_top10 = df_sort_group_top10()
                print("df_sort_group_top10 "+str(df_sort_group_top10))
                symbol_list = df_sort_group_top10['coin'] #매수할 종목 리스트
                print("Got Top10 Coin! here is Symbolist")
                print(symbol_list)
                print("a")
            for sym in symbol_list:
                # print("symbol "+ str(sym))
                print("b")
                print("sym" +str(sym))
                print("bought_list" +str(len(bought_list)))
                print("target_buy_count" +str(target_buy_count))
                
                #if len(bought_list) < target_buy_count: 
                #    print("c")
                buy_coin(sym)
                #    print("d")
                #    time.sleep(5)
        if sell_time < now < exit_time:
            if len(bought_list) > 0:
                print("sell all")
                sell_all()
                time.sleep(10)
                df_sort_group_top10 = df_sort_group_top10.drop(df_sort_group_top10.index[range(10)])


    except Exception as e:
        print(e)
        time.sleep(10)

 
# print(json_val['acc_trade_price_24h'])
# df = pyupbit.get_ohlcv("KRW-MED", interval="day", count=1) # 9시 가져옴
# start_time = df.index[0]
# end_time = start_time + datetime.timedelta(days=1)
# print(end_time- datetime.timedelta(seconds=20))

# nohup python3 autotray.py > output.log & 
# git pull origin main
# 
