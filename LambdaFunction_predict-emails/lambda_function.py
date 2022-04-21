import json
import boto3
import email
import urllib.parse
import sms_spam_classifier_utilities as utilities

def lambda_handler(event, context):
    # bucket = 's3hmw3'
    # key = 'mm09ot5a3hdh8rtm15ciacu1n1cuaj5vbecgkd01'
    print(event)
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    vocabulary_length = 9013
    session = boto3.Session()
    s3 = session.client('s3')
    ses = session.client('ses')
    endpoint_name = 'sms-spam-classifier-mxnet-2022-04-14-19-42-21-300'
    runtime = session.client('runtime.sagemaker')

    response = s3.get_object(Bucket=bucket, Key=key)
    email_message = email.message_from_bytes(response['Body'].read())
    recipient = email_message.get('From')
    body = email_message.get_payload()[0].get_payload()
    msg_body = body[:240]
    date = email_message.get('Date')
    subject = email_message.get('Subject')
    To = email_message.get('To')
    print(email_message)
    print(recipient)
    print(body)
    
    mail_sent = [body.strip()]
    ohe = utilities.one_hot_encode(mail_sent, vocabulary_length)
    mail_sent = utilities.vectorize_sequences(ohe, vocabulary_length)
    data = json.dumps(mail_sent.tolist())
    msg = runtime.invoke_endpoint(EndpointName=endpoint_name, ContentType='application/json', Body=data)
    print(msg)

    result = json.loads(msg["Body"].read().decode('utf-8'))
    print(result)
    
    pred_res = result['predicted_label'][0][0]
    if pred_res == 1:
        CLASSIFICATION = 'Spam'
    elif pred_res == 0:
        CLASSIFICATION = 'Not Spam'
    CLASSIFICATION_CONFIDENCE_SCORE = str(float(result['predicted_probability'][0][0])*100)

    message = "We received your email sent at " + date + " with the subject " + subject + ".\nHere is a 240 character sample of the email body:\n" + msg_body + "\nThe email was categorized as " + CLASSIFICATION + " with a " + str(CLASSIFICATION_CONFIDENCE_SCORE) + "% confidence."
    print(message)
    
    response_email = ses.send_email(
        Destination={'ToAddresses': [recipient]},
        Message={
            'Body': {
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': message,
                },
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': 'Spam detection',
            },
        },
        Source = To,
    )
    print(response_email)
    return {
        'statusCode': 200,
        'body': json.dumps('Completed email detection and sent reply!')
    }
