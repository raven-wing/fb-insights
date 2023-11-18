import argparse
import fb_api
import google_sheet_api


def parse_arguments():
    parser = argparse.ArgumentParser(description='Facebook Insights')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--use-page-token', action='store_true', help='Use Facebook Page Access Token')
    group.add_argument('--use-app-secret', action='store_true', help='Use Facebook App Secret')

    parser.add_argument('--page-id', type=str, help='Facebook Page ID')
    parser.add_argument('--access-token', type=str, help='Facebook Page Access Token')
    parser.add_argument('--app-id', type=str, help='Facebook App ID')
    parser.add_argument('--app-secret', type=str, help='Facebook App Secret')

    parser.add_argument('--spreadsheet-id', type=str, help='Google Spreadsheet ID', required=True)

    parser.add_argument('--start-date', type=str, help='Start date', required=True)
    parser.add_argument('--end-date', type=str, help='End date', required=True)

    args = parser.parse_args()

    if args.use_page_token and (not args.page_id or not args.access_token):
        parser.error("--use-page-token requires --page-id and --access-token.")

    if args.use_app_secret and (not args.app_id or not args.app_secret):
        parser.error("--use-app-secret requires --app-id and --app-secret.")

    return args


def main():
    args = parse_arguments()
    if args.use_page_token:
        date_range = fb_api.DateRange(args.start_date, args.end_date)
        insights = fb_api.get_facebook_page_insights(args.page_id, args.access_token, date_range=date_range)
        output = fb_api.parse_insights(insights)
        for metric_name, values in output.items():
            google_sheet_api.upload_data(metric_name, values, args.spreadsheet_id)


if __name__ == "__main__":
    main()
