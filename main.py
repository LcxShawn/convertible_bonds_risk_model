import pandas as pd
import numpy as np
from scipy import stats

def menu():
    print('''
        -----------可转债退市风险评估系统-----------
        | 1. 
        | 2. 交易类风险
        | 3. 财务风险
        | 4. 
        | 5. 
        | 
        -----------------------------------------
        
        ''')
    
    
def read_data():
    print('说明：数据文件应包含以下列：收盘价、总市值（亿元）')
    way=input('请输入数据读取文件地址：')
    df = pd.read_excel(way)
    df=df.dropna()
    return df

def trade_risk(df):
    #计算波动率
    def volatility(data):
        #计算对数收益率
        data['Log_Return'] = np.log(data['收盘价'] / data['收盘价'].shift(1))
        #计算波动率
        volatility = data['Log_Return'].std()*np.sqrt(252)
        return volatility
    #计算可转债退市概率,s为收盘价，mv为市值，vol为波动率，t为时间
    def cal_risk(s, mv, vol, t):
        p1 = stats.norm.cdf((np.log(1) - np.log(s)) / (vol * (t ** 0.5)))
        p2 = stats.norm.cdf((np.log(5) - np.log(mv)) / (vol * (t ** 0.5)))
        return p1,p2
    vol=volatility(df)
    s= df.loc[0,'收盘价']
    mv=df.loc[0,'总市值']
    t=min(float(input('请输入剩余时间（年）：')),2)
    risk=cal_risk(s, mv, vol, t)
    print('面值退市概率为：',risk[0]*100,'%')
    print('市值退市概率为：',risk[1]*100,'%')
    return risk


def main():
    print('start')
    flag=True
    while flag:
        menu()
        choice = input('请输入选项：')
        if choice == '1':
            pass
        elif choice == '2':
            df=read_data()
            trade_risk(df)
        elif choice == '3':
            pass
        elif choice == '4':
            pass
        elif choice == '5':
            pass
        else:
            flag=False
            print('退出系统')
            
if __name__ == '__main__':
    main()
    
    