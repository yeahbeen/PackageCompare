import os
import shutil
import time

file1 = "Thunder9.5.62.2096Beta.exe"
file2 = "Thunder9.5.63.2128Beta.exe"


def extract(filename):
    dir = os.path.splitext(filename)[0]
    if os.path.exists(dir):
        shutil.rmtree(dir)  
    cmd = "7z x " + filename + " -y -o" + dir
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
t0 = time.time()
print(t0)
# extract(file1)
# extract(file2)
cmd = "BCompare.exe /silent @diff_to_html.txt " + os.path.splitext(file1)[0] + " " + os.path.splitext(file2)[0] + " my_report.html"
print(cmd)
tmp = os.system(cmd)
print(tmp)
print(time.time()-t0)