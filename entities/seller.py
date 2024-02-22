import json
#TODO onde estar usando buffer, não passar seller, so exp

class Seller:
    def __int__(self):
        self.user_id: str = ''
        self.profile_title: str = ''
        self.summary: str = ''
        self.experiences: list = []
        self.education: list = []
        self.articles: list = []
        self.recommendations_received: list = []
        self.recommendations_sent: list = []
        self.connections: str = ''
        self.level:int = 0
        self.stack:list = []
        self.secondary_stacks:list = []
        self.certifications:list = []
        self.skills:list = []
        self.career:str = ''
        self.recommendations_comments: list = []
        self.certifications_title: list = []
        self.experiences_title: list = []
        self.experiences_description: list = []

        self._total_experience_time = 0
        self._total_valid_experience_time = 0
        self._latest_experience_time = 0
        self._previous_experience_time = 0
        self._percent_experiences_between_jobs = 0
        self._key_words_count = 0
        self._articles_quantity = 0
        self._recommendations_quantity = 0
        self._percent_recommendations_right_size = 0
        self._percent_description_experience_size = 0
        self._last_description_experience_size = 0
        self._percent_primary_stacks_in_experiences = 0
        self._primary_stacks_in_profile_title = 0
        self._secondary_stacks_in_profile_tile = 0
        self._primary_stacks_in_summary = 0
        self._secondary_stacks_in_summary = 0
        self._summary_size = 0
        self._recommendations_multiplier = 1
        self._valid_secondary_stacks = []
        self._percent_career_in_experiences = 0
        self._career_in_profile_title = 0
        self._career_in_summary = 0
        self._career_in_recent_experiences = 0
        self._education_validity = 0
        self._stacks_in_skills = 0
        self._hard_skills_quantity_in_skills = 0
        self._hard_skills_quantity_in_fields = 0
        self._final_score = 0
        self._evaluation = 0

        self._time_experience_score = 0
        self._recent_time_experience_score = 0
        self._time_experience_between_jobs_score = 0
        self._recommendations_quantity_score = 0
        self._recommendations_size_score = 0
        self._connections_score = 0
        self._description_size_score = 0
        self._last_description_size_score = 0
        self._senior_score = 0
        self._pleno_score = 0
        self._leadership_score = 0
        self._tech_coord_score = 0
        self._articles_score = 0
        self._primary_stacks_in_exp_score = 0
        self._primary_stacks_in_profile_title_and_summary_score = 0
        self._career_in_exp_score = 0
        self._career_in_profile_title_and_summary_score = 0
        self._career_in_recent_exps_score = 0
        self._education_score = 0
        self._summary_size_score = 0
        self._stacks_in_skills_score = 0
        self._linkedin_seal_for_stacks_in_skills_score = 0
        self._colleagues_rec_for_stacks_in_skills_score = 0
        self._hard_skills_in_skills_score = 0
        self._hard_skills_in_fields_score = 0

    def build(self, data: dict):
        self.user_id = data.get('userId')
        self.profile_title =  data.get('linkedinData').get('userProfile').get('title')
        self.summary = data.get('linkedinData').get('userProfile').get('description')
        self.experiences = data.get('linkedinData').get('experiences')
        self.education = data.get('linkedinData').get('education')
        self.articles = data.get('linkedinData').get('publications')
        self.recommendations_received = data.get('linkedinData').get('recommendations').get('received') if data.get('linkedinData').get('recommendations') else []
        self.recommendations_sent = data.get('linkedinData').get('recommendations').get('sent') if data.get('linkedinData').get('recommendations') else []
        self.connections = data.get('linkedinData').get('userProfile').get('connections')
        self.certifications = data.get('linkedinData').get('licensesAndCertifications')
        self.skills = data.get('linkedinData').get('skills')
        self.level = data.get('level')
        self.stack = data.get('highlightedSkills')
        self.secondary_stacks = data.get('secondarySkills')
        self.career = data.get('career')

    def get_recommendations_comments(self, data: dict):
        if data.get('linkedinData').get('recommendations'):
            self.recommendations_comments = [d.get('comment') for d in data.get('linkedinData').get('recommendations').get('received')]

    def get_certifications_title(self, data: dict):
        self.certifications_title = [d.get('title') for d in data.get('linkedinData').get('licensesAndCertifications')]

    def get_experiences_fields(self, data:dict):
        self.experiences_title = [d.get('title') for d in data.get('linkedinData').get('experiences')]
        self.experiences_description = [d.get('description') for d in data.get('linkedinData').get('experiences')]

    def get_sum_scores(self):
        result = self._time_experience_score + self._recent_time_experience_score + self._time_experience_between_jobs_score + \
                 self._recommendations_quantity_score + self._recommendations_size_score + self._description_size_score + \
                 self._last_description_size_score + self._senior_score + self._pleno_score + self._leadership_score + self._tech_coord_score + \
                 self._articles_score + self._primary_stacks_in_exp_score + self._primary_stacks_in_profile_title_and_summary_score  \
                 + self._summary_size_score + self._career_in_profile_title_and_summary_score + self._career_in_exp_score + self._education_score + \
                 self._stacks_in_skills_score + self._linkedin_seal_for_stacks_in_skills_score +  \
                 self._colleagues_rec_for_stacks_in_skills_score + self._hard_skills_in_skills_score + self._hard_skills_in_fields_score + self._career_in_recent_exps_score
        self._final_score = result

    def set_total_experience_time(self, value):
        self._total_experience_time = value

    def set_total_valid_experience_time(self, value):
        self._total_valid_experience_time = value

    def set_latest_experience_time(self, value):
        self._latest_experience_time = value

    def set_previous_experience_time(self, value):
        self._previous_experience_time = value

    def set_percent_experiences_between_jobs(self, value):
        self._percent_experiences_between_jobs = value

    def get_time_experience_score(self):
        return self._time_experience_score

    def get_recent_time_experience_score(self):
        return self._recent_time_experience_score

    def get_time_experience_between_jobs_score(self):
        return self._time_experience_between_jobs_score

    def set_key_words_count(self, value):
        self._key_words_count = value

    def set_articles_quantity(self, value):
        self._articles_quantity = value

    def set_recommendations_quantity(self, value):
        self._recommendations_quantity = value

    def set_percent_recommendations_right_size(self, value):
        self._percent_recommendations_right_size = value

    def set_percent_description_experience_size(self, value):
        self._percent_description_experience_size = value

    def set_last_description_experience_size(self, value):
        self._last_description_experience_size = value

    def set_percent_primary_stacks_in_experiences(self, value):
        self._percent_primary_stacks_in_experiences = value

    def set_primary_stacks_in_profile_title(self, value):
        self._primary_stacks_in_profile_title = value

    def set_secondary_stacks_in_profile_tile(self, value):
        self._secondary_stacks_in_profile_tile = value

    def set_primary_stacks_in_summary(self, value):
        self._primary_stacks_in_summary = value

    def set_secondary_stacks_in_summary(self, value):
        self._secondary_stacks_in_summary = value

    def set_summary_size(self, value):
        self._summary_size = value

    def set_valid_secondary_stacks(self, value):
        self._valid_secondary_stacks = value

    def set_percent_career_in_experiences(self, value):
        self._percent_career_in_experiences = value

    def set_career_in_profile_title(self, value):
        self._career_in_profile_title = value

    def set_career_in_summary(self, value):
        self._career_in_summary = value

    def set_evaluation(self, value):
        self._evaluation = value

    def set_recommendations_multiplier(self, value):
        self._recommendations_multiplier = value

    def set_education_validity(self, value):
        self._education_validity = value

    def set_stacks_in_skills(self, value):
        self._stacks_in_skills = value

    def set_hard_skills_quantity_in_skills(self, value):
        self._hard_skills_quantity_in_skills = value

    def set_hard_skills_quantity_in_fields(self, value):
        self._hard_skills_quantity_in_fields = value

    def set_career_in_recent_experiences(self, value):
        self._career_in_recent_experiences = value

    def __str__(self):
        return f'{self.user_id}-{self.name}'







