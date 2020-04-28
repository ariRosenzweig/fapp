import requests


def get_api(first, last, state=0): 
                ur = f"https://www.legacy.com/obituaries/legacy/api/obituarysearch?&affiliateid=0&countryid=1&daterange=99999&lastname={last}&keyword={first}&stateid={state}&townname=&entriesperpage=15"   
                c  = requests.get(ur).json()['NumPageRemaining'] + 1     
                b = [f"{ur +'&page='}{n}" for n in range(1, c+1)]   
                return b 
def get_links(q):
       url="https://www.legacy.com/obituaries/name/"
       j=[]
       [j.append(b) for i in q for b in i] 
       mainurls=[f"{url}{j[i]['name'].replace('.', '').replace(' ', '-') + '-obituary?pid=' }{j[i]['id']}" for i in range(len(j))]
       main=[i.replace('"', '',) for i in mainurls]
       return main

def get_entries(list):
       entries=[list[i]['Entries'] for i in range(len(list))]
       return entries