import datetime
from typing import Tuple
from zoneinfo import ZoneInfo

class DateService:
    """Service for handling date calculations for stock data retrieval."""
    
    @staticmethod
    def get_period() -> Tuple[datetime.datetime, datetime.datetime]:
        """
        Get the period start and end dates for stock data retrieval.
        
        Returns:
            Tuple[datetime.datetime, datetime.datetime]: (start_date, end_date)
            - end_date: Previous business day (not Saturday or Sunday)
            - start_date: One month prior to the end_date
        """
        # Get current date in EST timezone
        try:
            est = ZoneInfo('America/New_York')
        except:
            # Fallback to UTC if timezone is not available
            est = ZoneInfo('UTC')
        current_date = datetime.datetime.now(est).date()
        
        # Find the previous business day (not Saturday or Sunday)
        end_date = current_date - datetime.timedelta(days=1)
        
        # If it's Sunday (weekday 6), go back to Friday
        if end_date.weekday() == 6:  # Sunday
            end_date = end_date - datetime.timedelta(days=2)
        # If it's Saturday (weekday 5), go back to Friday  
        elif end_date.weekday() == 5:  # Saturday
            end_date = end_date - datetime.timedelta(days=1)
        
        # Calculate start date as one month prior
        # Handle month rollover by going to the first day of current month, 
        # then subtracting one day to get last day of previous month
        if end_date.month == 1:
            start_year = end_date.year - 1
            start_month = 12
        else:
            start_year = end_date.year
            start_month = end_date.month - 1
        
        # Try to use the same day, but handle month-end edge cases
        try:
            start_date = end_date.replace(year=start_year, month=start_month)
        except ValueError:
            # Handle cases where the day doesn't exist in the target month (e.g., Jan 31 -> Feb 31)
            # Use the last day of the target month instead
            if start_month == 12:
                next_month_year = start_year + 1
                next_month = 1
            else:
                next_month_year = start_year
                next_month = start_month + 1
            
            # Get the last day of the target month
            first_day_next_month = datetime.date(next_month_year, next_month, 1)
            start_date = first_day_next_month - datetime.timedelta(days=1)
        
        # Convert to datetime objects with timezone info
        start_datetime = datetime.datetime.combine(start_date, datetime.time.min).replace(tzinfo=est)
        end_datetime = datetime.datetime.combine(end_date, datetime.time.max).replace(tzinfo=est)
        
        return start_datetime, end_datetime
