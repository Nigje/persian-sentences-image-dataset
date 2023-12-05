

## Introduction

The dataset comprises 264 Persian sentences presented in 11 distinct fonts. Each sentence is transformed into an individual image aligned in a single line. Subsequently, these images underwent a combination process with various types of noise to create the final dataset.  The dataset is suitable for training LSTM neural networks in optical character recognition (OCR) tasks.  The LSTM model can effectively learn the sequential patterns within the sentences and fonts. For your reference, please review the Noises directory for a detailed overview of the applied noise types.

Every sample within the dataset is accompanied by a corresponding text file. These text files contain the character and the coordinates of it present in the image. The format within each line of the text file follows a structured pattern: \<Starting pixel index> _\<Ending pixel index> _\<Character>. This format precisely delineates each character's position within the image matrix.

In the following image, red lines are used to denote the beginning and ending pixels of each character.



<p align="center">
  <img  src="Sample Images/Chunked sentence.jpg" alt="MainForm">
</p>
<p align="center">
  <img  src="Sample Images/Chunked characters.jpg" alt="MainForm">
    Character Boundaries
</p>



<p align="center">
  <img  src="Sample Images/Window 10px.png" alt="LSTM" style="width:80%">
	<br/>
	LSTM - window 10px
</p>






## Samples

Additionally, various fonts have been showcased in the images to illustrate font diversity within the dataset. For the following samples, the belongs text file is like the following.

```
<Starting pixel index>_<Ending pixel index>_<Character>

ز_3375_3459
ی_3333_3375
ر_3250_3333
ا_3214_3250
3171_3214_
س_3080_3171
ل_3028_3080
ا_2977_3028
م_2909_2977
ت_2787_2909
2744_2787_
م_2676_2744
ر_2592_2676
د_2534_2592
م_2476_2534
```





### Times New Roman

<p align="center">
  <img  src="Sample Images/Times New Roman.png" alt="Times New Roman" style="width:80%">
</p>
<p align="center">
  <img  src="Sample Images/Times New Roman_Noise.jpg" alt="Times New Roman" style="width:80%">
    <br/>
	Times New Roman
</p>







### B Mitra

<p align="center">
  <img  src="Sample Images/B Mitra.png" alt="B Mitra" style="width:80%">
</p>
<p align="center">
  <img  src="Sample Images/B Mitra_Noise.jpg" alt="B Mitra" style="width:80%">
    <br/>
    B Mitra
</p>







### Tahoma

<p align="center">
  <img  src="Sample Images/Tahoma.png" alt="Tahoma" style="width:80%">
</p>
<p align="center">
  <img  src="Sample Images/Tahoma_Noise.jpg" alt="Tahoma" style="width:80%">
    <br/>
    Tahoma
</p>







### Arial

<p align="center">
  <img  src="Sample Images/Arial.png" alt="Arial" style="width:80%">
</p>
<p align="center">
  <img  src="Sample Images/Arial_Noise.jpg" alt="Arial" style="width:80%">
    <br/>
    Arial
</p>







### B Homa

<p align="center">
  <img  src="Sample Images/B Homa.png" alt="B Homa" style="width:80%">
</p>
<p align="center">
  <img  src="Sample Images/B Homa_Noise.jpg" alt="B Homa" style="width:80%">
    <br/>
    B Homa
</p>







### B Nazanin

<p align="center">
  <img  src="Sample Images/B Nazanin.png" alt="B Nazanin" style="width:80%">
</p>
<p align="center">
  <img  src="Sample Images/B Nazanin_Noise.jpg" alt="B Nazanin" style="width:80%">
    <br/>
    B Nazanin
</p>







### B Traffic

<p align="center">
  <img  src="Sample Images/B Traffic.png" alt="B Traffic" style="width:80%">
</p>
<p align="center">
  <img  src="Sample Images/B Traffic_Noise.jpg" alt="B Traffic" style="width:80%">
    <br/>
    B Traffic
</p>







### B Lotus

<p align="center">
  <img  src="Sample Images/B Lotus.png" alt="B Lotus" style="width:80%">
</p>
<p align="center">
  <img  src="Sample Images/B Lotus_Noise.jpg" alt="B Lotus" style="width:80%">
    <br/>
    B Lotus
</p>







### B Yagut

<p align="center">
  <img  src="Sample Images/B Yagut.png" alt="B Yagut" style="width:80%">
</p>
<p align="center">
  <img  src="Sample Images/B Yagut_Noise.jpg" alt="B Yagut" style="width:80%">
    <br/>
    B Yagut
</p>







### B Zar

<p align="center">
  <img  src="Sample Images/B Zar.png" alt="B Zar" style="width:80%">
</p>
<p align="center">
  <img  src="Sample Images/B Zar_Noise.jpg" alt="B Zar" style="width:80%">
    <br/>
    B Zar
</p>







### Calibri

<p align="center">
  <img  src="Sample Images/Calibri.png" alt="Calibri" style="width:80%">
</p>
<p align="center">
  <img  src="Sample Images/Calibri_Noise.jpg" alt="Calibri" style="width:80%">
    <br/>
    Calibri
</p>

