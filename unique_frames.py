import os
import cv2
import shutil
from skimage.metrics import structural_similarity as ssim

def path_validator(input_path):
    if os.path.isdir(input_folder):
        return True
    else:
        print("Please provide valid directory path!")
        return False

def is_similar_to_any(frame,saved_frames,similarity_threshold):
    resized_frame=cv2.resize(frame,(256,256))
    frame_gray=cv2.cvtColor(resized_frame,cv2.COLOR_BGR2GRAY)
    for one_saved in saved_frames:
        resized_one_saved=cv2.resize(one_saved,(256,256))
        one_saved_gray=cv2.cvtColor(resized_one_saved,cv2.COLOR_BGR2GRAY)
        percent_match,_=ssim(frame_gray,one_saved_gray,full=True)
        if percent_match>=similarity_threshold:
            return True
    else:
        return False
            

def get_unique_frames(frames_folder,op_folder,threshold=0.75):
    print("Please wait we are extracting unique frames..........")
    all_images = sorted([
        f for f in os.listdir(input_folder)
        if f.lower().endswith(('.jpg', '.jpeg', '.png'))
    ])
    total_images=0
    saved=0
    unique_frames=[]
    for each_frame in all_images:
        img=cv2.imread(os.path.join(frames_folder,each_frame))
        if img is None:
            print(f"Unable to read the image: {each_frame}")
        else:
            total_images+=1
            if not is_similar_to_any(img,unique_frames,threshold):
                each_frames_op_path=os.path.join(op_folder,each_frame)
                shutil.copyfile(os.path.join(frames_folder,each_frame),each_frames_op_path)
                unique_frames.append(img)
                saved+=1
    print(f'''Total frames: {total_images}\n Unique frames: {len(unique_frames)}\n Saved frames: {saved}''')

if __name__=="__main__":
    input_folder=input("Please enter directory path containing your frames: ")
    if path_validator(input_folder):
        output_folder=input("Please enter folder path for storing unique frames: ")
        if path_validator(output_folder):
            get_unique_frames(input_folder,output_folder)


