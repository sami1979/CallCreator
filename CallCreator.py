#!/usr/bin/env python3

__author__ = "Nadim Khoury"
__version__ = "0.2.3"

import time
import random
import pickle
from os.path import isfile
from sys import exc_info

class Case:
	
	def __init__(self):
		self.__description = ""
		self.__start_time = ""
		self.__end_time = ""
	
	def setDescription(self, description):
		self.__description = description
	
	
	def setStartTime(self, stime):
		self.__start_time = Case.__defineTime(stime)
	
	def setEndTime(self, etime):
		self.__end_time = Case.__defineTime(etime)
		
	
	def getDescription(self):
		return self.__description
	
	def getStartTime(self):
		return time.strftime("%H:%M", self.__start_time)
	
	def getEndTime(self):
		return time.strftime("%H:%M", self.__end_time)
	
	@staticmethod
	def __defineTime(ltime):
		return time.strptime(ltime, "%H:%M")

class CaseWithCaseNumber(Case):
	
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

class CaseContainer:
	
	__casequeue = []
	
	@classmethod
	def addCase(cls, case):
		cls.__casequeue.append(case)
	
	@classmethod
	def removeCase(cls, case):
		cls.__casequeue.remove(case)
	
	@classmethod
	def getCaseQueue(cls):
		return cls.__casequeue
	
	@classmethod
	def emptyCaseQueue(cls):
		cls.__casequeue = []
	
	@classmethod
	def sortCaseQueue(cls):
		cls.__casequeue = sorted(cls.__casequeue, key=lambda case: case.getStartTime())

class CaseRandomCreator:
	
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
		c = Case()
		c.setDescription(CaseDescriptionContainer.getRandomDescription())
		shour, smin = cls.__createRandomStartTime(start_hour, end_hour)
		ehour, emin = cls.__createRandomEndTime(shour, smin, max_duration)
		c.setStartTime(str(shour) + ":" + str(smin))
		c.setEndTime(str(ehour) + ":" + str(emin))
		return c
	

class CaseStore:
	
	__FileDescriptionContainer = "CaseDescriptions.dat"
	
	@classmethod
	def storeDescriptionContainer(cls):
		f = open(CaseStore.__FileDescriptionContainer, "bw")
		p = pickle.Pickler(f, 3)
		p.dump(CaseDescriptionContainer.getDescriptions())
		f.close()
	
	@classmethod	
	def loadDescriptionContainer(cls):
		if isfile(cls.__FileDescriptionContainer):
			f = open(cls.__FileDescriptionContainer, "br")
			CaseDescriptionContainer.load(pickle.Unpickler(f).load())
			f.close()
		else:
			cls.storeDescriptionContainer()

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


class CaseManager:
	
	__session = None
	
	def __init__(self):
		try:
			self.loadCaseDescriptions()
		except OSError:
			raise
	
	def checkCaseDescriptionContainer(self):
		if CaseDescriptionContainer.isEmpty():
			print("Is Empty")
		else:
			print("Is not Empty")

	def createCase(self, description, starttime, endtime):
		c = Case()
		c.setDescription(description)
		c.setStartTime(starttime)
		c.setEndTime(endtime)
		return c

	def createCaseDescription(self, description):
		CaseDescriptionContainer.addDescription(description)
		CaseStore.storeDescriptionContainer()

	def loadCaseDescriptions(self):
		try:
			CaseStore.loadDescriptionContainer()
		except OSError:
			raise


	def createRandomCase(self, starthour, endhour, intervall):
		CaseContainer.addCase(CaseRandomCreator.createRandomCase(starthour, endhour, intervall))
	
	@classmethod
	def getCaseManagerObject(cls):
		if cls.__session is None:
			cls.__session = CaseManager()
		return cls.__session
	
	def getAllCaseDescriptions(self):
		CaseStore.loadDescriptionContainer
		return CaseDescriptionContainer.getDescriptions()
	
	def checkIfCaseDescriptionExists(self, case_description):
		if case_description in CaseDescriptionContainer.getDescriptions():
			return True
		else:
			return False
	
	def removeCaseDescription(self, case_description):
		CaseDescriptionContainer.removeDescription(case_description)
		CaseStore.storeDescriptionContainer()
	
	def getAllCases(self):
		return CaseContainer.getCaseQueue()
	
	def sortAllCases(self):
		CaseContainer.sortCaseQueue()
		
	def deleteCaseQueue(self):
		CaseContainer.emptyCaseQueue()


if __name__ == "__main__":
	try:
		cases = CaseManager.getCaseManagerObject()
	except OSError as e:
		print(e)
		print("Programmabbruch")
		exit(1)
	if input("Sollen Werte festgelegt werden (j/n)").upper() == "J":
		begin = int(input("Bitte die Anfangsstunde eingeben, ab der Calls erstellt werden sollen: "))
		end = int(input("Bitte die Stunde angeben bis welcher Calls erstellt werden sollen: "))
		intervall = int(input("Bitte das max Intervall von Calls eingeben: "))
	else:
		begin = 8
		end = 23
		intervall = 15
	for i in range(0, 20):
		c = CaseRandomCreator.createRandomCase(begin, end, intervall)
		#print(c.getStartTime() + "-" + c.getEndTime() + " " + c.getDescription())
		CaseContainer.addCase(c)
	CaseContainer.sortCaseQueue()
	for c in CaseContainer.getCaseQueue():
		print(c.getStartTime() + "-" + c.getEndTime() + " " + c.getDescription())

	
	
