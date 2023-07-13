from langchain.agents import create_pandas_dataframe_agent
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
import io
import pandas as pd

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.conf import settings

from .forms import UploadFileForm, NewUserForm


def home(request):
    return render(request, "main/home.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"New account created: {user.username}")
            login(request, user)
            return redirect("home")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(
                request=request,
                template_name="registration/register.html",
                context={"form": form},
            )

    form = NewUserForm
    return render(
        request=request,
        template_name="registration/register.html",
        context={"form": form},
    )


def upload_file_handler(file):
    if file.multiple_chunks():
        df = pd.read_csv(file.temporary_file_path())
    else:
        df = pd.read_csv(io.BytesIO(next(file.chunks())))

    return df


@login_required
def upload_csv_to_analyze(request):
    """Upload a CSV file to analyze."""
    form = UploadFileForm()

    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # File validation is done by the UploadFileForm class
            uploaded_file = request.FILES["file"]
            df = upload_file_handler(uploaded_file)

            # Get user profile
            userprofile = request.user.userprofile

            # Create OpenAI chat model
            llm = ChatOpenAI(
                temperature=0,
                model="gpt-3.5-turbo-0613",
                openai_api_key=userprofile.openai_api_key,
                verbose=settings.DEBUG,
            )

            # Create langchain agent
            agent = create_pandas_dataframe_agent(
                llm, df, agent_type=AgentType.OPENAI_FUNCTIONS, verbose=settings.DEBUG
            )

            # Run querys to get desired information
            prompt_suffix = " Please provide the response in a HTML format."

            # Data description
            df_description_prompt = "Analyze the CSV data and describe the key characteristics in each column such as datatype (numerical, categorical), range of values, and any notable patterns. The description should be comprehensive yet concise."
            df_description_response = agent.run(df_description_prompt + prompt_suffix)

            # Data analysis
            df_analysis_prompt = "Given the data properties outlined in your previous response, suggest specific analyses that would be insightful for this dataset. The suggestions should be specific to this data and avoid general or broad analysis recommendations."
            df_analysis_response = agent.run(df_analysis_prompt + prompt_suffix)

            return render(
                request,
                "main/csv_analysis.html",
                {
                    "uploaded_filename": uploaded_file.name,
                    "df_description": df_description_response,
                    "df_analysis": df_analysis_response,
                },
            )

    return render(request, "main/upload_csv_to_analyze.html", {"form": form})
