from views.views import ConsoleView
import argparse
from models.models import *

class HHDataController:
    """Controller for HH.ru data fetching operations"""
    def __init__(self, view: ConsoleView):
        self.view = view
        self.builder = HHRequestBuilder()
    
    def build_request(self, args: argparse.Namespace) -> Dict:
        if args.text:
            self.builder.set_text(args.text)
        if args.search_fields:
            self.builder.set_search_fields(args.search_fields)
        if args.only_with_salary:
            self.builder.set_only_with_salary(True)
        if args.salary and args.currency:
            self.builder.set_salary(args.salary, args.currency)
        if args.experience:
            self.builder.set_experience(args.experience)
        if args.employment_form:
            self.builder.set_employment_form(args.employment_form)
        if args.accept_temporary:
            self.builder.set_accept_temporary(True)
        if args.label:
            self.builder.set_label(args.label)
        if args.work_schedule:
            self.builder.set_work_schedule(args.work_schedule)
        if args.working_hours:
            self.builder.set_working_hours(args.working_hours)
        if args.work_format:
            self.builder.set_work_format(args.work_format)
        if args.period:
            self.builder.set_period(args.period)
        if args.page is not None:
            self.builder.set_page(args.page)
        if args.per_page:
            self.builder.set_per_page(args.per_page)
        
        params = self.builder.build()
        self.view.display_parameters(params)
        return params
    
    def fetch_data(self, params: Dict, pages: Optional[List[int]], output_file: str) -> bool:
        result = HHDataFetcher.fetch_vacancies(params, pages)
        
        if result:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            if pages:
                self.view.display_success(
                    f"Fetched {len(result.get('items', []))} vacancies from {len(pages)} pages to {output_file}"
                )
            else:
                self.view.display_success(
                    f"Fetched {len(result.get('items', []))} vacancies to {output_file}"
                )
            return True
        else:
            self.view.display_error("Failed to fetch data")
            return False


class JsonToCsvController:
    """Controller for JSON to CSV conversion operations"""
    def __init__(self, view: ConsoleView):
        self.view = view
    
    def convert_to_csv(self, args: argparse.Namespace) -> bool:
        if not args.all and not args.fields:
            self.view.display_error("You must specify either --all or --fields")
            return False
        
        builder = JsonToCsvBuilder()
        extractor = (builder
                    .with_input_file(args.input)
                    .with_output_file(args.output)
                    .with_delimiter(args.delimiter)
                    .with_flatten_nested(args.no_flatten))
        
        if args.all:
            extractor = builder.with_all_fields().build()
        else:
            extractor = builder.with_fields(args.fields).build()
        
        extractor.extract()
        self.view.display_success(f"Data extracted to {args.output}")
        return True