# CSCI E-29: ScottBot 
***

Final Project, Idan Nikritin (idannik) and Hila Paz Herszfang (hip023)

<img src="https://github.com/hip023/2021sp-final-project-idan-hila/blob/master/assets/scottbot.jpg?raw=true" alt="ScottBot" width="300"/>

[![Build Status](https://travis-ci.com/hip023/2021sp-final-project-idan-hila.svg?token=ystyYsaTfZ7QgRPbwMt6&branch=master)](https://travis-ci.com/hip023/2021sp-final-project-idan-hila)

[![Maintainability](https://api.codeclimate.com/v1/badges/583ebed631fbfeb3be9f/maintainability)](https://codeclimate.com/github/hip023/2021sp-final-project-idan-hila/maintainability)

[![Test Coverage](https://api.codeclimate.com/v1/badges/583ebed631fbfeb3be9f/test_coverage)](https://codeclimate.com/github/hip023/2021sp-final-project-idan-hila/test_coverage)


Link to Automatically Generated Sphinx Documentation: https://hip023.github.io/2021sp-final-project-idan-hila/index.html

Link to video: https://www.youtube.com/watch?v=g24RzWvGmZU&ab_channel=HilaPazHerszfang

Link to presentation: https://docs.google.com/presentation/d/1zoreOJfT8UlSWi5rYZbTVBS6YEZwn23axqGlHxx5LeE/edit?usp=sharing 

<img src="https://github.com/hip023/2021sp-final-project-idan-hila/blob/master/assets/UML.png?raw=true" alt="UML" width="500"/>


## Manual: Use It Yourself!
***
#### STEP 1: Install Elasticsearch

1.1 Go to: https://www.elastic.co/downloads/elasticsearch and download the proper version

1.2 Extract the files locally and run bin/elasticsearch

#### STEP 2: Update template.env file
Go to template.env and update secret keys
* hint: use this to use django secret key generator: https://djecrety.ir/

#### STEP 3: Run Luigi Pipeline
from your shell, run: 

```
pipenv run python -m final_project
```

#### STEP 4: Activate Django
from your shell, run:

```
cd SearchEngine
pipenv run python manage.py runserver 
```

