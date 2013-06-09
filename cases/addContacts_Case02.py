# Case02 - Compare Contact Detail #
#     preconditions:  snapshot of ready contacts #

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage
import datetime

dic = {
       'Detail00':{
                   'PhoneNum'    :'1234000',
                   'Email'       :'1234@000.com',
                   'Address'     :'Chengdu,China'
                   },
       'Detail01':{
                   'PhoneNum'    :'1234001',
                   'Email'       :'1234@001.com',
                   'Address'     :'Chengdu,China'
                   },
       'Detail02':{
                   'PhoneNum'    :'1234002',
                   'Email'       :'1234@002.com',
                   'Address'     :'Chengdu,China'
                   }
       }

# connecting device #
try:
    print str(datetime.datetime.now())+"  "+"connecting device"
    device = MonkeyRunner.waitForConnection(10.0)
    print str(datetime.datetime.now())+"  "+"connecting success"
except:
    print str(datetime.datetime.now())+"  "+"connecting fail, please check and run script again"
    pass


# start People activity #
device.wake()
MonkeyRunner.sleep(1)
device.press('KEYCODE_HOME','DOWN_AND_UP')
MonkeyRunner.sleep(2)
device.startActivity(component = 'com.android.contacts/.activities.PeopleActivity')
MonkeyRunner.sleep(5)


# add contact #
CaseResultCount = 0
for name in dic:
    try:
        # add contact stpes #
        print str(datetime.datetime.now())+"  "+"add contact "+name+" start"
        device.touch(430,760,'DOWN_AND_UP')
        MonkeyRunner.sleep(3)
        device.type(name)
        device.touch(50,410,'DOWN_AND_UP')
        device.type(dic[name]['PhoneNum'])
        device.touch(50,620,'DOWN_AND_UP')
        device.type(dic[name]['Email'])
        device.touch(50,785,'DOWN_AND_UP')        
        device.type(dic[name]['Address'])   
        MonkeyRunner.sleep(3)
        device.touch(76,74,'DOWN_AND_UP')
        MonkeyRunner.sleep(6)
        print str(datetime.datetime.now())+"  "+"add contact "+name+" end"
        MonkeyRunner.sleep(1)
        
        # shot Cmp Image and save #
        print str(datetime.datetime.now())+"  "+"shot cmpImage"
        cmpImage = device.takeSnapshot().getSubImage((0,38,480,762))
        cmpImage.writeToFile('./Case02_cmpImg/'+name+'.png','png')
        print str(datetime.datetime.now())+"  "+"cmpImage save success"
        MonkeyRunner.sleep(2)
        
        refImage1 = MonkeyRunner.loadImageFromFile('./Case02_refImg/'+name+'.png','png')
        refImage2 = MonkeyRunner.loadImageFromFile('./Case02_refImg/'+name+'_'+'.png','png')
        # judge this round pass or fail #
        if cmpImage.sameAs(refImage1) or cmpImage.sameAs(refImage2):
            print str(datetime.datetime.now())+"  "+"add success and detail of "+name+" is correct"
            CaseResultCount += 1
        else:
            print str(datetime.datetime.now())+"  "+"add fail , case stop"
            break

        device.shell("am force-stop com.android.contacts")
        MonkeyRunner.sleep(2)
        device.startActivity(component = 'com.android.contacts/.activities.PeopleActivity')
        MonkeyRunner.sleep(5)
        
        print str(datetime.datetime.now())+"  "+"round "+name+" over"
        print "*******************************************************"
        MonkeyRunner.sleep(3)           
            
    except:
        print "Exception detected , action of this round is wrong"
        print "Kill contacts and restart"
        device.shell("am force-stop com.android.contacts")
        MonkeyRunner.sleep(3)
        device.startActivity(component = 'com.android.contacts/.activities.PeopleActivity')
        MonkeyRunner.sleep(5)

# judge Case01 pass or not #        
if CaseResultCount== len(dic):
    print str(datetime.datetime.now())+"  "+"Case02 PASS!"
    device.shell("am force-stop com.android.contacts")
else:
    print str(datetime.datetime.now())+"  "+"Case02 FAIL!"
    device.shell("am force-stop com.android.contacts")



