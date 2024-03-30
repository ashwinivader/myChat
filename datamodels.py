from pydantic import BaseModel
class QuestionDetails(BaseModel):
    question_text: str
    user:str
    talktodata:bool
    history:str
    sessionid:int


class mongodata(BaseModel):
    user:str
    filename:str
    filesize: str
    filetype:str 
    weaviateprocess:bool
    filepath:str  
    sqltablename:str
    sessionid:str
    dbname:str

class UpdateTableRequest(BaseModel):
    filename: str
    user: str
    sqltablename: str

mysql_data_types = {
    'object': 'VARCHAR(255)',           # Mapping for string/object columns
    'float64': 'FLOAT',                  # Mapping for float columns
    'int64': 'INT',                      # Mapping for integer columns
    'bool': 'TINYINT(1)',                # Mapping for boolean columns
    'datetime64[ns]': 'DATETIME2',        # Mapping for datetime columns
    'timedelta[ns]': 'TIME',             # Mapping for timedelta columns
    'category': 'VARCHAR(255)'           # Mapping for category columns
}