import cv2, time

video = cv2.VideoCapture(0)

a=0
while True:
	a=a+1
	check, frame = video.read()
	# print(check)
	# print(frame)
	# time.sleep(2)
	cv2.imshow('Captured_grame', frame)

	key = cv2.waitKey(6000)

	if key == ord('q'):
		break
print(a)
video.release()
cv2.destroyAllWindows