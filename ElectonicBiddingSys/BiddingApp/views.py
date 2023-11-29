import time
from django.utils import timezone
from datetime import timedelta
from django.db import OperationalError
from django.shortcuts import redirect, render
from django.db import connection
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Max
from decimal import Decimal
from openai import OpenAI
from django.http import HttpResponseForbidden
import json
import random
import django.http

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# need to be improve, ask TA to get a api_key
# This is for chatbox, didn't finished yet

api_key = ""

openAIDescription = "This is sql, and table name is 空的, the coulum name is item_id, item_name, item_material(lower case), category(First charater is upper case, and it is plural, for example Rings), " \
                    "item_condition(it contains two type Brand New and Used), item_brand(First character is upper case), is_active(0 or 1), description, starting_ price, " \
                    "user_id_id, date_created"

# Create your models here.
def dashboard(request):
    return render(request, 'homepage_start.html')
def executeSQLQuery(sql_query):
    if not sql_query:
        print("SQL Query is null or empty")
        raise ValueError("SQL query must be a non-empty string")

    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        results = cursor.fetchall()

    print(results)
    # for p in Jewelry.objects.raw(sql_query):
    #     results.append(p)
    return results
def chatbot(request):
    chatbot_response = None
    print("test")
    print(request.method)
    if api_key is not None and request.method == 'POST':
        client = OpenAI(
            api_key=api_key
        )

        user_input = request.POST.get('user_input')
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": user_input,
                }
            ],
            model="gpt-3.5-turbo",
            functions=[
                {
                    "name": "query_database",
                    "description": user_input,
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "sql": {
                                "type": "string",
                                "description": openAIDescription,
                            },
                            # "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                        },
                        "required": ["sql"],
                    },
                }
            ],
            function_call='none',
        )

        print("response-----------------here")
        print(response)
        print(type(response))
        print("sql_message----------------here")
        ## response.choices[0].message.content
        print(response.choices[0])
        print(response.choices[0].message)
        print(response.choices[0].message.content)
        sql_message = response.choices[0].message.content
        start_index = sql_message.find('{')
        end_index = sql_message.find('}', start_index)

        if start_index != -1 and end_index != -1:
            sql_json = sql_message[start_index:end_index + 1]
        else:
            sql_json = None

        json_object = None
        if sql_json is not None:
            try:
                json_object = json.loads(sql_json)
            except Exception as e:
                sql_data = ["Invalid Input"]
                return render(request, 'chatbox.html', {'chatbox_data': sql_data})
        else:
            sql_data = ["Invalid Input"]
            return render(request, 'chatbox.html', {'chatbox_data': sql_data})

        sql = json_object["sql"]
        print("sql query here --------------- here")
        print(sql)
        try:
            sql_data = executeSQLQuery(sql)
        except ValueError as ve:
            print("SQL Query is null or empty")
        except OperationalError as e:
            print("bad luck")
        except Exception as e:
            print("bad luck")
        print("sql data -----------------here ")
        print(sql_data)
        if not sql_data:
            sql_data = ["Noting found in database"]
            print("you are here, man ")
        return render(request, 'chatbox.html', {'chatbox_data': sql_data})
    else:
        return render(request, 'chatbox.html', {})
    


