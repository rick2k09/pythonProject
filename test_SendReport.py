import win32com.client as win32
import time

outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
receivers = ['[rick_chang@perfectcorp.com]']
#timestr = time.strftime('%Y%m%d', time.localtime(time.time()))  # 本地日期作為報告名字
#filename = 'C:/Users/PERFECT/Documents/testreport/'  # 文件名字及保存路徑

def send(filename, timestr) :
    testreport = filename + timestr + '.html'
    print(testreport)
    mail.To = receivers[0]
    mail.Subject = 'test2'
    mail.Body = timestr + ' report'
    mail.Attachments.Add(testreport)
    mail.Send()
