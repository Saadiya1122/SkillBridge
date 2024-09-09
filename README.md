# SkillBridge: AI-Driven Resume Skill Gap Analysis

## Overview
**SkillBridge** is an AI-powered web application designed to assist job seekers in identifying gaps between their current skills and the requirements of their desired job roles. By leveraging Natural Language Processing (NLP) and Machine Learning (ML), SkillBridge compares uploaded resumes and job descriptions, highlighting the skills that are missing and providing tailored course recommendations to help users close those gaps.

## Features
- Upload resumes in PDF, DOCX, or HTML format.
- Input job descriptions to analyze and compare against resumes.
- Uses Machine Learning models (Random Forest, Logistic Regression, and SVM) for classification.
- Identifies missing skills by comparing the user's resume with the job description.
- Provides course and article recommendations for missing skills.
- Users can download a skill gap report in PDF format.
- Real-time analysis and quick response for skill matching and gap identification.

## Project Setup Instructions

After cloning the repository, you need to manually create two folders to organize the files:

1. Create a `templates` folder:
   - This folder should contain the HTML files.
   - Upload the following files into the `templates` folder:
     - `landing.html`
     - `upload.html`
     - `analyze.html`
     - `results.html`

   You can create the folder via the terminal:
   ```bash
   mkdir templates

2. Create a static folder:

This folder should contain static assets like CSS files and videos.
Upload the following files into the static folder:

- style.css
- loop_video.mp4

To create the folder:

```bash
mkdir static

## Installation

### Prerequisites
- Python 3.x
- Flask (for running the web application)

### Steps to Install and Run:
1. Clone the repository:
   
   ```bash
   git clone https://github.com/your-username/SkillBridge.git
   cd SkillBridge
   
2. Install required Packages:

Make sure you have Python installed, then install the required libraries by running :
pip install -r requirements.txt
   
3. Run the application:

Once the dependencies are installed, run the Flask application:
python app.py 


### How to Use the README:
1. Replace `your-username` in the `git clone` URL with your GitHub username.
2. Make sure to edit the **Known Issues** section if there are specific limitations you want to mention.
3. The **Future Work** section can be expanded based on your own plans for enhancing the project.

This README file provides clear instructions on what the project is, how to install it, and how to use it, making it helpful for others who want to contribute or explore the project.
