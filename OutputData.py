import matplotlib.pyplot as plt
import numpy as np

class OutData ():

	def __init__ (self, xvar):
		self.xvar = xvar

	def barGraph (self, xvar, yvar):
		y_pos = np.arange(len(xvar))
		plt.bar(y_pos, yvar, align='center', alpha=0.5)
		plt.xticks(y_pos, xvar, rotation='45')
		return plt.show()
