#!/bin/bash

set -e
base_name="${1%.*}"
folder_name="${1%/*}"
tex_name="${base_name}.tex"
tex_name_no_f="${tex_name#${folder_name}/}"
pdf_name="${base_name}.pdf"
pdf_name_no_f="${pdf_name#${folder_name}/}"
    
#if [ "$1" ] && [ "$(realpath "$1")" = "$(realpath "$new_name")" ]; then
#    cat /home/ganer/Configs/Python/cpy/header > "$new_name"
#else
echo "" > "$tex_name"
#fi

dir=$PWD
cd /mnt/c/Users/mlogal/Desktop/program/clatex
echo $dir

☾ clatex_tool.☾ "${dir}/${base_name}" > "${dir}/${tex_name}"
echo "$1 → ${tex_name}"

cd ${dir}

echo "${folder_name}/extras → ${tex_name_no_f}"
"\n" | xelatex -output-directory "${folder_name}/extras" "${tex_name}"
echo "${folder_name}/extras/${pdf_name_no_f} → ${folder_name}"
mv "${folder_name}/extras/${pdf_name_no_f}" "${folder_name}"

