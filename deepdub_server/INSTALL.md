# Deepdub Web Server - Installation Guide

## Step 1: Virtual Environment 
Use the same virtual environment as you use for the [CLI engine](../deepdub_cli/INSTALL.md).

## Step 2: Installing the Python dependencies
Run ```pip install -r requirements.txt``` to install the requirements for this web server.

## Step 3: Add the deepdub main script
1. Ensure that you've added deepdub as a package (by running ```pip install .``` in the **deepdub_cli** folder).
2. Run ```python manage.py addscript deepdub_script.py```.

## Step 4: Done! Let's launch... 🚀
Run ```python manage.py runserver``` to run the server.

If you need to access the admin panel, you can run ```python manage.py createsuperuser``` to create an admin.
