from qa import *
from secret import api_keys
import time
import asyncio
import google.generativeai as genai

# TODO: Enter your Gemini API key
# @title Set your Gemini API Key.
# GOOGLE_API_KEY = ""  # @param {type:"string"}
# genai.configure(api_key=GOOGLE_API_KEY)


# not working

# from google.ai import generativelanguage as glm

# clients = [
#   glm.GenerativeServiceClient(client_options={"api_key": key}) for key in api_keys
# ]
# model._client = glm.GenerativeServiceClient(
#     client_options={"api_key": ""}
# )


# for client in clients:
#    model._client = client
#
#    response = model.generate_content("What is the meaning of life?")
#    print(model._client)
#    print(response)
#    print(response.text)  # Model response gets printed


async def process_question(q: str, model) -> str:
    try:
        r = await model.generate_content_async(q)
    except:
        return None
    if r.text:
        return r.text
    return None


# questions += questions


async def main():
    for _ in range(3):
        failed = [i for i in range(len(questions))]
        solutions = [""] * len(questions)

        genai.configure(api_key=api_keys[0])
        model = genai.GenerativeModel("gemini-pro")
        cnt = 1
        while failed:
            jobs = asyncio.gather(
                *[process_question(questions[i], model) for i in failed]
            )
            results = await jobs

            for i, r in zip(failed, results):
                if r is None:
                    print("question {} failed".format(i))
                    failed.append(i)
                    continue
                else:
                    solutions[i] = r

            print(f"#{cnt} Failed to generate content for {len(failed)} questions.")
            # print(
            #    "Time taken to generate content: {} seconds".format(end_time - start_time)
            # )

        genai.configure(api_key=api_keys[1])
        model = genai.GenerativeModel("gemini-pro")


start_time = time.time()
asyncio.run(main())
end_time = time.time()

# print("still alive")
# try:
#    start_time = time.time()
#    #resp = model.generate_content(
#    #  question, stream=True
#    #)
#    resp = model.generate_content_async(question)
#    end_time = time.time()
#    print("Time taken to generate content: {} seconds".format(end_time - start_time))
#    print(type(resp))
#    print(resp.text)
#    #for chunk in resp:
#    #    print(chunk.text)
# except:
#    print("There seems to be something wrong with your Gemini API. Please follow our demonstration in the slide to get a correct one.")
