import time
import pyupbit
import datetime
import requests
from logging import handlers
import logging


########################################################################
##준수 로직에서 key 데이터 등을 바꿨고 매도는 9시 2분에 일괄로 하도록 변경 
########################################################################
 
access = "ASc4pLpj5pNA2U06jaBDbIx7bpxqOx2UTioPowhG"          # 본인 값으로 변경
secret = "xrwdu1ELJ0VxxL8GqwWKkqoNxUqQKdYhYxGh8BbD"          # 본인 값으로 변경
# coin_ticker = "KRW-BTC" # 구매하고자 하는 코인 티커
coinList = ["KRW-BTC","KRW-ETH","KRW-XRP","KRW-ADA","KRW-EOS","KRW-DOGE"] # 로직 적용 대상 코인 리스트
complete_coin = "" # 구매 완료한 코인
buy_currency = "KRW" # 구매 통화(무조건 원화)
sell_ticker = "" # 판매 종목
bestK = 0.4 # 최적의 K값
isBuying = False # 매수 여부  상태
high = "" # 고가 
low = "" # 저가
open = "" # 시가
close = "" # 종가
startFlag = False
myToken = "xoxb-2169356768131-2345914455761-iFtc5xSZJGE2bOmaprx2R3AI" # slack Key
slack = "#stock" # slack명
buy_krw = "" # 매수 원화 합계 
sell_krw = "" # 매도 원화 합계
goal = "" # 목표가 출력

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

timedFileHandler = logging.handlers.TimedRotatingFileHandler(filename='/home/ubuntu/coinauto/log/autotray.log',when='midnight',interval=1,encoding='utf-8')
timedFileHandler.setFormatter(formatter)
timedFileHandler.suffix = "%Y%m%d"


def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )
    # print(response)

def get_target_price(ticker, k):
    #변동성 돌파 전략으로 매수 목표가 조회
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
   # 시작 시간 조회
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1) # 9시 가져옴
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    #잔고 조회
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else: 
                return 0
    return 0
  
def get_ma5(ticker):
    #"5일 이동 평균선 조회"
    df = pyupbit.get_ohlcv(ticker, interval="day", count=5)
    time.sleep(0.2)
    ma5 = df['close'].rolling(5).mean().iloc[-1]                               
    return ma5    

def get_current_price(ticker):
 #현재가 조회
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("Autotrade start..!!")

# ma5 = get_ma5(coin_ticker) # 5일 이동평균선

# 로그 생성
logger = logging.getLogger()

# 로그의 출력 기준 설정
logger.setLevel(logging.INFO)
logger.addHandler(timedFileHandler)


# 자동매매 시작
# 매수 조건 충족 시 한방에 모든 원화를 털어서 사기 때문에 한번 매수하면 이후 while문은 원화 잔고가 없어 그냥 루프만 돔
while True:
    try:
        now = datetime.datetime.now()
        now_date = now.strftime('%Y-%m-%d')
        start_time = get_start_time("KRW-BTC") + datetime.timedelta(minutes=2) #9:02 
        end_time = start_time + datetime.timedelta(days=1) 
        
        # 9:00 < 현재 < 8:59:50 사이에 타겟가를 충족 시 매수
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            if startFlag != True:
                announcement = now_date + " auto trade start!!.\n"
                logger.info(announcement)
                # post_message(myToken,slack,announcement)
                startFlag = True
                isBuying = False
                for coin_ticker in coinList:
                    (target_price, target_rate) = get_target_price(coin_ticker, bestK)
                    goal =  coin_ticker + " today's target price : " + str(target_price) + "\n required rate of increase : " + str(round(target_rate,2)) + "%\n"
                    logger.info(goal)
                    print(str(goal))
                    # post_message(myToken,slack,goal)
            if isBuying != True: # 매수 가능 시간대 중 아직 매수 안한 상태면
                for coin_ticker in coinList:
                    (target_price, target_rate) = get_target_price(coin_ticker, bestK)
                    ma5 = get_ma5(coin_ticker) # 5일 이동평균선 구하기
                    current_price = get_current_price(coin_ticker) # 현재가 구하기

                    print('목표가 :', coin_ticker, target_price)   
                    print('현재가 :', coin_ticker, current_price)
                    print('5일이동평균 :', coin_ticker, ma5)
                    
                    if target_price < current_price and ma5 < current_price: # 타겟가 도달하고 현재가가 5일 이동평균선 위일 경우
                        print(coin_ticker, '매수 시점 발견!!')
                        logger.info("find a target price!")
                        krw = get_balance(buy_currency)
                        if krw > 5000: # 최소 주문금액인 5000원 이상일 때 시장가 매수
                            upbit.buy_market_order(coin_ticker, krw*0.9995) #수수료 0.05% 포함
                            buy_krw = krw
                            print('매수 완료..')
                            # post_message(myToken,slack,"매수 완료")
                            logger.info("buy seccess")
                            complete_coin = coin_ticker # 구매된 코인 확정
                            sell_ticker = complete_coin.split('-')[1]
                            isBuying = True
                            break
                        #else: 
                            # print('매수할 원화가 부족합니다')
                    # else:
                    #     print(coin_ticker, "목표가에 도달하지 않았습니다.")        
            else: # 매수 가능 시간대 중 이미 매수한 상태면
                current_price = get_current_price(complete_coin) # 구매 완료된 코인의 현재가 구하기
                ##
                #
                # 여기에 고점 수익률 대비 현재 수익률과의 차이가 4% 넘는 시점에 매도
                #
                ##
                if current_price < target_price * 0.96:  # 매수가 기준 4% 이상 하락 시 전액 매도하는 로직 추가
                    s_balance = get_balance(sell_ticker)
                    if s_balance > 0.00008:
                        upbit.sell_market_order(complete_coin, s_balance*0.9995)
                        startFlag = False
                        print('현재가 : ', current_price)
                        print(sell_ticker, '매수가 4% 이상 하락해서 전액 매도 완료..')
                        # post_message(myToken,slack,"매수가 4% 이상 하락해서 전액 매도 완료..")
        else: # 마지막 10초 남기고 종가에 시장가 매도
            startFlag = False
            s_balance = get_balance(sell_ticker)
            if s_balance > 0.00008:
                current_price = get_current_price(complete_coin)
                upbit.sell_market_order(complete_coin,  s_balance*0.9995)
                sell_krw = get_balance(buy_currency) # 매도 후 원화 잔액
                print(sell_ticker, ' 매도 완료..')
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)