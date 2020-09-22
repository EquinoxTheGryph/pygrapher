import matplotlib.pyplot as plt
from matplotlib import dates
import json
import dateutil.parser
import sys
import io

# Set amount of x and y ticks
xamount = 10
yamount = 10

# Range with floating point support
def frange(start, stop, step, d = 2):
    out = []
    counter = start
    while True:
        out.append(round(counter, d))
        counter += step
        if counter >= stop:
            break
    return out

# Main Function
def graph(data_file, output_file = 'output.png'):
    # Get arguments
    #arglen = len(sys.argv)
    #data_file = sys.argv[1]
    #if arglen > 2:
        #output_file = sys.argv[2]
    #else:
        #output_file = 'output.png'

    # Load data_file
    jarr = []
    with io.open(data_file,'r',encoding='utf8') as json_file:
        jarr = json.load(json_file)


    # Parse array
    arr_x = []
    arr_y = []

    for i in jarr:
        state_value = 0
        try:
            state_value = float(i["state"])
            arr_x.append(dateutil.parser.isoparse(i["last_updated"]))
            arr_y.append(state_value)
        except ValueError:
            print("'%s' is not a number, skipped" % i["state"])
        
    sensor_name = jarr[0]["attributes"]["friendly_name"]
    sensor_unit = jarr[0]["attributes"]["unit_of_measurement"]
    
    # Init plot
    fig, ax = plt.subplots()
    #ax.plot(arr_x, arr_y)
    ax.plot_date(arr_x, arr_y, fmt='')
    
    fig.autofmt_xdate()
    hfmt = dates.DateFormatter('%m/%d %H:%M')
    ax.xaxis.set_major_locator(dates.HourLocator())
    ax.xaxis.set_major_formatter(hfmt)

    # Clean up the plot
    xticks = ax.get_xticks()
    yticks = ax.get_yticks()
    xticks_new = []
    yticks_new = []
    
    # Set X ticks
    xlen = len(xticks)
    for i in frange(0, xlen, (xlen / (xamount-1))):
        #print(i, valmap(i, 0, xlen, xticks[0], xticks[-1]))
        xticks_new.append(valmap(i, 0, xlen, xticks[0], xticks[-1]))
    #print(xlen, xticks[-1])
    xticks_new.append(xticks[-1])
    ax.set_xticks(xticks_new)
    
    # Set Y ticks
    ylen = len(yticks)
    #print(yticks, ylen)
    for i in frange(0, ylen, (ylen / (yamount-1))):
        #print(i, valmap(i, 0, ylen, yticks[0], yticks[-1]))
        yticks_new.append(valmap(i, 0, ylen, yticks[0], yticks[-1]))
    #print(ylen, yticks[-1])
    yticks_new.append(yticks[-1])
    ax.set_yticks(yticks_new)
    
    # Render plot
    ax.set(xlabel = 'Time', ylabel = sensor_unit,
        title = sensor_name)
    ax.grid()


    fig.savefig(output_file)
    #plt.show()

# Map Values
def valmap(value, istart, istop, ostart, ostop):
  return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))
