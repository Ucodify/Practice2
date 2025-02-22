from collections.abc import ValuesView
from dash import Dash, html, dcc, State, Output, Input
from requests import post
from dash import callback

#url = "http://127.0.0.1:8000"
result = post(url="http://localhost:8080", json={"question": ValuesView})

app = Dash(__name__)

# App layout
app.layout = html.Div(children=[
    html.Div(id="output-conversation", style={
        "width": "90%",
        "height": "80vh",
        "margin": "auto",
        "overflowY": "auto",
        "border": "1px solid #ccc",
        "padding": "10px"
    }),
    html.Div(children=[
        dcc.Textarea(
            id="input-text",
            placeholder="Type here...",
            style={"width": "100%"}
        ),
        html.Button("Submit", id="input-submit", n_clicks= 0)
    ],
        style={"width": "90%", "margin": "auto", "marginTop": "10px"}
    ),
    dcc.Store(id="store-chat", data="")
])

# Callback to handle user input and chatbot response
# @app.callback(
#     [Output("store-chat", "data"), Output("input-text", "value")],
#     [Input("input-submit", "n_clicks")],
#     [State("input-text", "value"), State("store-chat", "data")]
# )
@app.callback(
    [Output("store-chat", "data"), Output("input-text", "value")],
    [Input("input-submit", "n_clicks")],
    [State("input-text", "value"), State("store-chat", "data")]
)
def query_chatbot(n_clicks, input_value, chat):
    if n_clicks == 0:
        return "", ""

    if input_value=="" or input_value is None:
        return chat, ""

    # Append user input to chat
    chat += f"You: {input_value}<split>Bot: "

    # Create the query by cleaning up the chat text
    query = chat.replace("<split>", "\n").replace("Bot:", "").replace("You:", "")

    try:
        # Send POST request to chatbot server
        result = post(url, json={"question": query})

        if result.status_code == 200:
            response = result.json() ["response"]
        else:
            response = f"Error: {result.reason}"
    except Exception as e:
        response = f"Error: {str(e)}"

    # Append bot response to chat
    chat += f"{response}<split>"

    return chat, ""

# Callback to update the conversation display
@app.callback(
    Output("output-conversation", "children"),
    Input("store-chat", "data")
)
def update_conversation(conversation):
   
    return [
        html.Div(
            message,
            style={
                "maxWidth": "60%",
                "width": "max-content",
                "padding": "10px",
                "marginBottom": "5px",
                "borderRadius": "5px",
                "backgroundColor": "#f1f1f1" if "You:" in message else "#d1f1d1",
                "marginLeft": "auto" if "You:" in message else "0"
            }
        )
        for message in conversation.split("<split>")
    ]

if __name__ == "__main__":
    app.run_server(port=5000, debug=True)
