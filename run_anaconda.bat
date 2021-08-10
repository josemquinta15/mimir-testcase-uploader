
call C:\Users\nacho\anaconda3\Scripts\activate.bat C:\Users\nacho\anaconda3

call python generate.py 50 > gen_out.txt

call python sorter.py

FOR %%A IN (1, 2, 3, 4, 5, 6, 7) DO call python uploader.py %%A