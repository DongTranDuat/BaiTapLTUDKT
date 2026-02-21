import os
import warnings
import logging

# Tắt warning toàn bộ Python
warnings.filterwarnings("ignore")

# Tắt telemetry (Chroma, etc.)
os.environ["ANONYMIZED_TELEMETRY"] = "False"

# Tắt log rác
logging.getLogger().setLevel(logging.ERROR)

print(">>> sitecustomize loaded")