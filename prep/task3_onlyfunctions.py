def read_from_text(filename):      #Read Text .txt file
    """Reads a text file and returns its content as a string."""
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()
    
def read_json_as_string(file_path): #Read a json file as a string
    """Reads a JSON file and returns its content as a string."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.dumps(json.load(file), indent=4)
    

def extract_json_from_string(text): #Extracts JSON content from a string enclosed in json ``` ```  and returns it as a dictionary.
    """Extracts JSON content from a string enclosed in json``` ``` and returns it as a dictionary."""
    match = re.search(r'```json(.*?)```', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format inside the markers.")
    else:
        raise ValueError("No JSON content found in the provided string.")
    
def ocr_with_gemini_multiple_images(image_paths): #Extracts JSON content from multiple images for Question Paper.
    try:
        images = []
        for image_path in image_paths:
            with open(image_path, "rb") as img_file:
                img = PIL.Image.open(io.BytesIO(img_file.read()))
                images.append(img)

        model = genai.GenerativeModel("gemini-1.5-flash")
        qp_json_format = read_json_as_string('question_paper.json')
        prompt = (
            "Extract and return the text from these images into a carefully formatted question paper "
            "which follows this JSON format: " + qp_json_format
        )
        response = model.generate_content([prompt] + images)
        text = response.text
        return extract_json_from_string(text)
    except Exception as e:
        return {"error": str(e)}
    
def qp_string_with_gemini_to_json(qp_string): #Extracts JSON content from text for Question Paper.

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        qp_json_format = read_json_as_string('question_paper.json')

        prompt = "This is content extracted from a question paper and return this text into a carefully formatted question paper which follows this json format. (Your task is to return the json content between json``` content ```), also understand the rubrics for the given question paper and replace the sample rubric in the json given. In case of either or questions. Assume Part A, B, C and so on from the question paper. max_attempts in rubric means, how many questions are supposed to be written per section for maximum marks." + qp_json_format
        response = model.generate_content([prompt, qp_string])

        return response.text if response.text else "No text detected"

    except Exception as e:
        return f"Error: {e}"
    

def ocr_answer_key_to_qp_json(image_path, qp_json_format): #Extracts Answer Key from an Image and adds it to the extracted Json formatted question paper.
    try:
        # Load the image
        with open(image_path, "rb") as img_file:
            img = PIL.Image.open(io.BytesIO(img_file.read()))

        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = "Extract and return the answers from this image into this carefully formatted question paper which follows this json format. (Your task is to return the json content between json``` content ```) along with the extracted answers, also understand the rubrics for the given question paper while extracting the answers from the image." + qp_json_format
        response = model.generate_content([prompt, img])

        return response.text if response.text else "No text detected"

    except Exception as e:
        return f"Error: {e}"
    

def answer_key_string_with_gemini_to_json(ans_key_string, qp_json_format): #Extracts Answer Key from text and adds it to the extracted Json formatted question paper.
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = "This is content extracted from an answer sheet, return this text into a carefully formatted question paper which follows this json format. (Your task is to return the json content between json``` content ```), along with the extracted answers, also understand the rubrics for the given question paper while extracting the answers from this text." + qp_json_format
        response = model.generate_content([prompt, ans_key_string])

        return response.text if response.text else "No text detected"

    except Exception as e:
        return f"Error: {e}"
    
def extract_and_evaluate_answer_sheet_with_key(answer_sheet_img_path:str, qp_with_key:str, answer_format:str): #Extract and Evaluate an Answer Sheet from an image and creates a student answer sheet instance (JSON formatted)
    try:
        # Load the image
        with open(answer_sheet_img_path, "rb") as img_file:
            img = PIL.Image.open(io.BytesIO(img_file.read()))

        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = "Extract and return the answers from this image into this carefully formatted answer sheet which follows this json format. (Your task is to return the json content between json``` content ```) along with the extracted answers, also understand the rubrics for the given question paper while extracting the answers from the image. Only answers with appropriate question id should be there in the json output. Evaluate the answers based on the question paper and mark the answers with an explanation as required in the answer json format. Tally the marks and fill the answer_sheet_format properly. Only return the answer_sheet_format with answers extracted from the image along with proper evaluation." + f"QUESTION_PAPER: {qp_with_key}" + "ANSWER_SHEET_FORMAT: {answer_format}"
        response = model.generate_content([prompt, img])

        return response.text if response.text else "No text detected"

    except Exception as e:
        return f"Error: {e}"
    

