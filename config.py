# PDF
PDF_PATH = "document/policy.pdf"

# Models
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "qwen2.5:3b"

# Chunking
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Retrieval
TOP_K = 3

# FAISS
VECTOR_DB_PATH = "vector_db"

# SQL Server Configuration

SERVER = r"localhost\SQLEXPRESS"
DATABASE = "CompanyPolicyChatbot"
DRIVER = "ODBC Driver 17 for SQL Server"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "qwen2.5:3b"