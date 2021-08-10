#！/user/bin/env python3
# -*- coding:utf-8 -*-

'doc of a test module'

'''
引用
'''

import pandas as pd
from pandas import DataFrame
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
import numpy as np
import time
import datetime
import os
import matplotlib as mpl
import matplotlib.dates as mdates
import seaborn as sns
import unicodedata
import matplotlib.pyplot as plt
import chardet
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


__author__ = 'HeKazhou'

class helper(object):


    def get_data(path):
        f = open(path,'rb')  # 先用二进制打开
        data = f.read()  # 读取文件内容
        file_encoding = chardet.detect(data).get('encoding')  # 得到文件的编码格式
        with open(path,'r', encoding=file_encoding)as file:  # 使用得到的文件编码格式打开文件
            lines=file.readlines()
            for line in lines:
                print(line)


    def read_data(path):
        if path.endswith('.csv')|path.endswith('.txt')==True:
            data = pd.read_csv('%s'%path)
        if path.endswith('.xlsx')|path.endswith('.xls') == True:
            data = pd.read_excel('%s' % path)
        return data


    def updateFile(file,old_str,new_str):
        """
        替换文件中的字符串
        :param file:文件名
        :param old_str:旧字符串
        :param new_str:新字符串
        :return:
        """
        file_data = ""
        with open(file, "r", encoding="utf-8") as f:
            content=f.read()
            t=content.replace(old_str,new_str)
        with open(file,"w+",encoding="utf-8") as f:
            f.write(t)



# 离散性类型变量数量统计
    def get_count(dataline, name):
        '''输入离散型变量,统计该离散型变量的不同类别的数据,并绘制条形图
            @dataline:离散型变量列
            @name：图像的名称，字符串
            @r:旋转角度
            @file_dir: 图像保存路径
            result:返回该离散型变量不同类别的数量,DataFrame表格
            '''

        r_zj = pd.DataFrame(dataline.value_counts().sort_index())
        r_zj.columns = ['频数']
        r_zj.sort_values(by='频数', ascending=False, inplace=True)
        r_zj['频率'] = r_zj / r_zj['频数'].sum()  # 计算频率
        r_zj['累计频率'] = r_zj['频率'].cumsum()  # 计算累计频率
        r_zj['频率%'] = r_zj['频率'].map(lambda x: "%.2f%%" % (x * 100))  # 以百分比显示频率
        r_zj['累计频率%'] = r_zj['累计频率'].map(lambda x: "%.2f%%" % (x * 100))  # 以百分比显示累计频率


        # 绘制频率分布直方图
        #     from pylab import *
        #     mpl.rcParams['font.sans-serif']=['SimHei']
        #     plt.rcParams['font.family'] = 'KaiTi'
        #     plt.rcParams['axes.unicode_minus'] = False

        r_zj['频率'].plot(kind='bar',
                        width=0.8,
                        figsize=(20, 10),
                        rot=90,
                        color='k',
                        grid=True,
                        fontsize=20,
                        alpha=0.5)

        if r_zj.shape[0] <= 10:
            r = 0
            plt.xticks(rotation=r)
        else:
            r = 90
            plt.xticks(rotation=90)
        plt.title('%s' % name, fontsize=20)
        # 绘制直方图

        x = len(r_zj)
        y = r_zj['频率']
        m = r_zj['频数']
        for i, j, k in zip(range(x), y, m):
            plt.text(i - 0.1, j + 0.001, '%i' % k, color='k', fontsize=20, rotation=r)
        name = '病人信息表' + name
        plt.savefig('./'+f'{name}.png')
        plt.show()
        return r_zj


# 缺失值函数
    def merge_save_count(data):
        '''输入存储的表格，获得该表格记录总数,非空值数量，非空比例，空值数量，空值比例
            @data:输入原始表格
            result：DataFrame格式的表格'''

        info = data.count(axis=0)
        info_lack = data.shape[0] - info
        total = info_lack + info
        # dup=data[data.duplicated()].count()
        info_rate = (info / total).apply(lambda x: format(x, '.2%'))
        lack_rate = (info_lack / total).apply(lambda x: format(x, '.2%'))
        # dup_rate=(dup/total).apply(lambda x: format(x,'.2%'))
        data_info = pd.DataFrame([total, info, info_rate, info_lack, lack_rate])
        data_info.index = ['总数', '非空值数量', '非空比例', '空值数量', '空值比例']
        data_info = pd.DataFrame(data_info.values.T, index=data_info.columns, columns=data_info.index)
        return data_info


#总数
    def count_sum(data,name):
        d = data.drop(columns=name).duplicated().sum()
        d_ratio = d / data.shape[0]
        dd = DataFrame([[data.shape[0], d, d_ratio]], columns=['总数', '重复数量', '重复比例'], index=[''])
        dd['重复比例'] = dd['重复比例'].map(lambda x: "%.2f%%" % (x * 100))
        print(dd)
        return dd



#唯一性函数，id值唯一
    def get_Unique(data,line):
        '''输入表格，和标识唯一的id,获得重复几次的数量以及频率的表格a
            @data:表格数据
            @line:站点名称与Date的列表
            result：DataFrame格式的表格'''
        get_Unique_df = data.groupby(line)[line[0]].value_counts().value_counts()
        r_zj = pd.DataFrame(get_Unique_df)
        r_zj.columns = ['频数']
        r_zj['频率'] = r_zj / r_zj['频数'].sum()  # 计算频率
        r_zj['累计频率'] = r_zj['频率'].cumsum()  # 计算累计频率
        r_zj['频率%'] = r_zj['频率'].map(lambda x: "%.2f%%" % (x*100))  # 以百分比显示频率
        r_zj['累计频率%'] = r_zj['累计频率'].map(lambda x: "%.2f%%" % (x*100))  # 以百分比显示累计频率
        return r_zj

    def get_time(data,name):
        data1=data.copy()
        data1[name] = pd.to_datetime(data1[name])
        first_time=str(data1.loc[0,name])[0:10]
        last_time=str(data1.loc[data1.shape[0]-1,name])[0:10]
        return first_time,last_time

    def changetoyear(data,name):

        return data

    # 将数字全转为int类型, 不为数值的置空
    def is_int(x):
        try:
            float(x)
        except ValueError:
            return False
        else:
            if '.' in x:
                if int(x.split('.')[-1]) == 0:
                    return True
                else:
                    return False
            else:
                return True

    def count_plot_year(data,name):
        '''分离时间型变量列
            @data:表格数据
            result:返回该时间型变量不同类别的数量,DataFrame表格
            '''
        data1=data.copy()
        data1[name]=pd.to_datetime(data1[name])
        data1['year']=data1[name].apply(lambda x:x.year)
        get_count_=helper.get_count(data1['year'],'时间分布图')
        return get_count_

    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        return False

    def to_num(x):
        if helper.is_number(x):
            return float(x)
        else:
            return x

    def drop_unusual_char(data, columns):
        # 将非正常字符以及小于0的数据置空
        df = data.copy()
        for feature in columns:
            df[feature] = df[feature].apply(lambda x: np.nan if not helper.is_number(x) else x)
            df[feature] = df[feature].apply(lambda x: np.nan if x < 0 else x)
        return df

    '''
    数字变量的分布
    '''
    def data_distribution(data):
        list=[]
        name=[]
        count=0

        for c in range(len(data.columns)):
            if is_numeric_dtype(data.iloc[:, c]):
                name.append(data.columns[c])
                count+=1
        # 将数据转为float类型
        for i in range(count):
            list.append([])
        for c in range(len(name)):
            if sum(data[name[c]].notnull()) == 0:
                continue

        #     temp = data.loc[:,name[c]].copy()
        #     temp[temp.isnull()] = '缺失'
        #     temp = temp.value_counts()
        #     temp=pd.DataFrame(temp)
        #     df_value_counts = temp.reset_index()
        #     df_value_counts.columns = [name[c],'频数']
        #    # for j in range(len(df_value_counts.columns)):
        #      #   list[c].append(df_value_counts.iloc[:,j])
        #     continue
        # print(name,list)
        # return name,list
            r_zj = pd.DataFrame(data.value_counts().sort_index())
            r_zj.columns = ['频数']
            r_zj.sort_values(by='频数', ascending=False, inplace=True)
            r_zj['频率'] = r_zj / r_zj['频数'].sum()  # 计算频率
            r_zj['累计频率'] = r_zj['频率'].cumsum()  # 计算累计频率
            r_zj['频率%'] = r_zj['频率'].map(lambda x: "%.2f%%" % (x * 100))  # 以百分比显示频率
            r_zj['累计频率%'] = r_zj['累计频率'].map(lambda x: "%.2f%%" % (x * 100))  # 以百分比显示累计频率
            # 绘制频率分布直方图
            #     from pylab import *
            #     mpl.rcParams['font.sans-serif']=['SimHei']
            #     plt.rcParams['font.family'] = 'KaiTi'
            #     plt.rcParams['axes.unicode_minus'] = False

            r_zj['频率'].plot(kind='bar',
                            width=0.8,
                            figsize=(20, 10),
                            rot=90,
                            color='k',
                            grid=True,
                            fontsize=20,
                            alpha=0.5)

            if r_zj.shape[0] <= 10:
                r = 0
                plt.xticks(rotation=r)
            else:
                r = 90
                plt.xticks(rotation=90)
            plt.title('%s' % name, fontsize=20)
            # 绘制直方图

            x = len(r_zj)
            y = r_zj['频率']
            m = r_zj['频数']
            for i, j, k in zip(range(x), y, m):
                plt.text(i - 0.1, j + 0.001, '%i' % k, color='k', fontsize=20, rotation=r)
            name = '病人信息表' + name
            plt.savefig('./'+f'{name}.png')
            plt.show()
            return r_zj


    def statistic_analysis(data):
        mode = data.mode().loc[0].values
        min_ = data.min()
        q25 = data.quantile(0.25)
        median = data.median()
        q75 = data.quantile(0.75)
        max_ = data.max()
        mean = data.mean()
        std = data.std()
        skew = data.skew()
        df = DataFrame([mode,min_,q25,median,q75,max_,mean,std,skew],
                       index=['众数','最小值','25%分位数','中位数','75%分位数','最大值','均值','标准差','偏度'],columns=data.columns)
        df=df.T
    #     df = DataFrame(df.values.T,columns=['众数','最小值','25%分位数','中位数','75%分位数','最大值','均值','标准差','偏度'],index=[key_])
        return df

#if __name__ == '__main__':
        #updateFile('./op_visiting.csv', '\t', '')
        #data=read_table(r'./op.csv')
        #data=read_data(r'./op.xlsx')

        #data.to_csv(r'./op_visiting1.csv')
        #print(a,b)
        #data.info()