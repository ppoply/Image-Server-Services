# ESRI-Image-Server-Services

Program accepts an ArcGIS server to retrieve information related to Image Servers/Services and then processes the data

## Instructions for running the Program

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Clone the Repo

```
https://github.com/ppoply/ESRI-Image-Server-Services.git
```

### Install Dependencies

```
pip3 install requests opencv-python numpy
```

### Run the file

```
python3 prog.py
```

#### Program Information
The main program ([prog.py](prog.py)) consists of two classes namely **`ImageServer`** and **`ImageService`**.

**ImageServer** accepts an ArcGIS server as input and provides methods related to finding/displaying all items of type ImageServer (which may also be present in folders).

**ImageService** accepts an Instance of ImageServer object along with an Image Service name and provides methods related to Describing Image Service information and exporting an image, etc.

There is also a (pseudo) **main** method which provides Instantiation(s) for the class objects along with method calls for the provided features. You can play around with them and test different outputs.
