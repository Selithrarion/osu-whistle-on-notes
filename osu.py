import os
import tkinter as tk
from tkinter import filedialog


def process_hit_objects(lines):
    have_whistle = ['2', '6', '10', '14']
    hit_objects_section = False
    modified_lines = []

    for line in lines:
        if '[HitObjects]' in line:
            hit_objects_section = True
            modified_lines.append(line)
            continue

        if hit_objects_section and ',' in line:
            elements = line.split(',')

            if len(elements) > 5 and ('|' in elements[5]):
                try:
                    if len(elements) <= 8:
                        modified_lines.append(','.join(elements))
                        continue

                    # reverse can have a lot of hit objects tho, need to fix
                    hit_objects = elements[8].split('|')
                    if hit_objects[0] in have_whistle:
                        hit_objects[0] = str(int(hit_objects[0]) - 2)
                    if hit_objects[1] in have_whistle:
                        hit_objects[1] = str(int(hit_objects[1]) - 2)

                    hit_objects[0] = str(int(hit_objects[0]) + 2)
                    elements[8] = '|'.join(hit_objects)
                except IndexError:
                    print('err line', line)

                modified_lines.append(','.join(elements))
            elif len(elements) > 5 and elements[0].isdigit() and elements[3] == '12':
                modified_lines.append(line)
            else:
                hitsound = int(elements[4])
                if hitsound in have_whistle:
                    continue
                hitsound += 2  # Add whistle
                elements[4] = str(hitsound)
                modified_lines.append(','.join(elements))
        else:
            modified_lines.append(line)

    return modified_lines


def add_whistle_hitsound_to_file(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    modified_lines = process_hit_objects(lines)

    with open(input_file, 'w', encoding='utf-8') as file:
        file.writelines(modified_lines)


def process_mapset_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.osu'):
                file_path = os.path.join(root, file)
                add_whistle_hitsound_to_file(file_path)


def select_directory():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    directory = filedialog.askdirectory(title="Select Osu Mapset Directory")
    if directory:
        process_mapset_directory(directory)


def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(title="Select Osu Difficulty File", filetypes=[("Osu Files", "*.osu")])
    if file_path:
        add_whistle_hitsound_to_file(file_path)


# select_directory()


select_file()


def debug_with_single_line(test_line):
    lines = ['[HitObjects]\n', test_line + '\n']
    modified_lines = process_hit_objects(lines)
    for line in modified_lines:
        print(line.strip())

# debug_with_single_line('180,227,19186,2,0,P|180:274|188:324,1,87.5,0|0,0:2|0:2,0:0:0:0:')
# debug_with_single_line('180,227,19186,2,0,P|180:274|188:324,1,87.5,8|4,0:2|0:2,0:0:0:0:')
# debug_with_single_line('180,227,19186,2,0,P|180:274|188:324,1,87.5,8|4,0:2|0:2,0:0:0:0:')
# debug_with_single_line('173,182,13075,2,0,P|173:229|175:248,1,52.5000020027161,2|0,0:0|0:0,0:0:0:0:')
# debug_with_single_line('173,182,13631,2,0,P|173:229|175:248,1,52.5000020027161,6|0,0:0|0:0,0:0:0:0:')
# debug_with_single_line('173,182,14186,2,0,P|173:229|175:248,1,52.5000020027161,14|0,0:0|0:0,0:0:0:0:')
# debug_with_single_line('173,182,14742,2,0,P|173:229|175:248,1,52.5000020027161,12|0,0:0|0:0,0:0:0:0:')
# debug_with_single_line('173,182,15298,2,0,P|173:229|175:248,1,52.5000020027161,8|0,0:0|0:0,0:0:0:0:')
# debug_with_single_line('173,182,15853,2,0,P|173:229|175:248,1,52.5000020027161,10|0,0:0|0:0,0:0:0:0:')
# debug_with_single_line('173,182,16409,2,0,P|173:229|175:248,1,52.5000020027161,4|0,0:0|0:0,0:0:0:0:')
# debug_with_single_line('167,55,4877,6,0,L|137:36,3,30.0000011444092')
# debug_with_single_line('428,15,15801,2,0,B|486:7|486:7|513:23,2,80')
# debug_with_single_line('428,15,15801,2,0,B|486:7|486:7|513:23,2,80,0|0|0,0:2|0:2|0:2,0:2:0:0:')


