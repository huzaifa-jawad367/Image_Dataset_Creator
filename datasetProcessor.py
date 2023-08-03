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
    
    def __init__(self, files,parent, Name_of_dataset, augment=[False, False], size=224):
        """constructor for dataset processor class"""
        self.mainEngine(files, Name_of_dataset, augment, size)
        parent.notify("Processing Complete!", 1)
        
        
    def mainEngine(self, files, Name_of_dataset, augment = [False, False], size=224):
        """Main Engine"""

        # Create a datasets folder
        if not os.path.exists("Generated_datasets"):
            os.mkdir("Generated_datasets")

        # Create a dataset folder
        if not os.path.exists(f"Generated_datasets/{Name_of_dataset}"):
            os.mkdir(f"Generated_datasets/{Name_of_dataset}")
        else:
            count = 1
            # If dataset already exists, add a number to the end of the name
            while os.path.exists(f"Generated_datasets/{Name_of_dataset}"):
                Name_of_dataset = Name_of_dataset + str(count)
                count += 1
            os.mkdir(f"Generated_datasets/{Name_of_dataset}")

        # Your Code Here
        convert_to_dataset(files, Name_of_dataset, augment, size)
        
        pass

