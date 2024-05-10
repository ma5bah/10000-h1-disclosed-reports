import json

import requests

# GraphQL query
j = 0
while j < 20000000:
    graphql_query = {
        "operationName": "CompleteHacktivitySearchQuery",
        "variables": {          
            "queryString": "*:*",
            "size":25,
            "from":0+j,
            "sort":{
                "field":"disclosed_at",
                "direction":"DESC"
                }, 
            "product_area":"hacktivity",
            "product_feature":"overview"
            },
        "query": "query CompleteHacktivitySearchQuery($queryString: String!, $from: Int, $size: Int, $sort: SortInput!) {   me {     id     __typename   }   search(     index: CompleteHacktivityReportIndexService     query_string: $queryString     from: $from     size: $size     sort: $sort   ) {     __typename     total_count     nodes {       __typename       ... on CompleteHacktivityReportDocument {         id         _id         reporter {           id           name           username           ...UserLinkWithMiniProfile           __typename         }         cve_ids         cwe         severity_rating         upvoted: upvoted_by_current_user         public         report {           id           databaseId: _id           title           substate           url           disclosed_at           report_generated_content {             id             hacktivity_summary             __typename           }           __typename         }         votes         team {           handle           name           medium_profile_picture: profile_picture(size: medium)           url           id           currency           ...TeamLinkWithMiniProfile           __typename         }         total_awarded_amount         latest_disclosable_action         latest_disclosable_activity_at         submitted_at         disclosed         has_collaboration         __typename       }     }   } }  fragment UserLinkWithMiniProfile on User {   id   username   __typename }  fragment TeamLinkWithMiniProfile on Team {   id   handle   name   __typename } "
    }

    # URL of the GraphQL endpoint
    graphql_endpoint = 'https://hackerone.com/graphql'

    # Send POST request with GraphQL query
    response = requests.post(graphql_endpoint, json=graphql_query)

    # Print response content
    if response.status_code == 200:
        data = response.json()
        print(data)
        with open('h1reports.txt', 'a') as f:
            for i in data["data"]["search"]['nodes']:
                print(i['report']['url'])
                f.write(i['report']['url'] + '\n')
        
    else:
        print(f"Request failed with status code: {response.status_code}")

    j += 25
