import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from dependancies import patient_info
from deta import Deta

bh = 'https://black_hole-3kf-1-h9614251.deta.app/api/integration/1k00lrwmu6n2'



deta = Deta(bh)
db = deta.Base('xray_scans')
img = "E:\all_project\Pneumonia_Detection\images\Screenshot 2023-07-23 232711.png"
db.put({"image":img})

   

            
