from pydantic import BaseModel
class SQLBody(BaseModel):
    token:  str
    secretdecode: str 
    local: bool
    query:  str
    class Config:
        schema_extra = {
            "example": {
                "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJob3N0IjoicmRzLWRzZS1hdXJvcmEtdXMtZHN2LnJpc2twYWNrLmNvbS5iciIsInVzZXIiOiJtZGZtIiwicGFzc3dvcmQiOiIiLCJkYiI6InJhX2RzZSJ9.faZWTavL9jeK5AuC6MmCRI7cBXDSJlKusqT7XFW7azM",
                "secretdecode": "ZXhlbXBsbw==",
                "local": False,
                "query": "SELECT * FROM $ra_dse$.@ra_user@",
            }
        }


class Token(BaseModel):
    credentials : dict  
    secret: str
    class Config:
        schema_extra = {
                "example": {
                    "credentials": {"host":"rds-dse-aurora-us-dsv.riskpack.com.br","user":"adm","password":"adm123","database":"ra_dse"},
                    "secret": "MySecretPassWord",   

                }
            }