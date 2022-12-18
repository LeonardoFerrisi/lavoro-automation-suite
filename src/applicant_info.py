from essentials import Bunch

class ApplicantExp(list):
    """
    Stores information on work experience
    """
    def __init__(self, experience:list=None):
        if experience is None: experience = []
        for e in experience:
            self.append(e)

    def add_experience(self, position, company, start_date, end_date, location, type, description, skills):
        
        exp = {
            "position"   : position, 
            "company"    : company, 
            "start_date" : start_date,
            "end_date"   : end_date,
            "location"   : location,
            "type"       : type,
            "description": description,
            "skills"     : skills
        } 
        work_exp = Bunch(contents=exp)

        self.append(work_exp)

class Applicant(Bunch):

    def __init__(self, name, title, education:dict, work_experience:ApplicantExp, skillset:list, ):
        """
        Models an applicant with all their information

            Parameters:
                name                     (str): Your name
                title                    (str): Your current position or title
                education               (dict): A dictionary following the format {"institution": value, "start":2019, "end":end, "major":[major(s)]} 
                work_experience (ApplicantExp): An object containing work experience, preferably pre loaded.
                skillset                (list): A list of your skill        
        """
        self.name = name
        self.title = title
        self.__validate_education(education)
        self.education = education
        self.work_experience = work_experience
        self.skills = skillset

    def loadjson(self, json_file):
        pass
    
    def __validate_education(self, edu):
        assert len(list(edu.keys()))==4
        assert list(edu.keys()) == ["institution", "start", "end", "major"]
        assert isinstance(edu["major"],list)
        assert isinstance(edu["institution"], str)
        assert isinstance(edu["start"], str)
        assert isinstance(edu["end"], str)

    def __repr__(self):
        rep = f"""
        Applicant:
            Name       : {self.name}
            Title      : {self.title}
            Education  : {self.education["institution"]}, start: {self.education["start"]} - end: {self.education["end"]}
            Experience : {self.work_experience}
            Skills     : {self.skills} 
        """
        return rep

if __name__ == "__main__":

    a_exp = ApplicantExp()
    a_exp.add_experience(position="CEO", company="GamerGang", start_date="12212000", end_date="12182022", location="Albany, NY", type="On Site", description="Ate Cheetos", skills=["Apple Eating"])
    a_exp.add_experience(position="GamerInChief", company="GamerGang", start_date="122119990", end_date="12212000", location="Albany, NY", type="On Site", description="Ate Cheetos", skills=["Apple Eating"])

    for item in a_exp: print(item)

    a = Applicant(name="Leo", title="CEO", education={"institution":"UCLA", "start":"1221180","end":"12211985"}, work_experience=a_exp, skillset=["Apple Eating"])
    print("\n\n")
    print(a)