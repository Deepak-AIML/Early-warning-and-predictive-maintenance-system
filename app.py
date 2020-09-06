
import numpy as np
import pickle
import pandas as pd
import streamlit as st
from catboost import CatBoostClassifier

# Load the Catboost  model
filename ='cat_optimal2.pkl'
classifier = pickle.load(open(filename, 'rb'))

def predict_prob(partnumber,toplevelserialnumber,collid,chardesc,charvalue):

    data = np.array([[partnumber,toplevelserialnumber,collid,chardesc,charvalue]])
    prediction =classifier.predict_proba(data)[:,1]
    return round(prediction[0],2)

def main():

    st.sidebar.header('About')
    st.sidebar.info('This app is created to predict False reject')

    # add_selectbox = st.sidebar.selectbox(
    #     "How would you like to predict?",
    #     ("Online", "Batch"))

#     from PIL  import Image
#     image=Image.open('Capture.png')
#     st.sidebar.image(image,width=300)

    st.title("False Reject Prediction  App")

    html_temp = """
       <div style="background-color:#ADD8E6;padding:5px">
        <h2 style="color:white;text-align:center;">Web app Build using Streamlit, Deployed on Heroku </h2>
       </div>
       """
    st.markdown(html_temp, unsafe_allow_html=True)
    # if add_selectbox == 'Online':

    sitename=st.selectbox('Enter your Site name',('GMCFULL','GMCFULL'))
    linename = st.selectbox('Enter your Line name', ('T1XX Front Axle FA HiV','T1XX Front Axle FA HiV'))
    stationname = st.selectbox('Enter your Station name', ('OP180A','OP180B'))
    partnumber= st.selectbox('Enter your Part number', ('40217205','40217206','40217207'))
    toplevelserialnumber=st.selectbox('Enter your Top Level Serial number', ("01A200240722",
                                                                             "01A200250294",
                                                                             "01A200240856",
                                                                             "01A200250299",
                                                                             "01C200250128",
                                                                             "01C200140771",
                                                                             "01A200230993",
                                                                             "01A200220255",
                                                                             "01A200230640",
                                                                             "01A200250361",
                                                                             "01A200210080",
                                                                             "01A200240452",
                                                                             "01A200240367",
                                                                             "01C200240129",
                                                                             "01A200250286",
                                                                             "01A200230274",
                                                                             "01A200240210",
                                                                             "01A200230764",
                                                                             "01A200210660",
                                                                             "01A200250242",
                                                                             "01A200230775",
                                                                             "01A200250502",
                                                                             "01C200240066",
                                                                             "01A200250230",
                                                                             "01A200250201"))
    collid=st.number_input("Collid",min_value=-9999999999,max_value=9999999999,value=-1277499867)
    chardesc=st.selectbox('Enter your Char description', ('LH Slide To Full Depth Posn','NVH Torque Sweep Test Cycle Count','Pinion Slide To Full Depth Posn','RH Slide To Full Depth Posn'))
    charvalue=st.number_input("Charvalue",min_value=0,max_value=9999999999,value=0)

    if st.button("Predict"):
        result = predict_prob(partnumber, toplevelserialnumber, collid, chardesc, charvalue)
        print(result)

        if result > 0.0 and result <= 0.3:
            st.error("The Probability of False Reject  is {}, Please start downtime.".format(result))
        elif result > 0.3 and result <= 0.5:
            st.warning(
                "The Probability of False Reject  is {}, There is moderate risk of Reject and downtime should be planned .".format(
                    result))
        else:
            st.success("The Probability of False Reject  is {}, No need for maintenance downtime.".format(result))

# if add_selectbox == 'Batch':
#     file_upload = st.file_uploader("Upload csv file for predictions", type=["csv"])
#
#     if file_upload is not None:
#         data = pd.read_csv(file_upload)
#         data2= data.drop(['STATUS','PROD_TIMESTAMP','SITENAME','LINENAME','STATIONNAME'],axis=1)
#         data2=data2[['PARTNUMBER','TOPLEVELSERIALNUMBER','COLLID','CHARDESC','CHARVALUE']]
#         # Load the Catboost  model
#         predictions = classifier.predict_proba(data2)[:,1]
#         predictions=pd.DataFrame(predictions)
#         predictions.rename({0: 'P_1'}, axis=1,inplace=True)
#         final_data=pd.concat([data,predictions],axis=1)
#
#         if st.button("Predict"):
#             st.write(predictions)





if __name__ == '__main__':
    main()

