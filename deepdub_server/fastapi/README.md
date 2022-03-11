# How to run the application
1. Activate your virtual environment
2. Ensure deepdub is installed as a package.
3. Run the following command:
```
export DEEPDUB_NO_ARGS=True
```
4. Run the following command to launch the server:
```
uvicorn main:app --host 0.0.0.0 --port 8001
```