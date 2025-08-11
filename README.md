# task-prioritizer-ai
a simple task manager
# Task Prioritizer AI

A Python-based task management application with AI assistance, built using Tkinter for the GUI.

## Features

- **Task Management**: Add, delete, and view tasks with deadlines, importance, and urgency ratings
- **AI Assistant**: Get help with task management using OpenAI's API
- **Priority Scoring**: Automated priority calculation based on importance and urgency
- **Deadline Tracking**: Monitor task deadlines and identify overdue tasks
- **Data Persistence**: Save and load tasks from JSON files
- **Animated UI**: Fun animated interface with ASCII art

## Requirements

- Python 3.6+
- tkinter (usually included with Python)
- openai library
- OpenAI API key

## Installation

1. Clone this repository:
```bash
git clone https://github.com/your-username/task-prioritizer-ai.git
cd task-prioritizer-ai
```

2. Install required dependencies:
```bash
pip install openai
```

3. Set up your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Usage

Run the main application:
```bash
python main.py
```

Or run the fixed version with updated OpenAI API integration:
```bash
python main_with_ai_fixed.py
```

## File Structure

- `main.py`: Original version with environment variable API key handling
- `main_with_ai_fixed.py`: Updated version with proper OpenAI client usage
- `tasks.json`: Stores task data (created automatically)
- `data.json`: Additional data storage
- `pulse_log.json`: Log file for application events

## Features Overview

### Task Creation
- Task name (alphabetic characters only)
- Deadline (YYYY-MM-DD format)
- Importance level (1-10)
- Urgency level (1-10)
- Estimated time in minutes

### Task Management
- View all tasks with status indicators
- Delete specific tasks
- Mark all tasks as completed
- View detailed task information

### AI Integration
- Ask questions about task management
- Get suggestions for prioritization
- Requires valid OpenAI API key

### Priority Calculation
Tasks are prioritized using the formula: `(Importance × 2) + Urgency`

## Security Note

This application requires an OpenAI API key to use the AI features. Make sure to:
- Never commit API keys to version control
- Use environment variables to store sensitive information
- Keep your API key secure and rotate it regularly

## License

This project is licensed under the MIT License.

## Contributing

Feel free to submit issues and pull requests to improve the application!
