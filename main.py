
import time

class Thread:
  def __init__(self):
    self.index = len(THREADS)
    self.time = 0
    self.requestSent = False
    self.sentRequests = []
    self.defferedReplies = []

    THREADS.append(self)
  
  def start(self):
    self.sendRequests()
    self.sendDefferedReplies()
  
  def sendRequests(self):
    self.requestSent = True

    for thread in THREADS:
      if (thread.index == self.index):
        continue

      self.sentRequests.append(thread)

    for thread in THREADS:
      if (thread.index == self.index):
        continue

      self.request(thread)

  def sendDefferedReplies(self):
    for thread in self.defferedReplies:
      self.reply(thread)

    self.requestSent = False

  def tryDoStuff(self):
    if (len(self.sentRequests) == 0):
      self.doStuff()

  def doStuff(self):
    self.tick()
    print("Thread {} doing stuff".format(self.index))
    time.sleep(1)
  
  def request(self, thread):
    self.tick()
    print("Thread {} received request from {} with time {}".format(thread.index, self.index, self.time))
    thread.syncTime(self)
    thread.tick()

    if (not thread.requestSent):
      thread.reply(self)
    else:
      if (thread.time > self.time or (thread.time == self.time and thread.index < self.index)):
        thread.reply(self)
      else:
        thread.defferedReplies.append(self)

  def reply(self, thread):
    self.tick()
    print("Thread {} replied to {}".format(self.index, thread.index))
    thread.syncTime(self)

    if (thread in self.defferedReplies):
      self.defferedReplies.remove(thread)
    
    if (self in thread.sentRequests):
      thread.sentRequests.remove(self)
    
    thread.tryDoStuff()
  
  def tick(self):
    self.time += 1
    print("Thread {}, time:{}".format(self.index, self.time))
  
  def syncTime(self, thread):
    self.time = max(self.time, thread.time)
    print("Thread {} time sync:{}".format(self.index, self.time))

THREADS = []

def main():
  thread1 = Thread()
  thread2 = Thread()
  thread3 = Thread()
  thread1.start()
  thread2.start()
  thread3.start()

if __name__ == '__main__':
  main()
