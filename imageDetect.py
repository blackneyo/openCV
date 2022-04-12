import cv2
import numpy as np
import matplotlib.pyplot as plt


'''
2022.04.08 이동한
edge 감지 / 이미지 그라디언트
subplot(nrows, ncols, index)
'''
image = cv2.imread('nft1.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
hgt, wdt,_ = image.shape

#Sobel Edges
x_sobel = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=5)
y_sobel = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=5)

plt.figure(figsize=(20, 20))
# subplot 각 column에 독립된 subplot 그리기
plt.subplot(3, 2, 1)
plt.title("Original")
plt.imshow(image)
plt.title("Sobel X")
plt.imshow(x_sobel)

plt.subplot(3, 2, 3)
plt.title("Sobel Y")
plt.imshow(y_sobel)
sobel_or = cv2.bitwise_or(x_sobel, y_sobel)
plt.subplot(3, 2, 4)
plt.imshow(sobel_or)

laplacian = cv2.Laplacian(image, cv2.CV_64F)
plt.subplot(3, 2, 5)
plt.title("Laplacian")
plt.imshow(laplacian)
# There are two values: threshold1 and threshold2.
# Those gradients that are greater than threshold2 => considered as an edge
# Those gradients that are below threshold1 => considered not to be an edge.
# Those gradients Values that are in between threshold1 and threshold2 => either classiﬁed as edges or non-edges
# The first threshold gradient
canny = cv2.Canny(image, 50, 120)
plt.subplot(3, 2, 6)
plt.imshow(canny.astype('uint8'))
plt.show()

'''
팽창, 열기, 닫기, 침식
'''

image = cv2.imread('fontstyle.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
plt.figure(figsize=(20, 20))
plt.subplot(3, 2, 1)
plt.title("Original")
plt.imshow(image)

kernel = np.ones((5,5), np.uint8)

erosion = cv2.erode(image, kernel, iterations = 1)
plt.subplot(3, 2, 2)
plt.title("Erosion")
plt.imshow(erosion)

dilation = cv2.dilate(image, kernel, iterations = 1)
plt.subplot(3, 2, 3)
plt.title("Dilation")
plt.imshow(dilation)

opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
plt.subplot(3, 2, 4)
plt.title("Opening")
plt.imshow(opening)

closing = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
plt.subplot(3, 2, 5)
plt.title("Closing")
plt.imshow(closing)
plt.show()

'''
시점 변환
'''

image = cv2.imread('confirm.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
plt.figure(figsize=(20, 20))
plt.subplot(1, 2, 1)
plt.title("Original")
plt.imshow(image)

points_A = np.float32([[320,15], [700,215], [85,610], [530,780]])
points_B = np.float32([[0,0], [420, 0], [0,594], [420,594]])
M = cv2.getPerspectiveTransform(points_A, points_B)
warped = cv2.warpPerspective(image, M, (420,594))
plt.subplot(1, 2, 2)
plt.title("warpPerspective")
plt.imshow(warped)
plt.show()

'''
이미지 피라미드
'''

image = cv2.imread('resume.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
plt.figure(figsize=(20, 20))
plt.subplot(2, 2, 1)
plt.title("Original")
plt.imshow(image)

smaller = cv2.pyrDown(image)
larger =  cv2.pyrUp(smaller)
'''
pyrDown = 단계적 축소, 화질 떨어짐
'''
plt.subplot(2, 2, 2)
plt.title("smaller")
plt.imshow(smaller)
'''
pyrUp = 단계적 확대, 화질 떨어짐
'''
plt.subplot(2, 2, 3)
plt.title("Larger")
plt.imshow(larger)
plt.show()

'''
자르기. 이미지 특정 부분을 가져오는 데 사용
'''
image = cv2.imread('confirm.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
plt.figure(figsize=(10, 10))
plt.subplot(2, 2, 1)
plt.title("Original")
plt.imshow(image)
hgt, wdt = image.shape[:2]
start_row, start_col = int(hgt * .25), int(wdt * .25)
end_row, end_col = int(hgt * .78), int(wdt * .75)
cropped = image[start_row:end_row, start_col:end_col]
plt.subplot(2, 2, 2)
plt.imshow(cropped)
plt.show()


'''
Hough Line을 사용한 라인 감지
임계값은 라인으로 간주되기 위한 최소치 
'''
image = cv2.imread('confirm.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
plt.figure(figsize=(10, 10))

# Grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Canny Edges
edges = cv2.Canny(gray, 100, 170, apertureSize = 3) #cv2.Canny(gray타입, minval=100, maxval=170, aperturesize 이미지 그레디언트 크기를 구할때 사용하는 소벨 커널의 크기
plt.subplot(2, 2, 1)
plt.title("edges")
plt.imshow(edges)

# Run HoughLines Fuction
lines = cv2.HoughLines(edges, 1, np.pi/180, 200) #cv2.HoughLines(edge를 사용, 매개변수 분해능 1을 사용, 180도를 180으로 나는 1도, threshold(만나는 점의 기준) = 200)

# Run for loop through each line
for line in lines:
    rho, theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x_1 = int(x0 + 1000 * (-b))
    y_1 = int(y0 + 1000 * (a))
    x_2 = int(x0 - 1000 * (-b))
    y_2 = int(y0 - 1000 * (a))
    cv2.line(image, (x_1, y_1), (x_2, y_2), (255, 0, 0), 2) # cv2.line(이미지, 시작점좌표(x,y), 종료점좌표(x,y), 선색, 선 두깨)
# Show Final output
plt.subplot(2, 2, 2)
plt.imshow(image)
plt.show()

'''
코너 찾기
이미지 모서리를 찾기 위해 cornerHarris 함수 사용
'''
image = cv2.imread('confirm.jpg')

# Grayscaling
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
plt.figure(figsize=(10, 10))
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# CornerHarris function want input to be float
gray = np.float32(gray)
h_corners = cv2.cornerHarris(gray, 3, 3, 0.05) #cv2.cornerHarris(gray스케일, 블록사이즈 3, 소벨 도함수 매개변수 = 3, Harris 검출기 자유 매개변수 = 0.05)
kernel = np.ones((7, 7), np.uint8) # 1로 가득찬 7x7 행렬 datatype = uint8 타입
h_corners = cv2.dilate(h_corners, kernel, iterations = 10) #cv2.dilate 이미지 팽창 (h_corners, ㅇ,
image[h_corners > 0.024 * h_corners.max() ] = [256, 128, 128]
plt.subplot(1, 1, 1)

# Final Output
plt.imshow(image)
plt.show()

'''
2022.04.12 이동한
원, 타원 계산
SimpleBlobDetector = BLOB는 이진scale로 연결된 픽셀 그룹
자잘한 객체는 노이즈로 여기고 특정 크기 이상의 객체만 찾아내는 검출기
'''
image = cv2.imread('BlobTest.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
plt.figure(figsize=(10, 10))
detector = cv2.SimpleBlobDetector_create() # BLOB 검출기 생성자

# Detect Blobs
points = detector.detect(image)  #키 포인트 검출
blank = np.zeros((1, 1))
blobs = cv2.drawKeypoints(image, points, blank, (0, 0, 255),
                          cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS) #keypoints를 (0, 0, 255) 빨간색으로 표시
# Detect blobs
keypoints = detector.detect(image)

number_of_blobs = len(keypoints)
text = "Total Blobs: " + str(len(keypoints))
cv2.putText(blobs, text, (20, 550), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 0, 255), 2) #원형 도형 그리기 문자 hershey_simplex는 폰트

plt.subplot(2, 2, 1)
plt.imshow(blobs)
# Filtering Parameters
# Initialize parameter setting using cv2.SimpleBlobDetector
params = cv2.SimpleBlobDetector_Params()

# Area filtering parameters 지역별 필터링
params.filterByArea =True
params.minCircularity = 0.9

# Convexity filtering parameters 볼록성 필터링
params.filterByConvexity = False
params.minInertiaRatio = 0.01

# detector with the parameters
detector = cv2.SimpleBlobDetector_create(params)


# Draw blobs on our image as red circles
blank = np.zeros((1, 1))
blobs = cv2.drawKeypoints(image, keypoints, blank, (0, 255, 0),
                          cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
number_of_blobs = len(keypoints)
text = "No. Circular Blobs: " + str(len(keypoints))
cv2.putText(blobs, text, (20, 550), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 255), 2)

# Show blobs
plt.subplot(2, 2, 2)
plt.title("Filtering Circular BLobs Only")
plt.imshow(blobs)
plt.show()