from openai import OpenAI
import json

client = OpenAI(base_url="https://bcb9-170-250-110-57.ngrok-free.app/v1")

email_topic = "The potential of ai"

def prompt_for_json(prompt, keys=[]):
    if len(keys) > 0:
        prompt += "The keys for the json response are: " + ", ".join(keys) + ". "
    final_prompt = f"Please product json for this request: {prompt}. Format your response as json. Please only respond with json with no other text, outside of a formatted code block. We'll be calling json.loads on it, so write such that it can be parsed by that python function."

    completion = client.chat.completions.create(
        model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
        messages=[
            {
                "role": "user", 
                "content": final_prompt
            }
        ],
        response_format={ "type": "json_object" }
    )

    result = completion.choices[0].message.content
    print(result)

    if "```" in result:
        result = result.split("```")
        result = result[1]

    ## sometimes we get """ and so we need to extract the contents of that manually, and replace it with an empty string, but handle it separately later
    if '"""' in result:
        extracted_content = result.split('"""')[1] 
        result = result.split('"""')[0] + '""' + result.split('"""')[2]
        print("splitting")
        print(result)
        print(extracted_content)    
        
    try:
        parsed_result = json.loads(result)
        ## figure out which thing is empty, put extracted_content in the empty thing
        if len(extracted_content) > 0:
            for key in parsed_result:
                if len(parsed_result[key]) == 0:
                    parsed_result[key] = extracted_content

    except:
        print("Error parsing json, retrying")
        parsed_result = prompt_for_json(prompt, keys)
    
    return parsed_result





def write_file(filename,contents):
    with open(filename, "w") as f:
        f.write(contents)

complete = False 
total_generated_files = 0
while not complete:

    file_contents = prompt_for_json(f"Can you write python scripts as .py files, that will create music?", keys=["contents", "filename"])
    
    if file_contents.get("filename") and file_contents.get("contents"):
        write_file(file_contents.get("filename"), file_contents.get("contents"))
        total_generated_files += 1

    if total_generated_files > 3:
        complete = True