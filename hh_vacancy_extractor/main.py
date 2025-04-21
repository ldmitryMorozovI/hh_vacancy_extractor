
import argparse
from views.views import ConsoleView
from controllers.controllers import HHDataController, JsonToCsvController
from models.models import *

def setup_parser() -> argparse.ArgumentParser:
    """Setup the command line argument parser"""
    parser = argparse.ArgumentParser(
        description='HH.ru Data Fetcher and JSON to CSV Converter'
    )
    
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # HH.ru API Parser
    fetch_parser = subparsers.add_parser('fetch', help='Fetch data from HH.ru API')
    fetch_parser.add_argument('--text', type=str, help='Search text for vacancy')
    fetch_parser.add_argument('--search-fields', nargs='+', 
                             choices=['name', 'company_name', 'description'],
                             help='Fields to search in')
    fetch_parser.add_argument('--only-with-salary', action='store_true',
                             help='Only show vacancies with salary')
    fetch_parser.add_argument('--salary', type=int, help='Minimum salary amount')
    fetch_parser.add_argument('--currency', choices=['RUB', 'USD', 'EUR'], 
                             help='Salary currency')
    fetch_parser.add_argument('--experience', nargs='+',
                             choices=['noExperience', 'between1And3', 
                                     'between3And6', 'moreThan6'],
                             help='Required experience level')
    fetch_parser.add_argument('--employment-form', nargs='+',
                             choices=['FLY_IN_FLY_OUT', 'PROJECT', 'PART', 'FULL'],
                             help='Employment form')
    fetch_parser.add_argument('--accept-temporary', action='store_true',
                             help='Accept temporary work')
    fetch_parser.add_argument('--label', nargs='+',
                             choices=['internship', 'night_shifts', 'accept_kids',
                                     'accept_handicapped', 'not_from_agency',
                                     'with_address', 'accredited_it'],
                             help='Special labels')
    fetch_parser.add_argument('--work-schedule', nargs='+',
                             choices=['WEEKEND', 'FIVE_ON_TWO_OFF', 'TWO_ON_TWO_OFF',
                                     'SIX_ON_ONE_OFF', 'THREE_ON_THREE_OFF', 
                                     'FOUR_ON_FOUR_OFF', 'FOUR_ON_THREE_OFF',
                                     'FOUR_ON_TWO_OFF', 'THREE_ON_TWO_OFF',
                                     'TWO_ON_ONE_OFF', 'ONE_ON_THREE_OFF',
                                     'ONE_ON_TWO_OFF', 'FLEXIBLE', 'OTHER'],
                             help='Work schedule')
    fetch_parser.add_argument('--working-hours', nargs='+',
                             choices=['OTHER', 'FLEXIBLE', 'HOURS_24', 'HOURS_12',
                                     'HOURS_11', 'HOURS_10', 'HOURS_9', 'HOURS_8',
                                     'HOURS_7', 'HOURS_6', 'HOURS_5', 'HOURS_4',
                                     'HOURS_3', 'HOURS_2'],
                             help='Working hours')
    fetch_parser.add_argument('--work-format', nargs='+',
                             choices=['ON_SITE', 'REMOTE', 'HYBRID', 'FIELD_WORK'],
                             help='Work format')
    fetch_parser.add_argument('--period', type=int, choices=[3, 7],
                             help='Vacancy freshness in days')
    fetch_parser.add_argument('--page', type=int, 
                             help='Specific page number to fetch (0-based)')
    fetch_parser.add_argument('--pages', type=int, nargs='+',
                             help='List of specific pages to fetch (0-based)')
    fetch_parser.add_argument('--per-page', type=int, 
                             help='Number of vacancies per page (default: 100)')
    fetch_parser.add_argument('--all-pages', action='store_true',
                             help='Fetch all available pages')
    fetch_parser.add_argument('--output', type=str, default='output.json',
                             help='Output JSON file name')
    
    # JSON to CSV Parser
    convert_parser = subparsers.add_parser('convert', help='Convert JSON to CSV')
    convert_parser.add_argument('input', help='Input JSON file path')
    convert_parser.add_argument('-o', '--output', default='output.csv', 
                               help='Output CSV file path')
    convert_parser.add_argument('-a', '--all', action='store_true',
                               help='Extract all fields from JSON')
    convert_parser.add_argument('-f', '--fields', nargs='+', 
                               help='Specific fields to extract (dot notation for nested)')
    convert_parser.add_argument('-d', '--delimiter', default=',',
                               help='CSV delimiter character')
    convert_parser.add_argument('--no-flatten', action='store_false',
                               help='Do not flatten nested structures')
    
    return parser


def main():
    parser = setup_parser()
    args = parser.parse_args()
    view = ConsoleView()
    
    if args.command == 'fetch':
        controller = HHDataController(view)
        params = controller.build_request(args)
        
        pages_to_fetch = None
        if args.pages:
            pages_to_fetch = args.pages
        elif args.page is not None:
            pages_to_fetch = [args.page]
        elif args.all_pages:
            temp_params = params.copy()
            temp_params['page'] = 0
            temp_params['per_page'] = 1
            initial_data = HHDataFetcher.fetch_vacancies(temp_params)
            if initial_data:
                total_pages = initial_data.get('pages', 1)
                pages_to_fetch = list(range(total_pages))
                view.display_message(f"Fetching all {total_pages} pages...")
        
        controller.fetch_data(params, pages_to_fetch, args.output)
    
    elif args.command == 'convert':
        controller = JsonToCsvController(view)
        controller.convert_to_csv(args)


if __name__ == "__main__":
    main()