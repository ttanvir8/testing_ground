#!/usr/bin/env python3
import os
import argparse
import json
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich import print as rprint

class LLMConversationCLI:
    def __init__(self, base_url, api_key, model, system_prompt=None, temperature=0.6):
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )
        self.model = model
        self.temperature = temperature
        self.conversation_history = []

        # Initialize with system prompt if provided
        if system_prompt:
            self.conversation_history.append({"role": "system", "content": system_prompt})
        else:
            self.conversation_history.append({"role": "system", "content": "You are a helpful assistant."})

        self.console = Console()

    def add_message(self, role, content):
        """Add a message to the conversation history."""
        self.conversation_history.append({"role": role, "content": content})

    def get_llm_response(self):
        """Get response from the LLM based on the conversation history."""
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                temperature=self.temperature,
                top_p=0.95,
                max_tokens=4096,
                frequency_penalty=0,
                presence_penalty=0,
                stream=True
            )

            # Start response processing
            self.console.print("\n[bold blue]Assistant:[/bold blue]", end=" ")
            full_response = ""

            for chunk in completion:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    self.console.print(content, end="")

            # Add assistant's response to conversation history
            self.add_message("assistant", full_response)
            self.console.print("\n")
            return full_response

        except Exception as e:
            self.console.print(f"\n[bold red]Error: {str(e)}[/bold red]")
            return None

    def save_conversation(self, filename="conversation.json"):
        """Save the conversation history to a JSON file."""
        with open(filename, 'w') as f:
            json.dump(self.conversation_history, f, indent=2)
        self.console.print(f"\n[green]Conversation saved to {filename}[/green]")

    def load_conversation(self, filename="conversation.json"):
        """Load conversation history from a JSON file."""
        try:
            with open(filename, 'r') as f:
                self.conversation_history = json.load(f)
            self.console.print(f"\n[green]Conversation loaded from {filename}[/green]")
        except FileNotFoundError:
            self.console.print(f"\n[yellow]File {filename} not found. Starting new conversation.[/yellow]")

    def run_cli(self):
        """Run the interactive CLI loop."""
        self.console.print("[bold green]===== LLM Conversation CLI =====\n[/bold green]")
        self.console.print("Type '/help' for available commands. Type '/exit' to quit.\n")

        while True:
            user_input = Prompt.ask("\n[bold green]You[/bold green]")

            # Handle commands
            if user_input.lower() == '/exit':
                self.console.print("[yellow]Exiting conversation...[/yellow]")
                break
            elif user_input.lower() == '/help':
                self.show_help()
                continue
            elif user_input.lower() == '/clear':
                # Clear all messages except system prompt
                system_prompt = next((msg for msg in self.conversation_history if msg["role"] == "system"), None)
                self.conversation_history = [system_prompt] if system_prompt else []
                self.console.print("[yellow]Conversation history cleared.[/yellow]")
                continue
            elif user_input.lower().startswith('/save'):
                parts = user_input.split(maxsplit=1)
                filename = parts[1] if len(parts) > 1 else "conversation.json"
                self.save_conversation(filename)
                continue
            elif user_input.lower().startswith('/load'):
                parts = user_input.split(maxsplit=1)
                filename = parts[1] if len(parts) > 1 else "conversation.json"
                self.load_conversation(filename)
                continue
            elif user_input.lower() == '/history':
                self.show_history()
                continue
            elif user_input.lower().startswith('/system '):
                new_system_prompt = user_input[8:].strip()
                # Update or add system message
                system_index = next((i for i, msg in enumerate(self.conversation_history)
                                   if msg["role"] == "system"), None)
                if system_index is not None:
                    self.conversation_history[system_index]["content"] = new_system_prompt
                else:
                    self.conversation_history.insert(0, {"role": "system", "content": new_system_prompt})
                self.console.print("[yellow]System prompt updated.[/yellow]")
                continue
            elif not user_input.strip():
                continue

            # Add user message to history
            self.add_message("user", user_input)

            # Get LLM response
            self.get_llm_response()

    def show_help(self):
        """Show available commands."""
        help_text = """
        Available Commands:
        - /exit: Exit the conversation
        - /help: Show this help message
        - /clear: Clear the conversation history (keeps system prompt)
        - /save [filename]: Save the conversation to a file (default: conversation.json)
        - /load [filename]: Load a conversation from a file (default: conversation.json)
        - /history: Show the current conversation history
        - /system [prompt]: Update the system prompt
        """
        self.console.print(Markdown(help_text))

    def show_history(self):
        """Show the current conversation history."""
        self.console.print("\n[bold]Current Conversation History:[/bold]")
        for i, message in enumerate(self.conversation_history):
            role_color = {
                "system": "magenta",
                "user": "green",
                "assistant": "blue"
            }.get(message["role"], "white")

            self.console.print(f"[{i+1}] [{role_color}]{message['role'].upper()}:[/{role_color}]")
            self.console.print(f"{message['content']}\n")


def main():
    parser = argparse.ArgumentParser(description="LLM Conversation CLI Tool")
    parser.add_argument("--base-url", type=str, default="https://integrate.api.nvidia.com/v1",
                      help="Base URL for the API")
    parser.add_argument("--api-key", type=str,
                      default=os.environ.get("OPENAI_API_KEY", "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"),
                      help="API key (can be set via OPENAI_API_KEY env variable)")
    parser.add_argument("--model", type=str,
                      default="nvidia/llama-3.3-nemotron-super-49b-v1",
                      help="Model to use for completion")
    parser.add_argument("--system-prompt", type=str, default="You are a helpful assistant.",
                      help="System prompt to use")
    parser.add_argument("--temperature", type=float, default=0.6,
                      help="Temperature for completion")
    parser.add_argument("--load", type=str, default=None,
                      help="Load conversation from file")

    args = parser.parse_args()

    # Create CLI instance
    cli = LLMConversationCLI(
        base_url=args.base_url,
        api_key=args.api_key,
        model=args.model,
        system_prompt=args.system_prompt,
        temperature=args.temperature
    )

    # Load conversation if specified
    if args.load:
        cli.load_conversation(args.load)

    # Run CLI
    cli.run_cli()


if __name__ == "__main__":
    main()
