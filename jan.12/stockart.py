import json as js
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt

class StockArt():
	"Generating art with data from stock market"

	def __init__(self, configpath, alphakey):
		self.config = js.load(open(configpath))
		self.alphakey = alphakey
		self.outPath = None
		self.outFile = None
		self.w = None
		self.h = None
		self.resolution = None
		self.background = None
		self.colormap = None
		self.ts = TimeSeries(self.alphakey, output_format='pandas')
		self.symbols = []
		self.data = []
		self.metadata = []
		self.volume = None
		StockArt.setConfig(self, self.config)
		print(self)
		StockArt.loadStockData(self.data, self.metadata, self.symbols, self.ts)
		StockArt.scatterArtVol(self.w, self.h, self.resolution, self.background, self.colormap, self.data,
								self.volume, self.outPath, self.outFile)

	def scatterArtVol(w, h, resolution, background, colormap, dataframes, volume, path, filename):
		print("-- extracting art from the data...", end="\r")
		figure = plt.figure(num=None, figsize=(w, h), dpi=resolution, facecolor=background, edgecolor=background)
		for s in range(len(dataframes)):
			plt.scatter(x=dataframes[s].index, y=dataframes[s]['4. close'], s=dataframes[s]['5. volume'] / volume, \
				c=dataframes[s]['4. close']-dataframes[s]['1. open'], cmap=colormap, marker="o")
		ax = plt.gca()
		ax.set_facecolor(background)
		ax.axes.xaxis.set_visible(False)
		ax.axes.yaxis.set_visible(False)
		plt.tight_layout(rect=[0, 0, 1, 1])
		print("-- art is ready!                     ", end="\n")
		StockArt.saveArt(path + filename, figure)

	def loadStockData(data, metadata, symbols, ts):
		print("-- loading data from alphavantage...", end="\r")
		for s in range(len(symbols)):
			d, m = ts.get_daily(symbol=symbols[s])
			data.append(d)
			metadata.append(m)
		print("-- data loaded!                       ", end="\n")

	def setConfig(self, data):
		self.outPath = data["outPath"]
		self.outFile = data["outFile"]
		self.w = data["width"]
		self.h = data["height"]
		self.resolution = data["resolution"]
		self.background = StockArt.getBackground(data)
		self.colormap = data["colormap"]
		self.symbols = data["symbols"].split(",")
		self.volume = data["VolumeDiv"]

	def getBackground(data):
		values = data["background"].split(",")
		color = (float(values[0])/255,float(values[1])/255,float(values[2])/255)
		return color

	def saveArt(file, figure):
		plt.savefig(file + ".png", facecolor=figure.get_facecolor(), bbox_inches='tight', pad_inches=1)
		print("-- the image was saved!", end="\n")

	def __str__(self):
		return "-- stockart --\n" + \
				"-- https://gitlab.com/rodrigovalla/genuary2021\n" + \
				"-- version: 0.50\n" + \
				"-- Some work to be part of #genuary2021"
