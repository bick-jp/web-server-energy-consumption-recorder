import threading
import ina219_datarecorder
import imagesize_pingpong

thread1 = threading.Thread(target=ina219_datarecorder.recordEnergyConsumption)
thread2 = threading.Thread(target=imagesize_pingpong.pingpongImage)
thread1.start()
thread2.start()
thread1.join()
thread2.join()

print("main done")
#ina219_datarecorder.recordEnergyConsumption()
#imagesize_pingpong.pingpongImage()