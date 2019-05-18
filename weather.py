#90's weather channel display thingy by 99710
#inspired by the weather displays that enviroment canada used in the 80s/90s
#https://www.youtube.com/watch?v=fco9mR2Uzko was used as reference for this
#should note enviroment canada used different layouts such as this one from 86 https://www.youtube.com/watch?v=Pp4-Gsz2i8I


from tkinter import *
from tkinter import ttk
from tkinter import font
from yahoo_weather.weather import YahooWeather
from yahoo_weather.config.units import Unit
import time


root = Tk()

###Parameters###

# A raspberry pi (using composite) runs at 720x480?
#i tested this with mine, PAL i think is 720x576 and NTSC is 720x480
window_size = "720x480"
#title of the window, not visible if using fullscreen
window_title = 'enviroment_canada'
#uncomment to enable fullscreen, only do this on a pi running composite
#root.attributes("-fullscreen", True)

#yahoo weather API keys
Y_id = ""
Y_key = ""
Y_secret = ""

#weather stuff
#(have to add UK to the end because there is also a durham in USA)
weather_location = "Durham UK"

#screen switch time in ms
screen_time = 20000


#startup
print('90s Weather channel by 99710')
print("Initializing...")
#weather_location = input('Enter a location: ')

def show_time():
    time_text.set(time.strftime("TIME %H:%M:%S"))
    root.after(1000, show_time)

def show_date():
    date_text.set(time.strftime("%a  %B %d"))
    root.after(1000, show_date)

def quit(*args):
    root.destroy()

   

#init the window
root.title(window_title)
root.geometry(window_size)
#disable resizing
root.resizable(0, 0)
#advance the clock every second
root.after(1000, show_time)
#date doesn't need to be updated as frequently
root.after(10000, show_date)
# bind esc to quit
root.bind("<Escape>", quit)

#font settings
#'system' isn't present on linux but is on any windows machine
#with the fonts i went with something blocky looking to mimic the orginial, system came to mind
#probably some font out there that does it better than system but eh
weather_font = font.Font(family='system', size=18, weight='bold')

#canvas settings
w = Canvas(root, width=720, height=480, borderwidth=0)

#more weather stuff
data = YahooWeather(APP_ID=Y_id, api_key=Y_key, api_secret=Y_secret)

def weather(*args):
    data.get_yahoo_weather_by_city("Durham UK", Unit.celsius)
    data.get_forecasts()
    #update the weather after 20mins
    root.after(20000, weather)
    
#start the weather loop
root.after(400, weather)    
    
#clock#
time_text = StringVar()
time_text.set(time.strftime("TIME %H:%M:%S"))
date_text = StringVar()
date_text.set(time.strftime("%a  %B %d"))


#background sections
#top
w.create_rectangle(0, 0, 720, 100, fill="dark green")

#bottom
w.create_rectangle(720, 380, 0, 480, fill="dark green")

#the text

#time and date
time_label = ttk.Label(root, textvariable=time_text, font=weather_font, foreground="white", background="dark green")
time_label.place(relx=0.35, rely=0.85, anchor='center')
date_label = ttk.Label(root, textvariable=date_text, font=weather_font, foreground="white", background="dark green")
date_label.place(relx=0.67, rely=0.85, anchor='center')

#bottom text, in the original it says enviroment canada weather
w.create_text(360, 455, text="Enviroment Gensokyo Weather", font=weather_font, fill='white', justify='center')

def mainscreen(*args):

    #delete stuff from hi_low screen
    w.delete(22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43)

    #draw background
    w.create_rectangle(0, 100, 720, 380, fill="dark red")
    
    #location name
    w.create_text(160, 120, text=weather_location, font=weather_font, fill='white', justify='center', tags="location")

    #weather text
    w.create_text(150, 170, text="TEMP  " , font=weather_font, fill='white', justify='center')
    w.create_text(210, 170, text=(data.condition.temperature) , font=weather_font, fill='white', justify='center')
    w.create_text(245, 170, text="C" , font=weather_font, fill='white', justify='center')

    #humidity
    w.create_text(150, 205, text="HUM  " , font=weather_font, fill='white', justify='center')
    w.create_text(210, 205, text=str(data.atmosphere.humidity) , font=weather_font, fill='white', justify='center')
    w.create_text(245, 205, text="%" , font=weather_font, fill='white', justify='center')

    #cloud info
    w.create_text(415, 205, text=str(data.condition.text) , font=weather_font, fill='white', justify='center')

    #wind
    w.create_text(395, 170, text="WIND  " , font=weather_font, fill='white', justify='center')
    w.create_text(455, 170, text=str(data.wind.direction) , font=weather_font, fill='white', justify='center')
    #this outputs in degrees, would be a good idea to convert to cardinal directions
    w.create_text(510, 170, text=str(data.wind.speed) , font=weather_font, fill='white', justify='center')
    w.create_text(580, 170, text="KM/H" , font=weather_font, fill='white', justify='center')

    #Visibilty
    w.create_text(260, 270, text="VISIBILITY" , font=weather_font, fill='white', justify='center')
    w.create_text(370, 270, text=str(data.atmosphere.visibility) , font=weather_font, fill='white', justify='center')
    w.create_text(425, 270, text="KM" , font=weather_font, fill='white', justify='center')

    #Pressure 
    w.create_text(260, 305, text="PRESSURE" , font=weather_font, fill='white', justify='center')
    w.create_text(375, 305, text=str(data.atmosphere.pressure) , font=weather_font, fill='white', justify='center')
    w.create_text(450, 305, text="KPA" , font=weather_font, fill='white', justify='center')

#go to the hi_low screen
    root.after(screen_time, hi_lo_screen)



#the high low screen (blue background)    
def hi_lo_screen(*args):
    #delete the elements from main screen
    w.delete(4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22)
    #draw the new background
    w.create_rectangle(0, 100, 720, 380, fill="dark blue")

    #make the new text
    #title
    w.create_text(150, 120, text=weather_location, font=weather_font, fill='white', justify='center', tags="location")
    w.create_text(400, 120, text="WEEKLY FORECAST", font=weather_font, fill='white', justify='center')

    #hi_low_1
    #the [0] controls where in the list it'll read from, 0 being the first
    w.create_text(160, 180, text=str(data.forecasts[0].day), font=weather_font, fill='white', justify='center')
    w.create_text(220, 180, text=str(data.forecasts[0].high) , font=weather_font, fill='white', justify='center')
    w.create_text(265, 180, text=str(data.forecasts[0].low) , font=weather_font, fill='white', justify='center')
    w.create_text(415, 180, text=str(data.forecasts[0].text) , font=weather_font, fill='white', justify='center')

    #hi_low_1
    #the [0] controls where in the list it'll read from, 0 being the first
    w.create_text(160, 220, text=str(data.forecasts[1].day), font=weather_font, fill='white', justify='center')
    w.create_text(220, 220, text=str(data.forecasts[1].high) , font=weather_font, fill='white', justify='center')
    w.create_text(265, 220, text=str(data.forecasts[1].low) , font=weather_font, fill='white', justify='center')
    w.create_text(415, 220, text=str(data.forecasts[1].text) , font=weather_font, fill='white', justify='center')

    #hi_low_2
    #the [0] controls where in the list it'll read from, 0 being the first
    w.create_text(160, 260, text=str(data.forecasts[2].day), font=weather_font, fill='white', justify='center')
    w.create_text(220, 260, text=str(data.forecasts[2].high) , font=weather_font, fill='white', justify='center')
    w.create_text(265, 260, text=str(data.forecasts[2].low) , font=weather_font, fill='white', justify='center')
    w.create_text(415, 260, text=str(data.forecasts[2].text) , font=weather_font, fill='white', justify='center')

    #hi_low_3
    #the [0] controls where in the list it'll read from, 0 being the first
    w.create_text(160, 300, text=str(data.forecasts[3].day), font=weather_font, fill='white', justify='center')
    w.create_text(220, 300, text=str(data.forecasts[3].high) , font=weather_font, fill='white', justify='center')
    w.create_text(265, 300, text=str(data.forecasts[3].low) , font=weather_font, fill='white', justify='center')
    w.create_text(415, 300, text=str(data.forecasts[3].text) , font=weather_font, fill='white', justify='center')

    #hi_low_4
    #the [0] controls where in the list it'll read from, 0 being the first
    w.create_text(160, 340, text=str(data.forecasts[4].day), font=weather_font, fill='white', justify='center')
    w.create_text(220, 340, text=str(data.forecasts[4].high) , font=weather_font, fill='white', justify='center')
    w.create_text(265, 340, text=str(data.forecasts[4].low) , font=weather_font, fill='white', justify='center')
    w.create_text(415, 340, text=str(data.forecasts[4].text) , font=weather_font, fill='white', justify='center')
    

    #switch back to the main screen after 20s
    root.after(screen_time, mainscreen)




#print(data.condition.text)

#start the screen loop    
root.after(400, mainscreen)


w.pack()
root.mainloop()

