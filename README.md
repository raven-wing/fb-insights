# Facebook Page Insights to Google Sheets

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This Python script allows you to download insights from a Facebook page using the Facebook Graph API
and write them to a google spreadsheet. It retrieves data such as page impressions and engaged users.

## Setup

1. **Create a Facebook App:**
    - Go to the [Facebook Developers](https://developers.facebook.com/) website and create a new app.

2. **Obtain Access Token:**
    - Use the [Graph API Explorer](https://developers.facebook.com/tools/explorer/) to generate a user access token with the required permissions.
    - Select your app, click on "Get Token," and choose "Get User Access Token."
    - Grant the necessary permissions:
      - `pages_read_engagement`
      - `read_insights`
      - `business_management`
      - `pages_show_list`

3. **Retrieve Page ID:**
    - Use the Graph API Explorer or other methods to obtain the Page ID of the Facebook page you want to analyze.

4. **Obtain credentials.json for google sheets:**
    - Follow the instructions [here](https://developers.google.com/sheets/api/quickstart/python) to
   obtain `credentials.json` for google sheets.

5. **Install Dependencies:**
   ```bash
    poetry install
   ```

## Usage

```bash
  poetry run python main.py --page-id YOUR_PAGE_ID --access-token YOUR_ACCESS_TOKEN --spreadsheet-id YOUR_SPREADSHEET_ID --use-page-token
```

Replace YOUR_PAGE_ID and YOUR_ACCESS_TOKEN with the actual Page ID and access token obtained in the previous steps.

## Options
* `--page-id`: The ID of the Facebook page you want to analyze.
* `--access-token`: The access token generated in the previous steps.
* `--spreadsheet-id`: The ID of the google spreadsheet you want to write the data to.
* `--use-page-token`: Use the page access token instead of the user access token.
