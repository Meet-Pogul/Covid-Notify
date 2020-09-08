from plyer import notification
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


def remind(msg):
    """Notify the message"""
    notification.notify(
        title="COVID-19 Alert",
        message=msg,
        app_icon=r"D:\Meet\Python\firstprog\CovidNotify\covid.ico",
        timeout=6
    )


def int_put(s):
    try:
        ans = int(input(s))
    except ValueError:
        print("Wrong Input")
        ans = int_put(s)
    return ans


def get_Table(url, main_cond="", condition=""):
    """Get DataFrame Table from the link"""
    data = requests.get(url).text  # request url and convert into text
    if main_cond in data:  # check main condition that webpage has perticular word or not
        data = BeautifulSoup(data, 'html.parser')  # parse html into python form
        n = 0
        # a = []
        df = pd.DataFrame()
        First = True
        for i in data.find_all('table'):  # find all tables
            if condition in i.get_text():  # if it is a table which we want, any coloumn name
                for i in data.find_all('tr'):  # find row
                    now = i.get_text().split('\n')[1:]  # split by new line character
                    if First == True:  # first row iteration i.e.coloumn iteration
                        df = pd.DataFrame(columns=now[:len(now) - 1])  # create coloumn
                        First = False
                    else:
                        if 'Total#' in now:  # if it has total
                            k = [i for i in now if i != ""]  # remove "" from list
                            # a.append(['36'] + k)
                            df.drop(df.tail(1).index, inplace=True)  # drop previous row
                            df.loc[n - 1] = ['36'] + k  # insert new row
                            break  # break from the loop
                        # a.append(now[:len(now)-1])
                        df.loc[n] = now[:len(now) - 1]  # insert new row
                        n += 1
            else:
                print("Data Not Found")
                return pd.DataFrame(columns=[])
        # del a[len(a)-2]
        # for i in a:
        #     print(i)
        return df
    else:
        print("Data Not Found")
        return pd.DataFrame(columns=[])


def get_States(df):
    """Get list of states to notify"""
    states = df['Name of State / UT'].to_dict()
    print(states[0])
    for i in states:
        print(f"{i} : {states[i]}")
    state = []
    n = int_put("No. of States you want:")
    for i in range(n):
        sno = int_put("Enter states corresponding number: ")
        state.append(states[sno])
    return state


if __name__ == "__main__":
    df = get_Table("https://www.mohfw.gov.in/",
                   main_cond="COVID-19 Statewise", condition='Name of State')
    state = get_States(df)
    # state = ['Gujarat']
    info = df[df['Name of State / UT'].isin(state)]  # exract perticular state row from df
    info = info.set_index('S. No.').to_dict('list')  # convert into dictionary and setting index = 'S. No.'
    msg = ""
    for i in range(len(state)):
        for key in info:  # get keys from info one by one
            msg += f"{key} : {info[key][i]}\n"  # concat
        remind(msg)  # notify
        time.sleep(6)  # till it notifying
        msg = ""  # clear for next iteration
