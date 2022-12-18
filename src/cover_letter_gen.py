import openai
import os

from applicant_info import ApplicantExp, Applicant

def generate_cover_letter(company="generic company", position="untitled", job_description=None, applicant:Applicant=None, num_words=400):
    if job_description is None: raise ValueError("Job Description cannot be None")

    openai.api_key = os.environ.get('OPEN_AI_KEY')


    # Load applicant
    if applicant is None: raise ValueError("Applicant cannot be None")

    background = applicant.education["major"]
    background_str = background[0]
    if len(background) > 1:
        for m in background[1:]:
            background_str += " and "
            background_str += m

    request = f"Write a cover letter for the positon of {position} at the comapny {company}. The Job Description for this positon is: {job_description}. I am a {applicant.title} with a background in {background_str}. I have experience with everything in the following list: {applicant.skills}. This cover letter should be no fewer than {num_words} words long."

    print(f"Request: {request}")
    print("\n Request Acknowleded. Processing....\n")
    out = openai.Completion.create(model="text-davinci-003", prompt=str(request),\
        temperature=0.7, max_tokens=3000, echo=True, presence_penalty=1.0, frequency_penalty=1.5)

    outtext = out["choices"][0]["text"]
    print(outtext)

if __name__ == "__main__":
    prompt = input("This is a program for generating cover letters.\nPlease input how long you would like this cover letter to be in terms of number of words\n>> ")
    num_words = prompt

    job_desc = """
Observe animals' physical conditions to detect illness or unhealthy conditions requiring medical care.
Cue or signal animals during performances.
Administer prescribed medications to animals.
Evaluate animals to determine their temperaments, abilities, or aptitude for training.
Feed or exercise animals or provide other general care, such as cleaning or maintaining holding or performance areas.
Talk to or interact with animals to familiarize them to human voices or contact.
Conduct training programs in order to develop and maintain desired animal behaviors for competition, entertainment, obedience, security, riding and related areas.
Keep records documenting animal health, diet, or behavior.
Advise animal owners regarding the purchase of specific animals.
Instruct jockeys in handling specific horses during races.
Train horses or other equines for riding, harness, show, racing, or other work, using knowledge of breed characteristics, training methods, performance standards, and the peculiarities of each animal.
Use oral, spur, rein, or hand commands to condition horses to carry riders or to pull horse-drawn equipment.
Place tack or harnesses on horses to accustom horses to the feel of equipment.
Train dogs in human assistance or property protection duties.
Retrain horses to break bad habits, such as kicking, bolting, or resisting bridling or grooming.
Train and rehearse animals, according to scripts, for motion picture, television, film, stage, or circus performances.
Organize or conduct animal shows.
Arrange for mating of stallions and mares and assist mares during foaling"""
    
    a_exp = ApplicantExp()
    a_exp.add_experience(position="CircusCoordinator", company="ClownCorp", start_date="122119990", end_date="12212000", location="Albany, NY", type="On Site", description="Arranging events at ClownCorpo circus. Training monkeys", skills=["Showmanship", "Teamwork", "Monkey Training"])


    a = Applicant(name="Leo", title="CircusCoordinator", education={"institution":"UCLA", "start":"1221180","end":"12211985", "major":["Business"]}, work_experience=a_exp, skillset=["Showmanship", "Teamwork", "Monkey Training"])
    
    # Feed prompt into GPT
    generate_cover_letter(company="BogosCircus", position="Lion Tamer", job_description=job_desc, applicant=a, num_words=num_words)


    # Get result

    # Copy it to clipboard

