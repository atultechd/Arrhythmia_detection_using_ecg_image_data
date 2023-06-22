from skimage.io import imread
from skimage import color
import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu,gaussian
from skimage.transform import resize
from numpy import asarray
from skimage.metrics import structural_similarity
from skimage import measure
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
import joblib
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
import os
from natsort import natsorted
from sklearn import linear_model, tree, ensemble
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
import streamlit as st
# import urllib.parse

class ECG:
	def  getImage(self,image):
		"""
		this functions gets user image
		return: user image
		"""
		image=imread(image)
		return image

	def GrayImgae(self,image):
		"""
		This funciton converts the user image to Gray Scale
		return: Gray scale Image
		"""
		image_gray = color.rgb2gray(image)
		image_gray=resize(image_gray,(1572,2213))
		return image_gray

	def DividingLeads(self,image):
		"""
		This Funciton Divides the Ecg image into 13 Leads including long lead. Bipolar limb leads(Leads1,2,3). Augmented unipolar limb leads(aVR,aVF,aVL). Unipolar (+) chest leads(V1,V2,V3,V4,V5,V6)
  		return : List containing all 13 leads divided
		"""
		Lead_1 = image[300:600, 150:643] # Lead 1
		Lead_2 = image[300:600, 646:1135] # Lead aVR
		Lead_3 = image[300:600, 1140:1625] # Lead V1
		Lead_4 = image[300:600, 1630:2125] # Lead V4
		Lead_5 = image[600:900, 150:643] #Lead 2
		Lead_6 = image[600:900, 646:1135] # Lead aVL
		Lead_7 = image[600:900, 1140:1625] # Lead V2
		Lead_8 = image[600:900, 1630:2125] #Lead V5
		Lead_9 = image[900:1200, 150:643] # Lead 3
		Lead_10 = image[900:1200, 646:1135] # Lead aVF
		Lead_11 = image[900:1200, 1140:1625] # Lead V3
		Lead_12 = image[900:1200, 1630:2125] # Lead V6
		Lead_13 = image[1250:1480, 150:2125] # Long Lead

		#All Leads in a list
		Leads=[Lead_1,Lead_2,Lead_3,Lead_4,Lead_5,Lead_6,Lead_7,Lead_8,Lead_9,Lead_10,Lead_11,Lead_12,Lead_13]
		fig , ax = plt.subplots(4,3)
		fig.set_size_inches(10, 10)
		x_counter=0
		y_counter=0

		#Create 12 Lead plot using Matplotlib subplot

		for x,y in enumerate(Leads[:len(Leads)-1]):
			if (x+1)%3==0:
				ax[x_counter][y_counter].imshow(y)
				ax[x_counter][y_counter].axis('off')
				ax[x_counter][y_counter].set_title("Leads {}".format(x+1))
				x_counter+=1
				y_counter=0
			else:
				ax[x_counter][y_counter].imshow(y)
				ax[x_counter][y_counter].axis('off')
				ax[x_counter][y_counter].set_title("Leads {}".format(x+1))
				y_counter+=1
	    
		#save the image
		fig.savefig('Leads_1-12_figure.png')
		fig1 , ax1 = plt.subplots()
		fig1.set_size_inches(10, 10)
		ax1.imshow(Lead_13)
		ax1.set_title("Leads 13")
		ax1.axis('off')
		fig1.savefig('Long_Lead_13_figure.png')

		return Leads

	def PreprocessingLeads(self,Leads):
		"""
		This Function Performs preprocessing to on the extracted leads.
		"""
		fig2 , ax2 = plt.subplots(4,3)
		fig2.set_size_inches(10, 10)
		#setting counter for plotting based on value
		x_counter=0
		y_counter=0

		for x,y in enumerate(Leads[:len(Leads)-1]):
			#converting to gray scale
			grayscale = color.rgb2gray(y)
			#smoothing image
			blurred_image = gaussian(grayscale, sigma=1)
			#thresholding to distinguish foreground and background
			#using otsu thresholding for getting threshold value
			global_thresh = threshold_otsu(blurred_image)

			#creating binary image based on threshold
			binary_global = blurred_image < global_thresh
			#resize image
			binary_global = resize(binary_global, (300, 450))
			if (x+1)%3==0:
				ax2[x_counter][y_counter].imshow(binary_global,cmap="gray")
				ax2[x_counter][y_counter].axis('off')
				ax2[x_counter][y_counter].set_title("pre-processed Leads {} image".format(x+1))
				x_counter+=1
				y_counter=0
			else:
				ax2[x_counter][y_counter].imshow(binary_global,cmap="gray")
				ax2[x_counter][y_counter].axis('off')
				ax2[x_counter][y_counter].set_title("pre-processed Leads {} image".format(x+1))
				y_counter+=1
		fig2.savefig('Preprossed_Leads_1-12_figure.png')

		#plotting lead 13
		fig3 , ax3 = plt.subplots()
		fig3.set_size_inches(10, 10)
		#converting to gray scale
		grayscale = color.rgb2gray(Leads[-1])
		#smoothing image
		blurred_image = gaussian(grayscale, sigma=1)
		#thresholding to distinguish foreground and background
		#using otsu thresholding for getting threshold value
		global_thresh = threshold_otsu(blurred_image)
		print(global_thresh)
		#creating binary image based on threshold
		binary_global = blurred_image < global_thresh
		ax3.imshow(binary_global,cmap='gray')
		ax3.set_title("Leads 13")
		ax3.axis('off')
		fig3.savefig('Preprossed_Leads_13_figure.png')


	def SignalExtraction_Scaling(self,Leads):
		"""
		This Function Performs Signal Extraction using various steps,techniques: conver to grayscale, apply gaussian filter, thresholding, perform contouring to extract signal image and then save the image as 1D signal
		"""
		fig4 , ax4 = plt.subplots(4,3)
		#fig4.set_size_inches(10, 10)
		x_counter=0
		y_counter=0
		for x,y in enumerate(Leads[:len(Leads)-1]):
			#converting to gray scale
			grayscale = color.rgb2gray(y)
			#smoothing image
			blurred_image = gaussian(grayscale, sigma=0.7)
			#thresholding to distinguish foreground and background
			#using otsu thresholding for getting threshold value
			global_thresh = threshold_otsu(blurred_image)

			#creating binary image based on threshold
			binary_global = blurred_image < global_thresh
			#resize image
			binary_global = resize(binary_global, (300, 450))
			#finding contours
			contours = measure.find_contours(binary_global,0.8)
			contours_shape = sorted([x.shape for x in contours])[::-1][0:1]
			for contour in contours:
				if contour.shape in contours_shape:
					test = resize(contour, (255, 2))
			if (x+1)%3==0:
				ax4[x_counter][y_counter].invert_yaxis()
				ax4[x_counter][y_counter].plot(test[:, 1], test[:, 0],linewidth=1,color='black')
				ax4[x_counter][y_counter].axis('image')
				ax4[x_counter][y_counter].set_title("Contour {} image".format(x+1))
				x_counter+=1
				y_counter=0
			else:
				ax4[x_counter][y_counter].invert_yaxis()
				ax4[x_counter][y_counter].plot(test[:, 1], test[:, 0],linewidth=1,color='black')
				ax4[x_counter][y_counter].axis('image')
				ax4[x_counter][y_counter].set_title("Contour {} image".format(x+1))
				y_counter+=1
	    
			#scaling the data and testing
			lead_no=x
			scaler = MinMaxScaler()
			fit_transform_data = scaler.fit_transform(test)
			Normalized_Scaled=pd.DataFrame(fit_transform_data[:,0], columns = ['X'])
			Normalized_Scaled=Normalized_Scaled.T
			#scaled_data to CSV
			if (os.path.isfile('scaled_data_1D_{lead_no}.csv'.format(lead_no=lead_no+1))):
				Normalized_Scaled.to_csv('Scaled_1DLead_{lead_no}.csv'.format(lead_no=lead_no+1), mode='a',index=False)
			else:
				Normalized_Scaled.to_csv('Scaled_1DLead_{lead_no}.csv'.format(lead_no=lead_no+1),index=False)
	      
		fig4.savefig('Contour_Leads_1-12_figure.png')


	def CombineConvert1Dsignal(self):
		"""
		This function combines all 1D signals of 12 Leads into one FIle csv for model input.
		returns the final dataframe
		"""
		#first read the Lead1 1D signal
		test_final=pd.read_csv('Scaled_1DLead_1.csv')
		location= os.getcwd()
		print(location)
		#loop over all the 11 remaining leads and combine as one dataset using pandas concat
		for files in natsorted(os.listdir(location)):
			if files.endswith(".csv"):
				if files!='Scaled_1DLead_1.csv':
					df=pd.read_csv('{}'.format(files))
					test_final=pd.concat([test_final,df],axis=1,ignore_index=True)

		return test_final
		
	def DimensionalReduciton(self,test_final):
		"""
		This function reduces the dimensinality of the 1D signal using PCA
		returns the final dataframe
		"""
		#first load the trained pca
		pca_loaded_model = joblib.load('PCA_ECG (1).pkl')
		result = pca_loaded_model.transform(test_final)
		final_df = pd.DataFrame(result)
		return final_df

	# def ModelLoad_predict(self,final_df):
	# 	"""
	# 	This Function Loads the pretrained model and perfrom ECG classification
	# 	return the classification Type.
	# 	"""
	# 	loaded_model = joblib.load('Heart_Disease_Prediction_using_ECG (4).pkl')
	# 	result = loaded_model.predict(final_df)
	# 	if result[0] == 1:
	# 		return st.markdown("[You ECG corresponds to Myocardial Infarction](server.py)")
	# 	elif result[0] == 0:
	# 		return st.markdown("[You ECG corresponds to Abnormal Heartbeat](server.py)")
	# 	elif result[0] == 2:
	# 		return st.markdown("[Your ECG is Normal](server.py)")
	# 	else:
	# 		return st.markdown("[You ECG corresponds to History of Myocardial Infarction](server.py)")

	def ModelLoad_predict(self, final_df):
		"""
		This Function Loads the pretrained model and performs ECG classification
		Return the classification type along with information about Myocardial Infarction.
		"""
		loaded_model = joblib.load('Heart_Disease_Prediction_using_ECG (4).pkl')
		result = loaded_model.predict(final_df)

		if result[0] == 1:
			return "Your ECG corresponds to Myocardial Infarction. \n\nMyocardial infarction, commonly known as a heart attack, happens when the blood flow to a part of the heart muscle is blocked. This blockage is usually caused by a clot that forms in one of the blood vessels supplying the heart. When the blood flow is blocked, the affected part of the heart muscle doesn't receive enough oxygen and nutrients. This lack of oxygen can cause damage or death to the heart tissue.\n\nThe most common reason for a heart attack is a condition called coronary artery disease (CAD). CAD occurs when fatty deposits, called plaque, build up in the arteries that supply blood to the heart. Over time, the plaque can rupture and form a blood clot that blocks the artery, leading to a heart attack.\n\nTo cure a heart attack, immediate medical attention is essential. When someone experiences a heart attack, they should call emergency services right away. Medical professionals will administer the following treatments:\n\n1. Medications: They may give medications to dissolve the blood clot or prevent further clotting. These medications help restore blood flow to the heart.\n2. Angioplasty and stenting: A procedure called percutaneous coronary intervention (PCI) may be performed. It involves inserting a thin tube with a balloon into the blocked artery. The balloon is then inflated to widen the artery, and a small metal mesh tube called a stent may be placed to keep the artery open.\n3. Bypass surgery: In more severe cases, coronary artery bypass graft (CABG) surgery may be necessary. During this surgery, a new blood vessel is used to create a detour around the blocked artery, restoring blood flow to the heart.\n\nIt's important to note that recovering from a heart attack involves ongoing care and lifestyle changes. This may include taking medications as prescribed, making dietary modifications, engaging in regular exercise, quitting smoking, and managing other health conditions like high blood pressure or diabetes."
		elif result[0] == 0:
			return "Your ECG corresponds to Abnormal Heartbeat. \n\nAbnormal heartbeat refers to any irregularity or unusual pattern in your heart's rhythm. Normally, your heart beats in a steady, regular rhythm to efficiently pump blood throughout your body. However, sometimes the heart may beat too fast, too slow, or in an irregular pattern.\n\nThere are several reasons why you might experience an abnormal heartbeat. Some common causes include:\n\n- Stress and anxiety\n- Physical exertion\n- Medications and substances\n- Underlying medical conditions\n\nResolving an abnormal heartbeat depends on the underlying cause. Here are a few steps you can take:\n\n- Relaxation techniques: If stress or anxiety triggers your irregular heartbeat, practicing relaxation techniques like deep breathing, meditation, or yoga can help restore normal rhythm.\n- Lifestyle changes: Avoiding excessive consumption of caffeine, alcohol, and nicotine can reduce the likelihood of irregular heartbeats. Regular exercise and maintaining a healthy diet also contribute to overall heart health.\n- Medication adjustments: If you're taking medications that may be causing your abnormal heartbeat, consult with your doctor. They may adjust your dosage or switch you to alternative medications.\n- Medical intervention: If your irregular heartbeat is persistent or accompanied by other concerning symptoms like chest pain, dizziness, or shortness of breath, it's important to seek medical attention. A healthcare professional can diagnose the underlying cause and recommend appropriate treatment, such as medications or procedures like cardioversion or ablation, to restore normal heart rhythm.\n\nRemember, it's essential to consult a healthcare professional for an accurate diagnosis and appropriate guidance regarding your specific situation. They can provide personalized advice and interventions to help resolve your abnormal heartbeat."

		elif result[0] == 2:
			return "Your ECG is Normal. \n\nA normal ECG reading indicates that your heart is functioning within the normal range. However, it is always recommended to consult with a healthcare professional for a comprehensive evaluation of your cardiac health."
		else:
			return "Your ECG corresponds to a History of Myocardial Infarction. \n\nHistory of Myocardial Infarction, commonly known as a heart attack, happens when the blood flow to a part of the heart muscle is blocked. This blockage is usually caused by a clot that forms in one of the blood vessels supplying the heart. When the blood flow is blocked, the affected part of the heart muscle doesn't receive enough oxygen and nutrients. This lack of oxygen can cause damage or death to the heart tissue.\n\nThe most common reason for a heart attack is a condition called coronary artery disease (CAD). CAD occurs when fatty deposits, called plaque, build up in the arteries that supply blood to the heart. Over time, the plaque can rupture and form a blood clot that blocks the artery, leading to a heart attack.\n\nTo cure a heart attack, immediate medical attention is essential. When someone experiences a heart attack, they should call emergency services right away. Medical professionals will administer treatments such as:\n\n- Medications: They may give medications to dissolve the blood clot or prevent further clotting. These medications help restore blood flow to the heart.\n- Angioplasty and stenting: A procedure called percutaneous coronary intervention (PCI) may be performed. It involves inserting a thin tube with a balloon into the blocked artery. The balloon is then inflated to widen the artery, and a small metal mesh tube called a stent may be placed to keep the artery open.\n- Bypass surgery: In more severe cases, coronary artery bypass graft (CABG) surgery may be necessary. During this surgery, a new blood vessel is used to create a detour around the blocked artery, restoring blood flow to the heart.\n\nIt's important to note that recovering from a heart attack involves ongoing care and lifestyle changes. This may include taking medications as prescribed, making dietary modifications, engaging in regular exercise, quitting smoking, and managing other health conditions like high blood pressure or diabetes.\n\nPrevention is also crucial. Making healthy lifestyle choices, such as eating a balanced diet, maintaining a healthy weight, exercising regularly, managing stress, and avoiding smoking, can significantly reduce the risk of a heart attack.\n\nRemember, if you suspect a heart attack, call for emergency help immediately. Time is of the essence, and prompt medical intervention can save lives and minimize damage to the heart."