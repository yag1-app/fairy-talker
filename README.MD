# Fairy_Webhook

DialogFlow ES backend service on Cloud Function

## HOW TO Deploy

```
gcloud functions deploy fairy_webhook \
 --runtime python311 \
 --trigger-http \
 --entry-point webhook \
 --allow-unauthenticated \
 --set-env-vars DIALOGFLOW_PROJECT_ID="YOUR-PROJECT-ID", LINE_CHANNEL_ACCESS_TOKEN="YOUR/TOKEN" \
 --region=us-central1
```


# Service URL

https://us-central1-fairybot-463913.cloudfunctions.net/fairy_webhook
