


import os
import sys
from pathlib import Path

ffmpeg = "/usr/local/bin/ffmpeg"
def ffmpeg_crf_encode(video, crf_value, encoded_video, filenameWithoutExt, transitionResolution):

    """ encodes a given `video` with a specified `crf_value` and stores the encoded video as `encoded_video` """
    if os.path.isfile(encoded_video):
        # we dont want to re-encode again and again if we run this cell several times
        return
    os.system(f"{ffmpeg} -i {video} -vf scale=-1:{transitionResolution} -c:v libaom-av1 -crf {crf_value} -b:v 0   {encoded_video} ")
    
    

def calculate_vmaf(video, crf_value, encoded_video, filenameWithoutExt):
    vmafFilename = f"{filenameWithoutExt}_encoded_{crf_value}.json"
    if os.path.isfile(vmafFilename):
        # we dont want to re-calculate VMAF again and again 
        return
    
    os.system(f"{ffmpeg} -i {video} -i  {encoded_video} -lavfi \"libvmaf=log_fmt=json:log_path=/dev/stdout:model_path=/Users/usman.khalid/Downloads/vmaf-master/model/vmaf_v0.6.1.json\"  -f null - > {vmafFilename}")



filename = sys.argv[1]
transitionResolution = sys.argv[2]
filenameWithoutExt = Path(filename).stem
print("File name without extension: ", filenameWithoutExt)
print("filename with extension: ", filename)   
crfs = [26]
for crf in crfs :  
    ffmpeg_crf_encode(filename, crf, f"{filenameWithoutExt}_encoded_{crf}.mkv", filenameWithoutExt, transitionResolution) 
    calculate_vmaf(filename, crf, f"{filenameWithoutExt}_encoded_{crf}.mkv", filenameWithoutExt) 