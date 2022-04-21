# Spam-Email-Detection-withML
Intelligent spam email detection system with automatic response

With an implemented Machine Learning model that predicts whether an email message is spam or not, upon the receipt of email, the system can automatically flag whether the incoming emails is spam or not based on the prediction result obtained from the ML model, and immediately send back an email response containing the basic info about the incoming emails, including date, time, subject, email body, confidence score, and the tag Spam/Not Spam.


## AWS architecture
- Sagemaker: train ML model and provide prediction endpoint
- Lambda Function: implement the logic of getting email info, getting prediction result, formulating and sending back response
- SES: provide the verified domain to receive emails
- S3: store the received emails put by SES


## How to test
- Verify email address in AWS SES and record it as a verified identity
- Use the above verified email address to send an email message to email@emaildetect.com
- Wait for the response
