import pandas as pd
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

train_id=input("Enter 5 Digit Train Number:")
if len(train_id)>5:
    print("Invalid train No.")
else:
    my_url='https://enquiry.indianrail.gov.in/xyzabc/ShowTrainSchedule?trainNo='+train_id+'&scrnSize=&langFile=props.en-us'

    uClient=uReq(my_url)
    page_html=uClient.read()
    uClient.close()
    page_soup=soup(page_html,"html.parser")
    if 'Invalid train No.' in page_soup.text :
        print('Invalid train No.')
    else:
        src_dstn=page_soup.findAll("span",{"class":"srcDstn"})
        src=src_dstn[0].text.strip()
        dstn=src_dstn[1].text.strip()
        print(src+' To '+dstn)

        train_type=page_soup.findAll("div",{"class":"w3-col s10 m4 l4"})
        print(train_type[0].text.strip())
        train_routine=page_soup.findAll("div",{"class":"w3-col s11 m7 l6"})
        print(train_routine[0].text.strip())

        tables = pd.read_html(my_url)
        df=pd.DataFrame(tables[4].values,columns=['S.N','Station Name','Day','Arr&Dep Time(hrs)','Distance(Km)'])
        print(df)

        map_url='https://enquiry.indianrail.gov.in/xyzabc/TrainScheduleOnMap?trainNo='+train_id+'&journeyStn=&scrnSize=&langFile=props.en-us'
        import webbrowser
        webbrowser.open(map_url)

        out = df.to_json(orient='records')[1:-1].replace('},{', '} {')
        with open('temp.json', 'w') as f:
            f.write(df.to_json(orient='records', lines=True))


