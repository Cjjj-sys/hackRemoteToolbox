import hackchat,uuid,threading
mac=uuid.UUID(int=uuid.getnode()).hex[-12:].upper()
nick=input('Input nickname(@mac=MAC):').replace('@mac',mac).replace('@MAC',mac)
channel=input('Input channel(whoami):')
if channel=='':
    channel='whoami'
conn=hackchat.HackChat(nick,channel)
conn.on_whisper+=[cmdexec]
conn.on_join+=[finddevices]
conn.on_leave+=[finddevices]
statu=0
identifyok=False
randmsg:str=''
stage=dict()
devices=set(conn.online_users.remove([conn.nick]))
for i in devices:
    stage.update(i:0)
t=threading.Thread(target=operate)
t.start()
conn.run()

def cmdexec(conn,msg,sender,result):
    global statu
    if msg[0]!='_':
        if statu==0:
            print(msg)
        else:
            statu-=1
            import base64,os
            fn=fn()+'.png'
            with open(fn,'wb') as f:
                f.write(base64.decodestring(msg))
                os.system('start '+fn)
                print('File saved in '+fn)
    else:
        msg2=msg.split(' ')
        if msg2[1].lower()=='identify2':
            import rsa,uuid,os
            (p,d,f)=os.walk('.')
            pub_keyfn_set=set()
            for i in f:
                if i.split('.')[-1].lower()=='pub':
                    pub_keyfn_set.add(i)
            for pub_keyfn in pub_keyfn_set:
                pub_keyfn=''
                pub_key1=None
                with open(pub_keyfn,'rb') as f:
                    pub_key1=rsa.PublicKey.load_pkcs1(f.read())
                if rsa.verify(randmsg.encode('utf-8'),msg2[2].encode('utf-8'),pub_key1):
                    pri_keyfn=''
                    pri_key=None
                    with open(pri_keyfn,'rb') as f:
                        pri_key=rsa.PrivateKey.load_pkcs1(f.read())
                    m=+rsa.sign(msg2[2].encode('utf-8'),pri_key,'SHA-1')
                    conn.send_to(sender,'_ identify2 '+m.decode('utf-8'))
                    identifyok=True
            identifyok=False



def finddevices(conn,nick):
    global devices
    print('Verifying devices...')
    print('Current devices:',end='')
    devices=set(conn.online_users.remove([conn.nick]))
    temp=devices
    for i in temp:
        if identify(conn,i)==False:
            devices.remove([i])
    print(devices,sep=',')

def identify(conn,u:str) -> bool:
    import rsa,uuid
    randmsg=uuid.uuid4().hex
    conn.send_to(target=u,msg='_ identify1 '+randmsg)
    
def operate():
    global conn
    finddevices(conn,'')
    while True:
        cmd=input('>').strip()
        target=set()
        if cmd[0]=='@':
            for i in cmd.split(' '):
                if i[0]=='@':
                    target+=i.lstrip('@')
        else:
            target=devices
        if cmd.lower()=='devices':
            finddevices(conn,'')
        elif cmd.lower()=='screenshot':
            global statu
            statu+=len(target)#!
            for i in target:
                conn.send_to(target=i,msg=cmd)
        elif cmd.lower()=='bye':
            exit(0)
        else:
            for i in target:
                conn.send_to(target=i,msg=cmd)
