from django.shortcuts import render

from templates.main_page.database_uploading import main_upload
import templates.main_page.request_creation as r


def index(request):
    # first url anyway will be created
    url = r.url_creation()
    while (True):
        # create response with url
        response = r.response(url)
        # upload all information into db
        main_upload(response)
        # check for the next page
        if 'next_page_token' in response:
            token = response['next_page_token']
            # if next page is exist we redefine url
            url = r.url_creation(token)
        else:
            break

    return render(request, "main_page/index.html")
