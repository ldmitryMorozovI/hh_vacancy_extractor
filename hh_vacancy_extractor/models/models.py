import json
import csv
import requests
from urllib.parse import urlencode
from typing import Dict, List, Optional, Any, Union

class HHRequestBuilder:
    """Model for building HH.ru API request parameters"""
    def __init__(self):
        self.params = {
            'host': 'hh.ru',
            'page': 0,
            'per_page': 100,
            'responses_count_enabled': 'true',
            'with_chat_info': 'true',
            'check_personal_data_resale': 'false',
            'with_skills_match': 'false'
        }
    
    def set_text(self, text: str) -> 'HHRequestBuilder':
        self.params['text'] = text
        return self
    
    def set_search_fields(self, fields: List[str]) -> 'HHRequestBuilder':
        if 'name' in fields or 'company_name' in fields or 'description' in fields:
            self.params['search_field'] = fields
        return self
    
    def set_only_with_salary(self, flag: bool) -> 'HHRequestBuilder':
        self.params['only_with_salary'] = 'true' if flag else 'false'
        return self
    
    def set_salary(self, amount: int, currency: str) -> 'HHRequestBuilder':
        self.params['salary'] = amount
        self.params['currency'] = currency.upper()
        return self
    
    def set_experience(self, experience_levels: List[str]) -> 'HHRequestBuilder':
        valid_levels = ['noExperience', 'between1And3', 'between3And6', 'moreThan6']
        filtered = [level for level in experience_levels if level in valid_levels]
        if filtered:
            self.params['experience'] = filtered
        return self
    
    def set_employment_form(self, forms: List[str]) -> 'HHRequestBuilder':
        valid_forms = ['FLY_IN_FLY_OUT', 'PROJECT', 'PART', 'FULL']
        filtered = [form for form in forms if form in valid_forms]
        if filtered:
            self.params['employment_form'] = filtered
        return self
    
    def set_accept_temporary(self, flag: bool) -> 'HHRequestBuilder':
        self.params['accept_temporary'] = 'true' if flag else 'false'
        return self
    
    def set_label(self, labels: List[str]) -> 'HHRequestBuilder':
        valid_labels = [
            'internship', 'night_shifts', 'accept_kids', 
            'accept_handicapped', 'not_from_agency', 
            'with_address', 'accredited_it'
        ]
        filtered = [label for label in labels if label in valid_labels]
        if filtered:
            self.params['label'] = filtered
        return self
    
    def set_work_schedule(self, schedules: List[str]) -> 'HHRequestBuilder':
        valid_schedules = [
            'WEEKEND', 'FIVE_ON_TWO_OFF', 'TWO_ON_TWO_OFF', 
            'SIX_ON_ONE_OFF', 'THREE_ON_THREE_OFF', 'FOUR_ON_FOUR_OFF',
            'FOUR_ON_THREE_OFF', 'FOUR_ON_TWO_OFF', 'THREE_ON_TWO_OFF',
            'TWO_ON_ONE_OFF', 'ONE_ON_THREE_OFF', 'ONE_ON_TWO_OFF',
            'FLEXIBLE', 'OTHER'
        ]
        filtered = [sched for sched in schedules if sched in valid_schedules]
        if filtered:
            self.params['work_schedule_by_days'] = filtered
        return self
    
    def set_working_hours(self, hours: List[str]) -> 'HHRequestBuilder':
        valid_hours = [
            'OTHER', 'FLEXIBLE', 'HOURS_24', 'HOURS_12', 
            'HOURS_11', 'HOURS_10', 'HOURS_9', 'HOURS_8',
            'HOURS_7', 'HOURS_6', 'HOURS_5', 'HOURS_4',
            'HOURS_3', 'HOURS_2'
        ]
        filtered = [hour for hour in hours if hour in valid_hours]
        if filtered:
            self.params['working_hours'] = filtered
        return self
    
    def set_work_format(self, formats: List[str]) -> 'HHRequestBuilder':
        valid_formats = ['ON_SITE', 'REMOTE', 'HYBRID', 'FIELD_WORK']
        filtered = [fmt for fmt in formats if fmt in valid_formats]
        if filtered:
            self.params['work_format'] = filtered
        return self
    
    def set_period(self, days: int) -> 'HHRequestBuilder':
        if days in [3, 7]:
            self.params['period'] = days
        return self
    
    def set_page(self, page: int) -> 'HHRequestBuilder':
        self.params['page'] = page
        return self
    
    def set_per_page(self, per_page: int) -> 'HHRequestBuilder':
        self.params['per_page'] = per_page
        return self
    
    def build(self) -> Dict:
        return self.params


class JsonToCsvBuilder:
    """Model for building JSON to CSV conversion configuration"""
    def __init__(self):
        self._config = {
            'input_file': None,
            'output_file': 'output.csv',
            'fields': None,
            'all_fields': False,
            'flatten_nested': True,
            'delimiter': ','
        }
    
    def with_input_file(self, input_file: str) -> 'JsonToCsvBuilder':
        self._config['input_file'] = input_file
        return self
    
    def with_output_file(self, output_file: str) -> 'JsonToCsvBuilder':
        self._config['output_file'] = output_file
        return self
    
    def with_fields(self, fields: List[str]) -> 'JsonToCsvBuilder':
        self._config['fields'] = fields
        return self
    
    def with_all_fields(self, all_fields: bool = True) -> 'JsonToCsvBuilder':
        self._config['all_fields'] = all_fields
        return self
    
    def with_flatten_nested(self, flatten: bool = True) -> 'JsonToCsvBuilder':
        self._config['flatten_nested'] = flatten
        return self
    
    def with_delimiter(self, delimiter: str) -> 'JsonToCsvBuilder':
        self._config['delimiter'] = delimiter
        return self
    
    def build(self) -> 'JsonToCsvExtractor':
        return JsonToCsvExtractor(**self._config)


class JsonToCsvExtractor:
    """Model for extracting data from JSON to CSV"""
    def __init__(self, input_file: str, output_file: str, fields: Optional[List[str]], 
                 all_fields: bool, flatten_nested: bool, delimiter: str):
        self.input_file = input_file
        self.output_file = output_file
        self.fields = fields
        self.all_fields = all_fields
        self.flatten_nested = flatten_nested
        self.delimiter = delimiter
        
    def extract(self) -> None:
        with open(self.input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if isinstance(data, dict) and 'items' in data:
            data = data['items']  # Handle HH.ru API response format
        
        if self.all_fields:
            self.fields = self._get_all_fields(data[0] if isinstance(data, list) else data)
        
        rows = []
        for item in (data if isinstance(data, list) else [data]):
            row = []
            for field in self.fields:
                value = self._get_nested_value(item, field)
                if self.flatten_nested and isinstance(value, (dict, list)):
                    value = self._flatten_value(value)
                row.append(value)
            rows.append(row)
        
        self._write_to_csv(rows)
    
    def _get_all_fields(self, data: Dict) -> List[str]:
        fields = []
        self._traverse_json(data, [], fields)
        return fields
    
    def _traverse_json(self, data: Any, path: List[str], fields: List[str]) -> None:
        if isinstance(data, dict):
            for key, value in data.items():
                new_path = path + [key]
                fields.append('.'.join(new_path))
                self._traverse_json(value, new_path, fields)
        elif isinstance(data, list) and data and isinstance(data[0], dict):
            for i, item in enumerate(data):
                new_path = path + [str(i)]
                self._traverse_json(item, new_path, fields)
    
    def _get_nested_value(self, data: Dict, field_path: str) -> Any:
        keys = field_path.split('.')
        value = data
        for key in keys:
            if isinstance(value, list) and key.isdigit():
                key = int(key)
                if key < len(value):
                    value = value[key]
                else:
                    return None
            elif isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return None
        return value
    
    def _flatten_value(self, value: Any) -> str:
        if isinstance(value, dict):
            return '; '.join(f"{k}: {v}" for k, v in value.items())
        elif isinstance(value, list):
            if all(isinstance(x, str) for x in value):
                return ', '.join(value)
            elif all(isinstance(x, dict) for x in value) and value:
                keys = value[0].keys()
                return ' | '.join(
                    ', '.join(f"{k}: {item.get(k, '')}" for k in keys)
                    for item in value
                )
            else:
                return ', '.join(str(x) for x in value)
        return str(value)
    
    def _write_to_csv(self, rows: List[List[Any]]) -> None:
        with open(self.output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=self.delimiter)
            writer.writerow(self.fields)
            writer.writerows(rows)


class HHDataFetcher:
    """Model for fetching data from HH.ru API"""
    @staticmethod
    def fetch_vacancies(params: Dict, pages: Optional[Union[int, List[int]]] = None) -> Optional[Dict]:
        base_url = "https://api.hh.ru/vacancies"
        all_results = {'items': [], 'found': 0, 'pages': 0}
        
        if pages is None:
            query_string = urlencode(params, doseq=True)
            url = f"{base_url}?{query_string}"
            
            try:
                response = requests.get(url)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                print(f"Error fetching data: {e}")
                return None
        else:
            if isinstance(pages, int):
                pages = [pages]
            
            for page in pages:
                params['page'] = page
                query_string = urlencode(params, doseq=True)
                url = f"{base_url}?{query_string}"
                
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    data = response.json()
                    
                    if page == pages[0]:
                        all_results['found'] = data.get('found', 0)
                        all_results['pages'] = data.get('pages', 0)
                    
                    all_results['items'].extend(data.get('items', []))
                except requests.exceptions.RequestException as e:
                    print(f"Error fetching page {page}: {e}")
                    continue
            
            return all_results