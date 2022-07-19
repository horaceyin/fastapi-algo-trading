from enum import Enum
from typing import Optional
from pydantic import BaseModel, root_validator ,validator, StrictInt
from schemas.backtesting.indicator_schemas import Indicator

class TimeConverter(Enum):
    day = 86400
    hour = 3600
    minute = 60
    second = 1

def range_checking_and_convertion(input_time, bar_type):
    if input_time < 1 or input_time > 60:
        raise ValueError(f'Please enter an integer of 1 to 60.')

    ret = input_time * TimeConverter[bar_type].value

    if bar_type == 'second':
        if input_time % 5 != 0:
            raise ValueError(f'Please enter a multiple of 5.')
    elif bar_type == 'hour':
        if input_time < 1 or input_time > 24:
            raise ValueError(f'Please enter a integer of 1 to 24.')
    elif bar_type == 'day':
        if input_time != 1:
            raise ValueError(f'Bar summary for {bar_type} only allow 1 day.')
            
    return ret

class BarSummary(BaseModel):
    day: Optional[bool] = False
    hour: Optional[bool] = False
    minute: Optional[bool] = False
    second: Optional[bool] = True
    input_time: StrictInt = 5

    @root_validator
    def check_exclusive(cls, values):
        input_time = values.get('input_time')

        true_count = 0
        bar_type = None
        bar_is_not_selected = True

        for key, val in list(values.items()):
            if key in TimeConverter.__members__ and val == True:
                bar_is_not_selected = False
                true_count += 1
                bar_type = key

        if bar_is_not_selected: raise ValueError('Please select ones of the bar summary.')

        if true_count > 1: raise ValueError('Only one bar summary should be selected.')

        time_in_sec = range_checking_and_convertion(input_time, bar_type)
        
        values['input_time'] = time_in_sec

        return values