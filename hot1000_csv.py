import tkinter as tk
from pylsl import StreamInlet, resolve_streams
import time
import csv
import datetime

name = str("hiro_normal_")

# ============== get nirs data ===============

streams = resolve_streams(wait_time=3.)  # put all stream data into streams. list
streams_count = len(streams)

for i in range(streams_count):
    inlet = StreamInlet(streams[i])  # StreamInletという関数を使用し、引数としてstream[i]を使う
    get_address = inlet.info().source_id()
    # print(i)
    # print(get_address)

    if get_address != "78:61:7c:64:46:16":
        continue
    print(i)
    target_address = inlet.info().source_id()
    print(target_address)
    target_stream = i

print("================================")
print("target stream is ...")
print(target_stream)
print(target_address)

inlet = StreamInlet(streams[target_stream])

all_data_list = []

def main():
    after_id = None
    repet_nums = 0
    update_intarval = 10  # 更新時間(msec)

    def export_csv(nirslist, csv_dir):
        with open(csv_dir, "w") as f:
            writer = csv.writer(f, lineterminator='\n')

            if isinstance(nirslist[0], list):  # 多次元かどうかを判別してる
                writer.writerows(nirslist)

            else:
                writer.writerows(nirslist)

    def convert_data():
        global after_id
        ####この下の部分に繰り返したい操作を書く#########################################

        all_data = inlet.pull_sample()
        all_data_list.append(all_data[0])

        print(all_data[0])


        #############################################################################

        after_id = showinfo.after(update_intarval, convert_data)

    def start():
        global repet_nums
        repet_nums = 0
        convert_data()

    def stop_convert():
        global after_id
        if after_id:
            showinfo.after_cancel(after_id)
            after_id = None

            # =============== export csv =================
            day_data = datetime.datetime.now()

            dir1 = r"C:\Users\usura\Desktop\研究\hot_data\ "
            dir2 = day_data.strftime('%Y-%m-%d %H_%M ')
            dir3 = name
            dir4 = '.csv'
            file_name = dir1+dir2+dir3+dir4

            now = datetime.datetime.now()

            print(file_name)

            export_csv(all_data_list, file_name) # file_name問題は時間を表す：マークがあることによって起きてた。：マークがあるとcsvファイルとして認識されない

            showinfo.destroy()

    showinfo = tk.Tk()

    frame_top = tk.Frame(showinfo, bd=2, relief="ridge")
    frame_top.pack(fill="x", pady=2)

    label1 = tk.Label(frame_top, text="recording...")
    label1.pack(side="left")

    frame_bottom = tk.Frame(showinfo, bd=2)
    frame_bottom.pack(fill="x")

    button1 = tk.Button(frame_bottom, text="STOP", bg="#f0e68c", fg="#ff0000", command=stop_convert)
    button1.pack()

    start()

    showinfo.mainloop()

if __name__ == '__main__':
    main()

# 挙動確認　6月14日