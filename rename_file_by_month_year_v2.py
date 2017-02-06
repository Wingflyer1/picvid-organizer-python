import os
from time import gmtime
import time
from PIL import Image
import PIL.ExifTags

top_folder = os.getcwd()
dest_top = top_folder +'\\001_ordered_files\\'
dest_other = top_folder + '\\002_needs attention\\'
pic_vid_files_to_move = {}
other_files_to_move = {}

# create serialized file to store with pictures
try:
    f=open("sys_ser_num.py", "r")
except:
    f = open("sys_ser_num.py", "w")
    f.write("0")
    f.close()


def change_names():
    start = time.time()
    count_files = 0
    ser_num_file = open("sys_ser_num.py", "r")
    count_start = int(ser_num_file.read())
    count_vid_pic_files = count_start
    count_dirs = 0
    other_files_count = 0

    # walk through all folders within top_folder and find folders and files
    for path, dirnames, filenames in os.walk(str(top_folder)):
        count_dirs += len(dirnames)
        # iterate over each file in the directories and select video and picture files
        for file in filenames:
            count_files += 1
            i = file.split('.')[-1]
            if i.lower() in fil_ext:
                # print(i.lower())


                try:
                    count_vid_pic_files += 1
                    img = PIL.Image.open(str(path + '\\' + file))
                    exif = {PIL.ExifTags.TAGS[k]:v for k, v in img._getexif().items() if k in PIL.ExifTags.TAGS}

                    file_created_year = exif['DateTime'][:4]
                    file_created_month = exif['DateTime'][5:7]
                    print(exif['DateTime'][:10] + '-' + exif['DateTime'][11:], file_created_year, file_created_month)

                # """
                # There is no exif info on the file, therefore most possibly
                # a videofile or a altered picfile. Anyways is should be moved to a
                # folder for the user to select correct action. Do NOT change
                # name of file.
                # -- A test could be made to see if the file has it's creation
                # year and month in the filename, then it should be possible
                # to give a filename and put i correct folder. (another try except
                # within this exception :)
                # """
                except AttributeError as e:
                    print(e, path, file)
                    continue
                #     print("except", file)
                    # #get year and month the file was created
                    # file_stat = os.stat((path+'\\'+file))
                    # file_created_year = gmtime(file_stat.st_ctime).tm_year
                    # file_created_month = gmtime(file_stat.st_ctime).tm_mon
                # src file and path name
                src_file = "{}{}{}".format(path, '\\', file)

                # dest file and path name

                new_file_number = str(count_vid_pic_files).zfill(5)
                new_file_name = "{} {}-{}.{}".format(new_file_number, file_created_month, file_created_year, file.split('.')[-1])
                dest_file = "{}{}\{}\\{}".format(dest_top, file_created_year, file_created_month, new_file_name)

                # src and dest into dictionary
                pic_vid_files_to_move[src_file] = dest_file

            else:
                if file.split('.')[-1].lower() != "py" :
                    other_files_count += 1
                    src_other_file = "{}\\{}".format(path, file)
                    dst_other_file = "{}{}".format(dest_other, file)

                    other_files_to_move[src_other_file] = dst_other_file

    for key, value in pic_vid_files_to_move.items():
        src = key
        dst = value
        try:
            os.renames(str(src), str(dst))
        except:
            print("Unsuccessfull: {}".format(src))



    for key, value in other_files_to_move.items():
        src = key
        dst = value
        try:
            os.renames(str(src), str(dst))
            # print("Other success")
        except:
            print("Unsuccessfull: {}".format(src))

    end = time.time() - start
    print("\nIterated over {} files, within {} folders.\n"
          "Found {} video/picture files.\n"
          "Fount {} other files.\n"
          "in {} seconds".format(str(count_files), str(count_dirs), str(count_vid_pic_files), str(other_files_count), str(end)))

    # update file sys_ser_num.txt
    f = open("sys_ser_num.py", 'w')
    f.write(str(count_vid_pic_files))
    f.close()

fil_ext = ['ani', 'bmp', 'cal', 'fax', 'gif', 'img', 'jbg', 'jpe',
           'jpeg', 'jpg', 'mac', 'pbm', 'pcd', 'pcx', 'pct', 'pgm',
           'png', 'ppm', 'psd', 'ras', 'tga', 'tiff', 'wmf', 'yuv',
           'wmv', 'webm', 'vob', 'svi', 'roq', 'rmvb', 'rm', 'ogv',
           'ogg', 'nsv', 'mxf', 'mpg', 'mpeg', 'm2v', 'mpg', 'mp2',
           'mpeg', 'mpe', 'mpv', 'mp4', 'm4v', 'mov', 'qt', 'mng',
           'mkv', 'm4v', 'gifv', 'gif', 'flv ', 'f4v ', 'f4p',
           'f4a', 'f4b', 'flv', 'flv', 'drc', 'avi', 'asf', 'amv',
           '3gp', '3g2']

if __name__ == "__main__":
    change_names()
