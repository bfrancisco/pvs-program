# Running main.py on local computer
#   Run Anaconda Environment
#   Go to main.py's directory
#   type "streamlit run main.py" on anaconda environment

# streamlit, for user interface of web app
import streamlit as st

# for csv processing
import pandas as pd

# for img processing
from PIL import Image

# for directory handling
import os
import shutil

# other .py files
import process_election
import process_graphs

if __name__ == "__main__":
    
    # page configuration
    progvarlogo = Image.open("progvar_logo.png")
    progvarlogobg = Image.open("progvar_logo_wbg.png")
    comeleclogo = Image.open("comelec_logo.png")
    st.set_page_config(
        page_title="PVS Program",
        page_icon=progvarlogobg,
    )

    # title
    col1, col2 = st.columns([1, 6])
    with col1:
        st.image(progvarlogobg, width=90)
    with col2:
        st.image(comeleclogo, width=110)
    st.title("Preferential Voting System Program")
    st.caption("© ASHS ProgVar '21-'22 in partnership with ASHS ComElec '21-'22")

    # upload csv file
    file = st.file_uploader("Upload a correctly formatted csv file.", type={"csv"})

    # error code. utilized when 'except' occurs
    
    error_code = 4
    #   error_code 4: Problem is at process_election.py
    #   error_code 3: Problem is at process_graph.py, specifically at make_figures function
    #   error_code 2: Problem is at process_graph.py, specifically at show_figures function
    #   error_code 1: Problem is at download buttons of streamlit
    #   error_code 0: means everything is good
    
    # on button click
    bttn = st.button('Calculate results')
    st.caption("A sample csv file will be processed if no file was uploaded.")
    
    if bttn:
        if file is None:
            file = 'sample_data.csv'
        try:
            # read csv file as panda DataFrame
            csvfile = pd.read_csv(file)

            # progress bar
            pbar = st.progress(0)

            # initialize new folder
            current_directory = os.getcwd()
            final_directory = os.path.join(current_directory, r"election_result") # election_result - folder name
            if not os.path.exists(final_directory):
                os.makedirs(final_directory)

            # calculate results
            majority_c, voter_c, log, graph_data, winner = process_election.calc_winner(csvfile)
            error_code -= 1
            figures, titles = process_graphs.make_figures(graph_data, majority_c, voter_c)
            error_code -= 1
            pbar.progress(60)

            # list of ballots
            st.header("List of ballots")
            st.write(csvfile)
            pbar.progress(70)

            # show figures
            st.header("Election rounds")
            process_graphs.show_figures(figures, titles)
            error_code -= 1
            pbar.progress(80)

            # winner
            st.subheader("Winning candidate")
            st.write(winner)
            pbar.progress(90)

            # download files
            st.header("Download results")
            st.download_button('Download log file', data=log, file_name='log.txt')
            
            shutil.make_archive('election_graphs', 'zip', 'election_result') # convert election_graphs to zip file

            with open("election_graphs.zip", "rb") as fp:
                btn = st.download_button(
                    label="Download graphs",
                    data=fp,
                    file_name="election_graphs.zip",
                    mime="application/zip"
                )

            error_code -= 1
            pbar.progress(100)

        except:
            st.error("An error occured." + " Exit code:" + str(error_code))
            bttn = False
