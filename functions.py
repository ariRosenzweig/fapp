import eventlet
requests = eventlet.import_patched('requests')
import bs4, json, lxml
from bs4 import BeautifulSoup
from redis import Redis 
import en_core_web_sm
nlp = en_core_web_sm.load()

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

def get_entries(lst):
       entries=[lst[i]['Entries'] for i in range(len(lst))]
       return entries

def soup_it(item):
	soup=BeautifulSoup(item, 'lxml')
	return soup

def extract_json(i):  
         data=i.select('script')[-2].text.split('_STATE__ = ')[-1].replace('\n', '').strip().rstrip(';') 
         return json.loads(data)
def get_ents(text):
  tentities = dict([(str(x), x.label_) for x in nlp(text).ents if x.label_ == 'PERSON'])  
  return tentities
def process_json(i):
        href=i['personStore']['meta']['seoCanonicalUrl']
        names=i['personStore']['name']
        loc=i['personStore']['location'] #deathloc
        t=i['personStore']['obituaries'] 
        c=[i['obituaryText'] for i in t]   
        text=[BeautifulSoup(i, 'lxml').text.strip() for i in c]
        e={}
        for i in range(len(text)):     
            e['Text'+str(i)]=get_ents(text[i])        
        uv=[{'obituaryText':text[i], 'published_by':t[i]['gaSitename'], 'date_published':t[i]['dateCreated']} for i in range(len(t))]	
        #tu=i['personStore']['guestBook']['condolences']['edges']
        #condols =[{'Name':i['node']['name'], 'msg': i['node']['message'], 'city':i['node']['city'], 'state': i['node']['state'], 'date':i['node']['date']} for i in tu]   
        record={'Entries':uv, 'Name': names, 'Location':loc, 'Source':href, 'Condolences':[], 'Entities': e}
        return record

def get_key(i):
    r=Redis()
    key= "celery-task-meta-" + str(i)
    val=json.loads(r.get(key))
    return json.dumps(val, indent=1)
