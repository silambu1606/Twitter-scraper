import streamlit as st
st.title('Twitter scraper')

from datetime import date
import pandas as pd
import pymongo
import snscrape.modules.twitter as sntwitter
Hashtag=st.sidebar.text_input('Enter the hashtag or keyword of tweets:')
No_of_tweets=st.sidebar.number_input('Number of twees needed:',min_value=1,max_value=500,step=1)
st.sidebar.write(':green[Select the date range]')
start_date=st.sidebar.date_input('Start Date (YYYY-MM-DD):')
end_date=st.sidebar.date_input('End Date(YYYY-MM-DD):')
scraped_date=str(date.today())
Total_tweets=[]
if Hashtag:
    for a,tweet in enumerate(sntwitter.TwitterSearchScraper(f"{Hashtag} since:{start_date} until:{end_date}").get_items()):
      if a>=No_of_tweets:
                                                            
        break
    
      Total_tweets.append([tweet.id,tweet.user.username,tweet.lang,tweet.date,tweet.url,tweet.replyCount,tweet.likeCount,tweet.rawContent])
def data_frame(t_data):
    return pd.DataFrame(t_data,columns=['User_id','User_name','language','datetime','Url','replyCount','likeCount','rawContent'])
def convert_to_json(t_j):
    return t_j.to_json(orient='index')
def convert_to_csv(t_c):
    return t_c.to_csv().encode('utf-8')
df = data_frame(Total_tweets)
csv = convert_to_csv(df)
json = convert_to_json(df)
client=pymongo.MongoClient('mongodb://localhost:27017/')
db=client.twitterScraping
col=db.scraped_tweets
scr_data={"Scraped_word" : Hashtag,
            "Scraped_date" : scraped_date,
            "Scraped_tweets" : df.to_dict('records')
           }
if df.empty:
    st.subheader(":point_left:.Scraped tweets will vissible after entering hashtag or keywords")
else:
    st.success(f"**:green[{Hashtag}tweets]:thumbsup:**")
    st.write(df)
    st.write("**:green[choose any option from below]**")
    b2,b3,b4=st.columns([43,40,30])
    if b2.button("Upload to mongoDB"):
        try:
            col.delete_many({})
            col.insert_One(scr_data)
            b2.success('Upload to mongoDB successfully:thumbsup:')
        
    
        except:
            b2.error('please try again after submitting the hashtag or keyword')
    if b3.download_button(label="Download CSV",data=csv,
                          file_name=f'{Hashtag}_tweets.csv',
                          mime='text/csv'):
        b3.success('CSV Download successfully:thumbsup:')
    if b4.download_button(label="Download JSON",
                         data=json,
                         file_name=f'{Hashtag}_tweets.json',
                         mime='text/csv'):
       b4.success('Json Download successfully:thumbsup:')
             