from collections import deque
from time import time

"""Provides a convinient way to return expiration masks only after a certain amount of time.
   LEDs should stay on for a fixed time once being turned on, so this allows us to turn 
   them off (make them go extinct) after certain amount of time."""

ALL_BITS_ON = 0xFFFFFFFFFFFFFFFF 

class ExpirationQueue:
    def __init__(self):
        self.time_deque = deque()
        self.ext_deque = deque()

    def pop(self):
        try:
            popped = self.time_deque.pop()#we save this elem in case we need to push it again
            
            if popped < time():#time to pop from ext_queue has passed
                return self.ext_deque.pop()

            self.time_deque.append(popped)#if its not ready, push the time we popped back to top of deque
            #we are anding this value with the current state, so 
            #if we don't want the state to change, use all ones
            return ALL_BITS_ON
        except IndexError:
            return ALL_BITS_ON

    def push(self, expiration_mask, time):
        self.ext_deque.appendleft(expiration_mask)
        self.time_deque.appendleft(time)
