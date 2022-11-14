# summary
 Based on the physics Ⅰ problem, this program created a predictive natural language processing model with a neuron network model using Orange3. I loaded that model into Python and built the GUI using Tkinter. When you input a problem, it predicts the problem unit through the model and randomly recommends the unit problem prepared in advance.

***

# why the project started
 While helping my friend's graduation thesis, I was looking for an easy way to make a model and use it, so I decided to use Orange3. However, there were many difficulties in loading the Orange3 model in Python, so I leave a project record.
 
 Of course, I see "Orange is not really intended to be used as a library. I would suggest using it via GUI or rather using other Python libraries, such as sklearn, on which Orange is based anyway." in [stackoverflow.com](https://stackoverflow.com/a/56579707/16530517)

 Nevertheless, I hope this project will help those who are having the same problem as me.

***

# needed features
 1. Create a model with Orange3.
 2. Load the model.
 3. I use the camera with opencv.
 4. Select Take Photo/Recognize Image/Enter Text.
 5. When taking a picture is selected, the camera turns on and a window to take a picture appears.
 6. After taking a picture, OCR with pytesseract.
 7. When OCR is finished, a window will appear where you can edit the text.
 8. After modification, use the model to derive results.
 9. Based on the derived results, 5 random problems are recommended in the img_data folder. Then go back to step 4.
 10. If image recognition is selected, you can select a file from the folder and try steps 6 to 9.
 11. When text input is selected, a window for writing text appears and repeat steps 8 to 9.

***

# problems and solutions

 ModuleNotFoundError: No module named 'pytesseract'
 
    > pip install pytesseract
    > download exe in https://github.com/UB-Mannheim/tesseract/wiki
    > check Additional language data (download)
***
 ModuleNotFoundError: No module named 'orangecontrib'
    
    > copy GUI_Orange/orangecontrib -> Python3\Lib\site-packages/
***
 ModuleNotFoundError: No module named 'Orange'
    
    > copy GUI_Orange/Orange -> Python3\Lib\site-packages/
***
 ModuleNotFoundError: No module named 'orangecanvas'
    
    > copy GUI_Orange/orangecanvas -> Python3\Lib\site-packages/
***
 ModuleNotFoundError: No module named 'gensim'
    
    > pip install gensim
***
 ModuleNotFoundError: No module named 'simhash'
    
    > copy GUI_Orange/Orange -> Python3\Lib\site-packages/
***
 ModuleNotFoundError: No module named 'cv2'
    
    > pip install opencv-python
***
 ModuleNotFoundError: No module named 'ufal'
    
    > copy GUI_Orange/Orange -> Python3\Lib\site-packages/
***
 ModuleNotFoundError: No module named 'lemmagen3'
    
    > copy GUI_Orange/Orange -> Python3\Lib\site-packages/
***
 UserWarning: Trying to unpickle estimator LabelBinarizer from version 1.0.2 when using version 1.1.3. This might lead to breaking code or invalid results. Use at your own risk. For more info please refer to:
 https://scikit-learn.org/stable/model_persistence.html#security-maintainability-limitations      
   warnings.warn(
    
    > pip install scikit-learn==1.0.2