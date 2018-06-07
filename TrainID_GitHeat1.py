import pandas as pd
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import webbrowser

def request_webpage():
    uClient=uReq(my_url)
    page_html=uClient.read()
    uClient.close()
    page_soup=soup(page_html,"html.parser")
    return page_soup

def find_source_destination_TrainType_TrainRoutine(page_soup):
    src_dstn=page_soup.findAll("span",{"class":"srcDstn"})
    src=src_dstn[0].text.strip()
    dstn=src_dstn[1].text.strip()
    print(src+' To '+dstn)

    train_type=page_soup.findAll("div",{"class":"w3-col s10 m4 l4"})
    print(train_type[0].text.strip())
    train_routine=page_soup.findAll("div",{"class":"w3-col s11 m7 l6"})
    print(train_routine[0].text.strip())
    
def writeToJSON(df):
    out = df.to_json(orient='records')[1:-1].replace('{"','{\n\t"').replace('},{', '}\n{').replace(',"',',\n\t"')
    with open('temp.json', 'w') as f:
        f.write(out)
        
def open_MapURL(train_id):
    map_url='https://enquiry.indianrail.gov.in/xyzabc/TrainScheduleOnMap?trainNo='+train_id+'&journeyStn=&scrnSize=&langFile=props.en-us'
    option=input("enter y to open map in browser,else enter n:")
    if option=='y':
        webbrowser.open(map_url)
    else:
        pass
    
train_id=input("Enter 5 Digit Train Number:")
if len(train_id)>5:
    print("Invalid train No.")
else:
    my_url='https://enquiry.indianrail.gov.in/xyzabc/ShowTrainSchedule?trainNo='+train_id+'&scrnSize=&langFile=props.en-us'
    page_soup=request_webpage()
    if 'Invalid train No.' in page_soup.text :
        print('Invalid train No.')
    else:
        find_source_destination_TrainType_TrainRoutine(page_soup)
        tables = pd.read_html(my_url)
        df=pd.DataFrame(tables[4].values,columns=['S.N','Station Name','Day','Arr&Dep Time(hrs)','Distance(Km)'])
        print(df)
        writeToJSON(df)
        open_MapURL(train_id)
        
