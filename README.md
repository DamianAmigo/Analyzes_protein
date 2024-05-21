<div align="center">
<h1 align="center">Project <a href="">Microscopy image analysis tool.</a> </h1>
</div>
<img  width="100%" src="https://www.leica-microsystems.com/fileadmin/_processed_/b/2/csm_Mica-Mouse-embryo_622730d9e7.png">


## Details:

- ⭐ Personal project.
- 📲 Python.
- ✏️ Libraries: CV2, tifffile, os, openpyxl.
- 📗 Analyzes different protein expression surfaces on different biological tissues.
- 🧑‍🏫 Returns the user a data sheet with the different proteins contained in the images.
<br>

## Specific use ...
<table>
<tr>
<td width="50%">
<h3 align="center">Analysis of organoids with makers DAPI, MAP2, SOX2 and DCX.</h3>
<div align="center">
OPERATION: the analysis of the aforementioned, in images with tiff format, will result in an Excel sheet in which the percentage of the surface will be represented (taking the total surface of positives in DAPI as 100%) 
in which a positive can be seen for each marker ( SOX2, MAP3 and DCX). Internally it will work by applying the OTSU system included in the CV2 library. Additionally, a new filter (GAUSSIAN_C) 
can be applied in case the images do not have good quality.
<p>

</p>
  
</div>
                                                                                      
</td> 
<td width="50%">
<h3 align="center">Considerations</h3>
<div align="center">

<p>
The photographs taken should go in the images folder. In this folder, we will have 2 directories, the "WT" directory (control samples) and the "HET" (mutant samples). 
It is recommended to create a directory for each organoid analyzed within these folders. The file naming format <strong> MUST </strong> be as follows:

SOX2 1-3.tiff

<p> Where "SOX2" is the name of the reagent.</p>
<p> Where "1" is the organoid number.</p>
<p> Where "3" is the section of said organoid.</p>
</a>

</p>
</div>
                                                                                      
</td>

      

 
</table>     
<p>For reasons of confidentiality and property of images, I cannot add images as an example.</p>
</div>
<br>
