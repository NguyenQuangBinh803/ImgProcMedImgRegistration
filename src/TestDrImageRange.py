import pydicom
import numpy as np
import cv2



if __name__ == '__main__':
    # file = pydicom.dcmread("../rsrc/images/RTIMAGE_201803241603531692910.dcm.xml.raw.dcm", force=True)
    file = pydicom.dcmread("../rsrc/images/TestData-DrDataHeadMayo/RTIMAGE.1.2.392.200036.9122.100.30.310.300.7.4.202211141411450370001.dcm", force=True)
    file.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
    print()
    print(f"SOP Class........: {file.SOPClassUID} ({file.SOPClassUID.name})")
    print()

    pat_name = file.PatientName
    print(f"Patient's Name...: {pat_name.family_comma_given()}")
    print(f"Patient ID.......: {file.PatientID}")
    print(f"Modality.........: {file.Modality}")
    print(f"Study Date.......: {file.StudyDate}")
    print(f"Image size.......: {file.Rows} x {file.Columns}")
    # print(f"Pixel Spacing....: {file.PixelSpacing}")
    print(f"Bits Allocated...: {file.BitsAllocated}")
    print(f"Bits Stored......: {file.BitsStored}")
    
    original_image = (file.pixel_array * 2**(file.BitsAllocated - file.BitsStored))
    print(np.max(original_image), np.min(original_image))

    cv2.imshow("image", original_image)
    cv2.waitKey(0)
