import os
import errno
import time

FIFO = 'kolejka'

# utworzenie kolejki
try:
    os.mkfifo(FIFO)
except OSError as oe: 
    if oe.errno != errno.EEXIST:
        raise

# kolejka otwarta do odczytu 
fifo_in = os.open(FIFO, os.O_RDONLY)

# kolejka otwarta do zapisu,
# żeby zakończenie klienta jej nie zamykało 
fifo_out1 = os.open(FIFO, os.O_WRONLY|os.O_NDELAY) 

while True:
    r = os.read(fifo_in, 2) # czytanie 2 bajtów
    if len(r)>0:    
      print("Serwer: %s" % r.decode())
    else:       
      print("Klient skończył")
      break
    time.sleep(5) # spowolnienie do testowania
