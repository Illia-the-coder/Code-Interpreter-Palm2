

# Palm 2🌴 Chatbot with Code Interpreter

Welcome to the Palm 2🌴 Chatbot project! This Streamlit app provides an interactive interface for users to communicate with the Palm 2🌴 Chatbot. The chatbot is capable of interpreting code, prompting the user, exporting code to repl.it, and displaying images.

## Features

- **Language Selection**: Users can select their preferred language from a list. The language codes are loaded from a `lang.json` file.
  
- **Code Interpreter**: The chatbot can interpret and execute code snippets. Users can toggle this feature on or off.
  
- **System Prompt**: Users can set a system prompt for the code interpreter. The default prompt is: "Rule 1: If a user requests a code snippet, provide only one that can run in a Streamlit app without requiring additional libraries."
  
- **Export to repl.it**: Users have the option to export the interpreted code to repl.it.
  
- **Image Display**: The chatbot can display images in the chat interface. Users can toggle the display of images on or off.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Illia-the-coder/Code-Interpreter-Palm2.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Code-Interpreter-Palm2
   ```

3. Install the required packages:
   ```bash
   pip install streamlit json os requests
   ```

4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Open the Streamlit app in your browser.
  
2. Use the sidebar to select your preferred language, toggle the code interpreter, set the system prompt, toggle the export to repl.it option, and toggle the image display option.
  
3. In the chat interface, type your message or code snippet and press enter. The chatbot will respond accordingly.

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/Illia-the-coder/Code-Interpreter-Palm2/blob/main/LICENSE) file for details.
