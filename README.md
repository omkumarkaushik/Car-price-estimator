###############################################################
######### Install and start virtual environment ###############

python -m venv venv

###############################################################
########## Install all the requirements #######################

pip install -r requirements.txt

###############################################################
########### Run the uvicorn app (Fast API) ####################

uvicorn main:app --reload

############################################################
########### Run the streamlit app (for front-end) ##########

streamlit run .\streamlit_app.py
