#!/usr/bin/env python3

import time
import random
import pickle
from os.path import isfile
from sys import exc_info

class Call:
	
	def __init__(self):
		self.__description = ""
		self.__start_time = ""
		self.__end_time = ""
	
	def setDescription(self, description):
		self.__description = description
	
	
	def setStartTime(self, stime):
		self.__start_time = Call.__defineTime(stime)
	
	def setEndTime(self, etime):
		self.__end_time = Call.__defineTime(etime)
		
	
	def getDescription(self):
		return self.__description
	
	def getStartTime(self):
		return time.strftime("%H:%M", self.__start_time)
	
	def getEndTime(self):
		return time.strftime("%H:%M", self.__end_time)
	
	@staticmethod
	def __defineTime(ltime):
		return time.strptime(ltime, "%H:%M")

class CallWithCaseNumber(Call):
	
	def __init__(self):
		self.__case_number = 0
		super().__init__()
	
	def setCaseNumber(self, number):
		self.__case_number = number
	
	def setRandomCaseNumber(self, start_number, end_number):
		random.seed()
		self.__case_number = random.randint(start_number, end_number)
	
	def getCaseNumber(self):
		return self.__case_number

class CallContainer:
	
	__callqueue = []
	
	@classmethod
	def addCall(cls, call):
		cls.__callqueue.append(call)
	
	@classmethod
	def removeCall(cls, call):
		cls.__callqueue.remove(call)
	
	@classmethod
	def getCallQueue(cls):
		return cls.__callqueue
	
	@classmethod
	def sortCallQueue(cls):
		cls.__callqueue = sorted(cls.__callqueue, key=lambda call: call.getStartTime())

class CallRandomCreator:
	
	@staticmethod
	def __createRandomStartTime(start_hour, end_hour):
		if start_hour > end_hour:
			end_hour += 24
		random.seed()
		h = random.randint(start_hour, end_hour) % 24
		m = random.randint(0, 59)
		return h, m
	
	@staticmethod
	def __createRandomEndTime(start_hour, start_min, max_duration):
		random.seed()
		duration = random.randint(3, max_duration)
		if start_min + duration > 59:
			return (start_hour + int((start_min + duration) / 60)) % 24 , (start_min + duration) % 60
		else:
			return start_hour, (start_min + duration)
		
	@classmethod
	def createRandomCase(cls, start_hour, end_hour, max_duration = 15):
		c = Call()
		c.setDescription(CaseDescriptionContainer.getRandomDescription())
		shour, smin = cls.__createRandomStartTime(start_hour, end_hour)
		ehour, emin = cls.__createRandomEndTime(shour, smin, max_duration)
		c.setStartTime(str(shour) + ":" + str(smin))
		c.setEndTime(str(ehour) + ":" + str(emin))
		return c
	

class CallStore:
	
	__FileDescriptionContainer = "CaseDescriptions.dat"
	
	@classmethod
	def storeDescriptionContainer(cls):
		f = open(CallStore.__FileDescriptionContainer, "bw")
		p = pickle.Pickler(f, 3)
		p.dump(CaseDescriptionContainer.getDescriptions())
		f.close()
	
	@classmethod	
	def loadDescriptionContainer(cls):
		if isfile(cls.__FileDescriptionContainer):
			f = open(cls.__FileDescriptionContainer, "br")
			u = pickle.Unpickler(f)
			CaseDescriptionContainer.load(u.load())
			f.close()
			return True
		else:
			return False

class CaseDescriptionContainer:

	__descriptions = []
	
	@classmethod	
	def addDescription(cls,d):
		CaseDescriptionContainer.__descriptions.append(d)
	
	@classmethod
	def removeDescription(cls, d):
		if d in CaseDescriptionContainer.__descriptions:
			CaseDescriptionContainer.__descriptions.remove(d)
			return True
		else:
			return False
	
	@classmethod
	def getDescriptions(cls):
		return CaseDescriptionContainer.__descriptions
	
	@classmethod
	def reset(cls):
		CaseDescriptionContainer.__descriptions = []
	
	@classmethod
	def load(cls, container):
		CaseDescriptionContainer.__descriptions = container
	
	@classmethod
	def isEmpty(cls):
		if CaseDescriptionContainer.__descriptions == []:
			return True
		else:
			return False
	
	@classmethod
	def getNumberOfDescriptions(cls):
		return len(cls.__descriptions)
	
	@classmethod
	def getRandomDescription(cls):
		random.seed()
		return cls.__descriptions[random.randrange(0, len(cls.__descriptions))]

class CallTester:
	
	def checkCaseDescriptionContainer(self):
		if CaseDescriptionContainer.isEmpty():
			print("Is Empty")
		else:
			print("Is not Empty")

	def createCase(self, description, starttime, endtime):
		c = Call()
		c.setDescription(description)
		c.setStartTime(starttime)
		c.setEndTime(endtime)
		return c

	def createCaseDescription(self):
		d = input("Bitte Case Beschreibung eingeben: ")
		CaseDescriptionContainer.addDescription(d)

	def createCaseDescriptionsAndStore(self):
		checkCaseDescriptionContainer()
		n = int(input("Wie viele Case Beschreibungen sollen erfasst werden? "))
		for i in range(0, n):
			createCaseDescription()
		checkCaseDescriptionContainer()
		CallStore.storeDescriptionContainer()

	def loadCaseDescriptions(self):
		CallStore.loadDescriptionContainer()


	def createRandomCase(self, starthour, endhour):
		random.seed()
		c = Call.Call()
		c.setDescription(CaseDescriptionContainer.getRandomDescription())
		return c

if __name__ == "__main__":
	cases = CallTester()
	cases.loadCaseDescriptions()
	for i in range(0, 20):
		c = CallRandomCreator.createRandomCase(8, 2, 22)
		#print(c.getStartTime() + "-" + c.getEndTime() + " " + c.getDescription())
		CallContainer.addCall(c)
	CallContainer.sortCallQueue()
	for c in CallContainer.getCallQueue():
		print(c.getStartTime() + "-" + c.getEndTime() + " " + c.getDescription())
	CallStore.loadDescriptionContainer()
	#CaseDescriptionContainer.addDescription("Konfigurationsprobleme")
	#CallStore.storeDescriptionContainer()
	#for c in CaseDescriptionContainer.getDescriptions():
		#print(c)
	
	
