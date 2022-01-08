from pydantic import BaseModel



class Input_piad_model_2(BaseModel):
	EMPLOYEE_ID : str

class Input_piad_model_1(BaseModel):
	EMPLOYEE_ID : str
	FIRST_NAME : str

