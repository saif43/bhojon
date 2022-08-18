# BhojonTrial - Restaurant Management

## Dependency

Bhojon Desktop solution is programmed in python programming language, So there have some python package dependency, After download and install python version 3.9+ on your os, try to install all the dependencies from requirements.txt file,

    pip install -r requirements.txt

## Run the Project

After installing all the dependencies, try to run the project by this command, 

    python restora_lite.py

BhojonTrial should run properly on your os.

This project develped for working on windows system, So you should run this this project on windows system.

In the project, thier have two package maily, Trial and Pro, Trial can install anyone to verify Bhojon desktop functionality at most 7 days. After that it will be automatically disabled, user can not use this application more that 7 days from installation date. 
Bhojon Pro need to check client verification before run the POS

The only difference between Bhojon Trial and Bhojon Pro is the license and user module, This two module is different in two package.

## Make Executable

Two package full Bhojon in a exe, we are using pyinstaller exe creator, run this command in your terminal.

    pyinstaller --onefile --windowed restora_lite.py

It will create a exe file to dist/ folder, use this exe file to execute without code files.

## Important Files

Place your important files and images to your exe path folder, except will create not found error. 

The important files listed bellow,

    application/*
    license.txt
    restora.db

You should place all of this files to your root folder.
