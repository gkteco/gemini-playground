from vertexai.preview.generative_models import (
    FunctionDeclaration,
)


function_declarations = [
    FunctionDeclaration(
        name = "get_stock_price",
        description = "Get the stock price of a given ticker",
        parameters = {
        "type": "object",
        "properties": {
                "ticker": {
                "type": "string",
                "description": "The stock ticker"
            }
        }
    }),
    FunctionDeclaration(
        name = "list_files_in_drive",
        description = "List files in a given Google Drive folder",
        parameters = {
        "type": "object",
            "properties": None
        }
    ),
]
