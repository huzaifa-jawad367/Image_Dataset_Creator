"""
DatasetProcessor module handles the processing of the dataset
Dataset may include the following:
- images (jpg, png, jpeg)
- videos (mp4)
- pdfs (pdf)

Developed By : Huzaifa Jawad
"""

from dataset_creation import *

class DatasetEngine:
    """Main Data processing class"""
    
    def __init__(self, files,parent):
        """constructor for dataset processor class"""
        self.mainEngine(files)
        parent.notify("Processing Complete!", 1)
        
        
    def mainEngine(self, files, Name_of_dataset, augment = [False, False], size=224):
        """Main Engine"""
        
        # Your Code Here
        convert_to_dataset(files, Name_of_dataset, augment, size)
        
        pass

