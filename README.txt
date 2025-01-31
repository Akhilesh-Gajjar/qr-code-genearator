Steps

1) install streamlit, fastapi and fastapi by using the command prompt or anaconda prompt : pip install streamlit fastapi uvicorn

2) unzip and copy the folder in the directory where your conda related files are installed( most likely in users folder in windows)

3) open terminal in any IDE or open command prompt. If using command prompt, then change the directory to this folder.

4) first, launch the file containing api and backend implementation : uvicorn ext_hash_api:app --reload

5) then, launch the file containing frontend implementation : streamlit run ext_hash_app.py
