from ClassLib.Bluetooth_Car import Bluetooth_Car
from ClassLib.Bizhang_Car import Bizhang_Car
from ClassLib.xunji_Car import xunji_Car
class Multif_Car(Bluetooth_Car,Bizhang_Car,xunji_Car):
	def __init__(self,ENr,IN1r,IN2r,timerr,channelr,freqr,pwprr,ENl,IN1l,IN2l,timerl,channell,freql,pwprl,green_light,red_light,yellow_light,xunji_IN1,xunji_IN2,xunji_IN3,xunji_IN4,servo,trig,echo,uartx,baud_ratex=9600):
		Bluetooth_Car.__init__(self,ENr,IN1r,IN2r,timerr,channelr,freqr,pwprr,ENl,IN1l,IN2l,timerl,channell,freql,pwprl,green_light,red_light,yellow_light,uartx,baud_ratex)
		Bizhang_Car.__init__(self,ENr,IN1r,IN2r,timerr,channelr,freqr,pwprr,ENl,IN1l,IN2l,timerl,channell,freql,pwprl,green_light,red_light,yellow_light,servo,trig,echo)
		xunji_Car.__init__(self,ENr,IN1r,IN2r,timerr,channelr,freqr,pwprr,ENl,IN1l,IN2l,timerl,channell,freql,pwprl,green_light,red_light,yellow_light,xunji_IN1,xunji_IN2,xunji_IN3,xunji_IN4)
		#重写 commands
		self.commands={
		#前进3档
		11:[1,1],12:[1,2],13:[1,3],
		#后退三档
		21:[2,1],22:[2,2],23:[2,3],
		#左转三档
		31:[3,1],32:[3,2],33:[3,3],
		#右转三档
		41:[4,1],42:[4,2],43:[4,3],
		#刹车
		0:[0],
		#自由熄火
		-1:[-1],
		#避障模式
		5:[5],
		#循迹模式
		6:[6]
		}
		
		#重写 command_execute
	def command_execute(self,command_num):   #输入代表指令的数字（见self.commands），查字典，执行响应指令
		if self.commands[command_num][0]==-1:
			self.cutoff()
		elif self.commands[command_num][0]==0:
			self.stop()
		elif self.commands[command_num][0]==1:
			self.forward_with_speed(self.commands[command_num][1])
		elif self.commands[command_num][0]==2:
			self.back_with_speed(self.commands[command_num][1])
		elif self.commands[command_num][0]==3:
			self.turn_left(self.commands[command_num][1])
		elif self.commands[command_num][0]==4:
			self.turn_right(self.commands[command_num][1])
		elif self.commands[command_num][0]==5:
			self.bizhang()
		elif self.commands[command_num][0]==6:
			self.xunji()
		else:
			pass
			
def main():
	import pyb
	from pyb import LED
	from pyb import Pin
	from pyb import Timer
	from pyb import UART
	from pyb import Servo
	from ClassLib.Multif_Car import Multif_Car
	ENA=Pin('Y1',Pin.OUT_PP)
	ENB=Pin('Y2',Pin.OUT_PP)

	IN1=Pin('Y3',Pin.OUT_PP)
	IN2=Pin('Y4',Pin.OUT_PP)
	IN3=Pin('Y5',Pin.OUT_PP)
	IN4=Pin('Y6',Pin.OUT_PP)

	ECHO=Pin('Y11',Pin.OUT_PP)
	TRIG=Pin('Y12',Pin.OUT_PP)

	My_Servo=Servo(1)

	red_light	= Pin(Pin.cpu.A13,Pin.OUT_PP)
	green_light	= Pin(Pin.cpu.A14,Pin.OUT_PP)
	yellow_light= Pin(Pin.cpu.A15,Pin.OUT_PP)

	uart=UART(1,9600)
	uart.write("I am ready")
	pyb.delay(10)

	My_Car=Multif_Car(ENA,IN1,IN2,8,1,20000,0,ENB,IN3,IN4,8,2,20000,0,green_light,red_light,yellow_light,My_Servo,TRIG,ECHO,1,9600)

	while True:
		My_Car.bluetooth_receive_and_run()
	
if __name__=='__main__':
	main()