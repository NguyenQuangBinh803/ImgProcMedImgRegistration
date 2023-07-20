'''
Author: Edward J. C. Ashenbert
Date: 2023.07.11 (Tue)

Specifications: 
Design a image manipulation system that allows user/medical staff to load & operate & modify with DICOM images. 
We'll focus on CT and DR modality in the first place.
Also, the system is responsible for performing registration task, which means that we're gonna need to load 2 images.

Function 1: Load DR Images
    Get all avalable tags in the image and assign them to accessible dictionary. Cause, we're gonna need them in the future.
    Why? Cause, these tags can be used for coordinate transformation. In order to identify relationship between taken images and taken position. 
    
    Function 1.1: Read Dicom tags from the designated DR image
    Function 1.2: We extract the intensity data from the dicom image and display normally on bitmap panel on Qt

Function 2: Load CT Images
    Function 2.1: Read Dicom tags from the designated CT images
        This function is ways different from the first one, CT Images contains a series of images which is required to load all at once. 
    Funciton 2.2: We extract the intensity data from the dicom image and display normally on bitmap panel on Qt
        This one is also different, we have to define a way of visualizing the CT Images. Since it's a volumetric data. I'm thinking of a creative way of visualizing it. 
        By making a 3D cubic with texture
    
Function 3: 
    Allow the system to load a second image. In term for 
    
Function 4:
    We apply some basic filtering kernel into the displayed image.
    
'''
