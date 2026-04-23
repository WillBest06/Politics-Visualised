import json
import arrow

def main_parser(raw_json):
    file = json.loads(raw_json)

    return {
        'metadata': extract_metadata(file),
        'countries': extract_country_data(file),
        'regions': extract_regions_data(file),
        'constituencies': extract_constituencies_data(file)
    }

def extract_metadata(file):
    attributes = file['data']['attributes']

    return {
        'id': file['data']['id'],
        'title': attributes['action'],
        'state': attributes['state'],
        'background': attributes['background'],
        'additional_details': attributes['additional_details'],
        'signature_count': attributes['signature_count'],
        'dates': {
            'created_at': format_date(attributes.get('created_at')),
            'response_threshold_reached_at': format_date(attributes.get('response_threshold_reached_at')),
            'government_response_at': format_date(attributes.get('government_response_at')),
            'debate_threshold_reached_at': format_date(attributes.get('debate_threshold_reached_at')),
            'scheduled_debate_date': format_date(attributes.get('scheduled_debate_date')),
        },
        'departments': attributes['departments']
    }

def extract_country_data(file):
    countries = file['data']['attributes']['signatures_by_country']

    sorted_countries = sorted(countries, key=lambda x: x['signature_count'], reverse=True)

    labels = []
    values = []

    # sort by top 10 countries to avoid overcrowding chart
    for c in sorted_countries[:10]:
        labels.append(c['name'])
        values.append(c['signature_count'])

    return {
        'graph_name': 'Signatures by country',
        'labels': labels,
        'values': values
    }

def extract_regions_data(file):
    regions = file['data']['attributes']['signatures_by_region']

    sorted_regions = sorted(regions, key=lambda x: x['signature_count'], reverse=True)

    labels = []
    values = []
    for r in sorted_regions:
        labels.append(r['name'])
        values.append(r['signature_count'])

    return {
        'graph_name': 'Signatures by region',
        'labels': labels,
        'values': values
    }
    
def extract_constituencies_data(file):
    constituencies = file['data']['attributes']['signatures_by_constituency']

    sorted_constituencies = sorted(constituencies, key=lambda x: x['signature_count'], reverse=True)

    labels = []
    values = []

    # sort by top 10 constituencies to avoid overcrowding chart
    for c in sorted_constituencies[:10]:
        labels.append(c['name'])
        values.append(c['signature_count'])

    return {
        'graph_name': 'Signatures by constituency',
        'labels': labels,
        'values': values
    }

def format_date(iso_string):
    if not iso_string:
        return "N/A"
    
    try:
        dateObject = arrow.get(iso_string)
        
        return dateObject.format('D MMMM YYYY')
        
    except Exception:
        return "N/A"