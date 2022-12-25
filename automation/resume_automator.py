import json
import openai

class ResumeAutomator:
    
    def __init__(self, filename):
        self.file = filename
        self.load_resume()

    def load_resume(self):
        jsonresumefile = open(self.file)

        self.data = json.load(jsonresumefile)

        self.basics    = self.data["basics"]
   
        self.work      = self.load_work_exp()
   
        self.edu       = self.data["education"]
   
        self.awards    = self.data["awards"]

        self.skillsets = self.data["skills"]

        self.languages = self.data["languages"]

    def load_job_desc(self, desc):
        self.job_description = desc

    def tailor_resume(self):
        pass
    
    def load_work_exp(self):
        """
        Re formats some of the work experience into something that is easier
        for this program to parse
        """
        work_experiences = []
        for work_exp in self.data["work"]:
            work_content = ""
            work_content += work_exp["position"] + " at " + work_exp["company"]+ " from " + work_exp["startDate"] + " to " + work_exp["endDate"] + "\n"
            work_content += "Summary: " + work_exp["summary"]
            work_experiences.append(work_content)
        return work_experiences

    def choose_best_experience(self, n=4):
        """
        Choose n best experience matches to job description
        """
        score_exp_index_pairs = []
        for i, work_experience in enumerate(self.work):
            score = self.compare_experience_with_job(work_experience)
            score_exp_index_pairs.append((i, score))

    def compare_experience_with_job(self, exp):
        """
        Gets a score from a experience compared to job
        """
        pass

        

    

