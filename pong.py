from __future__ import print_function
from pynput.keyboard import Key, Controller
from PIL import ImageGrab
from PIL import Image
from mss import mss
import numpy as np
import cv2
import time
import sys
import math

kb = Controller()

color = (0, 0, 255)
colorTwo = (255, 23, 124)
colorThree = (173, 34, 12)
prevYDim = 0

class storeY:
    def __init__(self, yPos):
        self.yPos = yPos
        print(self.yPos)

yVar = storeY(0)

mon = {'top': 190, 'left': 200, 'width': 595, 'height': 400}

sct = mss()

while True:
	sct_img = sct.grab(mon) # x, y, width, height-
	img_np = np.array(sct_img)
	frame = img_np
	res = frame
	vis = res.copy()
	grayImg = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
	ret, binImg = cv2.threshold(grayImg, 100, 255, cv2.THRESH_BINARY)
	cnts, hierarchy = cv2.findContours(binImg.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	xArr = []
	h, w, c = res.shape
	wM = w / 2
	wUp = wM + 70
	wDown = wM - 20
	wl = w - 50
	mid = h / 2
	hl = h - 50

	cv2.circle(vis, (int(wUp), int(mid)), 10, color, 2)
	cv2.circle(vis, (int(wDown), int(mid)), 10, color, 2)
	cv2.circle(vis, (int(wl), int(mid)), 10, color, 2)
	cv2.circle(vis, (50, int(mid)), 10, color, 2)
	cv2.circle(vis, (int(wM), 50), 10, color, 2)

	numbArr = []
	dimArr = []
	for ct in cnts:
		(x, y, w, h) = cv2.boundingRect(ct)
		xDims = x + (w / 2)
		yDims = y + (h / 2)
		numbArr.append([xDims, yDims])
	#print(numbArr)
	gh = 0
	xD = []
	uD = []
	for c in cnts:
		(x, y, w, h) = cv2.boundingRect(c)
		xDim = x + (w / 2)
		yDim = y + (h / 2)
		if xDim > wl:
			cv2.circle(vis, (int(xDim), int(yDim)), 10, colorThree, 2)
			uD.append(xDim)
			uD.append(yDim)
		if w < 20 and h < 20:
			if xDim < wUp and xDim > wDown:
				gh += 1
			else:
				if xDim > 50 and xDim < wl:
					h = 0
					for u in numbArr:
						if (xDim - 30) < u[0] < (xDim + 30) and (yDim - 30) < u[1] < (yDim + 30) and xDim != u[0] and yDim != u[1]:
							h += 1
					if h == 0:
						cv2.circle(vis, (int(xDim), int(yDim)), 10, color, 2)
						xD.append(xDim)
						xD.append(yDim)
					else:
						cv2.circle(vis, (int(xDim), int(yDim)), 10, colorTwo, 2)


			if len(xD) == 2:
				print(xD)
				print(uD)
				yDim = xD[1]
				if len(uD) == 2:
					pngX = uD[0]
					pngY = uD[1]
					print([pngX, pngY])
					yVar.yPos = pngY
					cv2.circle(vis, (int(pngX), int(pngY)), 10, colorThree, 2)
					diffY = 0
					if yDim > (pngY + 20):
						print("Down")
						kb.release(Key.up)
						kb.press(Key.down)
					elif yDim < (pngY - 20):
						print("Up")
						kb.release(Key.down)
						kb.press(Key.up)
					else:
						print("Middle")
						kb.release(Key.up)
						kb.release(Key.down)
				else:
					print(yVar.yPos)
					if yDim > yVar.yPos:
						print("DownM")
						#kb.release(Key.up)
						#kb.press(Key.down)
					elif yDim < yVar.yPos:
						print("UpM")
						#kb.release(Key.down)
						#kb.press(Key.up)
	cv2.imshow("Thr", vis)
	if cv2.waitKey(25) & 0xFF == ord('q'):
		cv2.destroyAllWindows()
		break