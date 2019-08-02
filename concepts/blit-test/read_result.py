import pickle
import numpy

def getOnePercentLow(array):    
    one_percent = round(len(array) /100)
    
    array.sort()
    low_array = array[one_percent:]
    
    return numpy.mean(low_array)   

with open('blit.pickle','rb') as file:
    blit_data = pickle.load(file)

with open('blits.pickle','rb') as file:
    blits_data = pickle.load(file)
    
    
blit_data = numpy.array(list(filter(lambda x: x != 0, blit_data)))
blits_data = numpy.array(list(filter(lambda x: x != 0, blits_data)))

print("*BLIT RESULTS*")
print("Average: %.3f" % numpy.mean(blit_data))
print("1 percent Low: %.3f" % getOnePercentLow(blit_data))


print("*BLITS RESULTS*")
print("Average: %.3f" % numpy.mean(blits_data))
print("1 percent Low: %.3f" % getOnePercentLow(blits_data))

input()


  