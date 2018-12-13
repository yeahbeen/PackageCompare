from tkinter import *
import tkinter.filedialog
import tkinter.messagebox
import os
import shutil
import time
import threading
import ftplib

top = Tk()
top.title("文件对比工具")
#屏幕宽度和高度
sw = top.winfo_screenwidth()
sh = top.winfo_screenheight()
#窗口宽度和高度
ww = 400
wh = 200
#窗口居中
top.geometry("%dx%d+%d+%d" %(ww,wh,(sw-ww)/2,(sh-wh)/2))
E1 = Entry(top)
E2 = Entry(top)
L1 = Label(top)
initdir = "."
def openfile1():
    global initdir
    filename=tkinter.filedialog.askopenfilename(initialdir = initdir)
    if filename != "":
        E1.delete(0,END)
        E1.insert(0,filename)
        initdir = os.path.split(filename)[0]
def openfile2():
    global initdir
    filename=tkinter.filedialog.askopenfilename(initialdir = initdir)
    if filename != "":
        E2.delete(0,END)
        E2.insert(0,filename)
        initdir = os.path.split(filename)[0]
def extract(filename,dir):
    # dir = os.path.splitext(filename)[0]
    if os.path.exists(dir):
        shutil.rmtree(dir)  
    cmd = "7z x \"" + filename + "\" -y -o\"" + dir + "\""
    print(cmd)
    tmp = os.system(cmd)
    print(tmp)
    # tmp = os.popen(cmd).readlines()
    # print(tmp)
    for root, dirs, files in os.walk(dir):
        for name in files:
            if ".htm" in name or ".ico" in name or ".js" in name or ".pak" in name or ".png" in name or ".xar" in name:
                continue
            f = os.path.join(root, name)
            # print(f)
            cmd = "7z t " + f
            # print(cmd)
            tmp = os.popen(cmd).read()        
            if "Everything is Ok" in tmp and "Testing     .text" not in tmp:
                print(f)
                print(tmp)
                cmd = "7z x " + f + " -y -o" + os.path.splitext(f)[0]
                # print(cmd)
                tmp = os.system(cmd)
                # print(tmp)
        for name in dirs:
            # print(os.path.join(root, name))
            pass
def thread_it(func):
    t = threading.Thread(target=func) 
    t.setDaemon(True) 
    t.start()
  
def downfile(filename):
    print(filename)
    if re.match("^[b-kB-K]:\\\\",filename) or re.match("^[b-kB-K]:/",filename):
        return filename
    o = re.match("^ftp://(\d+\.\d+\.\d+\.\d+)(/.*)",filename)
    if o:
        ip = o.group(1)
        print(ip)
        remotepath = o.group(2)
        print(remotepath)    
        bufsize = 1024
        localpath = os.path.split(filename)[1]
        print(localpath)
        fp = open(localpath, 'wb')
        ftp = ftplib.FTP(ip)  
        ftp.login()  
        ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)
        ftp.set_debuglevel(0)
        fp.close()
        ftp.quit()
        return localpath
    if re.match("^\\\\\\\\(\d+\.\d+\.\d+\.\d+)",filename):
        localpath = os.path.split(filename)[1]
        print(localpath)
        shutil.copy(filename,localpath)
        return localpath
        
def compare():
    try:
        real_compare()
    except Exception as e:
        import traceback
        estr = traceback.format_exc()
        tkinter.messagebox.showinfo("异常",estr)
        L1.config(text="发生错误！")
  
def real_compare():
    t0 = time.time()
    print(t0)
    file1 = E1.get().strip()
    if file1 == "":
        tkinter.messagebox.showinfo(message='请先选择文件1')
        return
    file2 = E2.get().strip()  
    if file2 == "":
        tkinter.messagebox.showinfo(message='请先选择文件2')
        return
    L1.config(text="正在处理...")
    B3.config(state="disabled")        
    file1 = downfile(file1)
    print(file1)
    dir1 = os.path.splitext(os.path.split(file1)[1])[0]
    
    file2 = downfile(file2)
    print(file2)
    dir2 = os.path.splitext(os.path.split(file2)[1])[0]
    
    extract(file1,dir1)
    extract(file2,dir2)
    savefile = os.path.split(dir1)[1]+" vs "+os.path.split(dir2)[1]+".html"
    cmd = "BCompare.exe /silent @diff_to_html.txt " + dir1 + " " + dir2 + " \"" + savefile +"\""
    print(cmd)
    tmp = os.system(cmd)
    print(tmp)
    print(time.time()-t0)
    L1.config(text="处理结束")
    B3.config(state="normal")
    tkinter.messagebox.showinfo("完成","处理完成，结果存放在:"+savefile)
    
def opendir():
    file1 = E1.get().strip()
    dir1 = os.path.splitext(os.path.split(file1)[1])[0]
    file2 = E2.get().strip()
    dir2 = os.path.splitext(os.path.split(file2)[1])[0]
    savefile = dir1+" vs "+dir2+".html"
    if os.path.exists(savefile):
        os.system("start explorer.exe /select,"+os.path.realpath(savefile))
    else:
        os.system("start explorer.exe .")
    
B1 = Button(top, command = openfile1, text = "选择文件1")
B2 = Button(top, command = openfile2, text = "选择文件2")

B3 = Button(top, command = lambda :thread_it(compare), text = "开始对比")
B4 = Button(top, command = opendir, text = "打开结果目录")

E1.place(x=10,y=15,width=300,height=25)
E2.place(x=10,y=45,width=300,height=25)
B1.place(x=320,y=15,width=65,height=25)
B2.place(x=320,y=45,width=65,height=25)

B3.place(x=75,y=100,width=100,height=30)
B4.place(x=225,y=100,width=100,height=30)
L1.place(x=100,y=145,width=200,height=30)

top.mainloop()
