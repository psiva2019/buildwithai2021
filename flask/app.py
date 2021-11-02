from flask import Flask,request, url_for, redirect, render_template
import pickle
import numpy as np

app = Flask(__name__)

model=pickle.load(open('lgr_model.pkl','rb'))


@app.route('/')
def hello_world():
    #return render_template("forest_fire.html")
    return render_template("stu_form.html")


@app.route('/predict',methods=['POST','GET'])
def predict():
    input_features=[x for x in request.form.values()]
    
    code_module = {'AAA':0,'BBB':1,'CCC':2,'DDD':3,'EEE':4,'FFF':5,'GGG':6}
    activity_type= {'dataplus':0,'dualpane':1,'externalquiz':2,'folder':3,'forumng':4,'glossary':5,'homepage':6,'htmlactivity':7,'oucollaborate':8,'oucontent':9,'ouelluminate':10,'ouwiki':11,'page':12,'questionnaire':13,'quiz':14,'resource':15,'sharedsubpage':16,'subpage':17,'url':18}
    age_band={'35-55':1,'0-35':0,'55<=':2}
    assessment_type ={'CMA':0,'Exam':1,'TMA':2}
    code_presentation = {'2013B':0,'2013J':1,'2014B':2,'2014J':3}
    gender = {'F':0,'M':1}
    disability = {'N':0,'Y':1}
    highest_education = {'A Level or Equivalent':0,'HE Qualification':1,'Lower Than A Level':2,'No Formal quals':3,'Post Graduate Qualification':4}
    imd_band = {'0-10%':0,'10-20%':1,'20-30%':2,'30-40%':3,'40-50%':4,'50-60%':5,'60-70%':6,'70-80%':7,'80-90%':8,'90-100%':9}
    region = {'East Anglian Region':0,'East Midlands Region':1,'Ireland':2,'London Region':3,'North Region':4,'North Western Region':5,'Scotland':6,'South East Region':7,'South Region':8,'South West Region':9,'Wales':10,'West Midlands Region':11,'Yorkshire Region':12}
    
    s_code_mod = code_module[input_features[0]]
    s_activity_type = activity_type[input_features[4]]
    s_age_band = age_band[input_features[-5]]
    s_assess_type = assessment_type[input_features[5]]
    s_code_presentation = code_presentation[input_features[1]]
    s_edu = highest_education[input_features[-7]]
    s_imd_band = imd_band[input_features[-6]]
    s_region = region[input_features[-8]]
    s_gender = gender[input_features[11]]
    s_disability = disability[input_features[-2]]
    
    disp_activity = [k for k,v in activity_type.items() if v == s_activity_type]
    print(input_features)
    non_mapped = [input_features[2], input_features[3], input_features[6],input_features[7],input_features[8],input_features[9],input_features[10],input_features[-4],input_features[-3],input_features[-1]]    
    print(non_mapped)                           
    s_assign_date, s_sum_clicks, s_weight, s_mod_len, s_submit_date, s_banked, s_assess_score ,s_prev_attempts, s_stu_creds, s_reg_date = [int(x) for x in non_mapped]
                           
    features = [s_code_mod,s_code_presentation,s_assign_date,s_sum_clicks,s_activity_type,s_assess_type,s_weight,s_mod_len,s_submit_date,s_banked,s_assess_score,s_gender,s_region,s_edu,s_imd_band,s_age_band,s_prev_attempts,s_stu_creds,s_disability,s_reg_date]
    final=[np.array(features)]
    print(features)
    print(final)
    prediction=model.predict(final)
    print('output={0}'.format(prediction))

    if prediction==1:
        return render_template('stu_form.html',pred="Your student is likely to pass in his/her upcoming exams !! \n The strategies followed to access your course or the times followed to start/submit assignments seems fine.")
    else:
        return render_template('stu_form.html',pred="Your student is likely to fail in his/her upcoming exams !! \n May need improvements/changes in way of preparation, or resources other than {0} can be tried!".format(disp_activity[0]))
