import Pmw
import platform
import threading
import psutil
from datetime import datetime

ventana = Pmw.initialise(fontScheme = 'pmw1')
ventana.title("SYSTEM/HARDWARE INFO")

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def clear():
    display.clear()

def disk():
    display.appendtext(("="*20)+"Disk Information"+(("=")*20)+"\n")
    display.appendtext("Partitions and Usage:\n")
    partitions = psutil.disk_partitions()
    for partition in partitions:
        display.appendtext(f"=== Device: {partition.device} ===\n")
        display.appendtext(f"Mountpoint: {partition.mountpoint}\n")
        display.appendtext(f"File system type: {partition.fstype}\n")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        display.appendtext(f"Total Size: {get_size(partition_usage.total)}\n")
        display.appendtext(f"Used: {get_size(partition_usage.used)}\n")
        display.appendtext(f"Free: {get_size(partition_usage.free)}\n")
        display.appendtext(f"Percentage: {partition_usage.percent}%\n")
    disk_io = psutil.disk_io_counters()
    display.appendtext(f"Total read: {get_size(disk_io.read_bytes)}\n")
    display.appendtext(f"Total write: {get_size(disk_io.write_bytes)}\n")

def memory():
    display.appendtext(("="*40)+"Memory Information"+(("=")*40)+"\n")
    svmem = psutil.virtual_memory()
    display.appendtext(f"Total: {get_size(svmem.total)}\n")
    display.appendtext(f"Available: {get_size(svmem.available)}\n")
    display.appendtext(f"Used: {get_size(svmem.used)}\n")
    display.appendtext(f"Percentage: {svmem.percent}%\n")
    display.appendtext(("="*20)+"SWAP"+("="*20)+"\n")
    swap = psutil.swap_memory()
    display.appendtext(f"Total: {get_size(swap.total)}\n")
    display.appendtext(f"Free: {get_size(swap.free)}\n")
    display.appendtext(f"Used: {get_size(swap.used)}\n")
    display.appendtext(f"Percentage: {swap.percent}%\n")

def system():
    display.appendtext(("="*40)+"System Information"+(("=")*40)+"\n")
    uname = platform.uname()
    display.appendtext(f"System: {uname.system}\n")
    display.appendtext(f"Node Name: {uname.node}\n")
    display.appendtext(f"Release: {uname.release}\n")
    display.appendtext(f"Version: {uname.version}\n")
    display.appendtext(f"Machine: {uname.machine}\n")
    display.appendtext(f"Processor: {uname.processor}\n")
    
def cpu():
    display.appendtext(("="*40)+"CPU Information"+(("=")*40)+"\n")
    display.appendtext(("Physical cores: "+str(psutil.cpu_count(logical=False))))
    display.appendtext("\n")
    display.appendtext(("Total cores: "+str(psutil.cpu_count(logical=True))))
    display.appendtext("\n")
    cpufreq = psutil.cpu_freq()
    display.appendtext(f"Max Frequency: {cpufreq.max:.2f}Mhz\n")
    display.appendtext(f"Min Frequency: {cpufreq.min:.2f}Mhz\n")
    display.appendtext(f"Current Frequency: {cpufreq.current:.2f}Mhz\n")
    display.appendtext("CPU Usage Per Core:\n")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        display.appendtext(f"Core {i}: {percentage}%\n")
    display.appendtext(f"Total CPU Usage: {psutil.cpu_percent()}%\n")
    

def inicia(index):
    infos={0:system,1:cpu,2:memory,3:disk}
    t=threading.Thread(target=infos[index])
    t.start()


display = Pmw.ScrolledText(ventana, hscrollmode='none',
                      vscrollmode='dynamic', hull_relief='sunken',
                      hull_background='gray20', hull_borderwidth=10,
                      text_background='black', text_width=120,
                      text_foreground='green', text_height=37,
          text_padx=10, text_pady=10, text_relief='groove',
                      text_font=('Fixedsys', 10))
display.pack(padx=0,pady=0)

botones = Pmw.ButtonBox(ventana)
botones.pack(fill='both', expand=1, padx=1, pady=1)

botones.add('System',command=lambda:inicia(0))
botones.add('CPU',command=lambda:inicia(1))
botones.add('CLEAR',command=clear)
botones.add('MEMORY',command=lambda:inicia(2))
botones.add('DISK',command=lambda:inicia(3))

ventana.mainloop()
    

