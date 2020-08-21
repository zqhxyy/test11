# __author__:zhuqi
import os,sys
pdir = os.path.dirname(os.getcwd())
sys.path.append(pdir)
import pandas as pd

def dconvert(x):
    '''处理有些数值字段里面包含的汉字，如：无数据'''
    if isinstance(x, (float,int)):
        return float(x)
    elif isinstance(x,str):
        if x.isdigit():
            return float(x)
        else:
            return 0.0
class LoadBase(object):
    def __init__(self):
        self.dirfile = '' # 机组数据文件的目录
        self.wtdlist = []
        self.colname = ['F_Number', 'Date_Time', 'Speed', 'RealPower']

    def getsinglewtdata(self):
        '''此方法需要子类根据具体的文件格式重写'''
        pass

    def multi_to_one(self):
        self.getsinglewtdata()
        fdf = None
        for d in self.wtdlist:
            if fdf is None:
                fdf = d[self.colname]
            else:
                df = d[self.colname]
                fdf = pd.merge(fdf, df, left_on='Date_Time', right_on='Date_Time')
        keys = fdf.columns
        tpower = None
        tspeed = None
        ispfirst = True
        issfirst = True
        for i in range(len(keys)):
            c = keys[i]
            if 'Power' in c:
                if ispfirst:
                    tpower = fdf.iloc[:, [i]][c].apply(dconvert)
                    ispfirst = False
                else:
                    tmp = fdf.iloc[:, [i]][c].apply(dconvert)
                    tpower += tmp
            if 'Speed' in c:
                if issfirst:
                    tspeed = fdf.iloc[:, [i]][c].apply(dconvert)
                    issfirst = False
                else:
                    tmp2 = fdf.iloc[:, [i]][c].apply(dconvert)
                    tspeed += tmp2
        tpower = tpower / 1000.0  # 转换为MW
        tspeed = tspeed / len(self.wtdlist)  # 平均风速

        qcdata = pd.DataFrame({"Date_Time": fdf['Date_Time'], "Speed": tspeed, "RealPower": tpower})

        return qcdata

    def writer(self,data,fpath):

        dir ,ext = os.path.splitext(fpath)
        if ext == '.csv':
            data.to_csv(fpath,encoding='gb2312',index=False)
        if ext == '.xls' or ext == 'xlsx':
            data.to_excel(fpath,index=False)


