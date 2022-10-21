
import sys
import operator
import docker 


layeyrs_to_image = {}

def count_common_list_att(list1, list2) -> int:
    count_common_argument = 0
    for  i in list1:
        if i in list2:
            count_common_argument += 1
    return count_common_argument



# load data base to dict
import csv
DATA_BASE_FILE = sys.argv[1]
LAYERS_SPERITOR_SING = ":"
with open(DATA_BASE_FILE) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            layeyrs_to_image[row[0]] = row[1].split(LAYERS_SPERITOR_SING) 
            line_count += 1

# Searching base image 
SEARCH_IMAGE = sys.argv[2] 
base_images = {}
semi_match_base_images ={}
client = docker.APIClient(base_url='unix://var/run/docker.sock') 
client.inspect_image(SEARCH_IMAGE)
layers = [layer[7::] for layer in client.inspect_image(SEARCH_IMAGE)["RootFS"]["Layers"]]
for image_name in layeyrs_to_image:
    matches_layers =  count_common_list_att(layers ,layeyrs_to_image[image_name])
    if matches_layers == len(layeyrs_to_image[image_name]):
        base_images[image_name] = matches_layers
    else:
        semi_match_base_images[image_name] = matches_layers

# Print resualt
images_list = []
if base_images:
    print("base images orderd by earlist to latest ")
    images_list = base_images
    
else:
    print("No Base image was found but the clost ones are sorted fro mthe most close one to the last one")
    images_list = semi_match_base_images

print(images_list)
sorted_dict = dict(sorted(images_list.items(), key=lambda item: item[1])[::-1])
for i in sorted_dict:
    print(i)