import cv2

img = cv2.imread('galaxy.jpg',0)

print(img)
print(img.shape)


resized_img = cv2.resize(img, (int(img.shape[1]/2), int(img.shape[0]/2)))
cv2.imshow('test', resized_img)
cv2.imwrite('gray_galaxy2.jpg', resized_img)
cv2.waitKey(4000)
cv2.destroyAllWindows()