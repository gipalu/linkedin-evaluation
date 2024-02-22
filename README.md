# Linkedin Evaluation
This algorithm provides a technical assessment of the seller's linkedin, bringing a note and whether it has been technically approved by your linkedin or has failed and needs to pass a technical test
## Usage
This algorithm use dockerized FastAPI application to EC2 on AWS
### Deployment 
first, you have to install Docker. 

For run locally you have to start the docker, build docker image and run:
```
sudo service docker start
docker build -t ez-devs-linkedin-evaluation .
docker run -dp 8000:8000 ez-devs-linkedin-evaluation
```
For run in prod you have to start the docker and enter in ez-devs-linkedin-evaluation repository inside ECR and get the first push command and run the code in your project.

Next step is build, tag and post your image:
```
docker build -t ez-devs-linkedin-evaluation .
docker tag ez-devs-linkedin-evaluation:latest xxxxx.dkr.ecr.us-east-1.amazonaws.com/ez-devs-linkedin-evaluation:latest
docker push xxxxx.dkr.ecr.us-east-1.amazonaws.com/ez-devs-linkedin-evaluation:latest
```
After that, you have to connect to EC2 instance and configure your aws account in:
```
aws configure
```
Now, you have to pull your docker image, copy the image_url direct from ECR and run:
```
docker pull <IMAGE_URI> 
```
Grab the name of the image first by running 
```
docker images
```
and then write:
```
docker run -dp 80:8000 <NAME_OF_IMAGE>
```
Finally, navigate to your EC2 Instance, grab the public IPV4of DNS the instance and run

You can see more in: https://levelup.gitconnected.com/deploy-a-dockerized-fastapi-application-to-aws-cc757830ba1b

### Response
Running with linkedin profie: https://www.linkedin.com/in/barackobama/

Example response:
```python
{
    "userId": str,
    "final_score": float,
    "status": int,
    "score": {
        "time_experience": float,
        "recent_time_experience":float,
        "time_experience_between_jobs": float,
        "recommendations_quantity": float,
        "recommendations_size": float,
        "description_exp_size": float,
        "description_last_exp_size": float,
        "key_word_senior": float,
        "key_word_pleno": float,
        "key_word_leadership": float,
        "key_word_teech_coordenation": float,
        "articles": float,
        "stacks_in_experience": float,
        "stacks_in_profile_title_and_summary": float,
        "summary": float,
        "career_in_experience": float,
        "career_in_recent_experiences": float,
        "career_in_profile_title_and_summary": float,
        "education": float,
        "stacks_in_skills": float,
        "stacks_linkedin_seal_in_skills": float,
        "stacks_endorsed_by_colleagues_in_skills": float,
        "hard_skills_in_fields": float,
        "hard_skills_in_skills": float
    }
}
```

You can see more about this algorithm in notion:
https://www.notion.so/ezdevs/Algoritmo-do-LinkedIn-e993350740b048b7be09aeb65cd4bce9