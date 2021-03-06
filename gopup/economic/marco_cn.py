#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/24 0024
# @Author  : justin.郑 3907721@qq.com
# @File    : marco_cn.py
# @Desc    : 中国宏观数据

import pandas as pd
import numpy as np
import re
import json
import requests
from gopup.economic import cons


def marco_cmlrd():
    """
    中国宏观杠杆率数据
    :return:
    """
    url = "http://114.115.232.154:8080/handler/download.ashx"
    excel_data = pd.read_excel(url, sheet_name="Data", header=0, skiprows=1)
    excel_data["Period"] = pd.to_datetime(excel_data["Period"]).dt.strftime("%Y-%m")
    excel_data.columns = [
        "年份",
        "居民部门",
        "非金融企业部门",
        "政府部门",
        "中央政府",
        "地方政府",
        "实体经济部门",
        "金融部门资产方",
        "金融部门负债方",
    ]
    return excel_data


def get_gdp_year():
    """
    获取年度国内生产总值数据
    --------
    DataFrame
    year :统计年度
    gdp :国内生产总值(亿元)
    pc_gdp :人均国内生产总值(元)
    gnp :国民生产总值(亿元)
    pi :第一产业(亿元)
    si :第二产业(亿元)
    industry :工业(亿元)
    cons_industry :建筑业(亿元)
    ti :第三产业(亿元)
    trans_industry :交通运输仓储邮电通信业(亿元)
    lbdy :批发零售贸易及餐饮业(亿元)
    """
    rdint = cons.random()
    r = requests.get(cons.MACRO_URL%(cons.P_TYPE['http'], cons.DOMAINS['sina'],
                                    rdint, cons.MACRO_TYPE[0], 0, 70,
                                    rdint))
    text = r.text
    # # # text = text.decode('gbk') if ct.PY3 else text
    regSym = re.compile(r'\,count:(.*?)\}')
    datastr = regSym.findall(text)
    datastr = datastr[0]
    datastr = datastr.split('data:')[1]
    datastr = datastr.replace('"', '').replace('null', '0')
    js = json.loads(datastr)
    df = pd.DataFrame(js, columns=cons.GDP_YEAR_COLS)
    df[df==0] = np.NaN
    return df


def get_gdp_quarter():
    """
    获取季度国内生产总值数据
    --------
    DataFrame
    quarter :季度
    gdp :国内生产总值(亿元)
    gdp_yoy :国内生产总值同比增长(%)
    pi :第一产业增加值(亿元)
    pi_yoy:第一产业增加值同比增长(%)
    si :第二产业增加值(亿元)
    si_yoy :第二产业增加值同比增长(%)
    ti :第三产业增加值(亿元)
    ti_yoy :第三产业增加值同比增长(%)
    """
    rdint = cons.random()
    r = requests.get(cons.MACRO_URL%(cons.P_TYPE['http'], cons.DOMAINS['sina'],
                                    rdint, cons.MACRO_TYPE[0], 1, 250,
                                    rdint))
    text = r.text
    # # # text = text.decode('gbk') if ct.PY3 else text
    regSym = re.compile(r'\,count:(.*?)\}')
    datastr = regSym.findall(text)
    datastr = datastr[0]
    datastr = datastr.split('data:')[1]
    datastr = datastr.replace('"', '').replace('null', '0')
    js = json.loads(datastr)
    df = pd.DataFrame(js, columns=cons.GDP_QUARTER_COLS)
    df['quarter'] = df['quarter'].astype(object)
    df[df==0] = np.NaN
    url = cons.MACRO_URL%(cons.P_TYPE['http'], cons.DOMAINS['sina'],
                                    rdint, cons.MACRO_TYPE[0], 1, 250,
                                    rdint)
    return df


def get_gdp_for():
    """
    获取三大需求对GDP贡献数据
    --------
    DataFrame
        year :统计年度
        end_for :最终消费支出贡献率(%)
        for_rate :最终消费支出拉动(百分点)
        asset_for :资本形成总额贡献率(%)
        asset_rate:资本形成总额拉动(百分点)
        goods_for :货物和服务净出口贡献率(%)
        goods_rate :货物和服务净出口拉动(百分点)
    """
    rdint = cons.random()
    r = requests.get(cons.MACRO_URL % (cons.P_TYPE['http'], cons.DOMAINS['sina'],
                                      rdint, cons.MACRO_TYPE[0], 4, 80, rdint))
    text = r.text
    # # # text = text.decode('gbk') if ct.PY3 else text
    regSym = re.compile(r'\,count:(.*?)\}')
    datastr = regSym.findall(text)
    datastr = datastr[0]
    datastr = datastr.split('data:')[1]
    datastr = datastr.replace('"', '').replace('null', '0')
    js = json.loads(datastr)
    df = pd.DataFrame(js, columns=cons.GDP_FOR_COLS)
    df[df == 0] = np.NaN
    return df


def get_gdp_pull():
    """
    获取三大产业对GDP拉动数据
    --------
    DataFrame
        year :统计年度
        gdp_yoy :国内生产总值同比增长(%)
        pi :第一产业拉动率(%)
        si :第二产业拉动率(%)
        industry:其中工业拉动(%)
        ti :第三产业拉动率(%)
    """
    rdint = cons.random()
    r = requests.get(cons.MACRO_URL % (cons.P_TYPE['http'], cons.DOMAINS['sina'],
                                      rdint, cons.MACRO_TYPE[0], 5, 60, rdint))
    text = r.text
    # # # text = text.decode('gbk') if ct.PY3 else text
    regSym = re.compile(r'\,count:(.*?)\}')
    datastr = regSym.findall(text)
    datastr = datastr[0]
    datastr = datastr.split('data:')[1]
    datastr = datastr.replace('"', '').replace('null', '0')
    js = json.loads(datastr)
    df = pd.DataFrame(js, columns=cons.GDP_PULL_COLS)
    df[df == 0] = np.NaN

    return df


def get_gdp_contrib():
    """
        获取三大产业贡献率数据
    --------
    DataFrame
        year :统计年度
        gdp_yoy :国内生产总值
        pi :第一产业献率(%)
        si :第二产业献率(%)
        industry:其中工业献率(%)
        ti :第三产业献率(%)
    """
    rdint = cons.random()
    r = requests.get(cons.MACRO_URL%(cons.P_TYPE['http'], cons.DOMAINS['sina'], rdint,
                                    cons.MACRO_TYPE[0], 6, 60, rdint))
    text = r.text
    # # text = text.decode('gbk') if ct.PY3 else text
    regSym = re.compile(r'\,count:(.*?)\}')
    datastr = regSym.findall(text)
    datastr = datastr[0]
    datastr = datastr.split('data:')[1]
    datastr = datastr.replace('"', '').replace('null', '0')
    js = json.loads(datastr)
    df = pd.DataFrame(js, columns=cons.GDP_CONTRIB_COLS)
    df[df==0] = np.NaN
    return df


def get_cpi():
    """
        获取居民消费价格指数数据
    --------
    DataFrame
        month :统计月份
        cpi :价格指数
    """
    rdint = cons.random()
    r = requests.get(cons.MACRO_URL%(cons.P_TYPE['http'], cons.DOMAINS['sina'],
                                    rdint, cons.MACRO_TYPE[1], 0, 600,
                                    rdint))
    text = r.text
    # # text = text.decode('gbk') if ct.PY3 else text
    regSym = re.compile(r'\,count:(.*?)\}')
    datastr = regSym.findall(text)
    datastr = datastr[0]
    datastr = datastr.split('data:')[1]
    js = json.loads(datastr)
    df = pd.DataFrame(js, columns=cons.CPI_COLS)
    df['cpi'] = df['cpi'].astype(float)
    return df


def get_ppi():
    """
        获取工业品出厂价格指数数据
    --------
    DataFrame
        month :统计月份
        ppiip :工业品出厂价格指数
        ppi :生产资料价格指数
        qm:采掘工业价格指数
        rmi:原材料工业价格指数
        pi:加工工业价格指数
        cg:生活资料价格指数
        food:食品类价格指数
        clothing:衣着类价格指数
        roeu:一般日用品价格指数
        dcg:耐用消费品价格指数
    """
    rdint = cons.random()
    r = requests.get(cons.MACRO_URL%(cons.P_TYPE['http'], cons.DOMAINS['sina'],
                                    rdint, cons.MACRO_TYPE[1], 3, 600,
                                    rdint))
    text = r.text
    # # text = text.decode('gbk') if ct.PY3 else text
    regSym = re.compile(r'\,count:(.*?)\}')
    datastr = regSym.findall(text)
    datastr = datastr[0]
    datastr = datastr.split('data:')[1]
    js = json.loads(datastr)
    df = pd.DataFrame(js, columns=cons.PPI_COLS)
    for i in df.columns:
        df[i] = df[i].apply(lambda x:np.where(x is None, np.NaN, x))
        if i != 'month':
            df[i] = df[i].astype(float)
    return df


def get_deposit_rate():
    """
        获取存款利率数据
    --------
    DataFrame
        date :变动日期
        deposit_type :存款种类
        rate:利率（%）
    """
    rdint = cons.random()
    r = requests.get(cons.MACRO_URL%(cons.P_TYPE['http'], cons.DOMAINS['sina'],
                                    rdint, cons.MACRO_TYPE[2], 2, 600,
                                    rdint))
    text = r.text
    # text = text.decode('gbk')
    regSym = re.compile(r'\,count:(.*?)\}')
    datastr = regSym.findall(text)
    datastr = datastr[0]
    datastr = datastr.split('data:')[1]
    js = json.loads(datastr)
    df = pd.DataFrame(js, columns=cons.DEPOSIT_COLS)
    for i in df.columns:
        df[i] = df[i].apply(lambda x:np.where(x is None, '--', x))
    return df


def get_loan_rate():
    """
        获取贷款利率数据
    --------
    DataFrame
        date :执行日期
        loan_type :存款种类
        rate:利率（%）
    """
    rdint = cons.random()
    r = requests.get(cons.MACRO_URL%(cons.P_TYPE['http'], cons.DOMAINS['sina'],
                                    rdint, cons.MACRO_TYPE[2], 3, 800,
                                    rdint))
    text = r.text
    # text = text.decode('gbk')
    regSym = re.compile(r'\,count:(.*?)\}')
    datastr = regSym.findall(text)
    datastr = datastr[0]
    datastr = datastr.split('data:')[1]
    js = json.loads(datastr)
    df = pd.DataFrame(js, columns=cons.LOAN_COLS)
    for i in df.columns:
        df[i] = df[i].apply(lambda x:np.where(x is None, '--', x))
    return df


def get_rrr():
    """
        获取存款准备金率数据
    --------
    DataFrame
        date :变动日期
        before :调整前存款准备金率(%)
        now:调整后存款准备金率(%)
        changed:调整幅度(%)
    """
    rdint = cons.random()
    r = requests.get(cons.MACRO_URL%(cons.P_TYPE['http'], cons.DOMAINS['sina'],
                                    rdint, cons.MACRO_TYPE[2], 4, 100,
                                    rdint))
    text = r.text
    # text = text.decode('gbk')
    regSym = re.compile(r'\,count:(.*?)\}')
    datastr = regSym.findall(text)
    datastr = datastr[0]
    datastr = datastr.split('data:')[1]
    js = json.loads(datastr)
    df = pd.DataFrame(js, columns=cons.RRR_COLS)
    for i in df.columns:
        df[i] = df[i].apply(lambda x:np.where(x is None, '--', x))
    return df


def get_money_supply():
    """
        获取货币供应量数据
    --------
    DataFrame
        month :统计时间
        m2 :货币和准货币（广义货币M2）(亿元)
        m2_yoy:货币和准货币（广义货币M2）同比增长(%)
        m1:货币(狭义货币M1)(亿元)
        m1_yoy:货币(狭义货币M1)同比增长(%)
        m0:流通中现金(M0)(亿元)
        m0_yoy:流通中现金(M0)同比增长(%)
        cd:活期存款(亿元)
        cd_yoy:活期存款同比增长(%)
        qm:准货币(亿元)
        qm_yoy:准货币同比增长(%)
        ftd:定期存款(亿元)
        ftd_yoy:定期存款同比增长(%)
        sd:储蓄存款(亿元)
        sd_yoy:储蓄存款同比增长(%)
        rests:其他存款(亿元)
        rests_yoy:其他存款同比增长(%)
    """
    rdint = cons.random()
    r = requests.get(cons.MACRO_URL%(cons.P_TYPE['http'], cons.DOMAINS['sina'],
                                    rdint, cons.MACRO_TYPE[2], 1, 600,
                                    rdint))
    text = r.text
    # text = text.decode('gbk')
    regSym = re.compile(r'\,count:(.*?)\}')
    datastr = regSym.findall(text)
    datastr = datastr[0]
    datastr = datastr.split('data:')[1]
    js = json.loads(datastr)
    df = pd.DataFrame(js, columns=cons.MONEY_SUPPLY_COLS)
    for i in df.columns:
        df[i] = df[i].apply(lambda x:np.where(x is None, '--', x))
    return df


def get_money_supply_bal():
    """
        获取货币供应量(年底余额)数据
    --------
    DataFrame
        year :统计年度
        m2 :货币和准货币(亿元)
        m1:货币(亿元)
        m0:流通中现金(亿元)
        cd:活期存款(亿元)
        qm:准货币(亿元)
        ftd:定期存款(亿元)
        sd:储蓄存款(亿元)
        rests:其他存款(亿元)
    """
    rdint = cons.random()
    r = requests.get(cons.MACRO_URL%(cons.P_TYPE['http'], cons.DOMAINS['sina'],
                                    rdint, cons.MACRO_TYPE[2], 0, 200,
                                    rdint))
    text = r.text
    # text = text.decode('gbk')
    regSym = re.compile(r'\,count:(.*?)\}')
    datastr = regSym.findall(text)
    datastr = datastr[0]
    datastr = datastr.split('data:')[1]
    js = json.loads(datastr)
    df = pd.DataFrame(js, columns=cons.MONEY_SUPPLY_BLA_COLS)
    for i in df.columns:
        df[i] = df[i].apply(lambda x:np.where(x is None, '--', x))
    return df


def get_gold_and_foreign_reserves():
    """
    获取外汇储备
    Returns
    -------
    DataFrame
        month :统计时间
        gold:黄金储备(万盎司)
        foreign_reserves:外汇储备(亿美元)
    """
    rdint = cons.random()
    r = requests.get(cons.MACRO_URL % (cons.P_TYPE['http'], cons.DOMAINS['sina'],
                                      rdint, cons.MACRO_TYPE[2], 5, 200,
                                      rdint))
    text = r.text
    # text = r.decode('gbk')
    regSym = re.compile(r'\,count:(.*?)\}')
    datastr = regSym.findall(text)
    datastr = datastr[0]
    datastr = datastr.split('data:')[1]
    js = json.loads(datastr)
    df = pd.DataFrame(js, columns=cons.GOLD_AND_FOREIGN_CURRENCY_RESERVES)
    for i in df.columns:
        df[i] = df[i].apply(lambda x: np.where(x is None, '--', x))
    return df


if __name__ == '__main__':
    tmp = get_gold_and_foreign_reserves()

    print(tmp)

