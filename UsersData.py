

class User:
    def __init__(self, username, email, phone, password, type="patient"):
        self.username = username
        self.email = email
        self.phone = phone
        self.password = str(password)
        self.type = type


# Questionnaire model
class Report:
    def __init__(self, U_ID:int, symptoms:str, symptom_duration:str,
                 breathing_difficulty:str, coughing_mucus:str, mucus_color_consistency:str,
                 chest_pain:str, chest_pain_description:str, medical_conditions:str, smoking:str,
                 smoking_details:str, family_history:str, result:str):
        # make sure nothing is empty and U_ID is int if empty replace with dummy string Not Specified
        
        self.U_ID = int(U_ID)
        self.symptoms = symptoms if symptoms != "" else "Not stated"
        self.symptom_duration = symptom_duration if symptom_duration != "" else "Not stated"
        self.breathing_difficulty = breathing_difficulty if breathing_difficulty != "" else "Not stated"
        self.coughing_mucus = coughing_mucus if coughing_mucus != "" else "Not stated"
        self.mucus_color_consistency = mucus_color_consistency if mucus_color_consistency != "" else "Not stated"
        self.chest_pain = chest_pain if chest_pain != "" else "Not stated"
        self.chest_pain_description = chest_pain_description if chest_pain_description != "" else "Not stated"
        self.medical_conditions = medical_conditions if medical_conditions != "" else "Not stated"
        self.smoking = smoking if smoking != "" else "Not stated"
        self.smoking_details = smoking_details if smoking_details != "" else "Not stated"
        self.family_history = family_history if family_history != "" else "Not stated"
        self.result = result if result != "" else "Not stated"
        
        
    def __str__(self):
        return f"\nReport({self.U_ID} \n {self.symptoms} \n {self.symptom_duration} \n {self.breathing_difficulty} \n {self.coughing_mucus} \n {self.mucus_color_consistency} \n {self.chest_pain} \n {self.chest_pain_description} \n {self.medical_conditions} \n {self.smoking} \n {self.smoking_details} \n {self.family_history} \n {self.result}\n)\n\n"


