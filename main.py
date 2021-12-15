# D:\AteneoSHS12\ASHS ComElec\PVS Program 5.0.1
# Run Anaconda Environment
# streamlit run main.py

import streamlit as st
import pandas as pd
from PIL import Image
import os
import shutil
import process_election
import process_graphs

if __name__ == "__main__":
    
    # page configuration
    progvarlogo = Image.open("progvar_logo.png")
    progvarlogobg = Image.open("progvar_logo_wbg.png")
    st.set_page_config(
        page_title="PVS Program",
        page_icon=progvarlogobg,
    )

    # title
    st.image(progvarlogo, width=90)
    st.title("Preferential Voting System Program")
    st.caption("© ASHS ProgVar '21-'22")

    # upload csv file
    file = st.file_uploader("Upload a correctly formatted csv file.", type={"csv"})

    # error code. utilized when 'except' occurs
    error_code = 4

    # on button click
    bttn = st.button('Calculate results')

    if bttn and file is None:
        st.error("Please upload a csv file.")
    elif bttn:
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
                    label="Download election graphs",
                    data=fp,
                    file_name="election_graphs.zip",
                    mime="application/zip"
                )

            error_code -= 1
            pbar.progress(100)

        except:
            st.error("An error occured." + " Exit code:" + str(error_code))
            bttn = False
