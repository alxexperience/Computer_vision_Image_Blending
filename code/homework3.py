# -*- coding: utf-8 -*-
"""
By: Laura Uribe & Alex Perepechko
Project 3: Image Blending and Pyramids

"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

apple = cv2.imread('apple.jpg')
orange = cv2.imread('orange.jpg')
seattle = cv2.imread('seattle.jpg')
newyork = cv2.imread('newyork.jpg')
ocean1 = cv2.imread('ocean1.jpeg')
ocean2 = cv2.imread('ocean2.jpg')
grass1 = cv2.imread('grass1.jpg')
grass2 = cv2.imread('grass2.jpg')

def GaussianPyr(img1, img2):
# generate Gaussian pyramid for img1 and img2
    Gaus1 = img1.copy()
    gpyr1 = [Gaus1]
    Gaus2 = img2.copy()
    gpyr2 = [Gaus2]
    
    for i in xrange(5):
        Gaus1 = cv2.pyrDown(Gaus1) #decomposes into smaller pyramids
        gpyr1.append(Gaus1) #adds the gaussian pyramid to the list
        Gaus2 = cv2.pyrDown(Gaus2)
        gpyr2.append(Gaus2)
        
   #write images to root directory
    cv2.imwrite('Img1Gausian1.jpg',gpyr1[0])
    cv2.imwrite('Img1Gausian2.jpg',gpyr1[1])
    cv2.imwrite('Img1Gausian3.jpg',gpyr1[2])
    cv2.imwrite('Img1Gausian4.jpg',gpyr1[3])
    cv2.imwrite('Img1Gausian5.jpg',gpyr1[4])

    plt.subplot(151)
    plt.imshow(gpyr1[0],cmap="gray")
    plt.subplot(152)
    plt.imshow(gpyr1[1],cmap="gray")
    plt.subplot(153)
    plt.imshow(gpyr1[2],cmap="gray")
    plt.subplot(154)
    plt.imshow(gpyr1[3],cmap="gray") 
    plt.subplot(155)
    plt.imshow(gpyr1[4],cmap="gray")     
   
    
    cv2.imwrite('Img2Gausian1.jpg',gpyr2[0])
    cv2.imwrite('Img2Gausian2.jpg',gpyr2[1])
    cv2.imwrite('Img2Gausian3.jpg',gpyr2[2])
    cv2.imwrite('Img2Gausian4.jpg',gpyr2[3])
    cv2.imwrite('Img2Gausian5.jpg',gpyr2[4])
    
    plt.subplot(151)
    plt.imshow(gpyr2[0],cmap="gray")
    plt.subplot(152)
    plt.imshow(gpyr2[1],cmap="gray")
    plt.subplot(153)
    plt.imshow(gpyr2[2],cmap="gray")
    plt.subplot(154)
    plt.imshow(gpyr2[3],cmap="gray") 
    plt.subplot(155)
    plt.imshow(gpyr2[4],cmap="gray") 

    plt.show()
    return gpyr1, gpyr2;
    
#GPyr,GPyr2 = GaussianPyr(seattle,newyork);
GPyr,GPyr2 = GaussianPyr(grass1,grass2); #change name of images here to get different results saved to disk

def LaplacianPyr(Gaussian1, Gaussian2):
# generate Laplacian Pyramid for both images
    lpyr = [Gaussian1[4]]
    lpyr2 = [Gaussian2[4]]

    #range is one less than the Gaussian pyramid
    for i in xrange(4,0,-1):
        GausImg = cv2.pyrUp(Gaussian1[i]) #build the pyramid up
        Lap = cv2.subtract(Gaussian1[i-1],GausImg) #subtract the Gaussian of the previous image with the Gaussian of the current image
        lpyr.append(Lap)
        
        GausImg2 = cv2.pyrUp(Gaussian2[i])
        Lap2 = cv2.subtract(Gaussian2[i-1],GausImg2)
        lpyr2.append(Lap2)
    
    plt.subplot(151)
    plt.imshow(lpyr2[0],cmap="gray")
    plt.subplot(152)
    plt.imshow(lpyr2[1],cmap="gray")
    plt.subplot(153)
    plt.imshow(lpyr2[2],cmap="gray")
    plt.subplot(154)
    plt.imshow(lpyr2[3],cmap="gray") 
    plt.subplot(155)
    plt.imshow(lpyr2[4],cmap="gray") 
    plt.show()
    
    cv2.imwrite('Img1Lap1.jpg',lpyr[1])
    cv2.imwrite('Img1Lap2.jpg',lpyr[2])
    cv2.imwrite('Img1Lap3.jpg',lpyr[3])
    cv2.imwrite('Img1Lap4.jpg',lpyr[4])
    
    cv2.imwrite('Img2Lap1.jpg',lpyr2[1])
    cv2.imwrite('Img2Lap2.jpg',lpyr2[2])
    cv2.imwrite('Img2Lap3.jpg',lpyr2[3])
    cv2.imwrite('Img2Lap4.jpg',lpyr2[4])

    return lpyr,lpyr2

lpyramid1, lpyramid2 = LaplacianPyr(GPyr,GPyr2)

def ImgConstruct(laplac1, laplac2):
# Combine the left and right halves of each image for every pyramid level
    combine = []
    #zip iterates over the two different pyramid tuples simultaneously
    for l1,l2 in zip(lpyramid1,lpyramid2):
        rows,column,color = l1.shape # preserves shape of original image
        combined_img = np.hstack((l1[:,0:column/2], l2[:,column/2:])) #cuts images in half
        combine.append(combined_img)
        cv2.imwrite('RebuiltLaplacian.jpg',combined_img)#reconstructed laplacian image

    # reconstruct the image from the pyramids, blending them together
    final_image = combine[0] #start at the first pyramid in list
    for i in xrange(1,5):
        final_image = cv2.pyrUp(final_image) #climb up in the pyramid
        final_image = cv2.add(final_image, combine[i]) #add up the pyramids to reconstruct image

    #combine the image by cutting the first and second image in half, and then
    #combining the two sides
    #hstack = horizontal stack, turns array/list into stack ina  horizontal sequence column wise
    testcombine = np.hstack((apple[:,:column/2],orange[:,column/2:]))
    return final_image, testcombine
    
    
resulting_image, test = ImgConstruct(lpyramid1, lpyramid2)

cv2.imwrite('Pyramid_blending.jpg',resulting_image)
cv2.imwrite('Directly_blending_img.jpg',test)