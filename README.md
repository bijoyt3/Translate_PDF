# Translate_PDF
This script takes a PDF input, extracts the text, detects the language, translates it to English, and prints the output to a text file.

## Libraries
I used Apache Tika (https://tika.apache.org/1.8/) to parse the PDF file and extract data and the Google Cloud Translate API (https://cloud.google.com/translate/) to perform the translation. 

### Tip #1 

Half of the battle during development was ensuring my credentials were being correctly read. The best way to verify your credentials with the API is to download the credentials.json file from the Google Cloud Console and place it wherever your Scripts folder resides. 

You can do this by going to the Cloud Console > IAM & Admin > Service Account. From here, you want to confirm you have a Compute instance up - if not, create one. Once created, click the 3 dots on the right > Create Key > Key Type: JSON > Create. You've successfully downloaded the credentials.json file. Place it in your Scripts directory and you're golden. To call the credentials in your code, use:
```
client = translate.TranslationServiceClient.from_service_account_json('credentials.json')
```

### Tip #2
You'll also need your Project ID handy - you can find this on the home page of Cloud Console under the Project Info tile. It is used as a parameter for the client functions, for example:
```
parent = f"projects/{project_id}/locations/{location}"

response = client.detect_language(
        content=text,
        parent=parent,
        mime_type="text/plain",
    )
```

### Tip #3

This approach DOES cost money! Fortunately, it is free up to 500k characters but be wary of the character limits (https://cloud.google.com/translate/pricing). A free alternative is GoogleTrans (https://pypi.org/project/googletrans/). It has the same functionality as the Google Cloud Translate API but you don't need to worry about credentials or costs. It may have its limitations relative to the Google Cloud Translate API so user beware but it's an option. 

## Acknowledgements

Adapted many lines of code from the Google Translate API Quickstart page - https://cloud.google.com/translate/docs/advanced/quickstart
