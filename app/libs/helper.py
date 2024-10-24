import base64
import uuid
import pytz
import json
import os

import xml.etree.ElementTree as ET

from datetime import datetime, timezone, timedelta

def iter_all_items(products):
    for product in products:
        yield product
    
    while products.has_next_page():
        products = products.next_page()
        for product in products:
            yield product

def orderDateFormat(created_at):
    # Parse the string into a datetime object
    dt = datetime.strptime(created_at[:10], "%Y-%m-%d")

    # Format the datetime object into the desired string format
    return dt.strftime("%Y-%m-%d")

def getDiscountPercentage(original, discount):
    original = float(original)
    discount = float(discount)

    if(discount):
        percentage = ((original - discount) / original) * 100
    else:
        percentage = 0

    return percentage

def get_basic_auth_header(client_id, client_secret):
    # Combine client_id and client_secret with a colon
    auth_string = f"{client_id}:{client_secret}"
    
    # Encode the combined string to Base64
    encoded_auth_string = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
    
    # Create the Authorization header
    auth_header = f"Basic {encoded_auth_string}"
    
    return auth_header

def generate_correlation_id():
    # Generate a UUID for WM_QOS.CORRELATION_ID
    correlation_id = str(uuid.uuid4())
    return correlation_id

def xml_to_dict(element):
    return {
        element.tag: (
            {child.tag: xml_to_dict(child) for child in element} if element else element.text
        )
    }

async def write_json(data, path):
    # Define the path to the temp directory
    temp_dir = '/tmp'  # Use the /tmp directory for writing files
    file_path = os.path.join(temp_dir, path)  # Join the temp directory with the given path

    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Convert data to a JSON string with indentation for readability
    json_object = json.dumps(data, indent=4)

    # Write the JSON data to the specified file
    with open(file_path, 'w') as outfile:
        outfile.write(json_object)

    return file_path

def currentTime():
    # Get the current time in UTC
    now_utc = datetime.now(timezone.utc)

    # Format the time according to the required format
    timestamp = now_utc.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    return timestamp

# Current date in YYYY-MM-DD
def currentDate():
    return datetime.now().strftime('%Y-%m-%d')

# Start and End date of $this week YYYY-MM-DD
def weekDate():
    # Get today's date
    today = datetime.now()

    # Calculate the start and end of the week
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday

    # Format the dates
    start_of_week_str = start_of_week.strftime('%Y-%m-%d')
    end_of_week_str = end_of_week.strftime('%Y-%m-%d')

    return {"start": start_of_week_str, "end": end_of_week_str}

def monthDates():
    # Get today's date
    today = datetime.now()

    # Get the start of the month (first day)
    start_of_month = today.replace(day=1)

    # Calculate the end of the month
    # To get the last day, move to the first day of the next month and subtract one day
    if today.month == 12:
        next_month = today.replace(year=today.year + 1, month=1, day=1)
    else:
        next_month = today.replace(month=today.month + 1, day=1)
    end_of_month = next_month - timedelta(days=1)

    # Format the dates
    start_of_month_str = start_of_month.strftime('%Y-%m-%d')
    end_of_month_str = end_of_month.strftime('%Y-%m-%d')

    return {"start": start_of_month_str, "end": end_of_month_str}

def timeFrom():
    # Get the current time in UTC
    now_utc = datetime.now(timezone.utc)

    # Subtract 120 days from the current time
    time_120_days_ago = now_utc - timedelta(days=119)

    # Format the time according to the required format
    timestamp_120_days_ago = time_120_days_ago.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    return timestamp_120_days_ago

def timeTo():
    # Get the current time in UTC
    now_utc = datetime.now(timezone.utc)

    # Add 120 days to the current time
    time_120_days_later = now_utc + timedelta(days=120)

    # Format the time according to the required format
    timestamp_120_days_later = time_120_days_later.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    return timestamp_120_days_later

def strip_namespace(tag):
    """Helper function to remove namespace from XML tags."""
    if '}' in tag:
        return tag.split('}', 1)[1]  # Removes the namespace
    return tag

def api_xml_to_dict(element):
    """Converts XML element and its children into a dictionary."""
    result = {}
    
    # If the element has children
    if len(element):
        for child in element:
            child_dict = api_xml_to_dict(child)
            # Handle multiple children with the same tag by converting them into lists
            child_tag = strip_namespace(child.tag)
            if child_tag in result:
                if isinstance(result[child_tag], list):
                    result[child_tag].append(child_dict)
                else:
                    result[child_tag] = [result[child_tag], child_dict]
            else:
                result[child_tag] = child_dict
    else:
        # If the element has no children, check if it's an empty tag
        result = element.text if element.text is not None else ""

    # Add attributes (if any) to the dictionary
    if element.attrib:
        result = {"_attributes": element.attrib, "_content": result}

    # Check if the result is empty for specific tags
    if strip_namespace(element.tag) == "ItemArray" and not result:
        result = []  # Assign empty list for empty ItemArray

    return result

def xml_to_json(xml_string):
    """Parses XML string and converts it to JSON."""
    # Parse the XML string
    root = ET.fromstring(xml_string)
    
    # Convert XML to dictionary
    xml_dict = {strip_namespace(root.tag): api_xml_to_dict(root)}
    
    # Convert dictionary to JSON
    json_data = json.dumps(xml_dict, indent=4)
    return json_data

def timeZoneTimeStamp():
    # Define Central Time timezone
    tz = pytz.timezone('America/Chicago')  # Central Time

    # Get the current time with the specified timezone
    current_time = datetime.now(tz)

    # Format the current time in the desired format
    formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%S.%f%z')

    # Insert the colon in the timezone offset (e.g., "-06:00")
    formatted_time = formatted_time[:-2] + ':' + formatted_time[-2:]

    return formatted_time