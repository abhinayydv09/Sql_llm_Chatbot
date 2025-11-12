from huggingface_hub import InferenceClient

class LLMHandler:
    def __init__(self, hf_token: str, model_name: str):
        self.client = InferenceClient(model_name, token = hf_token)
        self.model_name = model_name

    def generate_sql(self, schema: str, user_query: str, sql_dialect: str = "PostgreSQL", temperature: float = 0.3) -> str:
        system_prompt = f"""
            You are an expert SQL generator. 
            You will be given a database schema and a natural language question. 
            Your task is to write an accurate SQL query that correctly answers the question.

            Follow these rules:
            1. Only use columns and tables from the provided schema.
            2. Write queries in standard SQL syntax (use {sql_dialect} conventions).
            3. Avoid adding any columns or tables not in the schema.
            4. Include JOINs only if they are necessary to answer the question.
            5. Return only the SQL query — do not include explanations or comments.                       
            """
           
        user_prompt = f"""
            {schema.strip()}
            {user_query.strip()}
            """
        
        full_prompt = f"{system_prompt.strip()}\n\n{user_prompt.strip()}"

        try :
            response = self.client.text_generation(
                prompt = full_prompt,
                max_new_tokens =600,
                temperature = temperature,
                )     
            return response.strip()
        except Exception as e:
            if "Supported task: conversational" in str(e) or "model_not_supported" in str(e):
                try:
                    response = self.client.chat_completion(
                        model = self.model_name,
                        messages =[
                            {"role":"system","content":system_prompt},
                            {"role":"user", "content":user_prompt},
                        ],
                        max_tokens = 600,
                        temperature = temperature,
                    )
                    return response.choices[0].message["content"].strip()
                except Exception as chat_error:
                    raise RuntimeError(f"Chat inference also failed: {chat_error}")
            else:
                raise RuntimeError(f"Text generation failed: {e}")
            