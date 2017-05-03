import pandas as pd
import numpy as np

class DataM ():

	def __init__ (self, frame):
		self.frame = frame
		
	def createFrame (self, frame, columns):
		return pd.DataFrame(self.frame, columns=columns)
	
	def createFrame2 (self, frame, columns):
		return pd.DataFrame.from_records(self.frame, columns=columns)
	
	def makeIntegerArray (self, frame, column):
		data_to_integer = self.frame[column].astype('int64')
		return np.array(data_to_integer)
	
	def createPercent(self, sum_array, frame, column):
		total = sum_array.sum()
		self.frame['percent'] = (self.frame[column] / total) * 100
		return self.frame
		