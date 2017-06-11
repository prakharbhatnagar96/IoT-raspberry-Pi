import sys
import os
import traceback
from time import sleep
import RPi.GPIO as GPIO
from time import sleep  
import Adafruit_DHT
import urllib2
import Adafruit_BMP.BMP085 as BMP085
import tweepy
import time
import MySQLdb
import smtplib
from datetime import datetime
from gpiozero import LightSensor
gmail_user ="weatherchasers27@gmail.com"
gmail_pwd = "weathervaale"
def get_api(cfg):
    auth=tweepy.OAuthHandler(cfg['consumer_key'],cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'],cfg['access_token_secret'])
    return tweepy.API(auth)

def getSensorData():
    RH, T = Adafruit_DHT.read_retry(11, 4)
    sensor = BMP085.BMP085()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23,GPIO.IN)
    state=GPIO.input(23)
    P=sensor.read_pressure()
    A=(sensor.read_altitude()-200)
    SP=sensor.read_sealevel_pressure()
    ldr=LightSensor(5)
    L=ldr.value
    t=datetime.now()
    t=str(t)
    db=MySQLdb.connect("localhost","root","root","weather")
    #print db
    curs=db.cursor()
    #print curs.execute("select * from geuweather where temperature=%s",(89))
    try:
        if state==0:
            curs.execute ("INSERT INTO  geuweather values (%s,%s,%s,%s,%s,%s,%s,%s)",(T,RH,P,A,SP,1,L,t))
        else:
            curs.execute ("INSERT INTO  geuweather values (%s,%s,%s,%s,%s,%s,%s,%s)",(T,RH,P,A,SP,0,L,t))
        db.commit()
        print "Data committed"
    except Exception,e:
        print "Error: the database is being rolled back"
        traceback.print_exc()
        db.rollback()
    if state==0:
        return (str(T), str(RH),str(P),str(A),str(SP),1,str(L),t)
    else:
        return (str(T), str(RH),str(P),str(A),str(SP),0,str(L),t)
# main() function
def main():
    # use sys.argv if needed
    if len(sys.argv) < 2:
        print('Usage: python tstest.py PRIVATE_KEY')
        exit(0)
    print 'starting...'

    baseURL = 'https://api.thingspeak.com/update?api_key=%s' % sys.argv[1]
    cfg={
        "consumer_key"          :"uqbEoSssKdaX5O98b0zYvgAJx",
        "consumer_secret"       :"hmIejEgWIrwwLb3IIk24I4LSAu1tIRALSRPWgO8rx8VlhTZ7ZO",
        "access_token"          :"844416340760956928-KRgrEZ7T1J1lRWuwBunp7i3quG6Z9Sw",
        "access_token_secret"   :"MxI2HJH8J9ZUPAG7NHpPlkqQeexyZhjTup6uKIBAdbBX9"
        }
    api=get_api(cfg)
    while True:
        try:
            T,RH, P, A, SP, R, L,t= getSensorData()
            f = urllib2.urlopen(baseURL +
                                "&field1=%s&field2=%s&field3=%s&field4=%s&field5=%s&field6=%s&field7=%s" % (T, RH, P, A, SP, R, L))
            print f.read()
            f.close()
            if R==1:
                tweet="\nT:"+t+"\nTemp:"+T+" C\nHumi:"+RH+"%\nPres:"+P+"Pas\nAlt:"+A+"mtr\nSLP:"+SP+"Pas\nRain!!"+"\nL:"+L
            else:
                tweet="\nT:"+t+"\nTemp:"+T+"C\nHumi:"+RH+"\nPres:"+P+"Pas\nAlt:"+A+"mtr\nSLP:"+SP+"Pas\nNo Rain"+"\nL:"+L
            status=api.update_status(status=tweet)
            try:
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.ehlo()
                server.starttls()
                server.login(gmail_user, gmail_pwd)
                server.sendmail("weatherchasers27@gmail.com","weatherchasers27@gmail.com", tweet)
                server.close()
                print 'successfully sent the mail'
            except:
                print "failed to send mail"
            sleep(100)
        except Exception,e:
            print 'exiting.'
            traceback.print_exc()
            break      
# call main
if __name__ == '__main__':
    main()
