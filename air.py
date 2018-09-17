import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.dates as mdates
import pickle

os.chdir(sys.path[0])

sample = 144
PANDA_FRAME_SRC = '/home/pi/Python/daikin/module/obj/panda_frame.pkl'
PANDA_FRAME_DST = os.getcwd()

def get_log_file():
	with open(r'C:\Users\Johan\Documents\Programming\Python\passwords\daikin_pi.pickle', 'rb') as f:
		p = pickle.load(f)
	passwd = p['passwd']
	username = p['username']
	remote_ip = p['ip']
	os.system('pscp -r -pw {0} {1}@{2}:{3} {4}'.format(passwd,username,remote_ip,PANDA_FRAME_SRC,PANDA_FRAME_DST))
			
def load_obj(path):
	with open(path,'rb') as f:
		return pickle.load(f)
	
def get_data_frame():
	path = os.path.join(PANDA_FRAME_DST,'panda_frame.pkl') 
	if not os.path.exists(path):
		return pd.DataFrame()
	else:
		return load_obj(path)
	
def plot_graph():
	df = get_data_frame()
	#print(df)
	style.use('fivethirtyeight')
	xfmt = mdates.DateFormatter('%H:%M')
		
	in_temp = df['Daikin Indoor Temp'][-sample:]
	in_temp_rolling = df['Daikin Indoor Temp'].rolling(30).mean()[-sample:]
	in_temp_kitchen = df['Sector Kitchen Temp'][-sample:]
	in_temp_kitchen_rolling = df['Sector Kitchen Temp'].rolling(30).mean()[-sample:]
	out_temp = df['Daikin Outdoor Temp'][-sample:]
	out_temp_yr = df['Yr Outdoor Temp'][-sample:]
	out_temp_future_yr = df['Yr Future Low Outdoor Temp'][-sample:]
	target_indoor_temp = df['Target Indoor Temp'][-sample:]
	mompow = df['mompow'][-sample:]
	mompow_rolling = df['mompow'].rolling(30).mean()[-sample:]
	
	plt.suptitle('Daikin Heatpump')
	
	# 	ax1 plot settings
	ax1 = plt.subplot2grid((2,2),(0,0))
	ax1.xaxis.set_major_formatter(xfmt)
	plt.ylabel('Celcius')
	plt.xlabel('Time')
	in_temp_kitchen_rolling.plot(ax=ax1, label='Sector Indoor Temp Rolling')
	in_temp_kitchen.plot(ax=ax1, label='Sector Indoor Temp')
	#target_indoor_temp.plot(ax=ax1, label='Daikin Target Indoor Temp')
	plt.legend(loc=6)
		
	#	ax2 plot setttings
	ax2 = plt.subplot2grid((2,2),(1,0))
	ax2.xaxis.set_major_formatter(xfmt)
	plt.ylabel('Celcius')
	plt.xlabel('Time')
	#out_temp.plot(ax=ax2, label='Daikin Outdoor Temp')
	out_temp_yr.plot(ax=ax2, label='Yr Outdoor Temp')
	out_temp_future_yr.plot(ax=ax2, label='Yr Lowest Temp in next {} hour'.format(df['number_of_hours'][-1]))
	#mompow.plot(ax=ax2, label='mompow')
	#mompow_rolling.plot(ax=ax2, label='mompow rolling')
	plt.legend(loc=6)
	
	# 	ax3 plot settings
	ax3 = plt.subplot2grid((2,2),(0,1))
	ax3.xaxis.set_major_formatter(xfmt)
	plt.ylabel('Celcius')
	plt.xlabel('Time')
	#out_temp.plot(ax=ax2, label='Daikin Outdoor Temp')
	#out_temp_yr.plot(ax=ax2, label='Yr Outdoor Temp')
	#out_temp_future_yr.plot(ax=ax2, label='Yr Lowest Temp in next 12 hour')
	#mompow.plot(ax=ax3, label='mompow')
	mompow_rolling.plot(ax=ax3, label='mompow rolling')
	plt.legend(loc=6)
	
	# 	ax4 plot settings
	ax4 = plt.subplot2grid((2,2),(1,1))
	ax4.xaxis.set_major_formatter(xfmt)
	plt.ylabel('Celcius')
	plt.xlabel('Time')
	#in_temp_rolling.plot(ax=ax4, label='Daikin Indoor Temp Rolling')
	#in_temp.plot(ax=ax4, label='Daikin Indoor Temp')
	target_indoor_temp.plot(ax=ax4, label='Daikin Target Indoor Temp')
	plt.legend(loc=6)
	
	plt.grid(True)
	mng = plt.get_current_fig_manager()
	mng.window.state('zoomed')
	plt.show()

if __name__== '__main__':
	get_log_file()	
	plot_graph()
	
		